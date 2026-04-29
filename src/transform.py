import pandas as pd


# ============================
# CLEAN DATA
# ============================
def clean_data(df):
    df = df.copy()

    # standardize column names
    df.columns = df.columns.str.lower().str.strip().str.replace(" ", "_")

    # rename possible variants
    df = df.rename(columns={
        'dob': 'dateofbirth',
        'date_of_birth': 'dateofbirth',
        'date_of_hire': 'dateofhire',
        'date_of_termination': 'dateoftermination'
    })

    # FIX MANAGER ID (handle duplicates safely)
    if 'managername' in df.columns and 'managerid' in df.columns:
        manager_map = (
            df[['managername', 'managerid']]
            .dropna()
            .drop_duplicates()
            .groupby('managername')['managerid']
            .first()
        )

        df['managerid'] = df['managerid'].fillna(df['managername'].map(manager_map))

    return df


# ============================
# DERIVED FEATURES
# ============================
def add_derived_columns(df):
    df = df.copy()
    today = pd.Timestamp.today()

    # AGE
    if 'dateofbirth' in df.columns:
        df['dateofbirth'] = pd.to_datetime(df['dateofbirth'], errors='coerce')
        df['age'] = (today - df['dateofbirth']).dt.days // 365
    else:
        df['age'] = None

    # TENURE
    if 'dateofhire' in df.columns:
        df['dateofhire'] = pd.to_datetime(df['dateofhire'], errors='coerce')

        if 'dateoftermination' in df.columns:
            df['dateoftermination'] = pd.to_datetime(df['dateoftermination'], errors='coerce')
            end_date = df['dateoftermination'].fillna(today)
        else:
            end_date = today

        df['tenure_years'] = (end_date - df['dateofhire']).dt.days // 365
    else:
        df['tenure_years'] = None

    # AGE GROUP (based on your distribution)
    df['age_group'] = pd.cut(
        df['age'],
        bins=[30, 40, 50, 60, 80],
        labels=["30-40", "40-50", "50-60", "60+"],
        include_lowest=True
    )

    # TENURE GROUP
    df['tenure_group'] = pd.cut(
        df['tenure_years'],
        bins=[0, 2, 5, 10, 20],
        labels=["0-2", "2-5", "5-10", "10+"],
        include_lowest=True
    )

    return df


# ============================
# DIMENSIONS (CLEANED)
# ============================

# 🔥 USE NAME ONLY (NOT ID)
def build_dim_department(df):
    dim = df[['department']].drop_duplicates().reset_index(drop=True)
    dim['department_key'] = dim.index + 1

    return dim.rename(columns={
        'department': 'department_name'
    })


def build_dim_position(df):
    dim = df[['position']].drop_duplicates().reset_index(drop=True)
    dim['position_key'] = dim.index + 1

    return dim.rename(columns={
        'position': 'position_name'
    })


def build_dim_performance(df):
    dim = df[['performancescore']].drop_duplicates().reset_index(drop=True)
    dim['performance_key'] = dim.index + 1

    return dim.rename(columns={
        'performancescore': 'performance_score'
    })


def build_dim_salary(df):
    df = df.copy()

    df['salary_band'] = pd.qcut(
        df['salary'],
        q=4,
        labels=["Low", "Mid", "High", "Very High"]
    )

    dim = df[['salary', 'salary_band']].drop_duplicates().reset_index(drop=True)
    dim['salary_key'] = dim.index + 1

    return dim, df


# ============================
# FACT TABLE
# ============================
def build_fact_employee(df, dim_department, dim_position, dim_salary, dim_performance):

    df = df.copy()

    # rename for consistency
    df = df.rename(columns={
        'department': 'department_name',
        'position': 'position_name',
        'performancescore': 'performance_score'
    })

    # 🔥 JOIN USING BUSINESS KEYS
    df = df.merge(dim_department, on='department_name', how='left')
    df = df.merge(dim_position, on='position_name', how='left')
    df = df.merge(dim_salary, on=['salary', 'salary_band'], how='left')
    df = df.merge(dim_performance, on='performance_score', how='left')

    fact = df[[
        'empid',
        'managerid',
        'department_key',
        'position_key',
        'salary_key',
        'performance_key',
        'salary',
        'age',
        'age_group',
        'tenure_years',
        'tenure_group',
        'engagementsurvey',
        'empsatisfaction',
        'specialprojectscount',
        'dayslatelast30',
        'absences',
        'termd'
    ]].copy()

    return fact.rename(columns={
        'empid': 'emp_id',
        'managerid': 'manager_id',
        'engagementsurvey': 'engagement_survey',
        'empsatisfaction': 'emp_satisfaction',
        'specialprojectscount': 'special_projects_count',
        'dayslatelast30': 'days_late_last30'
    })


# ============================
# MASTER
# ============================
def transform_data(df):

    df = clean_data(df)
    df = add_derived_columns(df)

    dim_department = build_dim_department(df)
    dim_position = build_dim_position(df)
    dim_salary, df = build_dim_salary(df)
    dim_performance = build_dim_performance(df)

    fact_employee = build_fact_employee(
        df,
        dim_department,
        dim_position,
        dim_salary,
        dim_performance
    )

    return {
        "dim_department": dim_department,
        "dim_position": dim_position,
        "dim_salary": dim_salary,
        "dim_performance": dim_performance,
        "fact_employee": fact_employee
    }