__author__ = 'wanderknight'
__time__ = '2018/6/9 21:07'
from tdx import industry_hy

"""601118.XSHG', '002772.XSHE"""


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
    pass


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


def get_price():
    """
    获取指定合约或合约列表的历史行情（包含起止日期，日线或分钟线），不能在’handle_bar’函数中进行调用。
    ('000001.XSHE', start_date='2015-04-01', end_date='2015-04-12')
    :return:
    """
    pass


def get_securities_margin():
    """
    融资融券信息
    :return:
    """
    pass
