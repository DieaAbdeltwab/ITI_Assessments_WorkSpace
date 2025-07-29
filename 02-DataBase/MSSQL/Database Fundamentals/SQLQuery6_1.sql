
CREATE DATABASE INSTRUCTOR 
USE INSTRUCTOR
CREATE TABLE Instructor 
(
	ID          INT            IDENTITY PRIMARY KEY     ,
	FIRST_Name  VARCHAR(20)    ,
	LAST_Name   VARCHAR(20)     ,
	BD			DATE                   ,
	OverTime	INT	           UNIQUE      ,
	Salary		INT		       DEFAULT 3000  ,
	hiredate    DATE		   DEFAULT  GETDATE()  ,
	Address     VARCHAR(50)   ,

	Age         AS YEAR(GETDATE())-YEAR(BD) ,
	NetSalary   AS (ISNULL(Salary,0)+ISNULL(OverTime,0))   ,

	CONSTRAINT  ADDRESS_CHECK  CHECK(Address IN ('cairo' , 'alex' ) ) , 
	CONSTRAINT  SALARY_RANGE   CHECK(Salary BETWEEN 1000 AND 5000 )   

)

CREATE TABLE Course 
(
	CID INT IDENTITY PRIMARY KEY  ,
	CName VARCHAR(20)             ,
	Duration INT UNIQUE           
)

CREATE TABLE Instructor_Course 
(
	ID  INT  NOT NULL ,
	CID INT  NOT NULL ,
	PRIMARY KEY ( ID , CID ) ,
	FOREIGN KEY (ID)   REFERENCES Instructor(ID) ON DELETE CASCADE ON UPDATE CASCADE ,
	FOREIGN KEY (CID)  REFERENCES Course(CID)    ON DELETE CASCADE ON UPDATE CASCADE 
)


CREATE TABLE Lab 

(
	LID INT IDENTITY   ,
	Location VARCHAR(50)    ,
	Capacity INT ,

	CID INT NOT NULL ,

	PRIMARY KEY (LID,CID ),
	FOREIGN KEY (CID) REFERENCES Course(CID)  ON DELETE CASCADE ON UPDATE CASCADE 

)
ALTER TABLE Lab ADD CONSTRAINT CAPACITY_CHECK CHECK(Capacity < 20 )
