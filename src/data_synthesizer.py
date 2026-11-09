
import pandas as pd
import random
from faker import Faker

# Initialize Faker and random
fake = Faker()
Faker.seed(42)
random.seed(42)

# Load original dataset
df = pd.read_csv("data/raw/employee_data.csv")

# Generate 100,000 employee records
employees = df.sample(
    n=100000,
    replace=True,
    random_state=42
).reset_index(drop=True)

# Assign unique employee IDs
employees["EmployeeNumber"] = range(1, 100001)

# Generate employee names using Faker
employees["EmployeeName"] = [
    fake.name() for _ in range(len(employees))
]

# Make age and salary slightly different
employees["Age"] = (
    employees["Age"] +
    [random.randint(-2, 2) for _ in range(100000)]
).clip(18, 60)

employees["MonthlyIncome"] = (
    employees["MonthlyIncome"] *
    [random.uniform(0.95, 1.05) for _ in range(100000)]
).astype(int)

# Add SCD Type 2 columns
employees["start_date"] = "2024-01-01"
employees["end_date"] = None
employees["is_current"] = 1

# Select 20,000 employees for historical changes
changed_indices = random.sample(range(100000), 20000)

historical_records = []

departments = employees["Department"].unique().tolist()
job_roles = employees["JobRole"].unique().tolist()

# Generate historical records
for index in changed_indices:

    current = employees.loc[index]
    old = current.copy()

    # Select a type of employee change
    change = random.choice(["department", "promotion", "salary"])

    if change == "department":

        other_departments = [
            d for d in departments
            if d != current["Department"]
        ]

        old["Department"] = random.choice(other_departments)

    elif change == "promotion":

        other_roles = [
            r for r in job_roles
            if r != current["JobRole"]
        ]

        old["JobRole"] = random.choice(other_roles)
        old["JobLevel"] = max(1, int(current["JobLevel"]) - 1)
        old["MonthlyIncome"] = int(current["MonthlyIncome"] * 0.90)

    else:

        old["MonthlyIncome"] = int(current["MonthlyIncome"] * 0.90)

    # Set historical dates
    old["start_date"] = "2024-01-01"
    old["end_date"] = "2025-12-31"
    old["is_current"] = 0

    # Current record starts from 2026
    employees.loc[index, "start_date"] = "2026-01-01"

    historical_records.append(old)

# Save 100,000 current employee records
employees.to_csv(
    "data/processed/employees_100k.csv",
    index=False
)

# Combine current and historical records
history_df = pd.DataFrame(historical_records)

employee_history = pd.concat(
    [employees, history_df],
    ignore_index=True
)

# Sort records by employee ID and date
employee_history = employee_history.sort_values(
    ["EmployeeNumber", "start_date"]
).reset_index(drop=True)

# Save complete historical dataset
employee_history.to_csv(
    "data/processed/employee_history.csv",
    index=False
)

# Display results
print("Data Generation Completed!")

print("Original Records:", len(df))
print("Current Employees:", len(employees))
print("Historical Records:", len(history_df))
print("Total History Records:", len(employee_history))

print(
    "Unique Employees:",
    employee_history["EmployeeNumber"].nunique()
)

print(
    "Current Records:",
    (employee_history["is_current"] == 1).sum()
)

print(
    "Old Records:",
    (employee_history["is_current"] == 0).sum()
)

print("\nGenerated files successfully!")
