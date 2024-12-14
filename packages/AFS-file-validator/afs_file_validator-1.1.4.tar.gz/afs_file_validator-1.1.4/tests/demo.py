from afs_file_validator import fv

if __name__ == "__main__":
    # res = fv.scan_file_dir("C:\Program Files (x86)\HitPaw\HitPaw Watermark Remover",**fv.hitpaw_params)
    res = fv.scan_file_dir(r"C:\Users\Administrator\Desktop\test", **fv.hitpaw_params)
    print(res)
