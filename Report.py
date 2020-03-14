"""Chua cac thong tin ve cac loai bao cao"""
from collections import namedtuple

Report = namedtuple("Report", [
    "name",
    "code",
    "url_short_name",
    "url_long_name",
])

# can doi ke toan
BS = Report(
    code=1,
    name="Can Doi Ke Toan",
    url_short_name="BSheet",
    url_long_name="can-doi-ke-toan",
)

# ket qua hoat dong kinh doanh
IS = Report(
    code=2,
    name="Ket Qua Hoat Dong Kinh Doanh",
    url_short_name="IncSta",
    url_long_name="ket-qua-hoat-dong-kinh-doanh",
)

# luu chuyen tien te gian tiep
CF = Report(
    code=3,
    name="Luu Chuyen Tien Te Gian Tiep",
    url_short_name="CashFlow",
    url_long_name="luu-chuyen-tien-te-gian-tiep",
)

# luu chuyen tien te truc tiep
CFD = Report(
    code=4,
    name="Luu Chuyen Tien Te Truc Tiep",
    url_short_name="CashFlowDirect",
    url_long_name="luu-chuyen-tien-te-truc-tiep",
)
