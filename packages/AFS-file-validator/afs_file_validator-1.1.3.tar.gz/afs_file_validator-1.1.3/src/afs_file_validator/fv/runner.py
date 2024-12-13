import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from tqdm import tqdm

from .files import FileInfo


class Runner:
    def __init__(self, path: Path, cert_name, cert_num, except_cert_name_list):
        self.path = path
        self.suffix_list = ["*.exe", "*.dll"]
        self.test_file_list = []
        self.cert_name = cert_name
        self.cert_num = cert_num
        self.except_cert_name_list = except_cert_name_list

    def run_file(self, filepath):
        file = FileInfo(filepath)
        if not file.cert_info[0]:
            return file.cert_info[1]
        else:
            # except_cert_name_list = ["hitpaw", ]
            for except_cert in self.except_cert_name_list:
                if except_cert in str(file.cert_info[0]).lower():
                    return f"WARNING: {filepath} 签名错误---{file.cert_info[0]}"
            else:
                if self.cert_name in str(file.cert_info[0]).lower():
                    if file.cert_num != self.cert_num:
                        return f"WARNING: {filepath} 签名校验失败---签名数量:{file.cert_num}"

    def run_dir(self):
        results = []
        for suffix in self.suffix_list:
            for file in self.path.rglob(suffix):
                self.test_file_list.append(file)
        with ProcessPoolExecutor(max_workers=6) as executor:
            tasks = {
                executor.submit(self.run_file, test_file): test_file
                for test_file in self.test_file_list
            }
            with tqdm(total=len(tasks), desc="测试进度") as pbar:
                for future in as_completed(tasks):
                    pbar.update(1)
                    results.append(future.result())
        print_result = [item for item in results if item]
        print(f"测试结果*失败:{len(print_result)}".center(60, "*"))
        for result in print_result:
            print(result)
        return print_result

    def run(self):
        ret = None
        time1 = time.time()
        if not str(self.path).startswith("\\"):
            if not self.path.exists():
                print(f"{self.path}，路径不存在！！！")
                return
        if self.path.is_file():
            if self.path.suffix.lower() in [".dll", ".exe"]:
                print_result = self.run_file(self.path)
                num = 1 if print_result else 0
                print(f"测试结果*失败:{num}".center(60, "*"))
                if print_result:
                    print(print_result)
                    ret = print_result
        else:
            print_result = self.run_dir()
            ret = print_result
        total_time = time.time() - time1
        total_file = len(self.test_file_list)
        result = "签名测试完成！共测试%d个文件!用时%.2fs!" % (
            total_file if total_file else 1,
            total_time,
        )
        print(result)
        print("*" * 65)
        return ret
