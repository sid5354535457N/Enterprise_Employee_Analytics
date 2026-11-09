
USE warehouse_db;

-- Rank Employees by Department Performance

WITH employee_performance AS (

    SELECT
        e.employee_id,
        e.employee_name,
        d.department_name,

        AVG(f.performance_score) AS average_score

    FROM Fact_PerformanceReviews f

    JOIN Dim_Employee e
        ON f.employee_key = e.employee_key

    JOIN Dim_Department d
        ON f.department_key = d.department_key

    GROUP BY
        e.employee_id,
        e.employee_name,
        d.department_name

),

ranked_employees AS (

    SELECT
        employee_id,
        employee_name,
        department_name,
        average_score,

        DENSE_RANK() OVER (
            PARTITION BY department_name
            ORDER BY average_score DESC
        ) AS employee_rank

    FROM employee_performance

)

SELECT *
FROM ranked_employees

WHERE employee_rank <= 5

ORDER BY department_name, employee_rank;

SELECT COUNT(*)
FROM oltp_db.Reviews;



SELECT COUNT(*) AS matched_records

FROM oltp_db.Reviews r

JOIN warehouse_db.Dim_Employee e
ON r.employee_id = e.employee_id

AND r.review_date >= e.start_date

AND (
    e.end_date IS NULL
    OR r.review_date <= e.end_date
);



SELECT COUNT(*) AS matched_records

FROM oltp_db.Reviews r

JOIN warehouse_db.Dim_Employee e
ON r.employee_id = e.employee_id

AND r.review_date >= e.start_date

AND (
    e.end_date IS NULL
    OR r.review_date <= e.end_date
)

JOIN warehouse_db.Dim_Date dt
ON r.review_date = dt.full_date

JOIN warehouse_db.Dim_Department d
ON e.department_name = d.department_name;


SHOW PROCEDURE STATUS
WHERE Db = 'warehouse_db'
AND Name = 'load_performance_fact';