"""Dung de debug va test code chuong trinh"""
import GetData
import pandas
import Report
import TimeType

_ = GetData.CafeFScraper("FPT", Report.BS, TimeType.Year(2018))
df = pandas.DataFrame(_.data,  index=_.index)
print(df)
