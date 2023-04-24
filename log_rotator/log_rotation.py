from datetime import datetime
from rotator import Rotator


start_time = datetime.now()
print("rotation_START_time", start_time)

Rotator.rotate()

end_time = datetime.now()
print("rotation_END_time", end_time)
