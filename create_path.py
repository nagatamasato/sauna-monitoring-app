from datetime import datetime


class CreatePath:
        
    def create_path(arg):

        now_time = datetime.now()
        now_time = str(now_time).replace(" ", "_")
        now_time = str(now_time).replace(":", "")
        now_time = str(now_time).replace(".", "")
        file = now_time + "_" + arg + ".log"
        path = ".\\logs\\" + arg + "\\" + file

        return path
    