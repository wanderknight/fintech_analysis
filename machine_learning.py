__author__ = 'wanderknight'
__time__ = '2018/6/15 9:32'
import pandas as pd
from tdx import api_base
import matplotlib.pyplot as plt
import numpy as np

"""
艾伯特python机器学习实践指南 chapter7 使用机器学习预测股票市场
"""


def read_and_show():
    df_szzs = api_base.get_price('000001.XSHG')
    df_szzs = df_szzs[df_szzs.index > pd.to_datetime('2000-01-01')]
    print(df_szzs.head())
    df_szzs['close'].plot()
    plt.title("szzs read and show", fontsize=20)
    plt.show()
    return df_szzs


df = read_and_show()


def get_stats(s, Division_str, n=252):
    print('***********************')
    print(Division_str)
    s = s.dropna()
    wins = len(s[s > 0])
    losses = len(s[s < 0])
    evens = len(s[s == 0])
    mean_w = round(s[s > 0].mean(), 3)
    mean_l = round(s[s < 0].mean(), 3)
    win_r = round(wins / losses, 3)
    mean_trd = round(s.mean(), 3)
    sd = round(np.std(s), 3)
    max_l = round(s.min(), 3)
    max_w = round(s.max(), 3)
    sharpe_r = round((s.mean() / np.std(s)) * np.sqrt(n), 4)
    cnt = len(s)
    print('Trades:', cnt, '\nWins:', wins, '\nLosses:', losses, '\nBreakeven:', evens, '\nWin/Loss Ratio', win_r,
          '\nMean Win:', mean_w, '\nMean Loss:', mean_l, '\nMean', mean_trd, '\nStd Dev:', sd, '\nMax Loss:', max_l,
          '\nMax Win:', max_w, '\nSharpe Ratio:', sharpe_r)


def first_analy(df_szzs):
    first_open = df_szzs['open'].iloc[0]
    last_close = df_szzs['close'].iloc[-1]
    print('all increase', last_close - first_open)
    df_szzs['daily_change'] = df_szzs['close'] - df_szzs['open']
    print('daily_change sum:', df_szzs['daily_change'].sum())
    df_szzs['overnight_change'] = df_szzs['open'] - df_szzs['close'].shift(1)
    print('overnight_change sum:', df_szzs['overnight_change'].sum())

    # df_szzs[['daily_change', 'overnight_change']].plot()
    # plt.show()

    df_szzs['daily_change'].mean()
    np.std(df_szzs['daily_change'])
    df_szzs['overnight_change'].mean()
    np.std(df_szzs['overnight_change'])

    df_szzs[df_szzs['daily_change'] < 0]['daily_change'].mean()
    df_szzs[df_szzs['overnight_change'] < 0]['overnight_change'].mean()

    daily_rtn = (df_szzs['close'] - df_szzs['close'].shift(1)) / df_szzs['close'].shift(1) * 100
    id_rtn = (df_szzs['close'] - df_szzs['open']) / df_szzs['open'] * 100
    on_rtn = (df_szzs['open'] - df_szzs['close'].shift(1)) / df_szzs['close'].shift(1) * 100

    get_stats(daily_rtn, 'daily_rtn')
    get_stats(id_rtn, 'id_rtn')
    get_stats(on_rtn, 'on_rtn')


first_analy(df)


def create_vecter(df_szzs):
    for i in range(1, 21):
        df_szzs.loc[:, 'Close Minus ' + str(i)] = df_szzs['close'].shift(i)
    df_szzs20 = df_szzs[[x for x in df_szzs.columns if 'Close Minus' in x or x == 'close']].iloc[20:, ]  # 不选择最初20个null
    df_szzs20 = df_szzs20.iloc[:, ::-1]
    return df_szzs20


df20 = create_vecter(df)


def get_signal(r):
    if r['Predicted Next Close'] > r['Next Day Open']:
        return 1
    else:
        return 0


def get_signal_high(r):
    if r['Predicted Next Close'] > r['Next Day Open'] + 1:
        return 1
    else:
        return 0


def get_signal_revers(r):
    if r['Predicted Next Close'] > r['Next Day Open'] + 1:
        return 0
    else:
        return 1


def get_ret(r):
    if r['Signal'] == 1:
        return ((r['Next Day Close'] - r['Next Day Open']) / r['Next Day Open']) * 100
    else:
        return 0


def support_vecter(df_szzs20, df_szzs):
    from sklearn.svm import SVR

    clf = SVR(kernel='linear')
    X_train = df_szzs20[:-1000]
    y_train = df_szzs20['close'].shift(-1)[:-1000]
    X_test = df_szzs20[-1000:]
    y_test = df_szzs20['close'].shift(-1)[-1000:]

    model = clf.fit(X_train, y_train)
    preds = model.predict(X_test)

    tf = pd.DataFrame(list(zip(y_test, preds)), columns=['Next Day Close', 'Predicted Next Close'], index=y_test.index)

    cdc = df_szzs20[['close']].iloc[-1000:]
    ndo = df_szzs[['open']].iloc[-1000:].shift(-1)
    tf1 = pd.merge(tf, cdc, left_index=True, right_index=True)
    tf2 = pd.merge(tf1, ndo, left_index=True, right_index=True)
    tf2.columns = ['Next Day Close', 'Predicted Next Close', 'Current Day Close', 'Next Day Open']

    tf2 = tf2.assign(Signal=tf2.apply(get_signal, axis=1))
    tf2 = tf2.assign(PnL=tf2.apply(get_ret, axis=1))
    print(tf2.head())
    # 预测收益
    print('predict sum:', (tf2[tf2['Signal'] == 1]['Next Day Close'] - tf2[tf2['Signal'] == 1]['Next Day Open']).sum())
    print('recent sum:', (df_szzs['close'].iloc[-1000:] - df_szzs['open'].iloc[-1000:]).sum())

    get_stats((df_szzs['close'].iloc[-1000:] - df_szzs['open'].iloc[-1000:]) / df_szzs['open'].iloc[-1000:] * 100,
              'support_vecter')
    get_stats(tf2['PnL'], 'tf2 PnL')

    tf2 = tf2.assign(Signal=tf2.apply(get_signal_high, axis=1))
    tf2 = tf2.assign(PnL=tf2.apply(get_ret, axis=1))
    print(tf2.head())
    # 预测收益
    print('get_signal_high predict sum:',
          (tf2[tf2['Signal'] == 1]['Next Day Close'] - tf2[tf2['Signal'] == 1]['Next Day Open']).sum())
    get_stats(tf2['PnL'], 'get_signal_high tf2 PnL')

    tf2 = tf2.assign(Signal=tf2.apply(get_signal_revers, axis=1))
    tf2 = tf2.assign(PnL=tf2.apply(get_ret, axis=1))
    print('get_signal_revers predict sum:',
          (tf2[tf2['Signal'] == 1]['Next Day Close'] - tf2[tf2['Signal'] == 1]['Next Day Open']).sum())
    get_stats(tf2['PnL'], 'get_signal_revers tf2 PnL')


support_vecter(df20, df)


def use_dtw(sp):
    from scipy.spatial.distance import euclidean
    from fastdtw import fastdtw

    def dtw_dist(x, y):
        distance, path = fastdtw(x, y, dist=euclidean)
        return distance

    tseries = []
    tlen = 5
    for i in range(tlen, len(sp), tlen):
        # 计算5天的相对收益，及最后一天的收益
        pctc = sp.iloc[i - tlen:i].pct_change()[1:].values * 100
        res = sp.iloc[i - tlen:i + 1].pct_change()[-1] * 100
        tseries.append((pctc, res))

    dist_pairs = []
    for i in range(len(tseries)):
        for j in range(len(tseries)):
            dist = dtw_dist(tseries[i][0], tseries[j][0])
            dist_pairs.append((i, j, dist, tseries[i][1], tseries[j][1]))

    dist_frame = pd.DataFrame(dist_pairs, columns=['A', 'B', 'Dist', 'A Ret', 'B Ret'])
    sf = dist_frame[dist_frame['Dist'] > 0].sort_values(['A', 'B']).reset_index(drop=1)
    sfe = sf[sf['A'] < sf['B']]
    # 按照DTW的定义，小的相近，因此使用小于1的条件。实际应该使用排序的最小值
    winf = sfe[(sfe['Dist'] <= 1) & (sfe['A Ret'] > 0)]
    # plt.plot(np.arange(4), tseries[18][0])
    # plt.plot(np.arange(4), tseries[250][0])
    # plt.show()
    excluded = {}
    return_list = []

    def get_returns(r):
        if excluded.get(r['A']) is None:
            return_list.append(r['B Ret'])
        if r['B Ret'] < 0:
            excluded.update({r['A']: 1})

    winf.apply(get_returns, axis=1);
    get_stats(pd.Series(return_list), 'dtw')


use_dtw(df['close'])
