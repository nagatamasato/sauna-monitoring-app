def get_datetime():

    from datetime import datetime

    datetime = datetime.now()
    datetime = str(datetime).replace(" ", "_")
    datetime = str(datetime).replace(":", "")
    datetime = str(datetime).replace(".", "")

    return datetime
