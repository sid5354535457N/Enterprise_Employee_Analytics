
-- Create Staging Database

CREATE DATABASE IF NOT EXISTS staging_db;

USE staging_db;


-- Table for 100,000 Current Employee Records

CREATE TABLE staging_current_employees (

    EmployeeNumber INT,
    EmployeeName VARCHAR(100),
    Age INT,
    Attrition VARCHAR(3),
    BusinessTravel VARCHAR(50),
    DailyRate INT,
    Department VARCHAR(100),
    DistanceFromHome INT,
    Education INT,
    EducationField VARCHAR(100),
    EmployeeCount INT,
    EnvironmentSatisfaction INT,
    Gender VARCHAR(20),
    HourlyRate INT,
    JobInvolvement INT,
    JobLevel INT,
    JobRole VARCHAR(100),
    JobSatisfaction INT,
    MaritalStatus VARCHAR(30),
    MonthlyIncome BIGINT,
    MonthlyRate INT,
    NumCompaniesWorked INT,
    Over18 VARCHAR(5),
    OverTime VARCHAR(5),
    PercentSalaryHike INT,
    PerformanceRating INT,
    RelationshipSatisfaction INT,
    StandardHours INT,
    StockOptionLevel INT,
    TotalWorkingYears INT,
    TrainingTimesLastYear INT,
    WorkLifeBalance INT,
    YearsAtCompany INT,
    YearsInCurrentRole INT,
    YearsSinceLastPromotion INT,
    YearsWithCurrManager INT,
    start_date DATE,
    end_date DATE,
    is_current TINYINT
);


-- Table for 120,000 Historical Records

CREATE TABLE staging_employee_history
LIKE staging_current_employees;


-- Verify Tables

SHOW TABLES;


USE staging_db;

SELECT COUNT(*)
FROM staging_current_employees;

SELECT COUNT(*)
FROM staging_employee_history;
