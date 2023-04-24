import os
import re
import shutil

class Rotator:


    def rotate():

        # monitor

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

        # 再度log_dirsの数をカウントして繰り返す



        # alert

        # ..\\alert\\alert-log.csvのファイルサイズをチェック
        
        
        # サイズがしきい値を超えていたらログ保存用ファイルの存在チェック → 削除


        # alert-log.csvをログ保存用ファイル名に変更
