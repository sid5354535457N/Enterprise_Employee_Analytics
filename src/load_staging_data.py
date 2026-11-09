
import pandas as pd
import mysql.connector
from getpass import getpass


# Load CSV files
current_df = pd.read_csv(
    "data/processed/employees_100k.csv"
)

history_df = pd.read_csv(
    "data/processed/employee_history.csv"
)


# Check column structure
if list(current_df.columns) != list(history_df.columns):
    raise ValueError("CSV columns do not match!")


# Get MySQL login details
username = input("MySQL username (default root): ").strip() or "root"
password = getpass("MySQL password: ")


# Connect to MySQL
connection = mysql.connector.connect(
    host="localhost",
    user=username,
    password=password,
    database="staging_db"
)

cursor = connection.cursor()


# Function to insert CSV records into MySQL
def load_data(df, table_name):

    columns = ", ".join(
        f"`{column}`" for column in df.columns
    )

    placeholders = ", ".join(
        ["%s"] * len(df.columns)
    )

    query = f"""
        INSERT INTO {table_name}
        ({columns})
        VALUES ({placeholders})
    """

    batch_size = 1000

    for start in range(0, len(df), batch_size):

        batch = df.iloc[start:start + batch_size]

        records = []

        for row in batch.itertuples(index=False, name=None):

            values = []

            for value in row:

                if pd.isna(value):
                    value = None

                elif hasattr(value, "item"):
                    value = value.item()

                values.append(value)

            records.append(tuple(values))

        cursor.executemany(query, records)

        connection.commit()

    print(f"{len(df)} records inserted into {table_name}")


try:

    # Clear old staging records before loading again
    cursor.execute("TRUNCATE TABLE staging_current_employees")
    cursor.execute("TRUNCATE TABLE staging_employee_history")

    connection.commit()

    # Load current employee records
    load_data(
        current_df,
        "staging_current_employees"
    )

    # Load historical employee records
    load_data(
        history_df,
        "staging_employee_history"
    )

    print("\nData Loading Completed Successfully!")


except Exception as e:

    connection.rollback()

    print("Error while loading data:", e)


finally:

    cursor.close()
    connection.close()
