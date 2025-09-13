from pyspark.sql import SparkSession
from pyspark.sql.functions import col, window, from_json
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, LongType

S3_ENDPOINT = "http://minio:9000"

spark = (
    SparkSession.builder.appName("kafka-to-parquet")
    .config("spark.hadoop.fs.s3a.endpoint", S3_ENDPOINT)
    .config("spark.hadoop.fs.s3a.path.style.access", "true")
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    .getOrCreate()
)

schema = StructType([
    StructField("user_id", StringType()),
    StructField("event", StringType()),
    StructField("value", IntegerType()),
    StructField("ts", LongType())
])

df = (
    spark.readStream
        .format("kafka")
        .option("kafka.bootstrap.servers", "kafka:9092")
        .option("subscribe", "events.raw")
        .option("startingOffsets", "latest")
        .load()
)

parsed = (
    df.selectExpr("CAST(value AS STRING) as json")
      .select(from_json(col("json"), schema).alias("d"))
      .select("d.*")
      .withColumn("ts_ts", (col("ts")/1000).cast("timestamp"))
)

# Raw append sink
raw_query = (
    parsed.writeStream
        .format("parquet")
        .option("checkpointLocation", "s3a://warehouse/checkpoints/kafka_parquet")
        .option("path", "s3a://warehouse/parquet/events_stream")
        .outputMode("append")
        .start()
)


# Add watermark for event time to support append mode with aggregation
parsed_with_watermark = parsed.withWatermark("ts_ts", "1 minutes")

# Windowed aggregate (5s)
agg = (
    parsed_with_watermark.groupBy(
        window(col("ts_ts"), "5 seconds"),
        col("event")
    ).count()
)

agg_query = (
    agg.writeStream
       .format("parquet")
       .option("checkpointLocation", "s3a://warehouse/checkpoints/agg_5s")
       .option("path", "s3a://warehouse/parquet/agg_5s")
       .outputMode("append")
       .start()
)

raw_query.awaitTermination()
agg_query.awaitTermination()
