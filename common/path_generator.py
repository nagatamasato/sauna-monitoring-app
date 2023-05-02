from datetime import datetime
import os


class PathGenerator:

    def __init__(self, job):
        self.job = job
        self.__child_folder_path = ""


    def create_folder(self):

        job = self.job
        folder_path = "..\\" + job + "\\logs"
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        
        if (job == 'monitor' or 'monitor_2'):
            if not os.path.exists(self.__child_folder_path):
                os.makedirs(self.__child_folder_path)
    
    
    def create_path(self):
        
        job = self.job
        if (job == 'monitor' or 'monitor_2'):
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

        file = path_date + job + "_log.csv"
        print("path_date", path_date)
        print("file", file)

        if (job == 'monitor' or 'monitor_2'):
            path = ".\\logs\\" + date_str + "\\" + file
            self.__child_folder_path = "..\\" + job + "\\logs\\" + date_str
        else:
            path = ".\\logs\\" + file
            
        self.create_folder()

        print("path", path)

        return path
