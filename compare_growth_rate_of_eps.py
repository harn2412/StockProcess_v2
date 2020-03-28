"""Tinh toan chi so Growth rate of EPS theo QUY va thong ke lai"""
import sqlite3

import pandas

import DefaultValues
import TimeType
from StockProcess_v2 import separate_print
from formula import quarterly_ratio

DATABASE = DefaultValues.FilePath.database_path


def get_all_quarter_reports(database):
    """Lay danh sach ten cua tat ca cac bao cao QUY hien co

    Args:
        database (str): Duong dan co so du lieu

    Returns:
        list: Danh sach ten cua cac bao cao quy hien co

    """

    conn = sqlite3.connect(database)
    query = (
        "SELECT name "
        "FROM sqlite_master "
        "WHERE type='table' AND name LIKE '%_QUARTERS';"
    )

    ser = pandas.read_sql(query, conn)["name"]  # type: ser: pandas.Series

    return ser.to_list()


def main():
    """Chuong trinh chinh"""
    separate_print("")
    print("Tinh toan va so sanh chi so 'Growth rate of EPS'")

    separate_print("INPUT")
    print("Vui long nhap vao NAM va QUY muon so sanh")
    year = int(input("NAM: "))
    quarter = int(input("QUY: "))
    time_type = TimeType.Quarter(year, quarter)

    print("Nhap vao gioi han so ket qua hien thi "
          "(Bo trong de hien thi tat ca)")
    try:
        limit = int(input(">: "))
    except ValueError:
        limit = None

    # Danh sach bao cao QUY cua cac co phieu hien co
    quarter_reports = get_all_quarter_reports(DATABASE)

    result = pandas.Series(dtype=float)  # Chua ket qua
    miss_report = []  # Bi thieu du lieu bao cao QUY
    miss_value = []  # Bi thieu du lieu cua ID 20022
    conn = sqlite3.connect(DATABASE)

    for report in quarter_reports:
        stock = report[:-9]  # type: report: str
        separate_print(stock)

        query = f"SELECT * FROM {report};"
        data = pandas.read_sql(query, conn, index_col="id")

        # Bao cao IS cua moc thoi gian duoc chon
        try:
            first_report = data[str(time_type)]
        except KeyError:
            print(f"Khong tim thay du lieu cua '{time_type}'")
            print("Chuyen qua co phieu ke tiep...")
            miss_report.append(stock)
            continue

        # Bao cao IS cua cung QUY trong NAM truoc do
        try:
            sqly_report = data[str(time_type.prev(4))]
        except KeyError:
            print(f"Khong tim thay du lieu cua '{time_type.prev(4)}'")
            print("Chuyen qua co phieu ke tiep...")
            miss_report.append(stock)
            continue

        try:
            growth_rate_of_eps = quarterly_ratio.F1.f_growth_rate_of_eps_v2(
                first_report.dropna(), sqly_report.dropna()
            )
        except (KeyError, IndexError):
            print("Khong tim thay ID '20022' trong bao cao")
            print("Chuyen qua co phieu ke tiep...")
            miss_value.append(stock)
            continue

        print(f"Ket qua: {growth_rate_of_eps}")
        result[stock] = growth_rate_of_eps

    result = result.sort_values(ascending=False)

    if limit is not None:
        result = result.head(limit)

    separate_print("RESULT")
    with pandas.option_context('display.max_rows', None):
        print(result)

    show_false = input("Ban co muon hien cac co phieu khong lay duoc du lieu khong (y/n)?")
    if show_false == "y":
        separate_print("FALSE RESULT")
        print("Cac co phieu bi thieu du lieu QUY:")
        for stock in miss_report:
            print(stock)

        print("Cac co phieu bi thieu du lieu ID 20022:")
        for stock in miss_value:
            print(stock)


if __name__ == "__main__":
    main()
    input("Press Enter to end process...")
