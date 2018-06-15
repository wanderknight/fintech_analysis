__author__ = 'wanderknight'
__time__ = '2018/6/15 9:32'
import pandas as pd
from tdx import api_base
import matplotlib.pyplot as plt
import numpy as np

df_szzs = api_base.get_price('000001.XSHG')
df_szzs = df_szzs[df_szzs.index>pd.to_datetime('2000-01-01')]
print(df_szzs.head())
# df_szzs['close'].plot()
# plt.show()

first_open = df_szzs['open'].iloc[0]
last_close = df_szzs['close'].iloc[-1]
print(first_open, last_close)
df_szzs['daily_change'] = df_szzs['close'] - df_szzs['open']
df_szzs['daily_change'].sum()
df_szzs['overnight_change'] = df_szzs['open'] - df_szzs['close'].shift(1)
df_szzs['overnight_change'].sum()

# df_szzs[['daily_change', 'overnight_change']].plot()
# plt.show()

df_szzs['daily_change'].mean()
np.std(df_szzs['daily_change'])
df_szzs['overnight_change'].mean()
np.std(df_szzs['overnight_change'])

df_szzs[df_szzs['daily_change'] < 0]['daily_change'].mean()
df_szzs[df_szzs['overnight_change'] < 0]['overnight_change'].mean()
