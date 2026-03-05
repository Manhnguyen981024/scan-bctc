import ssl
import requests
import urllib3

ssl._create_default_https_context = ssl._create_unverified_context
urllib3.disable_warnings()

old_request = requests.Session.request

def new_request(self, method, url, **kwargs):
    kwargs['verify'] = False
    return old_request(self, method, url, **kwargs)

requests.Session.request = new_request
import os

os.environ["HTTP_PROXY"] = ""
os.environ["HTTPS_PROXY"] = ""
os.environ["http_proxy"] = ""
os.environ["https_proxy"] = ""

from vnstock import Vnstock
from pprint import pprint
import pandas as pd
import numpy as np
from constants import *

def get_ratio(df, item_id, quarter="2025-Q4"):
    row = df[df["item_id"] == item_id]
    if not row.empty:
        return float(row.iloc[0][quarter])
    return None

ratio_dict = {}

stock = Vnstock().stock(symbol="STB", source=DATA_SOURCE)

ratio = stock.finance.ratio()

result = {}

for _, row in ratio.iterrows():

    key = row["item_id"]
    
    quarters = [c for c in ratio.columns if "Q" in c]

    if key in IMPORTANT_KEYS:

        result[key] = {}

        for q in quarters:
            result[key][q] = row[q]
            
# print(result)
df = pd.DataFrame(result)
print(df)

# lấy EPS các quý
eps_q1 = result["trailing_eps"]["2025-Q1"]
eps_q4 = result["trailing_eps"]["2025-Q4"]
# tính EPS growth
eps_growth = (eps_q4 - eps_q1) / eps_q1

# lấy PE mới nhất
pe = result["p_e"]["2025-Q4"]

# tính PEG
peg = pe / (eps_growth * 100)

print("EPS Growth:", round(eps_growth * 100, 2), "%")
print("PE:", pe)
print("PEG:", round(peg, 2))

pes = []

for s in BANK_STOCKS:

    stock = Vnstock().stock(symbol=s, source=DATA_SOURCE)

    ratio = stock.finance.ratio()

   # lấy tất cả cột quý
    quarters = [c for c in ratio.columns if "Q" in c]
    
    pe_row = ratio[ratio["item_id"] == "p_e"]

    pe_values = [pe_row[q].values[0] for q in quarters]

    pe_avg = sum(pe_values) / len(pe_values)

    pes.append(pe_avg)

industry_pe = np.median(pes)

print("Steel Industry PE:", round(industry_pe, 2))

print("Industry PE:", industry_pe)