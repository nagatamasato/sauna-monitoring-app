from datetime import datetime
import os


class LogManager:


    def create_folder(app):
        
        folder_path = "..\\" + app + "\\logs"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

    
    def create_path(app):

        LogManager.create_folder(app)

        now_time = datetime.now()
        date_str = str(now_time).split()[0]
        time_str = str(now_time).split()[1].split('.')[0]
        path_number = time_str.split(':')[0] + time_str.split(':')[1][0]
        path_str = date_str + "_" + path_number
        file = path_str + "_" + app + ".log"
        path = ".\\logs\\" + file

        return path
