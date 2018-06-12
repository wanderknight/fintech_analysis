__author__ = 'wanderknight'
__time__ = '2018/5/2 9:50'
import os
from pytdx.reader import HistoryFinancialReader

tdx_hf_path = 'D:\\NewTdxVipTc\\vipdoc\\cw\\'
files = os.listdir(tdx_hf_path)
for f in files:
    if 'dat' in f:
        tdx_hf_f_path = tdx_hf_path + f
        print(tdx_hf_f_path)
        df = HistoryFinancialReader().get_df(tdx_hf_f_path)
        df.to_csv('history_financial.csv', mode='a', header=False)
