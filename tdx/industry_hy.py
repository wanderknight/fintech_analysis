__author__ = 'wanderknight'
__time__ = '2018/5/24 13:03'
"""
all stock id is as SH#600000. block id as too.
hy code is T000000, 2 number means level 1, 4 number means level 2, and six number means level 3.
"""

incon_dat_path = 'E:\\fintech_data\\from_tdx\\incon.dat'
tdxzs_cfg_path = 'E:\\fintech_data\\from_tdx\\tdxzs.cfg'
tdxhy_cfg_path = 'E:\\fintech_data\\from_tdx\\tdxhy.cfg'


def _return_tdxhy_cfg_file_generator():
    """
    作为文件和使用间的隔离，便于日后增加其他检查
    文件格式如下：
    0|000001|T1001|440101
    0|000002|T110201|430101
    0 is sh
    1 is sz
    :return: file.lines
    """
    with open(tdxhy_cfg_path) as f:
        for line in f.readlines():
            yield line


def _return_tdxzs_cfg_file_generator():
    """
    煤炭开采|880302|2|1|1|T010101
    焦炭加工|880303|2|1|1|T010102
    :return: file.lines
    """
    with open(tdxzs_cfg_path) as f:
        for line in f.readlines():
            yield line


def get_stock_list(return_tdxhy_cfg_file_generator=_return_tdxhy_cfg_file_generator):
    """
    从tdxhy中读出所有沪深股票代码，并根据0、1，分别编写为SZ和SH，示例为：SZ#000001
    :param return_tdxhy_cfg_file_generator: tdxhy.cfg文件路径
    :return:SZ#000001类似的list 总计3680
    """
    stocks_list = []
    for line in return_tdxhy_cfg_file_generator():
        line_list = line.strip().split('|')
        if line_list[0] == '0':
            # stocks_list.append('SZ#' + line_list[1])
            stocks_list.append(line_list[1] + '.XSHE')
        if line_list[0] == '1':
            # stocks_list.append('SH#' + line_list[1])
            stocks_list.append(line_list[1] + '.XSHG')
    # print(stock_list.__len__())
    # print(stocks_list[2000])
    return stocks_list


# print(len(get_stock_list(_return_tdxhy_cfg_file_generator)))


def get_industry_classified_list_by_level(level=1, return_tdxzs_cfg_file_generator=_return_tdxzs_cfg_file_generator):
    """

    :param return_tdxzs_cfg_file_generator:
    :param level: 1,2,3 for T01,T0102,T010203
    :return:industry hy list
    """
    hy_list = []
    # incon_hy_list = neo4j_handle.return_hy_def(incon_dat_path, 'TDXNHY')  # 二维列表
    # for ele in incon_hy_list:
    #     if level == 1:
    #         if len(ele[0]) == 3:
    #             hy_list.append(ele)
    #     if level == 2:
    #         if len(ele[0]) == 5:
    #             hy_list.append(ele)
    #     if level == 3:
    #         if len(ele[0]) == 7:
    #             hy_list.append(ele)

    for line in return_tdxzs_cfg_file_generator():
        line_list = line.strip().split('|')
        if level == 1:
            if len(line_list[-1]) == 3 and line_list[-1].startswith('T'):
                hy_list.append(line_list[1])
        if level == 2:
            if len(line_list[-1]) == 5 and line_list[-1].startswith('T'):
                hy_list.append(line_list[1])
        if level == 3:
            if len(line_list[-1]) == 7 and line_list[-1].startswith('T'):
                hy_list.append(line_list[1])
    # print(len(hy_list))
    return hy_list


# print(get_industry_classified_list_by_level(_return_tdxzs_cfg_file_generator, 2))

def get_level_hyblock_by_stock(stock, level=2, return_tdxhy_cfg_file_generator=_return_tdxhy_cfg_file_generator):
    """

    :param return_tdxhy_cfg_file_generator:
    :param stock: 'sz#000001'
    :param level: todo, temp no use
    :return:
    """
    exchange_flag = '0' if stock.split('#')[0] == 'sz' else '1'
    for line in return_tdxhy_cfg_file_generator():
        print(exchange_flag, line.split('|')[1])
        if line.split('|')[0] == exchange_flag and line.split('|')[1] == stock.split('#')[1]:
            return line.split('|')[2]


# print(get_level_hyblock_by_stock('sz#000001', 1, _return_tdxhy_cfg_file_generator))


def get_stocks_by_hyblock(industry_code, return_tdxhy_cfg_file_generator=_return_tdxhy_cfg_file_generator):
    """
    通过通达信行业代码获得行业股票
    :param industry_code:
    :param return_tdxhy_cfg_file_generator:
    :todo 退市的股票包括在返回结果中
    :return:
    """
    stocks_list = []
    for line in return_tdxhy_cfg_file_generator():
        line_list = line.strip().split('|')
        if industry_code in line_list[2]:
            if line_list[0] == '0':
                stocks_list.append(line_list[1] + '.XSHE')
            if line_list[0] == '1':
                stocks_list.append(line_list[1] + '.XSHG')
    return stocks_list

# print(len(get_stocks_by_hyblock('T0305')))
