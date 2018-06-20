__author__ = 'wanderknight'
__time__ = '2018/6/19 20:35'

from machine_learning import read_and_show
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
import numpy as np
from pandas import DataFrame

df = read_and_show()


def create_vector(df_szzs):
    df_szzs['ratio'] = df_szzs['close'] / df_szzs['close'].shift(1) - 1
    # print(df_szzs.head())

    for i in range(1, 11):
        df_szzs.loc[:, 'ratio Minus ' + str(i)] = df_szzs['ratio'].shift(i)
    df_szzs['flag'] = df_szzs['ratio'].apply(lambda x: 1 if x > 0 else 0)
    df_szzs20 = df_szzs[[x for x in df_szzs.columns if 'ratio Minus' in x or x == 'flag']].iloc[11:, ]  # 不选择最初20个null
    df_szzs20 = df_szzs20.iloc[:, ::-1]
    return df_szzs20


df_szzs20 = create_vector(df)

# df_szzs20.reset_index(inplace=True)
# del df_szzs20['date']
_ = sns.pairplot(df_szzs20[:10], hue="flag")
plt.show()
print('end')

# X_train = df_szzs20[:-1000]
# y_train = df_szzs20['close'].shift(-1)[:-1000]
# X_test = df_szzs20[-1000:]
# y_test = df_szzs20['close'].shift(-1)[-1000:]
