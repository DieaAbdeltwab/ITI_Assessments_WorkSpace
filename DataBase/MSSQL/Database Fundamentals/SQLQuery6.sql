
--=====================================================================================================================================================================================
--Q1===================================================================================================================================================================================
--=====================================================================================================================================================================================

--==========================================================================================================
USE SD

GO
SP_ADDTYPE  loc,'nchar(2)'

GO
CREATE DEFAULT  LOC_DEF AS 'NY'

GO
CREATE RULE LOC_RUL AS @x IN ('NY','DS','KW')

GO
SP_BINDRULE   LOC_RUL , loc

GO
SP_BINDEFAULT LOC_DEF , loc

--==========================================================================================================
CREATE TABLE Department 
(
	DeptNo VARCHAR(5) PRIMARY KEY ,
	DeptName VARCHAR(20) ,
	Location loc

)

INSERT INTO Department VALUES('d1','Research','NY')
INSERT INTO Department VALUES('d2','Accounting','DS')
INSERT INTO Department VALUES('d3','Markiting','KW')

INSERT INTO Department VALUES('d5','Markiting','TA')
--==========================================================================================================

CREATE TABLE Employee 
(
	EmpNo INT PRIMARY KEY ,
	EmpFname VARCHAR(20) NOT NULL ,
	EmpLname VARCHAR(20) NOT NULL ,
	DeptNo  VARCHAR(5) FOREIGN KEY REFERENCES  Department(DeptNo) ,
	Salary INT UNIQUE 

)
GO
CREATE RULE SALARY_RULE AS @x < 6000

GO
SP_BINDRULE SALARY_RULE , 'Employee.Salary'

--==========================================================================================================
INSERT INTO Employee VALUES(25348, 'Mathew', 'Smith', 'd3', 2500);
INSERT INTO Employee VALUES(10102, 'Ann', 'Jones', 'd3', 3000);
INSERT INTO Employee VALUES(18316, 'John', 'Barrimore', 'd1', 2400);
INSERT INTO Employee VALUES(29346, 'James', 'James', 'd2', 2800);
INSERT INTO Employee VALUES(9031, 'Lisa', 'Bertoni', 'd2', 4000);
INSERT INTO Employee VALUES(2581, 'Elisa', 'Hansel', 'd2', 3600);
INSERT INTO Employee VALUES(28559, 'Sybl', 'Moser', 'd1', 2900);
--==========================================================================================================
INSERT INTO Project VALUES('p1', 'Apollo', 120000);
INSERT INTO Project VALUES('p2', 'Gemini', 95000);
INSERT INTO Project VALUES('p3', 'Mercury', 185600);

--==========================================================================================================
INSERT INTO Works_on VALUES(10102, 'p1', 'Analyst', '2006.10.1');
INSERT INTO Works_on VALUES(10102, 'p3', 'Manager', '2012.1.1');
INSERT INTO Works_on VALUES(25348, 'p2', 'Clerk', '2007.2.15');
INSERT INTO Works_on VALUES(18316, 'p2', NULL, '2007.6.1');
INSERT INTO Works_on VALUES(29346, 'p2', NULL, '2006.12.15');
INSERT INTO Works_on VALUES(2581, 'p3', 'Analyst', '2007.10.15');
INSERT INTO Works_on VALUES(9031, 'p1', 'Manager', '2007.4.15');
INSERT INTO Works_on VALUES(28559, 'p1', NULL, '2007.8.1');
INSERT INTO Works_on VALUES(28559, 'p2', 'Clerk', '2012.2.1');
INSERT INTO Works_on VALUES(9031, 'p3', 'Clerk', '2006.11.15');
INSERT INTO Works_on VALUES(29346, 'p1', 'Clerk', '2007.1.4');


--==========================================================================================================
INSERT INTO Works_on(EmpNo,ProjectNo,Job,Enter_Date) VALUES(11111, 'p2', 'Analyst', '2007.10.15');

UPDATE Works_on
SET EmpNo=11111 
WHERE  EmpNo=10102




UPDATE Employee
SET EmpNo=22222 
WHERE  EmpNo=10102

DELETE FROM  Employee
WHERE  EmpNo=10102

--==========================================================================================================

ALTER TABLE Employee ADD  TelephoneNumber  VARCHAR(20) 

ALTER TABLE Employee DROP COLUMN  TelephoneNumber

--=====================================================================================================================================================================================
--Q2===================================================================================================================================================================================
--=====================================================================================================================================================================================
GO
CREATE SCHEMA  Company

GO
ALTER SCHEMA Company TRANSFER Department

GO
CREATE SCHEMA   HumanResource

GO
ALTER SCHEMA HumanResource TRANSFER Employee

--=====================================================================================================================================================================================
--Q3===================================================================================================================================================================================
--=====================================================================================================================================================================================
--3. Write query to display the constraints for the Employee table.
SELECT 
    tc.CONSTRAINT_NAME,
    tc.CONSTRAINT_TYPE,
    kcu.COLUMN_NAME
FROM 
    INFORMATION_SCHEMA.TABLE_CONSTRAINTS AS tc
    LEFT JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE AS kcu 
        ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
WHERE 
    tc.TABLE_NAME = 'Employee'
ORDER BY 
    tc.CONSTRAINT_TYPE, tc.CONSTRAINT_NAME;
--=====================================================================================================================================================================================
--Q4===================================================================================================================================================================================
--=====================================================================================================================================================================================
CREATE SYNONYM Emp FOR HumanResource.Employee


Select*from Employee
Select*from HumanResource.Employee
Select*from Emp
Select*from HumanResource.Emp


--=====================================================================================================================================================================================
--Q5===================================================================================================================================================================================
--=====================================================================================================================================================================================
CREATE SYNONYM PRO FOR Company.Project

SELECT * FROM PRO
UPDATE PRO
SET Budget = Budget * 1.1
WHERE ProjectNo IN 
(SELECT ProjectNo FROM Works_on WHERE EmpNo =  10102 AND Job = 'Manager')


SELECT * FROM PRO


--=====================================================================================================================================================================================
--Q6===================================================================================================================================================================================
--=====================================================================================================================================================================================
CREATE SYNONYM DEP FOR Company.Department


SELECT * FROM DEP

UPDATE DEP
SET DeptName = 'Sales'
WHERE DEP.DeptNo = (SELECT Emp.DeptNo FROM  Emp WHERE EmpFname='James' )


SELECT * FROM DEP


--=====================================================================================================================================================================================
--Q7===================================================================================================================================================================================
--=====================================================================================================================================================================================
UPDATE Works_on
SET Enter_Date = '12.12.2007'
WHERE ProjectNo = 'p1' AND EmpNo IN 
(
SELECT Emp.EmpNo 
FROM Emp 
JOIN DEP 
ON  DEP.DeptNo = Emp.DeptNo
AND DeptName = 'Sales'
)


--=====================================================================================================================================================================================
--Q8===================================================================================================================================================================================
--=====================================================================================================================================================================================
SELECT * FROM Works_on


DELETE FROM Works_on
WHERE  EmpNo IN 
(
SELECT Emp.EmpNo 
FROM Emp 
JOIN DEP 
ON  DEP.DeptNo = Emp.DeptNo
AND Location = 'KW'
)

 SELECT * FROM Works_on

--=====================================================================================================================================================================================
--Q9===================================================================================================================================================================================
--=====================================================================================================================================================================================
--9.Try to Create Login Named(ITIStud) who can access Only student and Course tablesfrom ITI DB then allow him to select and insert data into tables and deny Delete and update
USE ITI;

CREATE LOGIN ITIStud WITH PASSWORD = 'StrongPassword123!';

CREATE USER ITIStud FOR LOGIN ITIStud;


-- Grant SELECT and INSERT on Student and Course tables
GRANT SELECT, INSERT ON dbo.Student TO ITIStud;
GRANT SELECT, INSERT ON dbo.Course TO ITIStud;


-- Deny DELETE and UPDATE on Student and Course tables
DENY DELETE, UPDATE ON dbo.Student TO ITIStud;
DENY DELETE, UPDATE ON dbo.Course TO ITIStud;


SELECT 
    pr.name AS PrincipalName,
    pr.type_desc AS PrincipalType,
    pe.permission_name,
    pe.state_desc,
    pe.class_desc,
    OBJECT_NAME(pe.major_id) AS ObjectName
FROM 
    sys.database_permissions AS pe
    JOIN sys.database_principals AS pr ON pe.grantee_principal_id = pr.principal_id
WHERE 
    pr.name = 'ITIStud';


--=====================================================================================================================================================================================
--=====================================================================================================================================================================================
--=====================================================================================================================================================================================











