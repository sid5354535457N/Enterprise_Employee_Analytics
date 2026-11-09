
-- Create Data Warehouse Database

CREATE DATABASE IF NOT EXISTS warehouse_db;

USE warehouse_db;


-- 1. Department Dimension

CREATE TABLE Dim_Department (

    department_key INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE

);


-- 2. Date Dimension

CREATE TABLE Dim_Date (

    date_key INT AUTO_INCREMENT PRIMARY KEY,
    full_date DATE NOT NULL UNIQUE,
    day_number INT,
    month_number INT,
    month_name VARCHAR(20),
    quarter_number INT,
    year_number INT

);


-- 3. Employee Dimension

CREATE TABLE Dim_Employee (

    employee_key INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    employee_name VARCHAR(100),
    age INT,
    gender VARCHAR(20),
    department_name VARCHAR(100),
    job_role VARCHAR(100),
    job_level INT,
    monthly_income BIGINT,
    attrition VARCHAR(3),
    years_at_company INT,

    start_date DATE NOT NULL,
    end_date DATE,
    is_current TINYINT NOT NULL DEFAULT 1,

    INDEX idx_employee_id (employee_id)

);


-- 4. Project Dimension

CREATE TABLE Dim_Project (

    project_key INT AUTO_INCREMENT PRIMARY KEY,
    project_id INT NOT NULL UNIQUE,
    project_name VARCHAR(100),
    start_date DATE,
    end_date DATE,
    project_status VARCHAR(30)

);


-- 5. Performance Review Fact Table

CREATE TABLE Fact_PerformanceReviews (

    fact_review_key INT AUTO_INCREMENT PRIMARY KEY,
    review_id INT NOT NULL UNIQUE,

    employee_key INT NOT NULL,
    project_key INT,
    date_key INT NOT NULL,
    department_key INT NOT NULL,

    performance_score DECIMAL(5,2),
    performance_rating INT,
    review_comments TEXT,

    FOREIGN KEY (employee_key)
    REFERENCES Dim_Employee(employee_key),

    FOREIGN KEY (project_key)
    REFERENCES Dim_Project(project_key),

    FOREIGN KEY (date_key)
    REFERENCES Dim_Date(date_key),

    FOREIGN KEY (department_key)
    REFERENCES Dim_Department(department_key)

);


-- Verify Tables

SHOW TABLES;
