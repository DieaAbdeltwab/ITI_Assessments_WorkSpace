--################################################################################################################################################################################
--################################################################################################################################################################################
--################################################################################################################################################################################
--Q1=============================================================================================================================
USE ITI
GO
CREATE or ALTER PROCEDURE Num_Student_Dept
AS
BEGIN 
	
	SELECT S.Dept_Id , COUNT( S.St_Id ) AS "Student Count" FROM Student  S WHERE S.Dept_Id IS NOT NULL GROUP BY  S.Dept_Id 

END
GO

EXEC  Num_Student_Dept


--Q2=============================================================================================================================
USE Company_SD
GO
CREATE OR ALTER PROCEDURE Check_P1_Num 
AS 
BEGIN 

	DECLARE @emp_num INT = (SELECT COUNT(ESSn) FROM Works_for WHERE  Pno = 100 )

	IF @emp_num > 3 
		SELECT 'The number of employees in the project p1 is 3 or more' AS "Massage",  
		CONCAT(Fname,' ',E.Lname) AS "Full Name" FROM Employee E , Works_for WO WHERE  E.SSN = WO.ESSn AND  Pno = 100
	ELSE IF @emp_num <= 3 
		SELECT 'The following employees work for the project p1' AS "Massage", 
		CONCAT(Fname,' ',E.Lname) AS "Full Name" FROM Employee E , Works_for WO WHERE  E.SSN = WO.ESSn AND  Pno = 100

END 
GO
EXEC Check_P1_Num
--=============================================================================================================================
GO
CREATE OR ALTER PROCEDURE Check_Num ( @project_ID INT )
AS 
BEGIN 
	IF  EXISTS(SELECT 1  FROM Works_for WHERE Pno = @project_ID )

		DECLARE @emp_num INT = (SELECT COUNT(ESSn) FROM Works_for WHERE  Pno = @project_ID )

		IF @emp_num > 3 
			SELECT 'The number of employees in the project p1 is 3 or more' AS "Massage",  
			CONCAT(Fname,' ',E.Lname) AS "Full Name" FROM Employee E , Works_for WO WHERE  E.SSN = WO.ESSn AND  Pno = @project_ID
		ELSE IF @emp_num <= 3 
			SELECT 'The following employees work for the project p1' AS "Massage", 
			CONCAT(Fname,' ',E.Lname) AS "Full Name" FROM Employee E , Works_for WO WHERE  E.SSN = WO.ESSn AND  Pno = @project_ID
	ELSE 
		SELECT 'NO Project HAS THIS ID'

END 
GO
EXEC Check_Num 600
--=============================================================================================================================

USE SD
GO
CREATE OR ALTER PROCEDURE Check_P1_Num 
AS 
BEGIN 

	DECLARE @emp_num INT = (SELECT COUNT(WO.EmpNo) FROM Works_on WO WHERE  WO.ProjectNo = 'p1' )


	IF @emp_num > 3 
		SELECT 'The number of employees in the project p1 is 3 or more' AS "Massage", 
		CONCAT(E.EmpFname,' ',E.EmpLname)  AS "Full Name" FROM HumanResource.Employee E , Works_on WO WHERE  E.EmpNo = WO.EmpNo AND  WO.ProjectNo = 'p1'
	ELSE IF @emp_num <= 3 
		SELECT 'The following employees work for the project p1'  AS "Massage" , 
		CONCAT(E.EmpFname,' ',E.EmpLname) AS "Full Name" FROM HumanResource.Employee E , Works_on WO WHERE  E.EmpNo = WO.EmpNo AND  WO.ProjectNo = 'p1'

END 
GO
EXEC Check_P1_Num

--Q3=============================================================================================================================
USE Company_SD

GO
CREATE OR ALTER PROCEDURE Update_Emp ( @Old_Emp_Num INT , @New_Emp_Num INT, @project_number INT )
AS 
BEGIN 
	IF NOT EXISTS(SELECT 1  FROM Works_for WHERE ESSn =  @New_Emp_Num AND Pno= @project_number )
	BEGIN
		update Works_for
		SET ESSn   =  @New_Emp_Num , Hours  = 0
		WHERE ESSn =  @Old_Emp_Num AND Pno= @project_number
	END
	ELSE 
		SELECT 'HE WORKED IN THIS Project !'
END
GO


EXEC Update_Emp 968574 , 112233 , 700

--=============================================================================================================================
USE SD

GO
CREATE OR ALTER PROCEDURE Update_Emp ( @Old_Emp_Num INT , @New_Emp_Num INT, @project_number VARCHAR(5) )
AS 
BEGIN 
	update Works_on
	SET EmpNo   =  @New_Emp_Num
	WHERE EmpNo =  @Old_Emp_Num AND ProjectNo= @project_number

END
GO


EXEC Update_Emp 2581 , 28559 , 'p3' 



--Q4=============================================================================================================================
USE Company_SD
ALTER TABLE Project ADD budget INT 

CREATE TABLE Audit_TABLE ( ProjectNo INT, UserName VARCHAR(100), ModifiedDate DATE , Budget_Old INT, Budget_New INT)

GO
CREATE OR ALTER TRIGGER Project_Audit  ON Project AFTER UPDATE
AS
BEGIN
	IF UPDATE(budget)
	BEGIN
		INSERT INTO Audit_TABLE 
		SELECT I.Pnumber , SUSER_NAME() , GETDATE(), D.budget , I.budget  FROM inserted I , deleted D 
		SELECT 'OK !'
	END
END 
GO

UPDATE Project 
SET budget = 86000
WHERE Pnumber = 100
--Q5=============================================================================================================================
USE ITI
GO
CREATE OR ALTER TRIGGER Trigg_Dept_Ins ON  Department INSTEAD OF  INSERT 
AS
BEGIN 
	SELECT 'Can’t insert a new record in that table'
END

GO

INSERT INTO Department (Dept_Id, Dept_Name) VALUES (101, 'Test Dept');

--Q6=============================================================================================================================
USE Company_SD

GO
CREATE OR ALTER TRIGGER Prevents_Employee_March ON Employee INSTEAD OF  INSERT 
AS 
BEGIN 
	IF MONTH(GETDATE()) = 3
	BEGIN
		SELECT 'YOU Can’t insert IN  March '
	END
	ELSE 
	BEGIN
		INSERT INTO Employee SELECT * FROM inserted
		SELECT 'OK !'
	END

END 
GO

INSERT INTO Employee 
VALUES ('Diea','Abdeltwab',102673 , '2001-02-22' ,'Fayoum','M',3600,102672,30)


--Q7=============================================================================================================================
USE ITI

CREATE TABLE Audit_table (Server_User_Name VARCHAR(50) , INSERT_Date DATE, Note VARCHAR(200))
 
GO
CREATE OR ALTER TRIGGER Student_Audit  ON Student AFTER INSERT
AS
BEGIN
	INSERT INTO Audit_table 
	VALUES ( SUSER_NAME() , GETDATE(), CONCAT(SUSER_NAME(),' Insert New Row with Key= ',(SELECT St_Id FROM inserted), ' in table : ', 'Student') )
	SELECT 'OK !'
END 
GO


INSERT INTO Student ( St_Id , St_Fname, St_Lname, St_Address)
VALUES (16,'John', 'Doe', 'Cairo');



--Q8=============================================================================================================================

GO
CREATE OR ALTER TRIGGER Student_Trigger ON Student INSTEAD OF  DELETE
AS
BEGIN
	INSERT INTO Audit_table 
	SELECT SUSER_NAME() , GETDATE(), CONCAT(SUSER_NAME(),' “ try to delete Row with Key= ', St_Id , ' in table : ', 'Student')
	FROM deleted
END 
GO

DELETE FROM  Student
WHERE St_Id = 16


--Q9=============================================================================================================================


USE AdventureWorks2022
GO

SELECT Emp.BusinessEntityID, Emp.NationalIDNumber, Emp.LoginID, Emp.JobTitle 
FROM HumanResources.Employee AS Emp 
FOR XML RAW, ELEMENTS;


GO
SELECT Emp.BusinessEntityID, Emp.NationalIDNumber, Emp.LoginID, Emp.JobTitle 
FROM HumanResources.Employee AS Emp 
FOR XML RAW, XMLDATA;

--Q10=============================================================================================================================
USE ITI;
GO

SELECT D.Dept_Name, I.Ins_Name
FROM Department D 
LEFT JOIN Instructor I ON D.Dept_Id = I.Dept_Id 
FOR XML AUTO;


GO

SELECT D.Dept_Name AS "Department/DeptName", 
       I.Ins_Name AS "Department/InstructorName"
FROM Department D 
LEFT JOIN Instructor I ON D.Dept_Id = I.Dept_Id 
FOR XML PATH('Departments');


--Q11=============================================================================================================================


USE Company_SD;
GO

CREATE TABLE Customers (
    CustomerID INT IDENTITY(1,1) PRIMARY KEY,
    FirstName NVARCHAR(100),
    Zipcode NVARCHAR(10),
    OrderID INT,
    OrderDetails NVARCHAR(100)
);

DECLARE @docs XML = 
'<customers>
    <customer FirstName="Bob" Zipcode="91126">
        <order ID="12221">Laptop</order>
    </customer>
    <customer FirstName="Judy" Zipcode="23235">
        <order ID="12221">Workstation</order>
    </customer>
    <customer FirstName="Howard" Zipcode="20009">
        <order ID="3331122">Laptop</order>
    </customer>
    <customer FirstName="Mary" Zipcode="12345">
        <order ID="555555">Server</order>
    </customer>
</customers>';

DECLARE @docHandle INT;

EXEC sp_xml_preparedocument @docHandle OUTPUT, @docs;

INSERT INTO Customers (FirstName, Zipcode, OrderID, OrderDetails)
SELECT 
    CustomerData.FirstName, 
    CustomerData.Zipcode,
    Orders.ID,
    Orders.OrderDetails
FROM OPENXML(@docHandle, '/customers/customer', 2) 
WITH (
    FirstName NVARCHAR(100) '@FirstName',
    Zipcode NVARCHAR(10) '@Zipcode'
) AS CustomerData
JOIN OPENXML(@docHandle, '/customers/customer/order', 2) 
WITH (
    ID INT '@ID',
    OrderDetails NVARCHAR(100) '.'
) AS Orders ON 1 = 1;

EXEC sp_xml_removedocument @docHandle;



--=====================================================================================================================================================
--Bonus================================================================================================================================================
--=====================================================================================================================================================

--Q1=====================================================================================================================================================

USE Company_SD
GO

CREATE OR ALTER TRIGGER Prevent_Table_Alter 
ON DATABASE 
FOR ALTER_TABLE 
AS
BEGIN
    PRINT 'You are not allowed to alter tables in the Company database.';
    ROLLBACK TRANSACTION;
END;
GO

--Q2=====================================================================================================================================================

USE ITI;
GO

SELECT 
    1 AS Tag,
    0 AS Parent,
    NULL AS "Students!1",
    NULL AS "Student!2!StudentId",
    NULL AS "Student!2!St_Fname",
    NULL AS "Student!2!St_Lname",
    NULL AS "Student!2!St_Address"
UNION ALL
SELECT 
    2 AS Tag,
    1 AS Parent,
    NULL,
    St_Id AS "Student!2!StudentId",
    St_Fname AS "Student!2!St_Fname",
    St_Lname AS "Student!2!St_Lname",
    St_Address AS "Student!2!St_Address"
FROM Student
ORDER BY Tag, "Student!2!StudentId"
FOR XML EXPLICIT;




--=====================================================================================================================================================
--=====================================================================================================================================================
--=====================================================================================================================================================

--################################################################################################################################################################################
--################################################################################################################################################################################
--################################################################################################################################################################################

--Q1=====================================================================================================================================================
USE Company_SD


GO

DECLARE Salary_Cursor CURSOR FOR 
SELECT E.SSN, E.Salary 
FROM Employee E ;

DECLARE @EmpNo INT, @Salary DECIMAL(18, 2);

OPEN Salary_Cursor;

-- Step 3: Fetch the First Record
FETCH NEXT FROM Salary_Cursor INTO @EmpNo, @Salary;

-- Step 4: Loop Through the Records
WHILE @@FETCH_STATUS = 0
BEGIN
    IF @Salary < 3000
    BEGIN
        UPDATE Employee 
        SET Salary = Salary * 1.10 
        WHERE SSN = @EmpNo;
    END
    ELSE
    BEGIN
        UPDATE Employee 
        SET Salary = Salary * 1.20 
        WHERE SSN = @EmpNo;
    END

    FETCH NEXT FROM Salary_Cursor INTO @EmpNo, @Salary;
END

CLOSE Salary_Cursor;
DEALLOCATE Salary_Cursor;

--Q2=====================================================================================================================================================
USE ITI

DECLARE  Department_Cursor CURSOR FOR 
SELECT D.Dept_Name , I.Ins_Name
FROM Department D , Instructor I 
WHERE I.Ins_Id = D.Dept_Manager

DECLARE @Dept_Name VARCHAR(50) , @Ins_Name VARCHAR(50)

OPEN Department_Cursor
FETCH NEXT FROM Department_Cursor INTO @Dept_Name , @Ins_Name 

WHILE @@FETCH_STATUS = 0
BEGIN
	SELECT @Dept_Name AS Dept_Name , @Ins_Name  AS Ins_Name
	FETCH NEXT FROM Department_Cursor INTO @Dept_Name , @Ins_Name 
END 

CLOSE Department_Cursor
DEALLOCATE Department_Cursor
--Q3=====================================================================================================================================================

DECLARE  Student_Cursor CURSOR FOR 
SELECT S.St_Fname FROM Student S

DECLARE  @St_Fname VARCHAR (50) , @All_St_Fname VARCHAR (500) = ''

OPEN Student_Cursor
FETCH NEXT FROM Student_Cursor INTO @St_Fname 
WHILE @@FETCH_STATUS = 0 
BEGIN
	SET @All_St_Fname = @All_St_Fname +  ISNULL(@St_Fname,'') + ' ,'

	FETCH NEXT FROM Student_Cursor INTO @St_Fname
END 
CLOSE Student_Cursor
DEALLOCATE Student_Cursor

SELECT @All_St_Fname

--Q4=====================================================================================================================================================
BACKUP DATABASE SD 
TO DISK = 'D:\SD_Full.bak'
WITH INIT, 
     NAME = 'Full Backup of SD Database',
     STATS = 10;  -- Displays progress every 10%


BACKUP DATABASE SD 
TO DISK = 'D:\SD_Diff.bak'
WITH DIFFERENTIAL, 
     INIT, 
     NAME = 'Differential Backup of SD Database',
     STATS = 10;


--Q5=====================================================================================================================================================
--Q6=====================================================================================================================================================


--Q7=====================================================================================================================================================


USE ITI;
GO

-- Create Sequence Object
CREATE SEQUENCE Seq_Example
    START WITH 1  
    INCREMENT BY 1  
    MINVALUE 1  
    MAXVALUE 10  
    NO CYCLE;

-- Fetch Next Value
SELECT NEXT VALUE FOR Seq_Example AS NextValue;

-- Test Sequence in Insert Statement
CREATE TABLE Test_Sequence (
    ID INT PRIMARY KEY,
    Name NVARCHAR(50)
);

INSERT INTO Test_Sequence (ID, Name)
VALUES (NEXT VALUE FOR Seq_Example, 'John Doe'),
       (NEXT VALUE FOR Seq_Example, 'Jane Smith'),
       (NEXT VALUE FOR Seq_Example, 'Mark Spencer');

-- Verify the Insert
SELECT * FROM Test_Sequence;



--=======================================================================================================================================================


