"""Dung de debug va test code chuong trinh"""

import GetData
import TimeType
import Report
import pandas
import deal_with_data

import re

data: pandas.Series = GetData.CafeFScraper("ACB", Report.CFD, TimeType.Year(2019)).data
data = deal_with_data.solve_duplicate_index(data)

data4 = pandas.Series(range(40001, 40001 + data.size), data.index)
index = data.index

new_name = []

for i in index:
    name = re.search(r"(.+)_\d+", i).group(1)
    new_name.append(name)

new_index = (i + 10001 for i in range(0, len(index)))

series = pandas.Series(new_name, new_index, name="name")
series.to_csv("default_data/cash_flow_direct.csv",index_label="id")