CREATE DATABASE Sales_DWH;
GO

USE Sales_DWH;
GO


CREATE TABLE Dim_Customer (
    CustomerID_SK       INT IDENTITY PRIMARY KEY,
    CustomerID_BK       INT,
    FirstName           VARCHAR(50),
    LastName            VARCHAR(50),
    Email               VARCHAR(100),
    PhoneNumber         VARCHAR(50),
    GenderID_BK         INT,
    GenderName          VARCHAR(50),
    SSC                 VARCHAR(50),
    start_date          DATE,
    end_date            DATE,
    is_current          INT
)



CREATE TABLE Dim_Product (
    ProductID_SK        INT IDENTITY PRIMARY KEY,
    ProductID_BK        INT,
    ProductName         VARCHAR(100),
    Price               INT,
    SubCategoryID_BK    INT,
    SubCategoryName     VARCHAR(100),
    CategoryID_BK       INT,
    CategoryName        VARCHAR(100),
    SSC                 VARCHAR(50),
    start_date          DATE,
    end_date            DATE,
    is_current          INT
)



CREATE TABLE Dim_Sales_Man (
    SalesmanID_SK      INT IDENTITY PRIMARY KEY,
    SalesmanID_BK      INT,
    FirstName          VARCHAR(50),
    LastName           VARCHAR(50),
    Email              VARCHAR(100),
    PhoneNumber        VARCHAR(50),
    AddressID_BK       INT,
    StreetAddress      VARCHAR(50),
    City               VARCHAR(50),
    State              VARCHAR(50),
    ZipCode            VARCHAR(50),
    SSC                VARCHAR(50),
    start_date         DATE,
    end_date           DATE,
    is_current         INT
)







CREATE TABLE Fact_Sales (
    Fact_Transaction_PK_SK        INT IDENTITY PRIMARY KEY,
    ProductID_FK                  INT,
    CustomerID_FK                 INT,
    SalesmanID_FK                 INT,
    OrderDate_FK                  INT,
    OrderTime_FK                  INT,

    OrderID_BK                    INT,
    OrderDetailsID_BK             INT,

    Quantity                      INT,
    TotalPrice                    INT,
    SSC                           VARCHAR(50),
    created_at                    DATETIME,

    FOREIGN KEY (ProductID_FK)  REFERENCES Dim_Product(ProductID_SK),
    FOREIGN KEY (CustomerID_FK) REFERENCES Dim_Customer(CustomerID_SK),
    FOREIGN KEY (SalesmanID_FK) REFERENCES Dim_Sales_Man(SalesmanID_SK),
    FOREIGN KEY (OrderDate_FK)  REFERENCES DimDate(DateSK),
    FOREIGN KEY (OrderTime_FK)  REFERENCES DimTime(TimeSK)
)


--=================================================================================================================================