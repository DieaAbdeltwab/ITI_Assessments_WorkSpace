-- Dim_Customer
INSERT INTO Sales_DWH.dbo.Dim_Customer (
    CustomerID_BK, FirstName, LastName, Email, PhoneNumber, GenderID_BK, GenderName,
    SSC, start_date, end_date, is_current
)
SELECT 
    c.CustomerID,
    c.FirstName,
    c.LastName,
    c.Email,
    c.PhoneNumber,
    c.GenderID,
    g.GenderName,
    'OLTP',
    GETDATE(),
    NULL,
    1
FROM Sales_OLTP.dbo.Customer c
JOIN Sales_OLTP.dbo.Gender g ON c.GenderID = g.GenderID;

-- Dim_Product
INSERT INTO Sales_DWH.dbo.Dim_Product (
    ProductID_BK, ProductName, Price, SubCategoryID_BK, SubCategoryName,
    CategoryID_BK, CategoryName, SSC, start_date, end_date, is_current
)
SELECT 
    p.ProductID,
    p.ProductName,
    p.Price,
    p.SubCategoryID,
    sc.SubCategoryName,
    c.CategoryID,
    c.CategoryName,
    'OLTP',
    GETDATE(),
    NULL,
    1
FROM Sales_OLTP.dbo.Product p
JOIN Sales_OLTP.dbo.SubCategory sc ON p.SubCategoryID = sc.SubCategoryID
JOIN Sales_OLTP.dbo.Category c ON sc.CategoryID = c.CategoryID;

-- Dim_Sales_Man
INSERT INTO Sales_DWH.dbo.Dim_Sales_Man (
    SalesmanID_BK, FirstName, LastName, Email, PhoneNumber, AddressID_BK,
    StreetAddress, City, State, ZipCode, SSC, start_date, end_date, is_current
)
SELECT 
    s.SalesmanID,
    s.FirstName,
    s.LastName,
    s.Email,
    s.PhoneNumber,
    s.AddressID,
    a.StreetAddress,
    a.City,
    a.State,
    a.ZipCode,
    'OLTP',
    GETDATE(),
    NULL,
    1
FROM Sales_OLTP.dbo.Salesman s
JOIN Sales_OLTP.dbo.Address a ON s.AddressID = a.AddressID;

-- Fact_Sales
INSERT INTO Sales_DWH.dbo.Fact_Sales (
    ProductID_FK, CustomerID_FK, SalesmanID_FK, OrderDate_FK, OrderTime_FK,
    OrderID_BK, OrderDetailsID_BK, Quantity, TotalPrice, SSC, created_at
)
SELECT
    dp.ProductID_SK,
    dc.CustomerID_SK,
    ds.SalesmanID_SK,
    dd.DateSK,
    dt.TimeSK,
    o.OrderID,
    od.OrderDetailsID,
    od.Quantity,
    od.TotalPrice,
    'OLTP',
    GETDATE()
FROM Sales_OLTP.dbo.OrderDetails od
JOIN Sales_OLTP.dbo.[Order] o ON od.OrderID = o.OrderID
JOIN Sales_OLTP.dbo.Product p ON od.ProductID = p.ProductID
JOIN Sales_OLTP.dbo.Customer c ON o.CustomerID = c.CustomerID
JOIN Sales_OLTP.dbo.Salesman s ON o.SalesmanID = s.SalesmanID
JOIN Sales_DWH.dbo.Dim_Product dp ON p.ProductID = dp.ProductID_BK
JOIN Sales_DWH.dbo.Dim_Customer dc ON c.CustomerID = dc.CustomerID_BK
JOIN Sales_DWH.dbo.Dim_Sales_Man ds ON s.SalesmanID = ds.SalesmanID_BK
JOIN Sales_DWH.dbo.DimDate dd ON CAST(o.OrderDate AS DATE) = dd.Date
JOIN Sales_DWH.dbo.DimTime dt ON CAST(o.OrderDate AS TIME) = dt.Time;


--==========================================================================================================================




