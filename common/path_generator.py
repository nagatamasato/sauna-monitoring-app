from datetime import datetime
import os


class PathGenerator:

    def __init__(self, job_name):
        
        self.job_name = job_name
        self.__LOG_FOLDER = ".\\logs"
        self.__child_log_folder = ""
        self.__APP_LOGS_DIR = '..\\app_logs'


    def create_folder(self):

        if not os.path.exists(self.__LOG_FOLDER):
            os.makedirs(self.__LOG_FOLDER)
        
        if not os.path.exists(self.__child_log_folder):
            os.makedirs(self.__child_log_folder)

        if not os.path.exists(self.__APP_LOGS_DIR):
            os.makedirs(self.__APP_LOGS_DIR)


    def create_path(self):
        
        now_time = datetime.now()
        date_str = str(now_time).split()[0].replace("-", "")
        path_date = date_str + "_"
        file = path_date + self.job_name + "_log.csv"
        log_folder_name = str(now_time).split()[0].split('-')[0] + str(now_time).split()[0].split('-')[1]
        self.__child_log_folder = self.__LOG_FOLDER + "\\" + log_folder_name
        path = self.__LOG_FOLDER + "\\" + log_folder_name + "\\" + file
            
        self.create_folder()

        print("job_name", self.job_name)
        print("path", path)

        return path
