"""Chuong trinh dung de lay du lieu bao cao cua cac ma co phieu tu trang Cafef
Sau do tien hanh tong hop va thong ke theo yeu cau"""
import shutil
import datetime
import re
import pandas
import os


class Info:
    """Chua cac thong tin ve chuong trinh"""
    name = "Stock Process v2"
    version = "beta 1"
    install_dir = os.path.dirname(os.path.abspath(__file__))
    basestocks = os.path.join(install_dir, "basestocks.csv")


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
    basestocks = pandas.read_csv(Info.basestocks)
    valid_stocks = basestocks["Symbol"].values
    return [stock for stock in stocks if stock not in valid_stocks]


def main():
    """Chuong trinh chinh"""
    separate_print("START")
    when_start()  # In thong tin khi chuong trinh khoi chay

    # Yeu cau nguoi dung nhap vao danh sach cac ma co phieu muon lay du lieu
    separate_print("INPUT STOCKS")
    print('Nhap vao cac ma co phieu muon lay du lieu, '
          'cac ma co phieu phan cach nhau bang dau phay ",". '
          'Vi du: fpt, aaa, vnm')
    stocks_str = input(">: ")
    stocks = create_stock_list(stocks_str)

    # Kiem tra danh sach cac ma co phieu hop le va khong hop le
    invalid_stocks = check_stock(stocks)
    if invalid_stocks:
        separate_print("INVALID STOCKS")
        print("Cac ma co phieu sau khong ton tai: \n"
              f"{', '.join(invalid_stocks)}\n"
              "Xin vui long kiem tra lai xem ban co nhap vao chinh xac chua, "
              "hoac chay tien trinh cap nhat danh sach co phieu hien co\n"
              "Ban cung co the nhan Enter de tiep tuc xu ly voi cac ma con lai")
        input("Press Enter to continues...")

    for stock in stocks:
        print(stock)


if __name__ == '__main__':
    main()
