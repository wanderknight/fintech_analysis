__author__ = 'wanderknight'
__time__ = '2018/4/29 15:30'
"""
config文件读取，tdx相关文件的路径配置
"""
import configparser
import tdx.tdx_data_process


def config_read():
    cf = configparser.ConfigParser()
    cf.read("tdx\\tdx_data_config.cfg")
    tdx.tdx_data_process.tdx_export_path = cf.get('dir', 'tdx_export_path')
    tdx.tdx_data_process.tdx2csv_data_path = cf.get('dir', 'tdx2csv_data_path')
