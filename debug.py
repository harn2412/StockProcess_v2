"""Dung de debug va test code chuong trinh"""
import sqlite3
import pandas as pd
import os
import DefaultValues

stock = "FPT"
number = 3
DATABASE = "database.db"
here = DefaultValues.FilePath.install_dir
REPORT_FORM_DIR = "report_forms"

YEAR_TABLE_DIC = {
    "balance_sheet": "BS Input (CafeF)",
    "cash_flow": "CS input (CafeF)",
    "cash_flow_direct": "CS input (CafeF)",
    "income_statement": "IS input (CafeF)",
}

conn = sqlite3.connect(DATABASE)

query = f"SELECT * FROM {stock}_YEARS"
full_df = pd.read_sql(query, conn, index_col="id")

if len(full_df.columns) < number:
    print("Khong du so luong bao cao")
    print(f"Hien chi co the lay toi da '{len(full_df.columns)}' ket qua")

full_df = full_df[sorted(full_df.columns)[-number:]]

for table_name in YEAR_TABLE_DIC.keys():
    template = pd.read_csv(
        os.path.join(here, REPORT_FORM_DIR, (table_name + ".csv")), index_col="id"
    )
    df = full_df.reindex[template.index]
