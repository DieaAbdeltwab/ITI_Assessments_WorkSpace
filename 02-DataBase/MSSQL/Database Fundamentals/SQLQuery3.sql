

USE Company_SD
--Q1
SELECT Departments.Dnum , Departments.Dname , Employee.SSN ,  Employee.Fname 
FROM Departments
JOIN Employee ON Employee.SSN = Departments.MGRSSN


--Q2
SELECT Departments.Dname , Project.Pname 
FROM Departments , Project 
WHERE Departments.Dnum = Project.Dnum

--Q3 
SELECT Dependent.* , Employee.Fname +' '+ Employee.Lname as "Full Name"  
FROM Dependent 
JOIN Employee  ON Employee.SSN = Dependent.ESSN


--Q4
SELECT Pnumber , Pname , Plocation
FROM Project
WHERE City IN ( 'Cairo' , 'Alex' )

--Q5
SELECT * 
FROM Project
WHERE Pname LIKE 'a%'

--Q6
SELECT Fname +' '+ Lname as "Full Name" 
FROM Employee  
WHERE  Dno = 30 
AND Salary BETWEEN 1000 AND 2000


--Q7 
SELECT  DISTINCT Employee.Fname +' '+ Employee.Lname as "Full Name"
FROM Employee , Works_for ,  Project
WHERE Project.Pnumber = Works_for.Pno AND Employee.SSN = Works_for.ESSn
AND Employee.Dno = 10 
AND Works_for.Hours >= 10
AND Project.Pname = 'AL Rabwah'


--Q8
SELECT  E.Fname +' '+ E.Lname as "Full Name"
FROM Employee E , Employee S
WHERE  S.SSN =  E.Superssn 
AND S.Fname = 'Kamel' AND S.Lname = 'Mohamed'


--Q9
SELECT  DISTINCT Employee.Fname +' '+ Employee.Lname as "Full Name" , Project.Pname
FROM Employee Join Works_for on  Employee.SSN =  Works_for.ESSn
              Join Project   on  Project.Pnumber = Works_for.Pno 
ORDER BY Project.Pname



--Q10
SELECT Project.Pnumber , Departments.Dname , Employee.Lname ,Employee.Address , Employee.Bdate 
FROM Project JOIN Departments ON Departments.Dnum = Project.Dnum
		     JOIN Employee    ON Employee.SSN = Departments.MGRSSN
WHERE  Project.City = 'Cairo'


--Q11
SELECT Employee.* 
FROM   Departments , Employee 
WHERE Employee.SSN = Departments.MGRSSN 



--Q12
SELECT Employee.* , Dependent.*
FROM Employee LEFT OUTER JOIN Dependent 
on Employee.SSN = Dependent.ESSN

--Q13
INSERT INTO Employee 
VALUES ('Diea' , 'Abdeltwab' ,102672 , '2001-02-22' , 'Fayoum' , 'M' ,3000 , 112233, 30 ) 

--Q14
INSERT INTO Employee(Fname , Lname , SSN , Bdate , Address , Sex , Dno ) 
VALUES ('Abdeltwab' , 'Diea' ,102660 , '2001-02-22' , 'Fayoum' , 'M' , 30 )  


--Q15
UPDATE Employee
SET Salary = Salary + Salary* 0.20 -- Salary* 1.20
WHERE SSN = 102672 

