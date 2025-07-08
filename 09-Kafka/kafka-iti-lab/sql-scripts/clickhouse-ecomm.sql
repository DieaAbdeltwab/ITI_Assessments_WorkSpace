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
-- Password: 
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
