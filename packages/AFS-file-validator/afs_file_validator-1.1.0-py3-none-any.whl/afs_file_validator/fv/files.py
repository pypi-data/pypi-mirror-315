import subprocess
from pathlib import Path

import pefile


class FileInfo:
    def __init__(self, filepath):
        self.filepath = filepath
        self.cert_num = self.get_cert_num()
        self.cert_info = self.get_certificate_info()

    @staticmethod
    def run_sigcheck(file_path):
        sigcheck_path = Path(__file__).resolve().parent / 'sigcheck.exe'
        result = subprocess.run([str(sigcheck_path), file_path],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                )
        try:
            data = result.stdout.decode('gbk')
        except UnicodeDecodeError:
            data = result.stdout.decode('utf-8', errors='ignore')
        path = Path(file_path)
        info = data.split(f'{path.name}:')
        # print(info[-1])
        check_res = {}
        for line in info[-1].strip().split('\n'):
            k, v = line.split(':\t')
            check_res[k.strip()] = v.strip()
        return check_res.get('Verified'), check_res.get('Publisher'), check_res.get('Signing date')

    def get_cert_num(self):
        try:
            pe = pefile.PE(self.filepath)
            size = pe.OPTIONAL_HEADER.DATA_DIRECTORY[4].Size
            if size // 1000 < 12:
                cert_num = 1
            else:
                cert_num = 2
            return cert_num
        except:
            return 0

    def get_certificate_info(self):
        verified, publisher, date = self.run_sigcheck(self.filepath)
        if verified == 'Signed':
            return publisher, date
        elif verified == 'Unsigned':
            return None, f"WARNING: {self.filepath} 签名校验失败---未签名"
        else:
            return None, f"WARNING: {self.filepath} 签名校验失败---无效签名"
        # try:
        #     binary = lief.parse(open(self.filepath, 'rb'))
        #     d = json.loads(lief.to_json(binary))
        #     issuer = d["signatures"][0]['signer_info'][0]["issuer"]
        #     lst = d["signatures"][0]['certificates']
        #     for item in lst:
        #         if item['issuer'] == issuer:
        #             name = item['subject'].split("=")[-1]
        #             valid = item['valid_to']
        #             if name:
        #                 return name, datetime.datetime(*valid)
        #             return None, f"WARNING: {self.filepath} 签名解析失败---请手动查看"
        # except KeyError:
        #     return None, f"WARNING: {self.filepath} 签名检查失败---未签名"
        # except TypeError:
        #     return None, f"WARNING: {self.filepath} 签名解析失败---请手动查看"
