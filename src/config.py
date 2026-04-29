# ===============================
# PostgreSQL Connection
# ===============================
DB_HOST = "localhost"
DB_PORT = 5432
DB_NAME = "hr_warehouse"
DB_USER = "postgres"
DB_PASSWORD = "admin"

# ===============================
# Schema Configuration
# ===============================
DWH_SCHEMA = "hr"
DM_SCHEMA = "datamart"  

# ===============================
# File Source
# ===============================
EXCEL_FILE = "data/HRDataset_v14.xlsx"

# ===============================
# Staging Table
# ===============================
STAGING_TABLE = "stg_employee"

# ===============================
# Dimension Tables
# ===============================
DIM_DEPARTMENT = "dim_department"
DIM_POSITION = "dim_position"
DIM_SALARY = "dim_salary"
DIM_PERFORMANCE = "dim_performance"

# ===============================
# Fact Table
# ===============================
FACT_EMPLOYEE = "fact_employee"

# ===============================
# Key Columns (Important)
# ===============================
PK_EMPLOYEE = "emp_id"
ATTRITION_COL = "termd"

# ===============================
# Derived Features Config
# ===============================
SALARY_BINS = 3
SALARY_LABELS = ["Low", "Medium", "High"]

# ===============================
# Optional Date Columns
# ===============================
DATE_COLUMNS = ["dateofhire", "dateoftermination"]

# ===============================
# Segmentation
# ===============================
DEPARTMENTS = [
    "Sales",
    "IT/IS",
    "Production",
    "Software Engineering",
    "Admin Offices"
]

# ===============================
# Datamart Tables (Later)
# ===============================
DM_ATTRITION_SUMMARY = "summary_attrition"
DM_PERFORMANCE_SUMMARY = "summary_performance"
DM_SALARY_ANALYSIS = "summary_salary"
DM_DEPARTMENT_ANALYSIS = "summary_department"