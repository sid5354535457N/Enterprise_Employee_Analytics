import pandas as pd

# Load employee dataset
df = pd.read_csv("data/raw/employee_data.csv")

# Display dataset information
print("Dataset Shape:")
print(df.shape)

print("\nFirst 5 Records:")
print(df.head())

print("\nColumn Names:")
print(df.columns.tolist())

print("\nMissing Values:")
print(df.isnull().sum().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

print("\nData Types:")
print(df.dtypes)

print("\nTotal Unique Employees:")
print(df["EmployeeNumber"].nunique())