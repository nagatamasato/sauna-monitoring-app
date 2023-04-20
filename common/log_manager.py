from datetime import datetime
import os


class LogManager:


    def create_folder(app, child_folder_path):

        folder_path = "..\\" + app + "\\logs"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        if not os.path.exists(child_folder_path):
            os.makedirs(child_folder_path)
    
    
    def create_path(app):
        
        now_time = datetime.now()
        date_str = str(now_time).split()[0]
        time_str = str(now_time).split()[1].split('.')[0]
        path_number = time_str.split(':')[0] + time_str.split(':')[1][0]
        path_str = date_str + "_" + path_number
        file = path_str + "_" + app + ".csv"
        path = ".\\logs\\" + date_str + "\\" + file

        child_folder_path = "..\\" + app + "\\logs\\" + date_str
        LogManager.create_folder(app, child_folder_path)

        print("path", path)

        return path
