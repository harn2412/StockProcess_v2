"""Doi pho giai quyet cac van de voi du lieu thu duoc khong phu hop
Vi du: bi trung Index, thong nhat lai index truoc khi luu, ..."""
import pandas


def solve_duplicate_index(data: pandas.Series):
    """Xu ly truong hop Index bi trung"""

    # truong hop index khong bi trung thi tra ve du lieu goc
    if data.index.is_unique:
        return data

    # bi trung nhung chua du lieu giong nhau thi giu lay

    # du lieu cua cac unique index
    data_of_unique_index = data.loc[data.index.drop_duplicates(keep=False)]

    duplicate_index = set(data.index[data.index.duplicated()])
    keep_index = []
    keep_value = []
    for index in duplicate_index:
        data_of_that_index = data[index]

        if data_of_that_index.nunique(dropna=False) != 1:
            print(f"Loai bo [{index}] vi chua nhieu du lieu khac nhau")

        print(f"Giu lay [{index}] = {data_of_that_index[0]}")
        keep_index.append(index)
        keep_value.append(data_of_that_index[0])

    return data_of_unique_index.append(pandas.Series(keep_value, keep_index))
