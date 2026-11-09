
from src.db_manager import DatabaseConnection
from mysql.connector import Error


class EmployeeManager:

    def __init__(self):
        self.db = DatabaseConnection()

    # CREATE: Add a new employee
    def add_employee(self, employee):

        connection = self.db.get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                INSERT INTO Employees (
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
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(query, employee.to_tuple())
            connection.commit()

            print("Employee added successfully!")
            return True

        except Error as e:
            connection.rollback()
            print("Error adding employee:", e)
            return False

        finally:
            if cursor:
                cursor.close()

            self.db.close_connection()

    # READ: Get employee by ID
    def get_employee_by_id(self, employee_id):

        connection = self.db.get_connection()

        if connection is None:
            return None

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT *
                FROM Employees
                WHERE employee_id = %s
            """

            cursor.execute(query, (employee_id,))

            return cursor.fetchone()

        except Error as e:
            print("Error fetching employee:", e)
            return None

        finally:
            if cursor:
                cursor.close()

            self.db.close_connection()

    # READ: Get all employees
    def get_all_employees(self, limit=10):

        connection = self.db.get_connection()

        if connection is None:
            return []

        cursor = None

        try:
            cursor = connection.cursor(dictionary=True)

            query = """
                SELECT *
                FROM Employees
                ORDER BY employee_id
                LIMIT %s
            """

            cursor.execute(query, (limit,))

            return cursor.fetchall()

        except Error as e:
            print("Error fetching employees:", e)
            return []

        finally:
            if cursor:
                cursor.close()

            self.db.close_connection()

    # UPDATE: Update employee details
    def update_employee(self, employee):

        connection = self.db.get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                UPDATE Employees
                SET
                    employee_name = %s,
                    age = %s,
                    gender = %s,
                    department_id = %s,
                    job_role = %s,
                    job_level = %s,
                    monthly_income = %s,
                    attrition = %s,
                    years_at_company = %s
                WHERE employee_id = %s
            """

            values = (
                employee.employee_name,
                employee.age,
                employee.gender,
                employee.department_id,
                employee.job_role,
                employee.job_level,
                employee.monthly_income,
                employee.attrition,
                employee.years_at_company,
                employee.employee_id
            )

            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                print("Employee updated successfully!")
                return True

            print("Employee not found or no changes made.")
            return False

        except Error as e:
            connection.rollback()
            print("Error updating employee:", e)
            return False

        finally:
            if cursor:
                cursor.close()

            self.db.close_connection()

    # DELETE: Delete employee by ID
    def delete_employee(self, employee_id):

        connection = self.db.get_connection()

        if connection is None:
            return False

        cursor = None

        try:
            cursor = connection.cursor()

            query = """
                DELETE FROM Employees
                WHERE employee_id = %s
            """

            cursor.execute(query, (employee_id,))
            connection.commit()

            if cursor.rowcount > 0:
                print("Employee deleted successfully!")
                return True

            print("Employee not found.")
            return False

        except Error as e:
            connection.rollback()
            print("Error deleting employee:", e)
            return False

        finally:
            if cursor:
                cursor.close()

            self.db.close_connection()
