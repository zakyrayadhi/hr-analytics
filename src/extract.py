import pandas as pd
from config import EXCEL_FILE


def extract_data():
    try:
        # 1. Read Excel
        df = pd.read_excel(EXCEL_FILE)

        # 2. Standardize column names (IMPORTANT)
        df.columns = (
            df.columns
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # 3. Basic validation
        if df.empty:
            raise ValueError("Dataframe is empty!")

        print(f"✅ Extract successful: {df.shape[0]} rows, {df.shape[1]} columns")

        return df

    except Exception as e:
        print(f"❌ Extract failed: {e}")
        raise