USE ITI

--Q1============================================================================
GO
CREATE VIEW V_Student_More_50
AS
SELECT CONCAT(S.St_Fname,' ',S.St_Lname  ) AS [Full_Name]  , C.Crs_Name 
FROM Student S
JOIN Stud_Course SC ON S.St_Id = SC.St_Id
JOIN Course C ON C.Crs_Id = SC.Crs_Id
WHERE SC.Grade > 50
GO

SELECT * FROM V_Student_More_50

EXEC sp_helptext  'V_Student_More_50'

--Q2============================================================================
GO
CREATE VIEW V_Ins_Manag_Crs
WITH ENCRYPTION 
AS
SELECT I.Ins_Name , C.Crs_Name
FROM Instructor I
JOIN Department D ON I.Ins_Id = D.Dept_Manager
JOIN Ins_Course IC ON I.Ins_Id = IC.Ins_Id
JOIN Course C ON C.Crs_Id = IC.Crs_Id
GO

SELECT * FROM V_Ins_Manag_Crs
EXEC sp_helptext  'V_Ins_Manag_Crs'

--Q3============================================================================
GO
CREATE VIEW V_Ins_Dept_Name
AS
SELECT I.Ins_Name , D.Dept_Name
FROM Instructor I
JOIN Department D ON D.Dept_Id = I.Dept_Id
WHERE D.Dept_Name IN ('SD','Java')
GO

SELECT * FROM V_Ins_Dept_Name


--Q4============================================================================
GO
CREATE OR ALTER VIEW V1
WITH SCHEMABINDING
AS
SELECT 
S.St_Id,S.St_Fname,S.St_Lname,S.St_Address 
FROM dbo.Student S
WHERE S.St_Address IN ('Cairo', 'Alex')
WITH CHECK OPTION;
GO

Update V1 set st_address='tanta'
Where st_address='alex';

Update Student set st_address='alex'
Where st_address='tanta';


SELECT * FROM V1
SELECT * FROM Student


--Q5============================================================================
USE Company_SD

GO
CREATE VIEW Project_Counters
AS
SELECT P.Pname , COUNT(WF.ESSn) AS Num_Employees
FROM Project P
JOIN Works_for WF ON P.Pnumber = WF.Pno
GROUP BY P.Pname
GO
SELECT * FROM Project_Counters


--Q6============================================================================
USE ITI

--DROP INDEX IF EXISTS Department.IDX_Department_Hiredate;
CREATE CLUSTERED INDEX IDX_Department_Hiredate
ON Department (Manager_hiredate);


--Q7============================================================================

CREATE UNIQUE INDEX IDX_Student_Age
ON Student (St_Age);


--Q8============================================================================

CREATE TABLE #DailyTransactions (
    UserID INT PRIMARY KEY,
    TransactionAmount DECIMAL(10, 2)
);

CREATE TABLE #LastTransactions (
    UserID INT PRIMARY KEY,
    TransactionAmount DECIMAL(10, 2)
);

INSERT INTO #DailyTransactions (UserID, TransactionAmount)
VALUES 
    (1, 1000),
    (2, 2000),
    (3, 1000);

INSERT INTO #LastTransactions (UserID, TransactionAmount)
VALUES 
    (1, 4000),
    (2, 2000),
    (4, 10000);




MERGE INTO #DailyTransactions AS D
USING #LastTransactions AS L
ON D.UserID = L.UserID
WHEN MATCHED THEN
    UPDATE SET D.TransactionAmount = D.TransactionAmount + L.TransactionAmount
WHEN  NOT MATCHED BY TARGET THEN
	INSERT (UserID, TransactionAmount) VALUES (L.UserID, L.TransactionAmount)
WHEN  NOT MATCHED BY SOURCE THEN
	DELETE ;


SELECT * FROM #DailyTransactions
SELECT * FROM #LastTransactions



--###############################################################################################################
--###############################################################################################################
--###############################################################################################################
USE SD
--Q1============================================================================
GO
CREATE VIEW v_clerk 
AS
SELECT WO.EmpNo, WO.ProjectNo, WO.Enter_Date
FROM Works_on WO
WHERE WO.Job = 'Clerk';
GO

SELECT * FROM v_clerk

--Q2============================================================================
GO
CREATE OR ALTER VIEW v_without_budget 
AS
SELECT P.ProjectNo, P.ProjectName
FROM Company.Project P
--WHERE P.Budget IS NULL;
GO
SELECT * FROM v_without_budget

--Q3============================================================================
GO
CREATE OR ALTER  VIEW v_count AS
SELECT P.ProjectName, COUNT(WO.Job) AS JobCount
FROM Company.Project P
JOIN Works_on WO ON P.ProjectNo = WO.ProjectNo --LEFT JOIN 
GROUP BY P.ProjectName
GO
SELECT * FROM v_count

--Q4============================================================================
GO
CREATE OR ALTER VIEW v_project_p2 
AS 
SELECT VC.EmpNo FROM v_clerk VC
WHERE VC.ProjectNo = 'p2'
GO
SELECT * FROM v_project_p2

GO
CREATE OR ALTER VIEW v_project_p2 
AS 
SELECT VC.EmpNo , E.EmpFname , E.EmpLname 
FROM v_clerk VC
JOIN HumanResource.Employee E ON E.EmpNo = VC.EmpNo
WHERE VC.ProjectNo = 'p2'
GO
SELECT * FROM v_project_p2

--Q5============================================================================

GO
ALTER VIEW v_without_budget
AS
SELECT P.ProjectNo, P.ProjectName
FROM Company.Project P
WHERE P.ProjectNo IN ( 'p1','p2')
--AND P.Budget IS NULL;
GO
SELECT * FROM v_without_budget


--Q6============================================================================
DROP VIEW v_clerk
DROP VIEW v_count
--Q7============================================================================
GO
CREATE VIEW v_emp_d2
AS 
SELECT E.EmpNo , E.EmpLname
FROM HumanResource.Employee E
JOIN Company.Department D ON D.DeptNo = E.DeptNo
WHERE D.DeptNo = 'd2'
GO
SELECT * FROM v_emp_d2

--Q8============================================================================
SELECT VED2.EmpLname FROM v_emp_d2 VED2
WHERE VED2.EmpLname LIKE '%J%'

--Q9============================================================================
GO
CREATE VIEW v_dept
AS 
SELECT D.DeptNo , D.DeptName
FROM Company.Department D
GO
SELECT * FROM v_dept


--Q10============================================================================
INSERT INTO v_dept VALUES ('d4','Development')



SELECT * FROM v_dept
SELECT * FROM Company.Department

--Q11============================================================================
GO
CREATE OR ALTER VIEW v_2006_check 
--WITH CHECK OPTION
AS
SELECT E.EmpNo , WO.ProjectNo
FROM HumanResource.Employee E
JOIN Works_on WO ON E.EmpNo = WO.EmpNo
WHERE   WO.Enter_Date BETWEEN '01-01-2006' AND '12-31-2006' -- YEAR(WO.Enter_Date) = 2006
WITH CHECK OPTION
GO

SELECT * FROM v_2006_check

--=============================================================================================================
