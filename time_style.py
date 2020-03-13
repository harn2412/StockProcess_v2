"""Tao ra cac thong so thoi gian dung trong URL tuong ung voi bao cao Nam va Quy"""


class Year:
    """Thoi gian hang nam"""

    def __init__(self, year: int):
        self.year = year
        self.quarter = 0

    def prev(self, step: int):
        """dem lui thoi gian ve khoan tuong ung
        step: so buoc lui"""

        year, quarter = self.year, self.quarter

        for i in range(0, step):
            year -= 1

        return year, quarter

    def __repr__(self):
        return f"YearStyle(year={self.year}, quarter={self.quarter})"


class Quarter:
    """Thoi gian hang quy"""

    def __init__(self, year: int, quarter: int):
        self.year = year
        self.quarter = quarter

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
        return f"QuarterStyle(year={self.year}, quarter={self.year})"


year1 = Year(2020)
quarter1 = Quarter(2020, 1)
print(year1)
print(quarter1)
