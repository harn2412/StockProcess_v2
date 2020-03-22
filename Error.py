"""Chua cac Exception dung cho chuong trinh"""


class CanNotScrapData(ValueError):
    """Bao loi khi khong the tim thay bang chua du lieu trong source code
    cua trang web tai ve, thuong la khi tai trang web bi loi"""
    pass


class EmptyTable(ValueError):
    """Bao loi khi tat ca du lieu trong bang tai ve deu la numpy.na"""
    pass


class EmptyColumn(ValueError):
    """Bao loi khi the lay du lieu cua mot cot,
    mac du da thu tai lai nhieu lan"""
    pass


class DuplicateIndex(ValueError):
    """Bao loi khi noi dung Index tao ra bi trung lap"""
    pass
