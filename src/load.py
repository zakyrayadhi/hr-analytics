import psycopg2
from config import (
    DB_HOST,
    DB_PORT,
    DB_NAME,
    DB_USER,
    DB_PASSWORD,
    DWH_SCHEMA,
    DIM_DEPARTMENT,
    DIM_POSITION,
    DIM_SALARY,
    DIM_PERFORMANCE,
    FACT_EMPLOYEE
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
# GENERIC INSERT FUNCTION
# ============================
def insert_data(cursor, table_name, df):
    cols = list(df.columns)
    col_str = ", ".join(cols)
    placeholder = ", ".join(["%s"] * len(cols))

    query = f"""
        INSERT INTO {DWH_SCHEMA}.{table_name} ({col_str})
        VALUES ({placeholder})
    """

    for _, row in df.iterrows():
        cursor.execute(query, tuple(row))


# ============================
# LOAD DIMENSIONS
# ============================
def load_dimensions(cursor, tables):
    print("📦 Loading dimensions...")

    insert_data(cursor, DIM_DEPARTMENT, tables["dim_department"])
    insert_data(cursor, DIM_POSITION, tables["dim_position"])
    insert_data(cursor, DIM_SALARY, tables["dim_salary"])
    insert_data(cursor, DIM_PERFORMANCE, tables["dim_performance"])


# ============================
# LOAD FACT
# ============================
def load_fact(cursor, tables):
    print("⭐ Loading fact table...")

    insert_data(cursor, FACT_EMPLOYEE, tables["fact_employee"])


# ============================
# MAIN
# ============================
def load_data(tables):
    conn = create_connection()
    cursor = conn.cursor()

    try:
        # load dim first
        load_dimensions(cursor, tables)

        # load fact
        load_fact(cursor, tables)

        conn.commit()
        print("✅ Data loaded successfully!")

    except Exception as e:
        conn.rollback()
        print("❌ Error loading data:", e)

    finally:
        cursor.close()
        conn.close()