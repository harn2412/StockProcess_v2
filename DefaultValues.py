"""Chua cac gia tri mac dinh dung chung trong trong trinh"""
from os import path


class FilePath:
    """Duong dan cua cac tap tin va thu muc"""

    # thu muc cai dat
    install_dir = path.dirname(path.abspath(__file__))

    # thu muc chua cac bang gia tri mac dinh
    default_data_dir = path.join(install_dir, "default_data")

    # tap tin co so du lieu
    database_path = path.join(install_dir, "database.db")


class Table:
    """Ten cac bang luu du lieu"""

    # bang luu du lieu cua cac co phieu hien co tren thi truong
    current_stocks = "current_stocks"
