__author__ = 'wanderknight'
__time__ = '2018/6/9 21:07'

"""
1.将通达信下载的数据导出到个人的数据目录中，切记使用前配置cfg文件中的目录。
  通达信中导出数据操作步骤：
  系统->数据导出(short key:34)->高级导出->设置导出目录->文件名:不修改->前复权->生成导出头部’选中‘->分隔格式’,‘->添加品种。
2.外部调用执行tdx.tdx_data_process.init_import_k_data()函数。
"""
import tdx.tdx_data_process
import tdx.tdx_data_config_parser

all__ = ['tdx_data_process']
tdx.tdx_data_config_parser.config_read()
tdx.tdx_data_process.get_status()
# tdx.tdx_data_process.init_import_k_data()  # todo, if run ,cancle the annotation

