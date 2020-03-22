"""Chuong trinh dung de lay du lieu bao cao cua cac ma co phieu tu trang Cafef
Sau do tien hanh tong hop va thong ke theo yeu cau"""
import shutil
import datetime
import re
import os
import sqlite3
from collections import namedtuple

import option_menu
import Report
import TimeType
import GetData
import Error
import DefaultValues
import deal_with_data

import pandas
import numpy


class Info:
    """Chua cac thong tin ve chuong trinh"""

    name = "Stock Process v2"
    version = "beta 1"

    # thu muc cai dat
    install_dir = os.path.dirname(os.path.abspath(__file__))

    # tap tin luu tru co so du lieu
    database_filename = "database.db"
    database_path = os.path.join(install_dir, database_filename)


class TableInfo:
    """Chua thong tin cua cac bang chua du lieu"""

    # cac co phieu hien co tren thi truong
    current_stocks = "current_stocks"


def separate_print(title: str, sep_char="="):
    """In dai phan cach giua cac tien trinh"""
    print(f"{title}".center(shutil.get_terminal_size().columns, sep_char))


def when_start():
    """In cac thong tin khi chuong trinh bat dau"""
    print(f"Name: {Info.name}")
    print(f"Version: {Info.version}")
    ctime = datetime.datetime.now()
    print(f"Started at: {ctime.strftime('%Y-%m-%d %H:%M:%S')}")


def create_stock_list(text):
    """Lam ra danh sach cac ma co phieu tu chuoi co phieu nhap vao"""
    pattern = re.compile(r"[\w\d]+")
    stocks = pattern.findall(text.upper())
    return stocks


def check_stock(stocks):
    """Kiem tra cac ma co phieu co nam trong co so du lieu
    cua cac ma co phieu hien tai hay khong, sau do tra ve
    danh sach cac ma co phieu khong hop le"""

    with sqlite3.connect(Info.database_path) as conn:
        query = f"SELECT Symbol\n" f"FROM {TableInfo.current_stocks}\n" f";"

        current_stocks = pandas.read_sql_query(query, conn)

    # chuyen ve dang set de tinh toan
    stocks = set(stocks)
    current_stocks = set(current_stocks["Symbol"])

    valid_stocks = stocks & current_stocks
    invalid_stocks = stocks - current_stocks

    # tra ve ket qua
    Result = namedtuple("Result", "valid invalid")
    return Result(valid=valid_stocks, invalid=invalid_stocks)


def main():
    """Chuong trinh chinh"""

    separate_print("START")
    when_start()  # In thong tin khi chuong trinh khoi chay

    # Yeu cau nguoi dung nhap vao danh sach cac ma co phieu muon lay du lieu
    separate_print("INPUT STOCKS")
    print("Nhap vao cac ma co phieu muon lay du lieu, "
          'cac ma co phieu phan cach nhau bang dau phay ",". '
          "Vi du: fpt, aaa, vnm")
    usr_input_stocks = input(">: ")
    stocks = create_stock_list(usr_input_stocks)

    # Kiem tra danh sach cac ma co phieu hop le va khong hop le
    stocks, invalid_stocks = check_stock(stocks)  # stock = valid_stocks
    if invalid_stocks:
        separate_print("INVALID STOCKS")
        print(
            "Cac ma co phieu sau khong ton tai: \n"
            f"{', '.join(invalid_stocks)}\n"
            "Xin vui long kiem tra lai xem ban co nhap vao chinh xac chua, "
            "hoac chay tien trinh cap nhat danh sach co phieu hien co\n"
            "Ban cung co the nhan Enter de tiep tuc xu ly voi cac ma con lai")
        input("Press Enter to continues...")

    # Chon loai bao cao muon lay
    separate_print("CHOOSE REPORTS")
    print(
        "Nhap vao so thu tu cac loai bao cao ban muon su dung\n"
        "\t[1] Can doi ke toan\n"
        "\t[2] Ket qua hoat dong kinh doanh\n"
        "\t[3] Luu chuyen tien te gian tiep\n"
        "\t[4] Luu chuyen tien te truc tiep\n"
        "\t[0] Tai tat ca\n"
        'Co the tai mot hoac nhieu loai bao cao va phan cach bang dau phay ",". Vi du: 1, 2 hoac 1, 3\n'
    )

    reports = None  # dummy value for linter
    while True:
        try:
            usr_input_report = input(">: ")
            options = (
                Report.BS,
                Report.IS,
                Report.CF,
                Report.CFD,
            )
            reports = option_menu.get_opts_from_input(
                user_input=usr_input_report,
                options=options,
                valid_choices="1234",
                choice_all="0",
            )
            break
        except ValueError as error:
            print(error)
            continue

    # chon kieu bao cao theo thoi gian
    separate_print("CHOOSE TIME STYLE")
    print("Ban muon lay bao cao theo NAM hay QUY?\n"
          "\t[1] Nam\n"
          "\t[2] Quy\n")

    time_type = None  # dummy value for linter
    while True:
        try:
            usr_input_time_type = input(">:")

            options = (
                TimeType.Year,
                TimeType.Quarter,
            )

            # time_type luc nay moi la class "type" chua phai Year hay Quarter
            _ = option_menu.get_opts_from_input(
                user_input=usr_input_time_type,
                options=options,
                valid_choices="12",
                multi=False,
            )
            time_type = _[
                0]  # vi gia tri tra ve la list trong khi chi can lay 1 gia tri thoi

            break

        except ValueError as error:
            print(error)
            continue

    # chon khoang thoi gian
    separate_print("HOW MANY REPORTS")

    # tu class type chuyen ve obj tuong ung voi nam va quy nhap vao
    time_type = TimeType.create_from_input(time_type, TimeType.Year,
                                           TimeType.Quarter)

    # so luong bao cao muon lay (tuong ung voi cac moc thoi gian hien tai va truoc do)
    report_num = int(input("Ban muon lay bao nhieu bao cao: "))

    # update / overwrite / bypass
    print("Trong truong hop da ton tai du lieu cu ban muon xu ly the nao?\n"
          "\t[1] Cap nhat cac du lieu moi (cac du lieu khac de nguyen)\n"
          "\t[2] Xoa cac du lieu cu va dung cac du lieu moi\n"
          "\t[3] Bo qua khong thay doi (Mac dinh)\n"
          "Nhan Enter de chon mac dinh")

    update_act = None  # dump value for linter
    while True:
        try:
            usr_ans = input(">:") or "3"

            options = (
                "update",
                "overwrite",
                "bypass",
            )

            update_act = option_menu.get_opts_from_input(user_input=usr_ans,
                                                         options=options,
                                                         valid_choices="123",
                                                         multi=False)[0]

            break

        except ValueError as error:
            print(error)
            continue

    # Luu ket qua
    Result = namedtuple("Result", "stock success catalog detail")
    scrap_data_fail = []
    empty_column = []
    unavailable_report = []

    for stock in stocks:
        separate_print(stock)
        print(f"Tien hanh lay du lieu co phieu {stock}")

        conn = sqlite3.connect(DefaultValues.FilePath.database_path)
        available_col = []  # cac moc thoi gian da ton tai
        tbl_frame = {}  # du lieu moi thu duoc

        if isinstance(time_type, TimeType.Year):
            table_name = f"{stock}_YEARS"
        else:
            table_name = f"{stock}_QUARTERS"

        try:
            # Tai du lieu neu co san
            data_table = pandas.read_sql(f"SELECT * FROM \"{table_name}\"",
                                         conn,
                                         index_col="id")

        except Exception as error:
            # Tao moi
            print(error)
            print("Khong co san bang du lieu, tien hanh tao moi...")
            data_table = pandas.DataFrame()

        for i in range(0, report_num):
            int_time_type = time_type.prev(i)
            separate_print(f"( Time = '{int_time_type}' )", "*")
            print(f"Dang lay du lieu cua: {str(int_time_type)}")

            # Khong lay du lieu khi moc thoi gian da co trong co so du lieu
            # va khong yeu cau update / overwrite du lieu cu
            if str(int_time_type
                   ) in data_table.columns and update_act == "bypass":
                print(f"Da ton tai du lieu cua {str(int_time_type)}")
                print("Bo qua va den moc thoi gian tiep theo")
                continue
            else:
                available_col.append(str(int_time_type))

            # Tong hop du lieu thu duoc
            col_truck = pandas.Series()

            for report in reports:
                separate_print(f"( '{report.name}' )", "#")
                print(f"Lay du lieu cua bao cao '{report.name}'...")
                reload_fail_page = 3
                reload_empty_col = 10
                while True:
                    try:
                        url_and_data = GetData.CafeFScraper(
                            stock, report, int_time_type)
                        data = url_and_data.data
                        data = deal_with_data.solve_duplicate_index(data)
                        col_truck = col_truck.append(data)

                    except Error.EmptyTable:
                        print(f"Khong tim thay du lieu tai moc thoi gian "
                              f"{str(int_time_type)} va 3 moc truoc do")

                        result = Result(stock, False, "EmptTable", report.name)

                        unavailable_report.append(result)

                    except Error.CanNotScrapData:
                        if reload_fail_page:
                            print("Trang tai ve khong chua bang du lieu")
                            print("Tien hanh tai lai ...")
                            reload_fail_page -= 1
                            continue
                        else:
                            print("Tai lai trang da that bai")
                            result = Result(stock, False, "CanNotScraptData",
                                            report.name)
                            scrap_data_fail.append(result)

                    except Error.EmptyColumn:
                        if reload_empty_col:
                            print("Khong tim thay du lieu trong cot hien tai")
                            print("Tien hanh tai lai ...")
                            reload_empty_col -= 1
                            continue
                        else:
                            print("Tai lai trang da that bai")
                            result = Result(
                                stock,
                                False,
                                "EmptyColumn",
                                f"{report.name}: {str(int_time_type)}",
                            )
                            empty_column.append(result)

                    break

            # Cap nhat lai index (dung general_id)
            separate_print("Update General ID", "+")
            print("Tien hanh cap nhat lai index...")
            querry = "SELECT * FROM cafef_index"
            cafef_id = pandas.read_sql(querry, conn, index_col="id")
            try:
                col_truck.index = cafef_id.loc[col_truck.index, "general_id"]
                tbl_frame[str(int_time_type)] = col_truck
                print("Hoan tat cap nhat Index")
            except KeyError:
                print(f"Co xuat hien cac ID moi trong bao cao, gom co:")
                for new_id in (set(col_truck.index) - set(cafef_id.index)):
                    print("\t", new_id)
                print("Vi vay se khong cap nhat du lieu nay, "
                      "vui long kiem tra lai sau")
            finally:
                print("Chuyen qua lay du lieu cua bao cao khac...")

        separate_print("WRITE TO TABLE")
        print("Da hoan tat viec lay du lieu")
        # xoa du lieu cu neu co yeu cau
        if update_act == "overwrite":
            data_table[available_col] = numpy.nan

        # cap nhat du lieu moi vao bang du lieu
        new_data = pandas.DataFrame(tbl_frame)
        data_table = new_data.combine_first(data_table)

        # luu du lieu
        print(f"Tien hanh luu du lieu vao bang {table_name}")
        data_table.to_sql(table_name,
                          conn,
                          if_exists="replace",
                          index_label="id")


if __name__ == "__main__":
    main()
