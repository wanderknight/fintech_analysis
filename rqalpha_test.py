__author__ = 'wanderknight'
__time__ = '2018/6/9 20:16'

from rqalpha.api import *
config = {
"base": {
"data_bundle_path": "E:\fintech_data\rqalpha_data\bundle",
"start_date": "2016-06-01",
"end_date": "2016-12-01",
"benchmark": "000300.XSHG",
"accounts": {
"stock": 100000
}
},
"extra": {
"log_level": "verbose",
},
"mod": {
"sys_analyser": {
"enabled": True,
"plot": True
}
}
}


# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。
def init(context):
    logger.info("init")
    context.s1 = "000001.XSHE"
    update_universe(context.s1)
    # 是否已发送了order
    context.fired = False


def before_trading(context):
    pass


# 你选择的证券的数据更新将会触发此段逻辑，例如日或分钟历史数据切片或者是实时数据切片更新
def handle_bar(context, bar_dict):
    # 开始编写你的主要的算法逻辑

    # bar_dict[order_book_id] 可以拿到某个证券的bar信息
    # context.portfolio 可以拿到现在的投资组合状态信息

    # 使用order_shares(id_or_ins, amount)方法进行落单

    # TODO: 开始编写你的算法吧！
    if not context.fired:
        # order_percent并且传入1代表买入该股票并且使其占有投资组合的100%
        order_percent(context.s1, 1)
        context.fired = True

run_func(init=init, handle_bar=handle_bar, config=config)
