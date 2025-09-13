SET 'fs.s3a.endpoint' = 'http://minio:9000';
SET 'fs.s3a.path.style.access' = 'true';
SET 'fs.s3a.connection.ssl.enabled' = 'false';
SET 'fs.s3a.access.key' = 'minio';
SET 'fs.s3a.secret.key' = 'minio12345';
SET 'fs.s3a.aws.credentials.provider' = 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider';
SET 'fs.s3a.endpoint.region' = 'us-east-1';
SET 'fs.s3a.fast.upload' = 'true';
USE CATALOG demo;
USE db;
CREATE TABLE IF NOT EXISTS events (
  id BIGINT,
  ts TIMESTAMP(3),
  payload STRING
) WITH ('format-version' = '2');