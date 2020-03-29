"""Tuy chinh cac co so du lieu thu cong"""
from tools.screen import separate_print
import TimeType
from DefaultValues import FilePath

import pandas
from pandas.io.sql import DatabaseError

import sqlite3
import os


def choose_timeline(report_type):
    """Tao TimeType tuong ung voi loai report da tao

    Args:
        report_type: La loai bao cao theo NAM hoac QUY

    Returns:
        :obj:`TimeType`

    """

    if report_type == "YEARS":
        year = int(input("NAM muon tuy chinh: "))
        time_type = TimeType.Year(year)
    elif report_type == "QUARTERS":
        print("Nhap vao NAM va QUY muon tuy chinh...")
        year = int(input("NAM: "))
        quarter = int(input("QUARTER: "))
        time_type = TimeType.Quarter(year, quarter)
    else:
        time_type = None

    return time_type


def delete_col(data, time_type):
    """Xoa cot trong bang du lieu

    Args:
        data (pandas.DataFrame): Co so du lieu can su ly
        time_type (TimeType.Year or TimeType.Quarter): NAM hoac QUY

    Returns:
        :obj:`pandas.DataFrame`: Co so du lieu sau khi su ly

    """

    try:
        data = data.drop(str(time_type), axis=1)
    except KeyError:
        print(f"Khong ton tai cot du lieu '{str(time_type)}'")

    print(f"Da xoa du lieu '{str(time_type)}' thanh cong")
    return data


def edit_col(data, time_type, valid_id):
    """Tuy chinh / thay doi mot cot du lieu co san

    Args:
        data (pandas.DataFrame): Co so du lieu can su ly
        time_type (TimeType.Year or TimeType.Quarter): NAM hoac QUY
        valid_id (pandas.Index): Cac ID hop le co the su dung

    Returns:
        :obj:`pandas.DataFrame`: Co so du lieu sau khi su ly

    """

    try:
        ser = data[str(time_type)]

    except KeyError:
        print(f"Khong ton tai cot du lieu '{str(time_type)}'")
        return data

    ser = manual_customize_series(ser, valid_id)

    df = pandas.DataFrame({str(time_type): ser})

    print(f"Hoan tat qua trinh chinh sua cot '{str(time_type)}'")
    return df.combine_first(data)


def create_col(data, time_type, valid_id):
    """Them moi mot cot vao co so du lieu co san

    Args:
        data (pandas.DataFrame): Co so du lieu can su ly
        time_type (TimeType.Year or TimeType.Quarter): NAM hoac QUY
        valid_id (pandas.Index): Cac ID hop le co the su dung

    Returns:
        :obj:`pandas.DataFrame`: Co so du lieu sau khi su ly

    """

    if str(time_type) in data.columns:
        print(f"Da ton tai cot '{str(time_type)}' trong CSDL.")
        return data

    # Tao moi series de luu du lieu
    index = pandas.Index([], dtype=int)
    ser = pandas.Series(index=index, dtype=float)

    ser = manual_customize_series(ser, valid_id)

    df = pandas.DataFrame({str(time_type): ser})

    print(f"Da tao moi cot '{str(time_type)}'")
    return df.combine_first(data)


def get_valid_id(database):
    """Lay ra danh sach cac Value ID hop le

    Args:
        database (str): Duong dan co so du lieu

    Returns:
        :obj:`pandas.Index`: Danh sach cac Value ID hop le

    """

    conn = sqlite3.connect(database)
    report_tables = [
        "balance_sheet",
        "income_statement",
        "cash_flow",
        "cash_flow_direct",
    ]

    valid_id = pandas.Index([], dtype=int)

    for table in report_tables:
        query = f"SELECT * FROM {table}"
        index = pandas.read_sql(query, conn, index_col="id").index
        valid_id = valid_id.append(index)

    return valid_id


def manual_customize_series(ser, valid_id):
    """Tuy chinh them moi du lieu vao Series mot cach thu cong

    Args:
        ser (pandas.Series): Cot du lieu can tuy chinh
        valid_id (pandas.Index): Cac ID hop le co the duoc them vao

    Returns:
        :obj:`pandas.Series`: Cot du lieu sau khi su ly

    """
    import numpy

    bk_ser = ser.copy()  # du phong truong hop huy ket qua

    while True:
        separate_print("INPUT VALUES", "*")
        value_id = int(input("ID ban muon thay doi: "))

        if value_id not in valid_id:
            print(f"[{value_id}] Khong hop le, vui long kiem tra lai")
            continue

        try:
            value = int(input("Gia tri nhap vao: "))
        except ValueError:
            print("Gia tri khong hop le, se gan gia NaN vao cho ID")
            value = numpy.nan

        ser[value_id] = value

        finish = input("Ban da hoan tat (nhan Enter de tiep tuc nhap du lieu) (y)? ")

        if finish == "y":
            break

    while True:
        save = input("Ban co muon su dung ket qua vua nhap (y/n)? ")

        if save == "y":
            return ser
        elif save == "n":
            return bk_ser
        else:
            continue


def edit_by_import_file(data, valid_id, fm_checker):
    """Chon mot file luu du lieu da co san va them vao trong co so du lieu

    Args:
        data (pandas.DataFrame): Co so du lieu can su ly
        valid_id (pandas.Index): Cac ID hop le co the duoc them vao
        fm_checker (:obj:): Func dung de kiem tra ten cua cot

    Returns:
        :obj:`pandas.DataFrame`

    """
    file_name = input("Vui long nhap vao ten file muon su dung: ")
    file_path = os.path.join(FilePath.import_dir, file_name)

    try:
        new_data = pandas.read_csv(file_path, index_col="id")
        new_data = new_data.drop("name", axis=1)  # bo cot ten cac gia tri

    except FileNotFoundError:
        print("File khong ton tai, vui long kiem tra lai")
        return data

    # kiem tra cac id co phu hop khong
    invalid_id = new_data.index.difference(valid_id)
    if not invalid_id.empty:
        print("Co ton tai cac ID khong hop le, bao gom:")
        print(invalid_id.to_list())
        print("Vui long kiem tra lai")
        return data

    # kiem tra cac cot co ten phu hop hay khong
    for column in new_data.columns:
        if fm_checker(column) is not True:
            print(f"'{column}' Khong phai ten hop le vui long kiem tra lai")
            return data

        if new_data[column].dtype not in (float, int):
            print(f"'{column}' chua dinh danh khong phu hop ({new_data[column].dtype})")
            return data

    print(f"Da hoan tat viec nhap du lieu tu file '{file_name}'")
    return new_data.combine_first(data)


def main():
    separate_print("STOCK INPUT")
    stock = input("Co phieu ban muon xu ly: ").upper()

    separate_print("CHOICE REPORT TYPE")
    while True:
        print("Loai bao cao ban muon thay doi:\n" "\t[1] - YEARS\n" "\t[2] - QUATERS\n")
        report_type = input(">: ")

        if report_type == "1":
            report_type = "YEARS"
        elif report_type == "2":
            report_type = "QUARTERS"
        else:
            continue

        break

    tb_name = f"{stock}_{report_type}"  # bang trong co so du lieu

    separate_print("PROCESSING")
    conn = sqlite3.connect(FilePath.database_path)
    try:
        query = f"SELECT * FROM {tb_name}"
        data = pandas.read_sql(query, conn, index_col="id")
    except DatabaseError:
        print("Khong co san trong co so du lieu. Tien hanh tao moi")
        data = pandas.DataFrame()

    valid_id = get_valid_id(FilePath.database_path)

    while True:
        separate_print("CHOOSE ACTIONS")
        print(
            "Chon thao tac ban muon thuc hien:\n"
            "\t[1] XOA cot du lieu\n"
            "\t[2] CHINH SUA cot du lieu\n"
            "\t[3] THEM MOI cot du lieu\n"
            "\t[4] NHAP TU FILE co san\n"
            "\t[0] LUU / THOAT"
        )
        action = input(">: ")

        if action == "0":
            save = input("Ban co muon luu ket qua vua chinh khong (y/n)?")
            if save == "y":
                data.index.name = "id"
                data.to_sql(tb_name, conn, if_exists="replace")
            break

        if action in "123":
            time_type = choose_timeline(report_type)

            if action == "1":
                data = delete_col(data, time_type)
            elif action == "2":
                data = edit_col(data, time_type, valid_id)
            elif action == "3":
                data = create_col(data, time_type, valid_id)

        if action == "4":
            if report_type == "YEARS":
                fm_checker = TimeType.Year.check_format
            else:
                fm_checker = TimeType.Quarter.check_format

            data = edit_by_import_file(data, valid_id, fm_checker)


if __name__ == "__main__":
    main()
