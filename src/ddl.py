import psycopg2
from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DWH_SCHEMA
)


def create_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )


# ============================
# DROP TABLES (RESET)
# ============================
def drop_tables(cursor):
    cursor.execute(f"""
        DROP TABLE IF EXISTS {DWH_SCHEMA}.fact_employee CASCADE;
        DROP TABLE IF EXISTS {DWH_SCHEMA}.dim_performance CASCADE;
        DROP TABLE IF EXISTS {DWH_SCHEMA}.dim_salary CASCADE;
        DROP TABLE IF EXISTS {DWH_SCHEMA}.dim_position CASCADE;
        DROP TABLE IF EXISTS {DWH_SCHEMA}.dim_department CASCADE;
    """)


# ============================
# CREATE TABLES
# ============================
def create_tables(cursor):

    # Schema
    cursor.execute(f"""
        CREATE SCHEMA IF NOT EXISTS {DWH_SCHEMA};
    """)

    # Dimensions
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.dim_department (
            department_key SERIAL PRIMARY KEY,
            department_name TEXT
        );
    """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.dim_position (
            position_key SERIAL PRIMARY KEY,
            position_name TEXT
        );
    """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.dim_salary (
            salary_key SERIAL PRIMARY KEY,
            salary NUMERIC,
            salary_band TEXT
        );
    """)

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {DWH_SCHEMA}.dim_performance (
            performance_key SERIAL PRIMARY KEY,
            performance_score TEXT
        );
    """)

    # Fact
    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS hr.fact_employee (
            emp_id INT PRIMARY KEY,

            manager_id INT,

            department_key INT,
            position_key INT,
            salary_key INT,
            performance_key INT,

            salary NUMERIC,

            age INT,
            age_group TEXT,

            tenure_years INT,
            tenure_group TEXT,

            engagement_survey NUMERIC,
            emp_satisfaction NUMERIC,
            special_projects_count INT,
            days_late_last30 INT,
            absences INT,
            termd INT,

            FOREIGN KEY (department_key)
                REFERENCES hr.dim_department(department_key),

            FOREIGN KEY (position_key)
                REFERENCES hr.dim_position(position_key),

            FOREIGN KEY (salary_key)
                REFERENCES hr.dim_salary(salary_key),

            FOREIGN KEY (performance_key)
                REFERENCES hr.dim_performance(performance_key)
        );
    """)


# ============================
# INDEXES
# ============================
def create_indexes(cursor):
    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_fact_department
        ON {DWH_SCHEMA}.fact_employee(department_key);
    """)

    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_fact_position
        ON {DWH_SCHEMA}.fact_employee(position_key);
    """)

    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_fact_salary
        ON {DWH_SCHEMA}.fact_employee(salary_key);
    """)

    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_fact_performance
        ON {DWH_SCHEMA}.fact_employee(performance_key);
    """)

    cursor.execute(f"""
        CREATE INDEX IF NOT EXISTS idx_fact_attrition
        ON {DWH_SCHEMA}.fact_employee(termd);
    """)


# ============================
# MAIN RUNNER
# ============================
def run_ddl(reset=False):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        if reset:
            print("⚠️ Dropping existing tables...")
            drop_tables(cursor)

        print("📦 Creating tables...")
        create_tables(cursor)

        print("⚡ Creating indexes...")
        create_indexes(cursor)

        conn.commit()
        print("✅ DDL completed successfully!")

    except Exception as e:
        conn.rollback()
        print("❌ Error:", e)

    finally:
        cursor.close()
        conn.close()


if __name__ == "__main__":
    # change to True if you want reset
    run_ddl(reset=True)