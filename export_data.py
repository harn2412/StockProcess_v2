"""Export du lieu trong database ra file Excel"""
import option_menu
import TimeType
import DefaultValues

import pandas as pd
from openpyxl import load_workbook

import os
import shutil
import re
from shutil import copyfile
import sqlite3

here = DefaultValues.FilePath.install_dir
DATABASE = "database.db"
REPORT_FORM_DIR = "report_forms"
EXPORTED_DATA_DIR = "exported_data"
xlsx_template = os.path.join(here, REPORT_FORM_DIR, "Template.xlsx")

#  sql_table -> excel_table
YEAR_TABLE_DIC = {
    "balance_sheet": "BS Input (CafeF)",
    "cash_flow": "CS input (CafeF)",
    "cash_flow_direct": "CS input (CafeF)",
    "income_statement": "IS input (CafeF)",
}

QUARTER_TABLE_DIC = {
    "balance_sheet": "Quarterly BS input (CafeF)",
    "cash_flow": "Quarterly CS input (CafeF)",
    "cash_flow_direct": "Quarterly CS input (CafeF)",
    "income_statement": "Quarterly IS input (Cafef)",
}


def separate_print(title: str, sep_char="="):
    """In dai phan cach giua cac tien trinh"""
    print(f"{title}".center(shutil.get_terminal_size().columns, sep_char))


def create_stock_list(text):
    """Lam ra danh sach cac ma co phieu tu chuoi co phieu nhap vao"""
    pattern = re.compile(r"[\w\d]+")
    stocks = pattern.findall(text.upper())
    return stocks


def to_excel(stock, year_dic, quarter_dic, excel_file_path):
    """Chuyen bang du lieu thanh file Excel"""

    # Mo file Excel dung de luu ket qua
    book = load_workbook(excel_file_path)
    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as writer:
        # Cac buoc chuan bi de khong bi ghi de file
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

        # YEARS
        for table in YEAR_TABLE_DIC.keys():
            querry = ""

        for csv_file in worksheet_name.keys():
            csv_file_bath = os.path.join(csv_dir_path, csv_file)

            # Kiem tra xem file co ton tai khong
            if os.path.exists(csv_file_bath):
                print("Chuan bi chuyen doi tap tin %s" % csv_file)
                dframe = pd.read_csv(csv_file_bath)

                # Chuyen gia tri ve dang so

                dframe.to_excel(writer, worksheet_name[csv_file], index=False)
                print("Hoan tat chuyen doi.")
            else:
                print('khong tim thay tap tin "%s", tien hanh bo qua' % csv_file)
        writer.save()


def get_year_report(stock, number):
    """Lay cac ban du lieu cua bao cao nam

    Args:
        stock: Ma co phieu
        number: So luong bao cao

    Returns:
        dict: Cac bang bao cao IS, BS, CF, CFD

    """

    result = {}
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
        df = full_df.reindex(template.index)
        result[table_name] = df

    return result


def get_quarter_report(stock, number):
    """Lay cac ban du lieu cua bao cao quy

    Args:
        stock: Ma co phieu
        number: So luong bao cao

    Returns:
        dict: Cac bang bao cao IS, BS, CF, CFD

    """

    result = {}
    conn = sqlite3.connect(DATABASE)

    query = f"SELECT * FROM {stock}_QUARTERS"
    full_df = pd.read_sql(query, conn, index_col="id")

    if len(full_df.columns) < number:
        print("Khong du so luong bao cao")
        print(f"Hien chi co the lay toi da '{len(full_df.columns)}' ket qua")

    full_df = full_df[sorted(full_df.column)[-number:]]

    for table_name in QUARTER_TABLE_DIC.keys():
        template = pd.read_csv(
            os.path.join(here, REPORT_FORM_DIR, table_name, ".csv"), index_col="id"
        )
        df = full_df.reindex(template.index)
        result[table_name] = df

    return result


def main():
    separate_print("START")
    print("Chuong trinh dung de trich xuat du lieu ra file Excel")

    separate_print("INPUT STOCKS")
    print(
        "Nhap vao cac ma co phieu muon lay du lieu, "
        'cac ma co phieu phan cach nhau bang dau phay ",". '
        "Vi du: fpt, aaa, vnm"
    )
    usr_input_stocks = input(">: ")
    stocks = create_stock_list(usr_input_stocks)

    separate_print("HOW MANY REPORT?")
    # Number of Year Report
    y_r_num = int(input("Ban muon trich suat bao nhieu bao cao NAM: "))

    # Number of Quarter Report
    q_r_num = int(input("Ban muon trich suat bao nhieu bao cao QUY: "))

    # TODO Build Report Form from Template
    # YEARS

    # TODO Get data form database

    # TODO Build Excel
    pass


if __name__ == "__main__":
    main()
