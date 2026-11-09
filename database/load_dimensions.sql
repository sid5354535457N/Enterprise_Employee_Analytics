
USE warehouse_db;

-- Start Transaction
START TRANSACTION;


-- 1. Load Department Dimension

INSERT INTO Dim_Department (department_name)

SELECT DISTINCT Department
FROM staging_db.staging_current_employees;


-- 2. Load Employee Dimension with Historical Records

INSERT INTO Dim_Employee (
    employee_id,
    employee_name,
    age,
    gender,
    department_name,
    job_role,
    job_level,
    monthly_income,
    attrition,
    years_at_company,
    start_date,
    end_date,
    is_current
)

SELECT
    EmployeeNumber,
    EmployeeName,
    Age,
    Gender,
    Department,
    JobRole,
    JobLevel,
    MonthlyIncome,
    Attrition,
    YearsAtCompany,
    start_date,
    end_date,
    is_current

FROM staging_db.staging_employee_history;


-- Save Changes
COMMIT;



SELECT employee_id, COUNT(*) AS total_versions
FROM Dim_Employee
GROUP BY employee_id
HAVING COUNT(*) > 1
LIMIT 5;


SELECT
    employee_id,
    employee_name,
    department_name,
    job_role,
    monthly_income,
    start_date,
    end_date,
    is_current
FROM Dim_Employee
WHERE employee_id = 101
ORDER BY start_date;




-- Load Employees from Staging into OLTP

START TRANSACTION;

INSERT INTO oltp_db.Employees (
    employee_id,
    employee_name,
    age,
    gender,
    department_id,
    job_role,
    job_level,
    monthly_income,
    attrition,
    years_at_company
)

SELECT
    s.EmployeeNumber,
    s.EmployeeName,
    s.Age,
    s.Gender,
    d.department_id,
    s.JobRole,
    s.JobLevel,
    s.MonthlyIncome,
    s.Attrition,
    s.YearsAtCompany

FROM staging_db.staging_current_employees s

JOIN oltp_db.Departments d
ON s.Department = d.department_name;

COMMIT;

SELECT COUNT(*) FROM oltp_db.Employees;




USE oltp_db;

START TRANSACTION;


-- 1. Insert Projects

INSERT INTO Projects
(project_name, start_date, end_date, project_status)

VALUES
('HR Management System', '2024-01-01', '2026-12-31', 'Active'),
('Employee Analytics Platform', '2024-03-01', '2026-12-31', 'Active'),
('Customer Portal', '2023-01-01', '2025-12-31', 'Completed'),
('Data Warehouse Migration', '2024-06-01', '2026-12-31', 'Active'),
('Payroll Automation', '2024-02-01', '2026-06-30', 'Completed'),
('Recruitment Portal', '2025-01-01', '2026-12-31', 'Active'),
('Sales Dashboard', '2023-05-01', '2025-12-31', 'Completed'),
('Cloud Migration', '2025-04-01', NULL, 'Active'),
('Mobile Application', '2025-06-01', NULL, 'Active'),
('Process Automation', '2024-08-01', '2026-12-31', 'Active');


-- 2. Assign Every Employee to One Project

INSERT INTO Assignments
(employee_id, project_id, assigned_date,
 project_role, allocation_percentage)

SELECT
    e.employee_id,
    MOD(e.employee_id - 1, 10) + 1,
    p.start_date,
    e.job_role,
    100.00

FROM Employees e

JOIN Projects p
ON p.project_id = MOD(e.employee_id - 1, 10) + 1;


-- 3. Give Additional Project Assignments
-- Every 5th employee gets one more project

INSERT INTO Assignments
(employee_id, project_id, assigned_date,
 project_role, allocation_percentage)

SELECT
    e.employee_id,
    MOD(e.employee_id + 2, 10) + 1,
    DATE_ADD(p.start_date, INTERVAL 30 DAY),
    e.job_role,
    50.00

FROM Employees e

JOIN Projects p
ON p.project_id = MOD(e.employee_id + 2, 10) + 1

WHERE MOD(e.employee_id, 5) = 0;


-- 4. Generate 2025 Performance Reviews

INSERT INTO Reviews
(employee_id, review_date, performance_score,
 performance_rating, review_comments)

SELECT
    e.employee_id,

    DATE_ADD('2025-01-01',
        INTERVAL MOD(e.employee_id, 365) DAY),

    60 + MOD(e.employee_id * 7, 40),

    s.PerformanceRating,

    'Annual performance review - 2025'

FROM Employees e

JOIN staging_db.staging_current_employees s
ON e.employee_id = s.EmployeeNumber;



INSERT INTO Reviews
(employee_id, review_date, performance_score,
 performance_rating, review_comments)

SELECT
    e.employee_id,

    DATE_ADD('2026-01-01',
        INTERVAL MOD(e.employee_id, 365) DAY),

    60 + MOD(e.employee_id * 3, 40),

    s.PerformanceRating,

    'Annual performance review - 2026'

FROM Employees e

JOIN staging_db.staging_current_employees s
ON e.employee_id = s.EmployeeNumber;