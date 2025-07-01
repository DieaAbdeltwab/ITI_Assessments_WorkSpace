CREATE DATABASE Sales_DWH;
GO

USE Sales_DWH;
GO

CREATE TABLE Dim_Customer (
    CustomerID_SK       INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID_BK       INT NOT NULL,
    FirstName           NVARCHAR(50) NOT NULL,
    LastName            NVARCHAR(50) NOT NULL,
    Email               NVARCHAR(100) NOT NULL,
    PhoneNumber         NVARCHAR(20) NOT NULL,
    GenderID_BK         INT NULL,
    GenderName          NVARCHAR(20) NULL,
    SSC                 TINYINT NULL,
    start_date          DATETIME NULL,
    end_date            DATETIME NULL,
    is_current          BIT NULL
);

CREATE TABLE Dim_Product (
    ProductID_SK        INT IDENTITY(1,1) PRIMARY KEY,
    ProductID_BK        INT NOT NULL,
    ProductName         NVARCHAR(100) NOT NULL,
    Price               DECIMAL(10,2) NOT NULL,
    SubCategoryID_BK    INT NULL,
    SubCategoryName     NVARCHAR(100) NULL,
    CategoryID_BK       INT NULL,
    CategoryName        NVARCHAR(100) NULL,
    SSC                 TINYINT NULL,
    start_date          DATETIME NULL,
    end_date            DATETIME NULL,
    is_current          BIT NULL
);

CREATE TABLE Dim_Sales_Man (
    SalesmanID_SK       INT IDENTITY(1,1) PRIMARY KEY,
    SalesmanID_BK       INT NOT NULL,
    FirstName           NVARCHAR(50) NOT NULL,
    LastName            NVARCHAR(50) NOT NULL,
    Email               NVARCHAR(100) NOT NULL,
    PhoneNumber         NVARCHAR(20) NOT NULL,
    AddressID_BK        INT NULL,
    StreetAddress       NVARCHAR(255) NULL,
    City                NVARCHAR(100) NULL,
    State               NVARCHAR(50) NULL,
    ZipCode             NVARCHAR(20) NULL,
    SSC                 TINYINT NULL,
    start_date          DATETIME NULL,
    end_date            DATETIME NULL,
    is_current          BIT NULL
);

CREATE TABLE Fact_Sales (
    Fact_Transaction_PK_SK INT IDENTITY(1,1) PRIMARY KEY,
    ProductID_FK           INT NULL,
    CustomerID_FK          INT NULL,
    SalesmanID_FK          INT NULL,
    OrderDate_FK           INT NULL,
    OrderTime_FK           INT NULL,
    OrderID_BK             INT NOT NULL,
    OrderDetailsID_BK      INT NOT NULL,
    Quantity               INT NOT NULL,
    TotalPrice             DECIMAL(10,2) NOT NULL,
    SSC                    TINYINT NULL,
    created_at             DATETIME2 NULL,
    
    FOREIGN KEY (ProductID_FK) REFERENCES Dim_Product(ProductID_SK),
    FOREIGN KEY (CustomerID_FK) REFERENCES Dim_Customer(CustomerID_SK),
    FOREIGN KEY (SalesmanID_FK) REFERENCES Dim_Sales_Man(SalesmanID_SK),
    FOREIGN KEY (OrderDate_FK) REFERENCES DimDate(DateSK),
    FOREIGN KEY (OrderTime_FK) REFERENCES DimTime(TimeSK)
);


--==================================================================================================

USE [Sales_DWH]
GO

-- Create the control table for tracking ETL loads
CREATE TABLE [dbo].[Meta_Control_Fact_Sales_Load](
    [id] INT IDENTITY(1,1) NOT NULL PRIMARY KEY,
    [SalesOrderDetails] NVARCHAR(255) NULL,
    [Last_load_date] DATETIME NULL,
    [Last_Load_OrderDetailsID_BK] INT NULL
)
INSERT INTO [dbo].[Meta_Control_Fact_Sales_Load]
    ([SalesOrderDetails], [Last_load_date], [Last_Load_OrderDetailsID_BK])
VALUES
    ('Orders_Details', '1900-01-01 00:00:00.000', 0)
GO

update [Meta_Control_Fact_Sales_Load]
set Last_Load_OrderDetailsID_BK = 0 
where id = 1





--==================================================================================================
DELETE FROM [Sales_DWH].[dbo].[Fact_Sales];

-- Optional: Reset identity counter if table has an identity column
DBCC CHECKIDENT ('[Sales_DWH].[dbo].[Fact_Sales]', RESEED, 0);


--==================================================================================================
SELECT *  FROM Dim_Product


SELECT *  FROM Dim_Customer

SELECT *  FROM Dim_Sales_Man

SELECT *  FROM [Meta_Control_Fact_Sales_Load]


SELECT * FROM Fact_Sales

