__author__ = 'wanderknight'
__time__ = '2018/6/19 20:35'

from machine_learning import read_and_show, create_vecter
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import make_classification
import numpy as np
from pandas import DataFrame

df = read_and_show()
df_szzs20 = create_vecter(df)

df_szzs20.reset_index(inplace=True)
del df_szzs20['date']
_ = sns.pairplot(df_szzs20[:10])
plt.show()
print('end')

# X_train = df_szzs20[:-1000]
# y_train = df_szzs20['close'].shift(-1)[:-1000]
# X_test = df_szzs20[-1000:]
# y_test = df_szzs20['close'].shift(-1)[-1000:]