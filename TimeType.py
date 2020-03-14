"""Tao ra cac thong so thoi gian dung trong URL tuong ung voi bao cao Nam va Quy"""
from datetime import datetime


class Year:
    """Thoi gian hang nam"""

    def __init__(self, year: int):
        self.year = year
        self.quarter = 0

    def __call__(self, *args, **kwargs):
        return self(*args, **kwargs)

    def prev(self, step: int):
        """dem lui thoi gian ve khoan tuong ung
        step: so buoc lui"""

        year, quarter = self.year, self.quarter

        for i in range(0, step):
            year -= 1

        return year, quarter

    def __repr__(self):
        return f"TimeType.Year(year={self.year}, quarter={self.quarter})"


class Quarter:
    """Thoi gian hang quy"""

    def __init__(self, year: int, quarter: int):
        self.year = year
        self.quarter = quarter

    def __call__(self, *args, **kwargs):
        return self(*args, **kwargs)

    def prev(self, step: int):
        """dem lui thoi gian ve khoan tuong ung
        step: so buoc lui"""

        year, quarter = self.year, self.quarter

        for i in range(0, step):
            if quarter == 1:
                year -= 1
                quarter = 4
            else:
                quarter -= 1

        return year, quarter

    def __repr__(self):
        return f"TimeType.Quarter(year={self.year}, quarter={self.quarter})"


def now():
    """Quy va nam hien tai"""
    today = datetime.now()
    cr_year = today.year
    cr_quarter = (today.month - 1) // 3 + 1

    return cr_year, cr_quarter


def check(time_type_obj):
    """Kiem tra xem nam va quy co hop le khong
    var:
        time_type_obj: Year / Quarter : Loai thoi gian da chon
    dieu kien kiem tra:
        thoi gian phai nho hon moc thoi gian hien tai (vi khong the co bao cao
        cua nam / quy hien tai duoc)
    ket qua:
        hop le: Tra lai time_type_obj da nhap vao
        khong hop le: ValueError Exception"""

    cr_year, cr_quarter = now()

    if isinstance(time_type_obj, Year):
        if time_type_obj.year < cr_year:
            return time_type_obj
        else:
            raise ValueError("Nam lay bao cao phai nho hon nam hien tai")

    elif isinstance(time_type_obj, Quarter):
        if time_type_obj.year < cr_year:
            return time_type_obj
        elif time_type_obj.year == cr_year:
            if time_type_obj.quarter < cr_quarter:
                return time_type_obj
            else:
                raise ValueError("Quy lay bao cao phai nho hon quy hien tai")
        else:
            raise ValueError("Nam lay bao cao phai nho hon hoac bang nam hien tai")


def create_from_input(time_type_class, year_class, quarter_class):
    """Kiem soat viec nhap va chon gia tri cua nguoi dung ung voi lai TimeStyle
    var:
        :type time_type_class: Year / Quarter : Class thoi gian tuong ung
        year_class: La class cua Year trong module nay da duoc import vao chuong trinh chinh
        quarter_class: La class cua Quarter trong module nay da duoc import vao trong chuong trinh chinh
    ket qua:
        hop le: Tra lai doi tuong TimeStyle Obj tuong ung voi gia tri da nhap
        khong hop le: Bat nguoi dung nhap den khi hop le
        """

    if time_type_class is year_class:
        while True:
            try:
                year = int(input("Nam ban muon lay bao cao: "))
            except ValueError:
                print("Gia tri khong hop le vui long nhap lai "
                      "(VD: 2020 hoac 2019)")
                continue

            try:
                time_type_obj = time_type_class(year)
                return check(time_type_obj)
            except ValueError as error:
                print(error)
                continue

    elif time_type_class is quarter_class:
        while True:
            try:
                year = int(input("Nam ban muon lay bao cao: "))
            except ValueError:
                print("Gia tri khong hop le vui long nhap lai "
                      "(VD: 2020 hoac 2019)")
                continue

            try:
                quarter = int(input("Quy ban muon lay bao cao (1, 2, 3, 4): "))
                if quarter not in (1, 2, 3, 4):
                    raise ValueError
            except ValueError:
                print("Gia tri khong hop le vui long nhap lai "
                      "(chi cho phep chon mot trong cac so 1, 2, 3, 4)")
                continue

            try:
                time_type_obj = check(time_type_class(year, quarter))
                return time_type_obj
            except ValueError as error:
                print(error)
                continue


def test():
    a = Quarter
    if a == Quarter:
        print("haha")
    print(type(a))
    create_from_input(a, Year, Quarter)


if __name__ == '__main__':
    test()
