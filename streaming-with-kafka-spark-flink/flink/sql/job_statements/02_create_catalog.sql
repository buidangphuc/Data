CREATE CATALOG demo WITH (
  'type' = 'iceberg',
  'catalog-impl' = 'org.apache.iceberg.hadoop.HadoopCatalog',
  'io-impl' = 'org.apache.iceberg.hadoop.HadoopFileIO',
  'warehouse' = 's3a://warehouse/iceberg/'
);
