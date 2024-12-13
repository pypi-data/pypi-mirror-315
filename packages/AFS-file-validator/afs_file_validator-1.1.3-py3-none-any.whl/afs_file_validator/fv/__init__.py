"""FV module"""

import multiprocessing
import winreg
from pathlib import Path

from .runner import Runner

hitpaw_params = {
    "cert_name": "hitpaw",
    "cert_num": 2,
    "except_cert_name_list": ["tenorshare", "afirstsoft"],
}
tenorshare_params = {
    "cert_name": "tenorshare",
    "cert_num": 1,
    "except_cert_name_list": ["hitpaw", "afirstsoft"],
}
afirstsoft_params = {
    "cert_name": "afirstsoft",
    "cert_num": 1,
    "except_cert_name_list": ["hitpaw", "tenorshare"],
}


def set_eula_accepted(tool_name="Sigcheck"):
    """
    设置 Sysinternals 工具的 EulaAccepted 注册表项为1，表示已接受许可协议。
    :param tool_name: Sysinternals 工具名称，默认为 "Sigcheck"
    """
    # 定义注册表路径和键名
    registry_path = rf"Software\Sysinternals\{tool_name}"
    eula_key_name = "EulaAccepted"
    eula_value = 1

    try:
        # 尝试打开注册表项
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_ALL_ACCESS
        )
    except FileNotFoundError:
        # 如果注册表项不存在，则创建它
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path)

    try:
        # 尝试获取 EulaAccepted 的值
        existing_value, _ = winreg.QueryValueEx(key, eula_key_name)
        if existing_value == eula_value:
            # print(f"{tool_name} EULA already accepted.")
            return
    except FileNotFoundError:
        pass  # 如果 EulaAccepted 不存在，则继续设置

    # 设置 EulaAccepted 值为 1
    winreg.SetValueEx(key, eula_key_name, 0, winreg.REG_DWORD, eula_value)
    winreg.CloseKey(key)
    # print(f"{tool_name} EULA accepted via registry.")


def scan_file_dir(file_dir, cert_name, cert_num, except_cert_name_list):
    """
    扫描测试文件夹
    :param file_dir: 文件夹
    :param cert_name: 证书名字
    :param cert_num: 证书数量
    :param except_cert_name_list: 排除证书名字列表
    :return: 签名失败列表
    """
    set_eula_accepted()
    multiprocessing.freeze_support()
    test_path = Path(file_dir)
    ret = Runner(test_path, cert_name, cert_num, except_cert_name_list).run()
    return ret
