"""FV module"""
import multiprocessing
from pathlib import Path

from .runner import Runner

hitpaw_params = {'cert_name': 'hitpaw', 'cert_num': 2,
                 'except_cert_name_list': ['tenorshare', 'afirstsoft']
                 }
tenorshare_params = {'cert_name': 'tenorshare', 'cert_num': 1,
                     'except_cert_name_list': ['hitpaw', 'afirstsoft']
                     }
afirstsoft_params = {'cert_name': 'afirstsoft', 'cert_num': 1,
                     'except_cert_name_list': ['hitpaw', 'tenorshare']
                     }


def scan_file_dir(file_dir, cert_name, cert_num, except_cert_name_list):
    """
    扫描测试文件夹
    :param file_dir: 文件夹
    :param cert_name: 证书名字
    :param cert_num: 证书数量
    :param except_cert_name_list: 排除证书名字列表
    :return: 签名失败列表
    """
    multiprocessing.freeze_support()
    test_path = Path(file_dir)
    ret = Runner(test_path,
                 cert_name,
                 cert_num,
                 except_cert_name_list).run()
    return ret
