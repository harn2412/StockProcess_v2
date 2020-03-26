"""Cac cong thuc tinh toan lien quan den bang Quarterly IS"""


class F1:
    # F1: Cong thuc tinh toan tu du lieu co san

    @staticmethod
    def f_tong_chi_phi_hoat_dong(ser):
        """Tinh toan tong chi phi hoat dong cua QUY (21017)

        21017 = 20007 + 20010 _20011
        20007: Chi phi tai chinh
        20010: Chi phi ban hang
        20011: Chi phi quan ly doanh nghiep

        Args:
            ser: 'obj'Serial : Chua du lieu co san cua QUY

        Returns:
            float: Ket qua

        """

        return ser[20007] + ser[20010] + ser[20011]


class F2:
    # F2: Cong thuc tinh toan tu du lieu F1

    @staticmethod
    def f_loi_nhuan_tu_hoat_dong_kinh_doanh(ser):
        """Tinh toan loi nhuan tu hoat dong kinh doanh cua QUY (21019)

        21019 = 20005 - 21017
        20005: Loi nhuan gop
        21017: Tong chi phi hoat dong

        Args:
            ser: 'obj'Serial : Chua du lieu co san cua QUY

        Returns:
            float: Ket qua

        """

        return ser[20005] - ser[21017]


class F3:
    # F3: Cong thuc tinh toan tu du lieu cua F2

    @staticmethod
    def f_loi_nhuan_thuan_tu_hoat_dong_kinh_doanh(ser):
        """Tinh toan loi nhuan thuan tu hoat dong kinh doanh cua QUY (21023)

        21023 = 21019 + 20006 + 20009
        21019: Loi nhuan tu hoat dong kinh doanh
        20006: Doanh thu hoat dong tai chinh
        20009: Lai lo trong cong ty lien doanh

        Args:
            ser: 'obj'Serial : Chua du lieu co san cua QUY

        Returns:
            float: Ket qua

        """

        return ser[21019] + ser[20006] + ser[20009]


class F4:
    # F4: Cong thuc tinh toan tu du lieu cua F3

    @staticmethod
    def f_tong_loi_nhuan_ke_toan_truoc_thue(ser):
        """Tinh toan tong loi nhuan ke toan truoc thue (21027)
        21027 = 21023 + 20015
        21023: Loi nhuan thuan tu hoat dong kinh doanh
        20015: Loi nhuan khac

        Args:
        ser: 'obj'Serial : Chua du lieu co san cua QUY

        Returns:
        float: Ket qua

        """

        return ser[21023] + ser[20015]


class F5:
    # F5: Cong thuc tinh toan tu du lieu cua F4

    @staticmethod
    def f_loi_nhuan_sau_thue_thu_nhap_doanh_nghiep(ser):
        """Tinh toan loi nhuan sau thue thu nhap doanh nghiep (21032)
        21032 = 21027 - (20017 + 20018)
        21027: Tong loi nhuan ke toan truoc thue
        20017: Chi phi thue TNDN hien hanh
        20018: Chi phi thue TNDN hoan lai

        Args:
            ser: 'obj'Serial : Chua du lieu co san cua QUY

        Returns:
            float: Ket qua

        """

        return ser[21027] - (ser[20017] + ser[20018])


class F6:
    # F6: Cong thuc tinh toan tu du lieu cua F5

    @staticmethod
    def f_loi_nhuan_sau_thue_cong_ty_me(ser):
        """Tinh toan loi nhuan sau thue cong ty me (21035)
        21035 = 21032 - 20020
        21032: Loi nhuan sau thue thu nhap doanh nghiep
        20020: Loi ich cua co dong toi thieu

        Args:
            ser: 'obj'Serial : Chua du lieu co san cua QUY

        Returns:
            float: Ket qua

        """

        return ser[21032] - ser[20020]
