#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from toexcel.pd2xl import pandas2excel

data = {
    "Name": ["Alice", "Bob", "Charlie"],
    "Age": [24, 27, 22],
    "City": ["New York New York New York", "Los Angeles", "Chicago"]
}

df = pd.DataFrame(data)
pandas2excel(
    filename="test.xlsx",
    df=df,
    header=True,
    engine="openpyxl"
)
