"""Chuong trinh dung de lay du lieu bao cao cua cac ma co phieu tu trang Cafef
Sau do tien hanh tong hop va thong ke theo yeu cau"""
import shutil
import datetime
import re
import pandas
import os
import sqlite3
from collections import namedtuple
import option_menu
import Report
import TimeType


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
    pattern = re.compile(r'[\w\d]+')
    stocks = pattern.findall(text.upper())
    return stocks


def check_stock(stocks):
    """Kiem tra cac ma co phieu co nam trong co so du lieu
    cua cac ma co phieu hien tai hay khong, sau do tra ve
    danh sach cac ma co phieu khong hop le"""

    with sqlite3.connect(Info.database_path) as conn:
        query = (
            f"SELECT Symbol\n"
            f"FROM {TableInfo.current_stocks}\n"
            f";"
        )

        current_stocks = pandas.read_sql_query(query, conn)

    # chuyen ve dang set de tinh toan
    stocks = set(stocks)
    current_stocks = set(current_stocks["Symbol"])

    valid_stocks = stocks & current_stocks
    invalid_stocks = stocks - current_stocks

    # tra ve ket qua
    Result = namedtuple("Result", "valid invalid")
    return Result(valid=valid_stocks, invalid=invalid_stocks)


def create_option_list(text):
    """Lam ra danh sach cac tuy chon bao cao muon tai ve"""
    pattern = re.compile(r'[12345]+')
    options = tuple([int(opt_text) for opt_text in pattern.findall(text)])
    if 5 in options:
        return 1, 2, 3, 4
    else:
        return options


def main():
    """Chuong trinh chinh"""

    separate_print("START")
    when_start()  # In thong tin khi chuong trinh khoi chay

    # Yeu cau nguoi dung nhap vao danh sach cac ma co phieu muon lay du lieu
    separate_print("INPUT STOCKS")
    print('Nhap vao cac ma co phieu muon lay du lieu, '
          'cac ma co phieu phan cach nhau bang dau phay ",". '
          'Vi du: fpt, aaa, vnm')
    usr_input_stocks = input(">: ")
    stocks = create_stock_list(usr_input_stocks)

    # Kiem tra danh sach cac ma co phieu hop le va khong hop le
    stocks, invalid_stocks = check_stock(stocks)  # stock = valid_stocks
    if invalid_stocks:
        separate_print("INVALID STOCKS")
        print("Cac ma co phieu sau khong ton tai: \n"
              f"{', '.join(invalid_stocks)}\n"
              "Xin vui long kiem tra lai xem ban co nhap vao chinh xac chua, "
              "hoac chay tien trinh cap nhat danh sach co phieu hien co\n"
              "Ban cung co the nhan Enter de tiep tuc xu ly voi cac ma con lai")
        input("Press Enter to continues...")

    # Chon loai bao cao muon lay
    separate_print("CHOOSE REPORTS")
    print(
        'Nhap vao so thu tu cac loai bao cao ban muon su dung\n'
        '\t[1] Can doi ke toan\n'
        '\t[2] Ket qua hoat dong kinh doanh\n'
        '\t[3] Luu chuyen tien te gian tiep\n'
        '\t[4] Luu chuyen tien te truc tiep\n'
        '\t[0] Tai tat ca\n'
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
                choice_all="0"
            )
            break
        except ValueError as error:
            print(error)
            continue

    # chon kieu bao cao theo thoi gian
    separate_print("CHOOSE TIME STYLE")
    print(
        "Ban muon lay bao cao theo NAM hay QUY?\n"
        "\t[1] Nam\n"
        "\t[2] Quy\n"
    )

    time_type = None  # dummy value for linter
    while True:
        try:
            usr_input_time_type = input(">:")

            options = (
                TimeType.Year,
                TimeType.Quarter,
            )

            # time_type luc nay moi la class "type" chua phai Year hay Quarter
            time_type = option_menu.get_opts_from_input(
                user_input=usr_input_time_type,
                options=options,
                valid_choices="12",
                multi=False
            )

            break

        except ValueError as error:
            print(error)
            continue

    # chon khoang thoi gian
    separate_print("HOW MANY REPORTS")

    # tu class type chuyen ve obj tuong ung voi nam va quy nhap vao
    time_type = TimeType.create_from_input(time_type)

    # so luong bao cao muon lay (tuong ung voi cac moc thoi gian hien tai va truoc do)
    report_num = int(input("Ban muon lay bao nhieu bao cao: "))

    for stock in stocks:
        print(stock)
        for report in reports:
            for i in range(0, report_num):
                print(f"{1} - {report.name} - {time_type.prev(i)}")


if __name__ == '__main__':
    main()
