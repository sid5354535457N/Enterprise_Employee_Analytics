
USE warehouse_db;

-- Remove old procedure if it exists

DROP PROCEDURE IF EXISTS load_project_date_dimensions;

DELIMITER //

CREATE PROCEDURE load_project_date_dimensions()

BEGIN

    -- Load Project Dimension

    INSERT INTO Dim_Project (
        project_id,
        project_name,
        start_date,
        end_date,
        project_status
    )

    SELECT
        p.project_id,
        p.project_name,
        p.start_date,
        p.end_date,
        p.project_status

    FROM oltp_db.Projects p

    WHERE NOT EXISTS (
        SELECT 1
        FROM Dim_Project d
        WHERE d.project_id = p.project_id
    );


    -- Load Date Dimension

    INSERT INTO Dim_Date (
        full_date,
        day_number,
        month_number,
        month_name,
        quarter_number,
        year_number
    )

    SELECT DISTINCT
        r.review_date,
        DAY(r.review_date),
        MONTH(r.review_date),
        MONTHNAME(r.review_date),
        QUARTER(r.review_date),
        YEAR(r.review_date)

    FROM oltp_db.Reviews r

    WHERE NOT EXISTS (
        SELECT 1
        FROM Dim_Date d
        WHERE d.full_date = r.review_date
    );

END //

DELIMITER ;


-- Execute Procedure

CALL load_project_date_dimensions();



SELECT COUNT(*)
FROM warehouse_db.Fact_PerformanceReviews;

SELECT COUNT(*) FROM warehouse_db.Dim_Date;

SELECT COUNT(*) FROM warehouse_db.Dim_Project;
