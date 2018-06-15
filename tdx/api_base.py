__author__ = 'wanderknight'
__time__ = '2018/6/9 21:07'
from tdx import industry_hy

"""601118.XSHG', '002772.XSHE"""

from tdx.tdx_data_process import tdx2csv_data_path
import tdx
import pandas as pd
import datetime


def industrys():
    """
    获得所有行业
    :return: list of order_book_id
    """
    indst = industry_hy.get_industry_classified_list_by_level(2)
    return [x + '.XSHG' for x in indst]


# print(industrys())


def industry(industry_code):
    """
    获得属于某一行业的所有股票列表。
    :param industry_code:通达信行业代码 T0201
    :return: list of order_book_id
    """
    return industry_hy.get_stocks_by_hyblock(industry_code)


# print(len(industry('T0305')))


def get_trading_dates():
    """
    date='2016-05-02'
    :return:list[`datetime.date`]
    """
    import os
    szzs_path_999999 = tdx2csv_data_path + 'tdx\\k_line\\K_day\\SH#999999.csv'
    szzs_path_000001 = tdx2csv_data_path + 'tdx\\k_line\\K_day\\SH#000001.csv'
    if os.path.exists(szzs_path_999999):
        df = pd.read_csv(szzs_path_999999)
        return pd.to_datetime(df['date'].tolist())
    if os.path.exists(szzs_path_000001):
        df = pd.read_csv(szzs_path_000001)
        return pd.to_datetime(df['date'].tolist())
    print('no szzs 999999 or 000001')


# print(get_trading_dates())


def get_previous_trading_date():
    """
    date='2016-05-02'
    str | date | datetime | pandas.Timestamp
    :return:datetime.date
    """
    pass


def get_next_trading_date():
    """
    date='2016-05-02'
    :return: datetime.date
    """
    pass


def get_fundamentals():
    pass


def get_price(order_book_id):  # , start, end
    """
    获取指定合约或合约列表的历史行情（包含起止日期，日线或分钟线），不能在’handle_bar’函数中进行调用。
    这一函数主要是为满足在研究平台编写策略习惯而引入。
    ('000001.XSHE', start_date='2015-04-01', end_date='2015-04-12')
    :return:
    """
    order_book_id_0, order_book_id_1 = order_book_id.split('.')
    if order_book_id_1 == 'XSHG':
        file_name = 'SH#' + order_book_id_0 + '.csv'
    if order_book_id_1 == 'XSHE':
        file_name = 'SZ#' + order_book_id_0 + '.csv'

    path = tdx2csv_data_path + 'tdx\\k_line\\K_day\\' + file_name
    df = pd.read_csv(path)
    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    return df


# print(get_price('880301.XSHG').head())


def get_securities_margin():
    """
    融资融券信息
    :return:
    """
    pass
