"""Lay du lieu tu trang web"""
import pandas
import sqlite3
import DefaultValues
import requests
import Error
from bs4 import BeautifulSoup
from collections import namedtuple
import re
import numpy


def get_index_name(text):
    """Lam dep phan ten cua cac thong so"""

    # Loai bo khoang trang truoc va sau ten thong so
    pattern = re.compile(r"\s*(\w.*\w)\s*")
    search_result = pattern.search(text)

    if search_result is not None:

        index_name = search_result.group(1)
        return index_name

    else:
        return text


def remove_bullets_numbering(text: str):
    """Loai bo cac phan danh so o dau ten gia tri, Vi du "I -" , "1. ", ..."""

    pattern = re.compile(r'[\d\-.]+\s?([(]?.*)')
    search_result = pattern.search(text)

    try:
        return search_result.group(1)
    except AttributeError:
        return text


def convert_to_number(text):
    """Chuyen doi ket qua thanh so int hoac so float"""

    pattern = re.compile(r"-?[\d,.]+")
    search_result = pattern.search(text)

    if search_result is not None:
        num_text = search_result.group().replace(",", "")

        try:  # thu chuyen thanh so int
            result = int(num_text)
        except ValueError:
            try:  # thu chuyen thanh so float
                result = float(num_text)
            except ValueError:
                print("Khong phai Int hoac Float")
                result = numpy.nan

    else:
        result = numpy.nan

    return result


class CafeFScraper:
    """Lay du lieu tu trang http://cafef.vn"""

    def __init__(self, stock_symbol, report_type, time_type):
        """
        :param stock_symbol: Ma co phieu cua cong ty (str)
        :param report_type: Loai bao cao muon lay (Report.BeautifulSoup or Report.IS
        or Report.CF or Report.CFD)
        :param time_type: Moc thoi gian (TimeType.Year or TimeType.Quarter)
        """

        # dung dan tai du lieu bao cao
        self.url = self.create_url(
            stock=stock_symbol,
            report_short_name=report_type.url_short_name,
            report_long_name=report_type.url_long_name,
            year=time_type.year,
            quarter=time_type.quarter,
            company_url_name=self.get_company_url_name(stock_symbol),
        )

        # du lieu tho trong trang tai ve
        print(f"Dang lay du lieu tu duong dan: {self.url}")
        value_names, value_ids, raw_data = self.get_raw_data(self.url)

        # index cho cac du lieu
        index = self.create_index(value_names, value_ids)

        # Tao bang DataFrame de xu ly du lieu
        raw_data = pandas.DataFrame(
            data=raw_data, index=index)  # chuyen ve DataFrame de xu ly ve sau

        # lay du lieu cua cot cuoi cung
        self.data: pandas.Series = self.check_data(raw_data)

        # cap nhat ten
        self.data.name = str(time_type)

    @staticmethod
    def get_company_url_name(stock):
        """
        Lay ten cong ty dung trong viec tao url tai du lieu
        :param stock: str : ma co phieu
        :return: str
        """
        with sqlite3.connect(DefaultValues.FilePath.database_path) as conn:
            query = (f"SELECT URLName\n"
                     f"FROM {DefaultValues.Table.current_stocks}\n"
                     f"WHERE Symbol='{stock}'\n"
                     f";")

            _ = pandas.read_sql_query(query, conn)

            if _.empty:
                raise ValueError(
                    f"Khong tim thay URLName voi ma co phieu '{stock}'")

            else:
                return _.iloc[0, 0]

    @staticmethod
    def create_url(stock, report_short_name, report_long_name, year, quarter,
                   company_url_name):
        """
        Tao ra url de tai du lieu
        :param stock: ma co phieu can lay du lieu
        :param report_short_name: url_short_name cua bao cao can lay
        :param report_long_name: url_long_name cua bao cao can lay
        :param year: nam can lay du lieu
        :param quarter: quy can lay du lieu (Truong hop lay ca nam thi bang 0)
        :param company_url_name: ten cong ty dung trong viec tao url
        :return:
        """

        url = (f"http://s.cafef.vn/bao-cao-tai-chinh/{stock}/"
               f"{report_short_name}/"
               f"{year}/{quarter}/0/0/"
               f"{report_long_name}-"
               f"{company_url_name}"
               f".chn")

        return url

    @staticmethod
    def get_raw_data(url):
        """
        Lay bang du lieu tho tu duong dan duoc cho
        :param url: str : Duong dan de lay du lieu
        :return: namedtuple(value_names, value_ids, data) :
            value_names: list : Danh sach ten goi cua cac so lieu trong bang
            value_ids: list : Danh sach cac id cua cac so lieu trong bang
            data: list : Du lieu cac hang trong bang
        """

        # bien de luu tru du lieu
        RawData = namedtuple("RawData", "value_names value_ids data")
        value_ids = []
        value_names = []
        data = []

        # tai trang
        page = requests.get(url)
        page.raise_for_status()
        soup = BeautifulSoup(page.content, "lxml")

        # trich xuat du lieu
        # Bang chua du lieu duoi dang html
        table = soup.find("table", {"id": "tableContent"})

        if table is None:
            raise Error.CanNotScrapData(
                "Khong thay bang chua du lieu trong noi dung trang da tai")

        # Cac dong chua du lieu duoi dang html
        rows = table.find_all_next("tr", {"class": ["r_item", "r_item_a"]})

        for row in rows:
            # lay value_id
            value_ids.append(row.get("id"))

            # loc cac o chua du lieu
            cells = row.find_all_next("td", {"class": "b_r_c"})

            # lay ten cua so lieu trong o dau tien
            value_names.append(get_index_name(cells[0].text))

            # du lieu trong hang
            data.append((
                convert_to_number(cells[1].text),
                convert_to_number(cells[2].text),
                convert_to_number(cells[3].text),
                convert_to_number(cells[4].text),
            ))

        return RawData(
            value_names=value_names,
            value_ids=value_ids,
            data=data,
        )

    @staticmethod
    def check_data(raw_data):
        """Kiem tra xem co co du lieu nao hay khong
        :param raw_data : La DataFrame chua du lieu tho can kiem tra
        :return
            Truong hop 1: Neu 4 cot trong bang du lieu deu trong -> EmptyRepor Exception
            Truong hop 2: Neu cot can lay du lieu (cot cuoi cung) trong -> EmptyColumn Exception
            Truong hop 3: Neu trong cot cuoi cung co du lieu thi tra ve cot cuoi cung duoi
            dang pandas.core.series.Series"""

        if raw_data.isnull().to_numpy().all():
            raise Error.EmptyTable("Khong co du lieu trong bang raw_data")

        column = raw_data.iloc[:, -1]
        if column.isnull().all():
            raise Error.EmptyColumn("Cot cuoi cung khong chua du lieu")

        return column

    @staticmethod
    def create_index(value_names, value_ids):
        """Ket hop ten gia tri va id lai de ra index cho gia tri thu duoc
        (Vi cafef co dung trung ten va id cho du lieu trong bang du lieu)"""

        index = []

        for _name, _id in zip(value_names, value_ids):
            new_index = _name, _id
            index.append("_".join(new_index))

        return pandas.Index(index)
