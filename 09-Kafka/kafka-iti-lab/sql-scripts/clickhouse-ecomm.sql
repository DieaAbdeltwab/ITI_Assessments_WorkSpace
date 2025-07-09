-- Active: 1751788548434@@127.0.0.1@8123@default
--========================================================================

--========================================================================
--========================================================================
-- 1. Connect to the server 
-- Name: clickhouse
-- Host: 127.0.0.1
-- Port: 8123
-- Database: default
-- Username: default
-- Password: 123
--========================================================================
--========================================================================

CREATE TABLE IF NOT EXISTS "demo.ecomm.users" (
    id UInt32,
    username String,
    email String,
    password String,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY id;



CREATE TABLE IF NOT EXISTS "demo.ecomm.orders" (
    id UInt32,
    user_id UInt32,
    order_date DateTime
) ENGINE = MergeTree()
ORDER BY id;

CREATE TABLE "demo.ecomm.products" (
    id UInt32,
    name String,
    description String,
    price Float64,
    stock_quantity Int32,
    created_at DateTime
) ENGINE = MergeTree()
ORDER BY id;




CREATE TABLE "demo.ecomm.order_items" (
    id UInt32,
    order_id UInt32,
    product_id UInt32,
    quantity Int32,
    price Float64
) ENGINE = MergeTree()
ORDER BY id;

--========================================================================
--========================================================================
--========================================================================



DROP TABLE IF EXISTS "demo.ecomm.users";
DROP TABLE IF EXISTS "demo.ecomm.orders";
DROP TABLE IF EXISTS "demo.ecomm.products";
DROP TABLE IF EXISTS "demo.ecomm.order_items";



--========================================================================
--========================================================================
--========================================================================

--========================================================================
--========================================================================

CREATE TABLE IF NOT EXISTS "demo.ecomm.users" (
    id UInt32,
    username String,
    email String,
    password String,
    created_at DateTime,
    valid_from DateTime DEFAULT now(),
    valid_to DateTime DEFAULT toDateTime('9999-12-31 23:59:59'),
    is_current UInt8 DEFAULT 1
) ENGINE = MergeTree()
ORDER BY id;

DROP TABLE IF EXISTS users_scd2;

CREATE TABLE IF NOT EXISTS users_scd2 (
  id Int32,
  username String,
  email String,
  password String,
  created_at DateTime,
  valid_from DateTime,
  valid_to DateTime,
  is_current UInt8
) ENGINE = MergeTree()
ORDER BY (id, valid_from);
--========================================================================
--========================================================================
--========================================================================
DROP TABLE IF  EXISTS users_scd 


CREATE TABLE users_scd (
  id Int32,
  username String,
  email String,
  password String,
  created_at DateTime64(3),
  is_current UInt8,
  version Int32
) ENGINE = MergeTree()
ORDER BY id;







