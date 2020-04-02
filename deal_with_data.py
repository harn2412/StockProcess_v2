"""Doi pho giai quyet cac van de voi du lieu thu duoc khong phu hop
Vi du: bi trung Index, thong nhat lai index truoc khi luu, ..."""
import pandas
import numpy


def solve_duplicate_index(data: pandas.Series):
    """Xu ly truong hop Index bi trung"""

    # truong hop index khong bi trung thi tra ve du lieu goc
    if data.index.is_unique:
        return data

    print("WARNING: Phat hien co Index bi trung")
    print("Dang tim cach xu ly...")

    # "bi trung nhung chua du lieu giong nhau" hoac "chi co mot gia tri, con
    # cac hang khac la NaN" thi giu lay

    print("Loc va giu lai cac Index 'trung nhung co cung gia tri' "
          "sau khi da loai bo cac gia tri NaN")

    # du lieu cua cac unique index
    data_of_unique_index = data.loc[data.index.drop_duplicates(keep=False)]

    duplicate_index = set(data.index[data.index.duplicated()])
    keep_index = []
    keep_value = []
    for index in duplicate_index:
        data_of_that_index = data[index]

        if data_of_that_index.nunique() != 1:
            print(f"Loai bo [{index}] vi chua nhieu du lieu khac nhau")
            continue

        # Loai bo gia tri NaN
        data_of_that_index.dropna(inplace=True)

        try:
            will_be_keep = data_of_that_index[0]
        except KeyError:
            will_be_keep = numpy.nan

        print(f"Giu lay [{index}] = {will_be_keep}")
        keep_index.append(index)
        keep_value.append(will_be_keep)

    return data_of_unique_index.append(pandas.Series(keep_value, keep_index))
