
from src.db_manager import DatabaseConnection
from mysql.connector import Error


class AnalyticsManager:

    def __init__(self):
        self.db = DatabaseConnection()

    # Execute SELECT queries and return results
    def fetch_data(self, query, values=None):

        connection = self.db.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            cursor.execute(query, values or ())
            result = cursor.fetchall()

            return result

        except Error as e:
            print("Analytics error:", e)
            return []

        finally:
            if cursor:
                cursor.close()

            self.db.close_connection()

    # 1. Year-wise performance analysis
    def get_yearly_performance(self):

        query = """
            SELECT
                d.year_number AS review_year,
                ROUND(AVG(f.performance_score), 2) AS average_score

            FROM warehouse_db.Fact_PerformanceReviews f

            JOIN warehouse_db.Dim_Date d
                ON f.date_key = d.date_key

            GROUP BY d.year_number

            ORDER BY d.year_number
        """

        return self.fetch_data(query)

    # 2. Top performers in each department
    def get_top_performers(self, top_n=5):

        query = """
            WITH employee_performance AS (

                SELECT
                    e.employee_id,
                    e.employee_name,
                    d.department_name,
                    AVG(f.performance_score) AS average_score

                FROM warehouse_db.Fact_PerformanceReviews f

                JOIN warehouse_db.Dim_Employee e
                    ON f.employee_key = e.employee_key

                JOIN warehouse_db.Dim_Department d
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
                    ROUND(average_score, 2) AS average_score,

                    DENSE_RANK() OVER (
                        PARTITION BY department_name
                        ORDER BY average_score DESC
                    ) AS employee_rank

                FROM employee_performance
            )

            SELECT *
            FROM ranked_employees
            WHERE employee_rank <= %s
            ORDER BY department_name, employee_rank
        """

        return self.fetch_data(query, (top_n,))

    # 3. Department-wise attrition analysis
    def get_department_attrition(self):

        query = """
            SELECT
                d.department_name,

                COUNT(e.employee_id) AS total_employees,

                SUM(
                    CASE
                        WHEN e.attrition = 'Yes' THEN 1
                        ELSE 0
                    END
                ) AS employees_left,

                ROUND(
                    SUM(
                        CASE
                            WHEN e.attrition = 'Yes' THEN 1
                            ELSE 0
                        END
                    ) * 100.0 / COUNT(e.employee_id),
                    2
                ) AS attrition_percentage

            FROM warehouse_db.Dim_Employee e

            JOIN warehouse_db.Dim_Department d
                ON e.department_name = d.department_name

            WHERE e.is_current = 1

            GROUP BY d.department_name

            ORDER BY attrition_percentage DESC
        """

        return self.fetch_data(query)

    # 4. Project workload analysis
    def get_project_workload(self):

        query = """
            SELECT
                p.project_id,
                p.project_name,
                p.project_status,

                COUNT(DISTINCT a.employee_id) AS assigned_employees,

                ROUND(
                    COALESCE(SUM(a.allocation_percentage), 0),
                    2
                ) AS total_allocation,

                ROUND(
                    COALESCE(AVG(a.allocation_percentage), 0),
                    2
                ) AS average_allocation

            FROM oltp_db.Projects p

            LEFT JOIN oltp_db.Assignments a
                ON p.project_id = a.project_id

            GROUP BY
                p.project_id,
                p.project_name,
                p.project_status

            ORDER BY total_allocation DESC
        """

        return self.fetch_data(query)
