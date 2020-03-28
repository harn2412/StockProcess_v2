"""Export du lieu trong database ra file Excel"""
import DefaultValues
import TimeType

import pandas as pd
from pandas.io.sql import DatabaseError
from openpyxl import load_workbook

import os
import shutil
import re
from shutil import copyfile
import sqlite3

here = DefaultValues.FilePath.install_dir
DATABASE = "database.db"
REPORT_FORM_DIR = os.path.join(here, "report_forms")
EXPORTED_DATA_DIR = os.path.join(here, "exported_data")
xlsx_template = os.path.join(here, REPORT_FORM_DIR, "Template.xlsx")

#  sql_table -> excel_table
YEAR_TABLES = {
    "balance_sheet": "BS Input (CafeF)",
    "cash_flow": "CS Input (CafeF)",
    "cash_flow_direct": "CSD Input (CafeF)",
    "income_statement": "IS Input (CafeF)",
}

QUARTER_TABLES = {
    "balance_sheet": "Quarterly BS Input (CafeF)",
    "cash_flow": "Quarterly CS Input (CafeF)",
    "cash_flow_direct": "Quarterly CSD Input (CafeF)",
    "income_statement": "Quarterly IS Input (CafeF)",
}


def separate_print(title: str, sep_char="="):
    """In dai phan cach giua cac tien trinh"""
    print(f"{title}".center(shutil.get_terminal_size().columns, sep_char))


def create_stock_list(text):
    """Lam ra danh sach cac ma co phieu tu chuoi co phieu nhap vao"""
    pattern = re.compile(r"[\w\d]+")
    stocks = pattern.findall(text.upper())
    return stocks


def to_excel(year_reports, quarter_reports, excel_file_path):
    """Trich suat du lieu ra duoi dang file Excel

    Args:
        year_reports (dict): Cac bao cao nam
        quarter_reports (dict): Cac bao cao quy
        excel_file_path (str): Duong dan luu file

    Returns:
        None

    """

    book = load_workbook(excel_file_path)
    with pd.ExcelWriter(excel_file_path, engine="openpyxl") as writer:
        # Cac buoc chuan bi de khong bi ghi de file
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)

    # YEARS
    for name, data in year_reports.items():
        name: str
        data: pd.DataFrame
        data.to_excel(writer, YEAR_TABLES[name])

    # QUARTER
    for name, data in quarter_reports.items():
        name: str
        data: pd.DataFrame
        data.to_excel(writer, QUARTER_TABLES[name])

    # WRITE FILE
    writer.save()


def get_year_report(stock, number, years):
    """Lay cac ban du lieu cua bao cao nam

    Args:
        stock: Ma co phieu
        number: So luong bao cao
        years: Danh sach cac cot trong table du lieu

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

    for table_name in YEAR_TABLES.keys():
        template = pd.read_csv(os.path.join(here, REPORT_FORM_DIR,
                                            (table_name + ".csv")),
                               index_col="id")
        df = pd.DataFrame(index=template.index, columns=years)
        df.update(full_df)

        if not df.isna().all().all():
            result[table_name] = df
        else:
            pass

    return result


def get_quarter_report(stock, number, quarters):
    """Lay cac ban du lieu cua bao cao quy

    Args:
        stock: Ma co phieu
        number: So luong bao cao
        quarters: Danh sach cac cot trong table du lieu

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

    for table_name in QUARTER_TABLES.keys():
        template = pd.read_csv(os.path.join(here, REPORT_FORM_DIR,
                                            (table_name + ".csv")),
                               index_col="id")
        df = pd.DataFrame(index=template.index, columns=quarters)
        df.update(full_df)

        if not df.isna().all().all():
            result[table_name] = df
        else:
            pass

    return result


def main():
    separate_print("START")
    print("Chuong trinh dung de trich xuat du lieu ra file Excel")

    separate_print("INPUT STOCKS")
    print("Nhap vao cac ma co phieu muon lay du lieu, "
          'cac ma co phieu phan cach nhau bang dau phay ",". '
          "Vi du: fpt, aaa, vnm")
    usr_input_stocks = input(">: ")
    stocks = create_stock_list(usr_input_stocks)

    separate_print("HOW MANY REPORT?")
    # Number of Year Report
    print("Ban muon lay du lieu tu nam nao?")
    year = int(input(">: "))
    print("Ban muon trich xuat bao nhieu bao cao NAM? "
          "(-1: Khong lay bao cao NAM)")
    y_r_num = int(input(">: "))

    year_obj = TimeType.Year(year)
    years = [str(year_obj.prev(i)) for i in range(0, y_r_num)][::-1]

    # Number of Quarter Report
    print("Ban muon lay du lieu tu QUY nao?")
    year = int(input("NAM: "))
    quarter = int(input("QUY: "))
    print("Ban muon trich xuat bao nhieu bao cao QUY? "
          "(-1: Khong lay bao cao QUY)")
    q_r_num = int(input(">: "))

    quarter_obj = TimeType.Quarter(year, quarter)
    quarters = [str(quarter_obj.prev(i)) for i in range(0, q_r_num)][::-1]

    for stock in stocks:
        separate_print(stock)

        # GET YEARS and QUARTER
        print("Dang trich xuat du lieu NAM...")
        try:
            if y_r_num == -1:
                year_report = {}
            else:
                year_report = get_year_report(stock, y_r_num, years)
        except DatabaseError:
            print("Khong tim thay du lieu NAM")
            year_report = {}

        print("Dang trich xuat du lieu QUY...")
        try:
            if q_r_num == -1:
                quarter_report = {}
            else:
                quarter_report = get_quarter_report(stock, q_r_num, quarters)
        except DatabaseError:
            print("Khong tim thay du lieu QUY")
            quarter_report = {}

        # Pass if empty
        if (not year_report) and (not quarter_report):
            print(f"Khong co du lieu cho ma co phieu {stock}")
            continue

        print("Trich xuat du lieu hoan tat")

        # Save to Excel (xlsx)
        print("Chuan bi luu ket qua thanh file Excel...")
        f_path = os.path.join(EXPORTED_DATA_DIR, (stock + ".xlsx"))
        copyfile(xlsx_template, f_path)
        print(f"Duong dan file: {f_path}")

        to_excel(year_report, quarter_report, f_path)
        print("Hoan tat qua trinh chuyen doi")
        print("Chuyen qua ma co phieu tiep theo...")


if __name__ == "__main__":
    main()
    input("Press Enter to end process...")
