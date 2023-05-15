import json
import os
import re
import shutil
from datetime import datetime

class Rotator:
    
    def __init__(self):

        self.__hosts_files = [
            "..\\hosts_1.json",
            "..\\hosts_2.json",
            "..\\hosts_3.json"
        ]

    # monitor
    def app_log_rotation(self, app_name):

        print(app_name + " log_rotation START")
        # ディレクトリと条件を指定
        folder_path = "..\\" + app_name + "\\logs"
        pattern = r"^2[01][0-9]{2}[01][0-9]"
        log_dirs = []
        # ログフォルダを数える
        for i in os.listdir(folder_path):
            if os.path.isdir(os.path.join(folder_path, i)) and re.search(pattern, i):
                log_dirs.append(i)
            print("file", i)
        # 結果を表示
        print(app_name + " のログフォルダの数: " + str(len(log_dirs)))
        print("log_dirs", log_dirs)

        message = "No more than 3 " + app_name + " log folders."
        if len(log_dirs) > 3:
            oldest_dir = min(log_dirs)
            try: 
                shutil.rmtree(folder_path + "\\" + oldest_dir)
                message = app_name + " log folders exceeded 3. " + oldest_dir + " was deleted."
            except OSError as e:
                message = "Error: " + e.filename + " - " + e.strerror + "."
        print(message)

        app_log_path = ".\\logs\\" + app_name + "-log_rotator-log.csv"
        with open(app_log_path, "a") as f:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            log = now + "," + message + "\n"
            f.write(log)

        print(app_name + " log_rotation END")


    def log_rotator_log_rotation(self):

        print("log_rotator_log_rotation START")
        # しきい値を100MBに設定する
        threshold = 100 * 1024 * 1024
        # テスト用の設定値
        # threshold = 64
        folder_path = ".\\logs"
        files = [
            "monitor-log_rotator-log.csv",
            "alert-log_rotator-log.csv"
        ]
        for file in files:
            # ファイルの相対パスを取得する
            file_path = os.path.join(folder_path, file)
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
                    new_file_name = file.split('.')[0] + "_" + suffix + "." + file.split('.')[1]
                    new_file_path = os.path.join(folder_path, new_file_name)
                    os.rename(file_path, new_file_path)
                    print(f"{file} has been renamed to {new_file_name}")

            pattern = r"^" + file.split('-')[0] + "-log_rotator-log_2[01][0-9]{2}[01][0-9][0-3][0-9][0-2][0-9]([0-5][0-9]){2}\.csv$"
            log_files = []

            for i in os.listdir(folder_path):
                if os.path.isfile(os.path.join(folder_path, i)) and re.search(pattern, i):
                    log_files.append(i)
                print("file", i)

            print("Number of " + file.split('.')[0] + " files: ", len(log_files))
            print("log_files", log_files)

            message = "No more than 3 log_rotator log files."
            while len(log_files) > 3:
                oldest_file = min(log_files)
                try: 
                    os.remove(folder_path + "\\" + oldest_file)
                    log_files.remove(oldest_file)
                    message = "Alert log files exceeded 3. Deleted " + oldest_file + " was deleted."
                except OSError as e:
                    message = "Error: " + e.filename + " - " + e.strerror + "."
            print(message)

        print("log_rotator_log_rotation END")


    def history_rotation(self):

        print("history_rotation START")

        hosts_files = self.__hosts_files
        for i in range(len(hosts_files)):
            with open(hosts_files[i], "r") as jsonf:
                hosts = json.load(jsonf)

            for room in hosts.items():
                history = room[1]['history']

                if len(history) > 3:
                    for j in range(len(history) - 3):
                        oldest_date = min(history)
                        print("j", j)
                        print("oldest_date", oldest_date)
                        history.remove(oldest_date)
                        message = "History exceeded 3. " + oldest_date + " was deleted."
                        print(message)

            with open(hosts_files[i], "w") as jsonf:
                json.dump(hosts, jsonf)

        print("history_rotation END")
