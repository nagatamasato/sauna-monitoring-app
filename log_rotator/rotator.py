import os
import re
import shutil
from datetime import datetime

class Rotator:

    # monitor
    def rotate_monitor_log():
        # ディレクトリと条件を指定
        folder_path = "..\\monitor\\logs"
        pattern = r"^2[01][0-9]{2}[01][0-9][0-3][0-9]"
        log_dirs = []
        # ログフォルダを数える
        for i in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, i)) and re.search(pattern, i):
                log_dirs.append(i)
            print("file", i)
        # 結果を表示
        print("monitorのログフォルダの数: ", len(log_dirs))
        print("log_dirs", log_dirs)

        if len(log_dirs) > 3:
            oldest_dir = min(log_dirs)
            try: 
                shutil.rmtree(folder_path + "\\" + oldest_dir)
                print("Folder removed successfully")
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

            print("oldest_dir", oldest_dir)
            print(type(oldest_dir))


    # alert
    def rotate_alert_log():
        # しきい値を10MBに設定する
        # threshold = 10 * 1024 * 1024
        # テスト用の設定値
        threshold = 16
        folder_path = "..\\alert\\logs"
        file_name = "alert-log.csv"
        # ファイルの相対パスを取得する
        file_path = os.path.join(folder_path, file_name)
        # ファイルサイズを取得する
        if os.path.exists(file_path):
            file_size = os.path.getsize(file_path)
            print("file_size", file_size)

            # ファイルサイズがしきい値を超えた場合、ファイル名を変更する
            if (file_size > threshold):
                suffix = str(datetime.now()).split(".")[0]
                suffix = suffix.replace("-", "")
                suffix = suffix.replace(":", "")
                suffix = suffix.replace(" ", "")
                print(suffix)
                new_file_name = file_name.split('.')[0] + "_" + suffix + "." + file_name.split('.')[1]
                new_file_path = os.path.join(folder_path, new_file_name)
                os.rename(file_path, new_file_path)
                print(f"{file_name} has been renamed to {new_file_name}")

        pattern = r"^alert-log_2[01][0-9]{2}[01][0-9][0-3][0-9][0-2][0-9]([0-5][0-9]){2}\.csv$"
        log_files = []
        # ログファイルを数える
        for i in os.listdir(folder_path):
            if os.path.isfile(os.path.join(folder_path, i)) and re.search(pattern, i):
                log_files.append(i)
            print("file", i)

        # 結果を表示
        print("alertのログファイルの数: ", len(log_files))
        print("log_files", log_files)

        if len(log_files) > 3:
            oldest_file = min(log_files)
            try: 
                os.remove(folder_path + "\\" + oldest_file)
                print(f"{oldest_file} was deleted.")
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))

            print("oldest_file", oldest_file)
