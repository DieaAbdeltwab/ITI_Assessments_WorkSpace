-- --------------------------------------------
-- Required: Output format
-- --------------------------------------------
SET 'sql-client.execution.result-mode' = 'TABLEAU';

-- --------------------------------------------
-- 1. Kafka Source Table (Debezium Avro Format)
-- --------------------------------------------
CREATE TABLE users_kafka (
  id INT,
  username STRING,
  email STRING,
  password STRING,
  created_at STRING,  -- Removed trailing comma
  __op STRING

) WITH (
  'connector' = 'kafka',
  'topic' = 'demo.ecomm.users',
  'properties.bootstrap.servers' = 'broker:29092',
  'scan.startup.mode' = 'earliest-offset',
  'format' = 'avro-confluent',
  'avro-confluent.schema-registry.url' = 'http://schema-registry:8081'
);

SELECT __op , username from users_kafka;
-- --------------------------------------------
-- 2. ClickHouse Sink Table (MUST exist in ClickHouse)
-- --------------------------------------------
-- CREATE TABLE clickhouse_users (
--   id INT,
--   username STRING,
--   email STRING,
--   password STRING,
--   is_current TINYINT,
-- ) WITH (
--   'connector' = 'clickhouse',
--   'url' = 'jdbc:clickhouse://clickhouse:8123/default',
--   'table-name' = 'users_scd',
--   'username' = 'default',
--   'password' = '123'
-- );
-- --------------------------------------------
-- 3. Simple Insert into ClickHouse
-- --------------------------------------------

-- WHERE __op IN ('c', 'u');
-- __op value	Meaning
-- c	Create
-- u	Update
-- d	Delete

--  INSERT , UPDATE

-- --------------------------------------------
-- 4. Simple Insert into ClickHouse
-- --------------------------------------------
-- INSERT INTO clickhouse_users
-- SELECT
--   id,
--   username,
--   email,
--   password,
--   CAST(1 AS TINYINT) AS is_current
-- FROM users_kafka;
