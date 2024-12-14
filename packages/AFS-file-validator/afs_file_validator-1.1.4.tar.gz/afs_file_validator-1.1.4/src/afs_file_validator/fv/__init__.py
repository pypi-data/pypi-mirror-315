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


def _set_eula_accepted(tool_name="Sigcheck"):
    """
    设置 Sigcheck 工具的 EulaAccepted 注册表项为1，表示已接受许可协议
    """
    registry_path = rf"Software\Sysinternals\{tool_name}"
    eula_key_name = "EulaAccepted"
    eula_value = 1

    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER, registry_path, 0, winreg.KEY_ALL_ACCESS
        )
    except FileNotFoundError:
        key = winreg.CreateKey(winreg.HKEY_CURRENT_USER, registry_path)
    try:
        existing_value, _ = winreg.QueryValueEx(key, eula_key_name)
        if existing_value == eula_value:
            # print(f"{tool_name} EULA already accepted.")
            return
    except FileNotFoundError:
        pass
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
    _set_eula_accepted()
    multiprocessing.freeze_support()
    test_path = Path(file_dir)
    ret = Runner(test_path, cert_name, cert_num, except_cert_name_list).run()
    return ret
