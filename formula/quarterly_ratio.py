"""Cac cong thuc tinh toan lien quan den bang Quarterly Ratio"""


class F1:
    """F1: Cong thuc tinh toan tu du lieu co san"""

    @staticmethod
    def f_number_of_outstanding_share_of_current_quarter(ser):
        """ Tinh toan number of outstanding share of current quarter (50016)

        50016 = (10097 + 10104) / (int 10000)
        10097: Von gop cua chu so huu
        10104: Co phieu quy

        Args:
            ser: 'obj'Serial : Chua du lieu co san cua QUY

        Returns:
            float: Ket qua

        """
        return (ser[10097] + ser[10104]) / 10000


class F7:
    """F7: Cong thuc tinh toan tu du lieu F6"""

    @staticmethod
    def f_eps_of_current_quarter(ser):
        """Tinh toan EPS of current quarter (50017)

        50017 = 21035 / 50016
        21035: Loi nhuan sau thue cong ty me
        50016: Number of outstanding share of current quarter

        Args:
            ser: 'obj'Serial : Chua du lieu co san cua QUY

        Returns:
            float: Ket qua

        """

        return ser[21035] / ser[50016]


class F8:
    """F8: Cong thuc tinh toan tu du lieu F7"""

    @staticmethod
    def f_growth_rate_of_eps(ser1, ser2):
        """Tinh toan growth rate of EPS (50020)

        50020 = 50017 / SQLY 50017 - 1

        Args:
            ser1: 'obj'Serial : Chua du lieu co san cua QUY
            ser2: 'obj'Serial : Chua du lieu co san cua cung QUY nam truoc
                (SQLY) Same Quarter Last Year

        Returns:
            float: Ket qua

        """

        return ser1[50017] / ser2[50017] - 1
