"""Chep cac bang du lieu mac dinh trong thu muc default_data va trong file
co so du lieu"""
# Inter
from DefaultValues import FilePath

# Default
import os
import sqlite3

# 3th party
import pandas

DEFAULT_DATA_DIR = FilePath.default_data_dir
DATABASE = FilePath.database_path

for file in os.listdir(DEFAULT_DATA_DIR):
    try:
        df = pandas.read_csv(os.path.join(DEFAULT_DATA_DIR, file))
        with sqlite3.connect(DATABASE) as conn:
            df.to_sql(file, conn, index=False)
    except Exception as error:
        print(error)
