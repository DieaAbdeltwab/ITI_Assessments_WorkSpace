

USE Company_SD 

--Q1===================================================================================== 
SELECT D.Dependent_name , D.Sex  
FROM Employee E JOIN Dependent D   ON  E.SSN = D.ESSN
WHERE D.Sex = 'F' AND E.Sex  = 'F'

Union

SELECT D.Dependent_name , D.Sex  
FROM Employee E JOIN Dependent D   ON  E.SSN = D.ESSN
WHERE D.Sex = 'M' AND E.Sex  = 'M'
--Q2===================================================================================== 

SELECT P.Pname , SUM(W.Hours)
FROM Project P JOIN Works_for W ON P.Pnumber = W.Pno 
GROUP BY P.Pname

--Q3===================================================================================== 

SELECT D.*
FROM Departments D 
WHERE D.Dnum =  ( SELECT TOP (1) Dno FROM  Employee  WHERE Dno IS NOT NULL ORDER BY SSN  )


--Q4===================================================================================== 
SELECT  D.Dname , MAX(E.Salary) , MIN(E.Salary) , AVG(E.Salary)
FROM Employee E JOIN Departments D ON E.Dno = D.Dnum
GROUP BY D.Dname

--Q5===================================================================================== 
SELECT  E.Fname + ' ' + E.Lname AS "FULL NAME"
FROM Employee E JOIN Departments D ON E.SSN = D.MGRSSN 
WHERE E.SSN NOT IN (SELECT ESSN FROM Dependent )


SELECT  E.Fname + ' ' + E.Lname AS "FULL NAME"
FROM Employee E JOIN Departments D ON E.SSN = D.MGRSSN 
                LEFT JOIN Dependent ON  E.SSN = Dependent.ESSN
WHERE Dependent.ESSN IS NULL 

--Q6=====================================================================================

SELECT  D.Dnum , D.Dname , COUNT(E.SSN) AS "Employees COUTER " 
FROM Employee E JOIN Departments D ON E.Dno = D.Dnum
GROUP BY D.Dnum , D.Dname
HAVING AVG(E.Salary) < (SELECT AVG(Salary) FROM Employee)

--Q7=====================================================================================
SELECT E.Fname , P.Pname 
FROM Employee E 
JOIN Departments D ON E.Dno = D.Dnum 
JOIN Project P ON  D.Dnum = P.Dnum
ORDER BY D.Dnum , E.Fname , E.Lname



--Q8=====================================================================================
SELECT * FROM Employee 
WHERE Salary in
(SELECT distinct TOP(2) Salary 
FROM Employee 
ORDER BY Salary DESC )

--Q9=====================================================================================
SELECT E.Fname +' '+E.Lname AS "FULL NAME"
FROM Employee E JOIN Dependent D ON E.SSN = D.ESSN 
WHERE D.Dependent_name LIKE (E.Fname +' '+E.Lname)

SELECT E.Fname +' '+E.Lname AS "FULL NAME"
FROM Employee E JOIN Dependent D ON E.SSN = D.ESSN 
WHERE D.Dependent_name LIKE E.Fname  OR D.Dependent_name LIKE E.Lname
 
--Q10=====================================================================================
SELECT SSN, Fname + ' ' + Lname AS "Full Name"
FROM Employee E
WHERE EXISTS ( SELECT 1 FROM Dependent D WHERE D.ESSN = E.SSN )

--Q11=====================================================================================
INSERT INTO Departments (Dname , Dnum , MGRSSN , [MGRStart Date])
VALUES ( 'DEPT IT' ,100,112233, '1-11-2006')

--Q12=====================================================================================
-- a
UPDATE Departments
SET MGRSSN = 968574
WHERE Dnum = 100;

-- b
UPDATE Departments
SET MGRSSN = 102672
WHERE Dnum = 20;

-- c
UPDATE Employee
SET SuperSSN = 102672
WHERE SSN = 102660;

--Q13=====================================================================================

DELETE FROM Dependent
WHERE ESSN = 223344;

UPDATE Departments
SET MGRSSN = NULL
WHERE MGRSSN = 223344;

UPDATE Employee
SET SuperSSN = 102672
WHERE SuperSSN = 223344;

DELETE FROM Works_for
WHERE ESSN = 223344;

DELETE FROM Employee
WHERE SSN = 223344;
--Q14=====================================================================================


UPDATE Employee 
SET Salary = Salary + Salary * 0.30
where Employee.SSN IN  
(SELECT E.SSN 
FROM Employee E 
JOIN Departments D ON E.Dno = D.Dnum 
JOIN Project P ON  D.Dnum = P.Dnum 
and P.Pname = 'Al Rabwah' )
 