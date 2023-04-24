from datetime import datetime
import os


class LogManager:

    __app_name = ""
    __child_folder_path = ""


    def create_folder():

        app = LogManager.__app_name
        folder_path = "..\\" + app + "\\logs"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        if (app == 'monitor'):
            if not os.path.exists(LogManager.__child_folder_path):
                os.makedirs(LogManager.__child_folder_path)
    
    
    def create_path(app):
        
        LogManager.__app_name = app

        if (app == 'monitor'):
            now_time = datetime.now()
            date_str = str(now_time).split()[0].replace("-", "")
            time_str = str(now_time).split()[1].split('.')[0]
            path_number = time_str.split(':')[0] + time_str.split(':')[1][0]
            path_date = date_str + "_" + path_number + "_"
            print("now_time", now_time)
            print("date_str", date_str)
            print("time_str", time_str)
            print("path_number", path_number)
        else:
            path_date = ""

        file = path_date + app + "-log.csv"
        print("path_date", path_date)
        print("file", file)

        if (app == 'monitor'):
            path = ".\\logs\\" + date_str + "\\" + file
            LogManager.__child_folder_path = "..\\" + app + "\\logs\\" + date_str
        else:
            path = ".\\logs\\" + file
            
        LogManager.create_folder()

        print("path", path)

        return path
