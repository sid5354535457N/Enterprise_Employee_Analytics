class Employee:

    def __init__(
        self,
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
    ):

        self.employee_id = employee_id
        self.employee_name = employee_name
        self.age = age
        self.gender = gender
        self.department_id = department_id
        self.job_role = job_role
        self.job_level = job_level
        self.monthly_income = monthly_income
        self.attrition = attrition
        self.years_at_company = years_at_company

    # Convert employee details into a tuple
    def to_tuple(self):

        return (
            self.employee_id,
            self.employee_name,
            self.age,
            self.gender,
            self.department_id,
            self.job_role,
            self.job_level,
            self.monthly_income,
            self.attrition,
            self.years_at_company
        )