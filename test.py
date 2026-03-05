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

def get_ratio(df, item_id, quarter="2025-Q4"):
    row = df[df["item_id"] == item_id]
    if not row.empty:
        return float(row.iloc[0][quarter])
    return None


important_keys = [
    "trailing_eps",
    "p_e",
    "p_b",
    "roe_trailling",
    "roa_trailling",
    "net_profit_margin",
    "net_revenue",
    "profit_after_tax_for_shareholders_of_the_parent_company"
]
quarters = ["2025-Q1", "2025-Q2", "2025-Q3", "2025-Q4"]

ratio_dict = {}

stock = Vnstock().stock(symbol="HPG", source="KBS")

ratio = stock.finance.ratio()

result = {}

for _, row in ratio.iterrows():

    key = row["item_id"]

    if key in important_keys:

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



