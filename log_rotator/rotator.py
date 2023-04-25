import os
import re
import shutil
from datetime import datetime

class Rotator:

    # monitor
    def rotate_monitor_log():
        # ディレクトリと条件を指定
        directory = "..\\monitor\\logs"
        pattern = r"^2[01][0-9]{2}[01][0-9][0-3][0-9]"

        count = 0
        log_dirs = []

        # ディレクトリ内のフォルダを取得し、条件に一致するものを数える
        for i in os.listdir(directory):
            if os.path.isdir(os.path.join(directory, i)) and re.search(pattern, i):
                log_dirs.append(i)
                count += 1
            print("file", i)

        # 結果を表示
        print("条件に一致するフォルダの数：", count)
        print("log_dirs", log_dirs)

        if count > 3:
            oldest_dir = min(log_dirs)
            try:
                shutil.rmtree(directory + "\\" + oldest_dir)
                print("Directory removed successfully")
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

        print("oldest_dir", oldest_dir)
        print(type(oldest_dir))


    # alert
    def rotate_alert_log():
        # しきい値を10MBに設定する
        threshold = 10 * 1024 * 1024
        folder_path = "..\\alert"
        file_name = "alert-log.csv"
        # ファイルの相対パスを取得する
        file_path = os.path.join(folder_path, file_name)
        # ファイルサイズを取得する
        file_size = os.path.getsize(file_path)
        print("file_size", file_size)

        # ファイルサイズがしきい値を超えた場合、ファイル名を変更する
        if file_size > threshold:
            suffix = datetime.now()
            new_file_name = file_name + suffix
            new_file_path = os.path.join(folder_path, new_file_name)
            os.rename(file_path, new_file_path)
            print(f"{file_name} has been renamed to {new_file_name}")
