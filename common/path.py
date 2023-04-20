from datetime import datetime


class CreatePath:
        
    def create_path(arg):

        now_time = datetime.now()
        print("path date", now_time)
        date_str = str(now_time).split()[0]
        time_str = str(now_time).split()[1].split('.')[0]
        path_number = time_str.split(':')[0] + time_str.split(':')[1][0]
        path_str = date_str + "_" + path_number
        print("date_str", date_str)
        print("time_str", time_str)
        print("path_number", path_number)
        print("path", path_str)
        file = path_str + "_" + arg + ".log"
        path = ".\\logs\\" + file

        return path
    