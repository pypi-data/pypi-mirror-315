# AFS_File_Validator
```python
# 使用方法
from afs_file_validator import fv

res = fv.scan_file_dir(r"D:\AutoTest\install_path\version_com", **fv.hitpaw_params)
print(res)
assert len(res) == 0
```