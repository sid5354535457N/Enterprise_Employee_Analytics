
-- Create OLTP Database

CREATE DATABASE IF NOT EXISTS oltp_db;

USE oltp_db;


-- 1. Departments Table

CREATE TABLE Departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(100) NOT NULL UNIQUE
);


-- 2. Employees Table

CREATE TABLE Employees (
    employee_id INT PRIMARY KEY,
    employee_name VARCHAR(100) NOT NULL,
    age INT,
    gender VARCHAR(20),
    department_id INT NOT NULL,
    job_role VARCHAR(100),
    job_level INT,
    monthly_income DECIMAL(10,2),
    attrition VARCHAR(3),
    years_at_company INT,

    FOREIGN KEY (department_id)
    REFERENCES Departments(department_id)
);


-- 3. Projects Table

CREATE TABLE Projects (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(100) NOT NULL,
    start_date DATE,
    end_date DATE,
    project_status VARCHAR(30)
);


-- 4. Assignments Table

CREATE TABLE Assignments (
    assignment_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    project_id INT NOT NULL,
    assigned_date DATE,
    project_role VARCHAR(100),
    allocation_percentage DECIMAL(5,2),

    FOREIGN KEY (employee_id)
    REFERENCES Employees(employee_id),

    FOREIGN KEY (project_id)
    REFERENCES Projects(project_id)
);


-- 5. Reviews Table

CREATE TABLE Reviews (
    review_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT NOT NULL,
    review_date DATE,
    performance_score DECIMAL(5,2),
    performance_rating INT,
    review_comments TEXT,

    FOREIGN KEY (employee_id)
    REFERENCES Employees(employee_id)
);


-- Insert Department Records

INSERT INTO Departments (department_name)
VALUES
('Sales'),
('Research & Development'),
('Human Resources');


-- Display Created Tables

SHOW TABLES;

DESC Departments;
DESC Employees;
DESC Projects;
DESC Assignments;
DESC Reviews;


SELECT * FROM Departments;


USE oltp_db;

SHOW TABLES;