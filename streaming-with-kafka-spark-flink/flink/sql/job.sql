-- ===== S3A + MinIO (không dùng env) =====
SET 'fs.s3a.endpoint' = 'http://minio:9000';           -- LƯU Ý: có http://
SET 'fs.s3a.path.style.access' = 'true';
SET 'fs.s3a.connection.ssl.enabled' = 'false';

SET 'fs.s3a.access.key' = 'minio';
SET 'fs.s3a.secret.key' = 'minio12345';
SET 'fs.s3a.aws.credentials.provider' = 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider';

SET 'fs.s3a.endpoint.region' = 'us-east-1';
SET 'fs.s3a.fast.upload' = 'true';

-- ===== Iceberg HadoopCatalog =====
CREATE CATALOG demo WITH (
  'type' = 'iceberg',
  'catalog-impl' = 'org.apache.iceberg.hadoop.HadoopCatalog',
  'io-impl' = 'org.apache.iceberg.hadoop.HadoopFileIO',
  'warehouse' = 's3a://warehouse/iceberg/'
);

USE CATALOG demo;

CREATE DATABASE IF NOT EXISTS db;
USE db;

CREATE TABLE IF NOT EXISTS events (
  id BIGINT,
  ts TIMESTAMP(3),
  payload STRING
) WITH ('format-version' = '2');

INSERT INTO events VALUES (1, CURRENT_TIMESTAMP, 'ok from flink');
