USE ITI 
--Q1============================================================================================
GO
CREATE OR ALTER  FUNCTION Mounth_Name ( @date DATE)
RETURNS VARCHAR(10)
	BEGIN 
		DECLARE @x VARCHAR(10)  
		SELECT @x=FORMAT( @date , 'MMMM'  )
		RETURN  @x
		
	END 
GO

SELECT dbo.Mounth_Name( GETDATE())
SELECT dbo.Mounth_Name('1-1-2024')

--Q2============================================================================================
GO
CREATE OR ALTER FUNCTION Number_Range (@num1 INT , @num2 INT )
RETURNS @t TABLE ( num_value INT )
AS 
	BEGIN 
		DECLARE @counter INT  =IIF(@num1 %2 = 0, @num1,@num1 + 1)
		WHILE @num2 != @counter
			BEGIN 
			INSERT @t VALUES (@counter )
			SELECT @counter = @counter +2 
			END

	RETURN
	END 
GO

SELECT * FROM Number_Range(1,10)



--Q3============================================================================================
GO
CREATE OR ALTER FUNCTION Student_Department ( @Stu_ID INT )
RETURNS TABLE
AS RETURN
	( 
		SELECT CONCAT(S.St_Fname ,' ',S.St_Lname) AS [Full Name] , D.Dept_Name  
		FROM Student S , Department D 
		WHERE D.Dept_Id = S.Dept_Id 
		AND S.St_Id = @Stu_ID
	) 
GO

SELECT * FROM Student_Department(1)
SELECT * FROM Student_Department(10)

--Q4============================================================================================
GO
CREATE OR ALTER FUNCTION Student_Null_Checker( @Stu_ID INT )
RETURNS VARCHAR(50)
	BEGIN 
		DECLARE @Report VARCHAR(50) , @Fname VARCHAR(50) ,  @Lname VARCHAR(50)

				SELECT  @Fname = St_Fname , @Lname = St_Lname FROM Student WHERE  St_Id = @Stu_ID

				IF  @Fname IS NULL AND  @Lname IS NULL 
					SET @Report = 'First name & last name are null'
				ELSE IF @Fname IS NULl
					SET @Report = 'first name is null'
				ELSE IF @Lname IS NULL 
					SET @Report = 'last name is null'
				ELSE 
					SET @Report = 'First name & last name are not null'
		RETURN @Report
	END 

GO

SELECT  dbo.Student_Null_Checker(1)
SELECT  dbo.Student_Null_Checker(13)
SELECT  dbo.Student_Null_Checker(14)
SELECT  dbo.Student_Null_Checker(15)


--Q5============================================================================================
GO
CREATE OR ALTER FUNCTION Department_INFO ( @managerID INT )
RETURNS TABLE 
AS RETURN 
(
	SELECT D.Dept_Name , I.Ins_Name FROM Department D , Instructor I WHERE I.Ins_Id = D.Dept_Manager AND @managerID=D.Dept_Manager

)
GO

SELECT * FROM Department_INFO(1)
SELECT * FROM Department_INFO(10)
SELECT * FROM Department_INFO(12)

--Q6============================================================================================
GO
CREATE OR ALTER FUNCTION Student_Name ( @string VARCHAR(10) )
RETURNS @t TABLE ( name VARCHAR(15) )
AS 
BEGIN 
	If @string='first name'
		INSERT INTO @t SELECT ISNULL(St_Fname,' ') FROM Student
	ELSE If @string='last name' 
		INSERT INTO @t SELECT ISNULL(St_Lname,' ') FROM Student
	ELSE If @string='full name'
		INSERT INTO @t SELECT CONCAT(St_Fname,' ',St_Lname) AS [Full Name] FROM Student

RETURN
END 
GO

SELECT * FROM Student_Name('first name')
SELECT * FROM Student_Name('last name' )
SELECT * FROM Student_Name('full name')
--============================================================================================
GO
CREATE OR ALTER FUNCTION Student_Name_ID ( @string VARCHAR(10) , @Stu_ID INT )
RETURNS @t TABLE ( name VARCHAR(15) )
AS 
BEGIN 
	If @string='first name'
		INSERT INTO @t SELECT ISNULL(St_Fname,' ') FROM Student WHERE @Stu_ID = St_Id
	ELSE If @string='last name' 
		INSERT INTO @t SELECT ISNULL(St_Lname,' ') FROM Student WHERE @Stu_ID = St_Id
	ELSE If @string='full name'
		INSERT INTO @t SELECT CONCAT(St_Fname,' ',St_Lname) AS [Full Name] FROM Student WHERE @Stu_ID = St_Id

RETURN
END 
GO

SELECT * FROM Student_Name_ID('first name',1)
SELECT * FROM Student_Name_ID('last name' ,1)
SELECT * FROM Student_Name_ID('full name' ,1)

--Q7============================================================================================

SELECT St_Id, SUBSTRING( St_Fname,1,LEN(St_Fname)-1) FROM Student


--Q8============================================================================================

DELETE FROM Stud_Course 
WHERE St_Id IN (
    SELECT S.St_Id 
    FROM Student S 
    JOIN Department D ON S.Dept_Id = D.Dept_Id 
    WHERE D.Dept_Name = 'SD'
);

--Bonus:============================================================================================
--Q1============================================================================================
-- إنشاء جدول الموظفين باستخدام HIERARCHYID
CREATE TABLE Temp_Emp (
    EmpID INT PRIMARY KEY,
    EmpName VARCHAR(50),
    Position HIERARCHYID
);
GO

-- إدراج بيانات هرمية
INSERT INTO Temp_Emp (EmpID, EmpName, Position) 
VALUES 
    (1, 'CEO', HIERARCHYID::GetRoot()),             -- الجذر (CEO)
    (2, 'Manager1', HIERARCHYID::Parse('/1/')),     -- تابع للـ CEO
    (3, 'Manager2', HIERARCHYID::Parse('/2/')),     -- تابع للـ CEO
    (4, 'Employee1', HIERARCHYID::Parse('/1/1/')),  -- تابع لـ Manager1
    (5, 'Employee2', HIERARCHYID::Parse('/1/2/')),  -- تابع لـ Manager1
    (6, 'Employee3', HIERARCHYID::Parse('/2/1/'));  -- تابع لـ Manager2

-- عرض البيانات
SELECT EmpID, EmpName, Position.ToString() AS HierarchyPath
FROM Temp_Emp;

--Q2============================================================================================

USE Company_SD

GO
DECLARE @Counter INT = 1;
DECLARE @Dept_Num INT 
SELECT @Dept_Num=D.Dnum FROM Departments D WHERE D.Dname='DP1'
WHILE @Counter <= 3000
	BEGIN
		INSERT INTO Employee (SSN, Lname, Fname, Dno )
		VALUES (@Counter, 'Smith', 'Jane', @Dept_Num );
		SET @Counter = @Counter + 1;
	END
--============================================================================================
GO

DECLARE @Counter INT = 1;
WHILE @Counter <= 3000
	BEGIN
		DELETE FROM Employee 
		WHERE SSN = @Counter 
		SELECT @Counter += 1;
	END
--============================================================================================
GO


INSERT INTO Employee (SSN, Lname, Fname, Dno)
SELECT 
    ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) AS SSN,
    'Smith' AS Lname,
    'Jane' AS Fname,
    1 AS Dno
FROM sys.objects o1, sys.objects o2
WHERE ROW_NUMBER() OVER (ORDER BY (SELECT NULL)) <= 3000;
