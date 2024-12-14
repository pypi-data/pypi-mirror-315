import os
import subprocess
import sys
from pathlib import Path

import pefile


class FileInfo:
    def __init__(self, filepath):
        self.filepath = filepath
        self.cert_num = self.get_cert_num()
        self.cert_info = self.get_certificate_info()

    @staticmethod
    def get_resource_path(relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = Path(__file__).resolve().parent
        return os.path.join(base_path, relative_path)

    def run_sigcheck(self, file_path):
        sigcheck_path = self.get_resource_path("tools/sigcheck.exe")
        result = subprocess.run(
            [str(sigcheck_path), "-nobanner", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        try:
            data = result.stdout.decode("gbk")
        except UnicodeDecodeError:
            data = result.stdout.decode("utf-8", errors="ignore")
        # print(data)
        check_res = {}
        for line in data.strip().split("\n")[1:]:
            k, v = line.split(":\t")
            check_res[k.strip()] = v.strip()
        return (
            check_res.get("Verified"),
            check_res.get("Publisher"),
            check_res.get("Signing date"),
        )

    def get_cert_num(self):
        try:
            pe = pefile.PE(self.filepath)
            size = pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size
            if size // 1000 < 12:
                cert_num = 1
            else:
                cert_num = 2
            return cert_num
        except Exception:
            return 0

    def get_certificate_info(self):
        verified, publisher, date = self.run_sigcheck(self.filepath)
        if verified == "Signed":
            return publisher, date
        elif verified == "Unsigned":
            return None, f"WARNING: {self.filepath} 签名校验失败---未签名"
        else:
            return None, f"WARNING: {self.filepath} 签名校验失败---无效签名"
