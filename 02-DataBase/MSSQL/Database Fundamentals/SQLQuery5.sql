
--#########################################################################################################################################################################################
--#########################################################################################################################################################################################
--#########################################################################################################################################################################################
--#########################################################################################################################################################################################



USE ITI


--Q1========================================================================================
SELECT COUNT(S.St_Age) FROM Student S

--Q2========================================================================================
SELECT DISTINCT I.Ins_Name FROM Instructor I
--Q3========================================================================================

SELECT S.St_Id AS "Student ID" ,  ISNULL(S.St_Fname , '' ) + ' ' + ISNULL(S.St_Lname , '' ) AS  "Student Full Name" , D.Dept_Name AS "Department name" 
FROM Student S 
JOIN Department D
ON D.Dept_Id = S.Dept_Id 

--Q4========================================================================================
SELECT I.Ins_Name, D.Dept_Name 
FROM Instructor I
LEFT JOIN Department D
ON I.Dept_Id = D.Dept_Id
--Q5========================================================================================
SELECT   CONCAT(S.St_Fname ,' ',S.St_Lname)  AS  "Student Full Name"  , C.Crs_Name
FROM Student S 
JOIN Stud_Course SC
ON S.St_Id = SC.St_Id
JOIN Course C
ON C.Crs_Id = SC.Crs_Id 
WHERE SC.Grade IS NOT NULL

--Q6========================================================================================

SELECT  T.Top_Name , COUNT(C.Crs_Id) AS NumberOfCourses
FROM Course C
JOIN Topic T
ON C.Top_Id = T.Top_Id
GROUP BY T.Top_Name


--Q7========================================================================================
SELECT MAX(I.Salary) AS "MAX" , MIN(I.Salary) AS "MIN" FROM Instructor I

--Q8========================================================================================
 SELECT I.Ins_Name FROM Instructor I
 WHERE I.Salary < (SELECT AVG(ISNULL(Salary,0)) FROM Instructor )

--Q9========================================================================================
SELECT D.Dept_Name FROM Department D
WHERE D.Dept_Id =
( SELECT I.Dept_Id FROM Instructor I WHERE I.Salary = 
(SELECT MIN(Salary)  FROM Instructor ))


SELECT  D.Dept_Name  
FROM Instructor I
JOIN Department D
ON I.Dept_Id = D.Dept_Id
WHERE I.Salary = (SELECT MIN(Salary)  FROM Instructor ) 

--Q10========================================================================================

SELECT I.Ins_Name  FROM Instructor I
WHERE I.Salary IN 
( SELECT  TOP(2) Salary 
FROM  Instructor 
WHERE Salary IS NOT NULL  
ORDER BY Salary DESC  )


--Q11========================================================================================
ALTER TABLE Instructor ADD  Bonus INT 

SELECT Ins_Name, COALESCE(Salary, Bonus) AS Pay
FROM Instructor;
--Q12========================================================================================

SELECT AVG(ISNULL(Salary,0)) FROM Instructor 

--Q13========================================================================================
SELECT S.St_Fname , SV.* 
FROM Student S , Student SV
WHERE SV.St_Id = S.St_super

--Q14========================================================================================
SELECT *
FROM (SELECT * , DENSE_RANK () OVER( PARTITION BY I.Dept_Id ORDER BY I.Salary DESC )  AS DR FROM Instructor I WHERE I.Salary IS NOT NULL ) AS TT
WHERE DR = 1 OR DR = 2

--Q15========================================================================================

SELECT  *
FROM (SELECT * , ROW_NUMBER() OVER (PARTITION BY I.Dept_Id ORDER BY NEWID() ) AS RN FROM Instructor I) AS TT2
WHERE RN = 1 

--#########################################################################################################################################################################################
--#########################################################################################################################################################################################
--#########################################################################################################################################################################################
--#########################################################################################################################################################################################

 USE AdventureWorks2022
 
 --Q1==========================================================================

 SELECT SSH.SalesOrderID , SSH.ShipDate  FROM Sales.SalesOrderHeader AS SSH
 WHERE SSH.OrderDate BETWEEN '7/28/2002'  AND '7/29/2014'



--Q2==========================================================================
SELECT PP.ProductID , PP.Name FROM  Production.Product PP
WHERE PP.StandardCost < 110.00

--Q3==========================================================================
SELECT PP.ProductID , PP.Name FROM  Production.Product PP
WHERE PP.Weight IS NULL

--Q4==========================================================================
SELECT PP.ProductID , PP.Name , PP.Color  FROM  Production.Product PP
WHERE PP.Color  IN ('Silver' ,'Black','Red' )

--Q5==========================================================================
SELECT PP.ProductID , PP.Name  FROM  Production.Product PP
WHERE PP.Name LIKE 'B%'


--Q6==========================================================================
UPDATE Production.ProductDescription
SET Description = 'Chromoly steel_High of defects'
WHERE ProductDescriptionID = 3
----------------------------------------------------
SELECT  PPD.ProductDescriptionID , PPD.Description  FROM  Production.ProductDescription PPD
WHERE PPD.Description LIKE '%[_]%'

--Q7==========================================================================
SELECT  SSH.OrderDate , SUM(SSH.TotalDue)  AS TotalDueSum FROM  Sales.SalesOrderHeader SSH
WHERE SSH.OrderDate BETWEEN '7/1/2001' AND '7/31/2014' 
GROUP BY SSH.OrderDate
ORDER BY  OrderDate

--Q8==========================================================================

SELECT DISTINCT  HE.HireDate FROM HumanResources.Employee HE

--Q9==========================================================================


SELECT AVG(DISTINCT ISNULL(ListPrice,0))
FROM  Production.Product 


SELECT AVG(TT.ListPrice)
FROM ( SELECT DISTINCT PP.ListPrice  FROM  Production.Product PP WHERE  PP.ListPrice IS NOT NULL ) AS TT


--Q10==========================================================================
 SELECT CONCAT('The [ ',PP.Name,' ] is only! --> ',  PP.ListPrice) AS "Product" 
 FROM  Production.Product PP
 WHERE PP.ListPrice BETWEEN 100 AND 120
 ORDER BY PP.ListPrice

 SELECT 'The [ '+PP.Name+' ] is only! --> '+ CONVERT( varchar , PP.ListPrice) AS "Product" 
 FROM  Production.Product PP
 WHERE PP.ListPrice BETWEEN 100 AND 120
 ORDER BY PP.ListPrice



 --Q11==========================================================================

SELECT  rowguid ,Name, SalesPersonID, Demographics INTO store_Archive
FROM Sales.Store

SELECT COUNT(*) FROM store_Archive
SELECT COUNT(*) FROM  Sales.Store

SELECT  rowguid ,Name, SalesPersonID, Demographics 
FROM Sales.Store


--Q12==========================================================================

SELECT CONVERT(VARCHAR, GETDATE()) AS DATETIME
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT (GETDATE() , 'dd-mm-yy' ))
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT (GETDATE() , 'dd-mm-yy' ))
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT(GETDATE(), 'dd-MM-yy'))
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT(GETDATE(), 'dd-MM-yyyy')) 
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT(GETDATE(), 'MM/dd/yyyy'))
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT(GETDATE(), 'yyyy-MM-dd') )
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT(GETDATE(), 'dddd, dd MMMM yyyy') )
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT(GETDATE(), 'hh:mm tt'))
UNION ALL 
SELECT CONVERT(VARCHAR, FORMAT(GETDATE(), 'HH:mm:ss'))