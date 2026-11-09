
USE warehouse_db;

-- Remove procedure if it already exists

DROP PROCEDURE IF EXISTS load_performance_fact;

DELIMITER //

CREATE PROCEDURE load_performance_fact()

BEGIN

    INSERT INTO Fact_PerformanceReviews (
        review_id,
        employee_key,
        project_key,
        date_key,
        department_key,
        performance_score,
        performance_rating,
        review_comments
    )

    WITH primary_project AS (

        SELECT
            employee_id,
            project_id,

            ROW_NUMBER() OVER (
                PARTITION BY employee_id
                ORDER BY assignment_id
            ) AS row_num

        FROM oltp_db.Assignments

    ),

    matched_reviews AS (

        SELECT
            r.review_id,
            e.employee_key,
            p.project_key,
            dt.date_key,
            d.department_key,
            r.performance_score,
            r.performance_rating,
            r.review_comments,

            ROW_NUMBER() OVER (
                PARTITION BY r.review_id
                ORDER BY e.employee_key
            ) AS version_rank

        FROM oltp_db.Reviews r

        JOIN Dim_Employee e
            ON r.employee_id = e.employee_id
            AND r.review_date >= e.start_date
            AND (
                e.end_date IS NULL
                OR r.review_date <= e.end_date
            )

        JOIN Dim_Department d
            ON e.department_name = d.department_name

        JOIN Dim_Date dt
            ON r.review_date = dt.full_date

        LEFT JOIN primary_project pp
            ON r.employee_id = pp.employee_id
            AND pp.row_num = 1

        LEFT JOIN Dim_Project p
            ON pp.project_id = p.project_id

    )

    SELECT
        mr.review_id,
        mr.employee_key,
        mr.project_key,
        mr.date_key,
        mr.department_key,
        mr.performance_score,
        mr.performance_rating,
        mr.review_comments

    FROM matched_reviews mr

    WHERE mr.version_rank = 1

    AND NOT EXISTS (
        SELECT 1
        FROM Fact_PerformanceReviews f
        WHERE f.review_id = mr.review_id
    );

END //

DELIMITER ;


SHOW PROCEDURE STATUS
WHERE Db = 'warehouse_db'
AND Name = 'load_performance_fact';

SELECT COUNT(*)
FROM Fact_PerformanceReviews;

SELECT COUNT(*)
FROM Fact_PerformanceReviews
WHERE project_key IS NULL;

USE warehouse_db;

CALL load_performance_fact();


SELECT COUNT(*)
FROM warehouse_db.Fact_PerformanceReviews;


SELECT
    COUNT(*) AS total_reviews,
    COUNT(employee_key) AS employee_links,
    COUNT(project_key) AS project_links,
    COUNT(date_key) AS date_links,
    COUNT(department_key) AS department_links
FROM warehouse_db.Fact_PerformanceReviews;