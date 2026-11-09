
import streamlit as st
import pandas as pd

from src.db_manager import DatabaseConnection
from src.models.employee import Employee
from src.managers.employee_manager import EmployeeManager
from src.managers.analytics_manager import AnalyticsManager


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Employee Analytics System",
    page_icon="📊",
    layout="wide"
)


# --------------------------------------------------
# CREATE MANAGER OBJECTS
# --------------------------------------------------

employee_manager = EmployeeManager()
analytics_manager = AnalyticsManager()


# --------------------------------------------------
# GET DEPARTMENTS FROM MYSQL
# --------------------------------------------------

def get_departments():

    db = DatabaseConnection()
    connection = db.get_connection()

    if connection is None:
        return []

    cursor = None

    try:
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT department_id, department_name
            FROM Departments
            ORDER BY department_name
        """

        cursor.execute(query)

        return cursor.fetchall()

    except Exception as e:
        st.error(f"Unable to load departments: {e}")
        return []

    finally:
        if cursor:
            cursor.close()

        db.close_connection()


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("Enterprise Employee Analytics System")

st.write(
    "Manage employee information and analyse "
    "employee performance using Python, MySQL and Streamlit."
)


# --------------------------------------------------
# SIDEBAR NAVIGATION
# --------------------------------------------------

st.sidebar.title("Navigation")

section = st.sidebar.radio(
    "Select Section",
    [
        "Employee Management",
        "Analytics Dashboard"
    ]
)


# ==================================================
# EMPLOYEE MANAGEMENT
# ==================================================

if section == "Employee Management":

    st.header("Employee Management")

    departments = get_departments()

    department_options = {
        row["department_name"]: row["department_id"]
        for row in departments
    }

    if not department_options:

        st.warning(
            "No departments found. Please check your MySQL database."
        )

    else:

        # ------------------------------------------
        # ADD EMPLOYEE
        # ------------------------------------------

        st.subheader("Add New Employee")

        with st.expander("Open Add Employee Form"):

            with st.form("add_employee_form"):

                employee_id = st.number_input(
                    "Employee ID",
                    min_value=1,
                    value=100001,
                    step=1
                )

                employee_name = st.text_input(
                    "Employee Name"
                )

                age = st.number_input(
                    "Age",
                    min_value=18,
                    max_value=100,
                    value=25
                )

                gender = st.selectbox(
                    "Gender",
                    ["Male", "Female"]
                )

                department_name = st.selectbox(
                    "Department",
                    list(department_options.keys())
                )

                job_role = st.text_input(
                    "Job Role"
                )

                job_level = st.number_input(
                    "Job Level",
                    min_value=1,
                    max_value=5,
                    value=1
                )

                monthly_income = st.number_input(
                    "Monthly Income",
                    min_value=0.0,
                    value=30000.0
                )

                attrition = st.selectbox(
                    "Attrition",
                    ["No", "Yes"]
                )

                years_at_company = st.number_input(
                    "Years at Company",
                    min_value=0,
                    value=1
                )

                add_button = st.form_submit_button(
                    "Add Employee"
                )

                if add_button:

                    if not employee_name.strip() or not job_role.strip():

                        st.error(
                            "Employee name and job role are required."
                        )

                    else:

                        employee = Employee(
                            int(employee_id),
                            employee_name,
                            int(age),
                            gender,
                            department_options[department_name],
                            job_role,
                            int(job_level),
                            monthly_income,
                            attrition,
                            int(years_at_company)
                        )

                        if employee_manager.add_employee(employee):

                            st.success(
                                "Employee added successfully!"
                            )

                        else:

                            st.error(
                                "Unable to add employee. "
                                "Check the employee ID and database error."
                            )


        st.divider()


        # ------------------------------------------
        # SEARCH EMPLOYEE
        # ------------------------------------------

        st.subheader("Search Employee")

        search_id = st.number_input(
            "Enter Employee ID",
            min_value=1,
            step=1,
            key="search_employee_id"
        )

        if st.button("Search Employee"):

            result = employee_manager.get_employee_by_id(
                int(search_id)
            )

            if result:

                st.success("Employee found!")

                st.dataframe(
                    pd.DataFrame([result]),
                    width="stretch",
                    hide_index=True
                )

            else:

                st.warning("Employee not found.")


        st.divider()


        # ------------------------------------------
        # VIEW EMPLOYEES
        # ------------------------------------------

        st.subheader("View Employees")

        limit = st.number_input(
            "Number of records to display",
            min_value=1,
            max_value=1000,
            value=20,
            key="employee_limit"
        )

        if st.button("Load Employees"):

            employees = employee_manager.get_all_employees(
                int(limit)
            )

            if employees:

                st.dataframe(
                    pd.DataFrame(employees),
                    width="stretch",
                    hide_index=True
                )

            else:

                st.info("No employee records found.")


        st.divider()


        # ------------------------------------------
        # UPDATE EMPLOYEE
        # ------------------------------------------

        st.subheader("Update Employee")

        with st.expander("Open Update Employee Form"):

            with st.form("update_employee_form"):

                update_id = st.number_input(
                    "Employee ID to Update",
                    min_value=1,
                    step=1
                )

                update_name = st.text_input(
                    "Updated Employee Name"
                )

                update_age = st.number_input(
                    "Updated Age",
                    min_value=18,
                    max_value=100,
                    value=25
                )

                update_gender = st.selectbox(
                    "Updated Gender",
                    ["Male", "Female"]
                )

                update_department = st.selectbox(
                    "Updated Department",
                    list(department_options.keys())
                )

                update_role = st.text_input(
                    "Updated Job Role"
                )

                update_level = st.number_input(
                    "Updated Job Level",
                    min_value=1,
                    max_value=5,
                    value=1
                )

                update_income = st.number_input(
                    "Updated Monthly Income",
                    min_value=0.0,
                    value=30000.0
                )

                update_attrition = st.selectbox(
                    "Updated Attrition",
                    ["No", "Yes"]
                )

                update_years = st.number_input(
                    "Updated Years at Company",
                    min_value=0,
                    value=1
                )

                update_button = st.form_submit_button(
                    "Update Employee"
                )

                if update_button:

                    if not update_name.strip() or not update_role.strip():

                        st.error(
                            "Employee name and job role are required."
                        )

                    else:

                        employee = Employee(
                            int(update_id),
                            update_name,
                            int(update_age),
                            update_gender,
                            department_options[update_department],
                            update_role,
                            int(update_level),
                            update_income,
                            update_attrition,
                            int(update_years)
                        )

                        if employee_manager.update_employee(employee):

                            st.success(
                                "Employee updated successfully!"
                            )

                        else:

                            st.warning(
                                "Employee was not updated. "
                                "Check the employee ID or database error."
                            )


        st.divider()


        # ------------------------------------------
        # DELETE EMPLOYEE
        # ------------------------------------------

        st.subheader("Delete Employee")

        with st.expander("Open Delete Employee Form"):

            with st.form("delete_employee_form"):

                delete_id = st.number_input(
                    "Employee ID to Delete",
                    min_value=1,
                    step=1
                )

                confirm_delete = st.checkbox(
                    "I confirm that I want to delete this employee."
                )

                delete_button = st.form_submit_button(
                    "Delete Employee"
                )

                if delete_button:

                    if confirm_delete:

                        if employee_manager.delete_employee(
                            int(delete_id)
                        ):

                            st.success(
                                "Employee deleted successfully!"
                            )

                        else:

                            st.error(
                                "Deletion failed. The employee may not exist "
                                "or may have related records."
                            )

                    else:

                        st.warning(
                            "Please confirm before deleting."
                        )


# ==================================================
# ANALYTICS DASHBOARD
# ==================================================

elif section == "Analytics Dashboard":

    st.header("Employee Analytics Dashboard")


    # ----------------------------------------------
    # 1. YEAR-WISE PERFORMANCE
    # ----------------------------------------------

    st.subheader("1. Year-wise Performance Analysis")

    yearly_data = analytics_manager.get_yearly_performance()

    if yearly_data:

        yearly_df = pd.DataFrame(yearly_data)

        yearly_df["average_score"] = pd.to_numeric(
            yearly_df["average_score"]
        )

        st.dataframe(
            yearly_df,
            width="stretch",
            hide_index=True
        )

        st.line_chart(
            yearly_df.set_index("review_year")[
                ["average_score"]
            ]
        )

    else:

        st.info("No yearly performance data available.")


    st.divider()


    # ----------------------------------------------
    # 2. TOP PERFORMERS
    # ----------------------------------------------

    st.subheader("2. Top Performers by Department")

    top_n = st.slider(
        "Select number of top employees",
        min_value=1,
        max_value=10,
        value=5
    )

    top_data = analytics_manager.get_top_performers(top_n)

    if top_data:

        top_df = pd.DataFrame(top_data)

        st.dataframe(
            top_df,
            width="stretch",
            hide_index=True
        )

    else:

        st.info("No employee performance data available.")


    st.divider()


    # ----------------------------------------------
    # 3. DEPARTMENT ATTRITION
    # ----------------------------------------------

    st.subheader("3. Department-wise Attrition Analysis")

    attrition_data = analytics_manager.get_department_attrition()

    if attrition_data:

        attrition_df = pd.DataFrame(attrition_data)

        attrition_df["attrition_percentage"] = pd.to_numeric(
            attrition_df["attrition_percentage"]
        )

        st.dataframe(
            attrition_df,
            width="stretch",
            hide_index=True
        )

        st.bar_chart(
            attrition_df.set_index("department_name")[
                ["attrition_percentage"]
            ]
        )

    else:

        st.info("No attrition data available.")


    st.divider()


    # ----------------------------------------------
    # 4. PROJECT WORKLOAD
    # ----------------------------------------------

    st.subheader("4. Project Workload Analysis")

    project_data = analytics_manager.get_project_workload()

    if project_data:

        project_df = pd.DataFrame(project_data)

        project_df["total_allocation"] = pd.to_numeric(
            project_df["total_allocation"]
        )

        st.dataframe(
            project_df,
            width="stretch",
            hide_index=True
        )

        st.bar_chart(
            project_df.set_index("project_name")[
                ["total_allocation"]
            ]
        )

        st.caption(
            "Projects with higher total allocation have more assigned "
            "workload. This is an indicator for further investigation, "
            "not proof of a bottleneck."
        )

    else:

        st.info("No project workload data available.")
