import os
import re
import shutil
from datetime import datetime

class Rotator:
    
    __MONITOR_LOG_PATH = ".\\logs\\monitor-log_rotator-log.csv"
    __ALERT_LOG_PATH = ".\\logs\\alert-log_rotator-log.csv"

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

        message = "No more than 3 monitor log folders."
        if len(log_dirs) > 3:
            oldest_dir = min(log_dirs)
            try: 
                shutil.rmtree(folder_path + "\\" + oldest_dir)
                message = "Monitor log folders exceeded 3. " + oldest_dir + " was deleted."
            except OSError as e:
                message = "Error: " + e.filename + " - " + e.strerror + "."
        print(message)

        with open(Rotator.__MONITOR_LOG_PATH, "a") as f:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            rotate = now + "," + message + "\n"
            f.write(rotate)

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

        message = "No more than 3 alert log files."
        if len(log_files) > 3:
            oldest_file = min(log_files)
            try: 
                os.remove(folder_path + "\\" + oldest_file)
                message = "Alert log files exceeded 3. Deleted " + oldest_file + " was deleted."
                print(message)
            except OSError as e:
                message = "Error: " + e.filename + " - " + e.strerror + "."
        print(message)

        with open(Rotator.__ALERT_LOG_PATH, "a") as f:
            now = datetime.now().strftime("%Y/%m/%d %H:%M:%S")
            rotate = now + "," + message + "\n"
            f.write(rotate)


    # log_ratator
    def rotate_log_rotator_log():
        # しきい値を10MBに設定する
        # threshold = 10 * 1024 * 1024
        # テスト用の設定値
        threshold = 64
        folder_path = "..\\log_rotator\\logs"
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
