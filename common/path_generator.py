from datetime import datetime
import os


class PathGenerator:

    def __init__(self, job_name):
        self.job_name = job_name
        self.__LOG_FOLDER = ".\\logs"
        self.__child_log_folder = ""


    def create_folder(self):

        if not os.path.exists(self.__LOG_FOLDER):
            os.makedirs(self.__LOG_FOLDER)
        
        if self.job_name in [
            'monitor_1', 
            'monitor_2', 
            'monitor_3'
        ]:
            if not os.path.exists(self.__child_log_folder):
                os.makedirs(self.__child_log_folder)

    
    def create_path(self):
        
        if self.job_name in [
            'monitor_1',
            'monitor_2',
            'monitor_3'
        ]:
            now_time = datetime.now()
            date_str = str(now_time).split()[0].replace("-", "")
            # time_str = str(now_time).split()[1].split('.')[0]
            # path_number = time_str.split(':')[0] + time_str.split(':')[1][0]
            # path_date = date_str + "_" + path_number + "_"
            path_date = date_str + "_"
        else:
            path_date = ""

        file = path_date + self.job_name + "_log.csv"

        if self.job_name in [
            'monitor_1',
            'monitor_2',
            'monitor_3'
        ]:
            self.__child_log_folder = self.__LOG_FOLDER + "\\" + date_str
            path = self.__LOG_FOLDER + "\\" + date_str + "\\" + file

        else:
            path = self.__LOG_FOLDER + "\\" + file
            
        self.create_folder()

        print("job_name", self.job_name)
        print("path", path)

        return path
