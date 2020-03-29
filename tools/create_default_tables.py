"""Chep cac bang du lieu mac dinh trong thu muc default_data va trong file
co so du lieu"""
# Inter
from DefaultValues import FilePath

# Default
import os
import sqlite3

# 3th party
import pandas


def main():
    default_data_dir = FilePath.default_data_dir
    database = FilePath.database_path

    for file in os.listdir(default_data_dir):
        try:
            df = pandas.read_csv(os.path.join(default_data_dir, file))
            with sqlite3.connect(database) as conn:
                df.to_sql(file.rstrip(".csv"), conn, index=False)
        except Exception as error:
            print(error)


if __name__ == '__main__':
    main()
