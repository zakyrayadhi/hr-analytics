from extract import extract_data
from transform import transform_data
from load import load_data
from ddl import run_ddl


def initial_load():
    print("🚀 START INITIAL LOAD")

    # 1. Reset database
    print("🧹 Resetting tables...")
    run_ddl(reset=True)

    # 2. Extract
    print("📥 Extracting data...")
    df = extract_data()

    # 3. Transform
    print("🔄 Transforming data...")
    tables = transform_data(df)

    # 4. Load
    print("📦 Loading data...")
    load_data(tables)

    print("✅ INITIAL LOAD COMPLETE!")


if __name__ == "__main__":
    initial_load()