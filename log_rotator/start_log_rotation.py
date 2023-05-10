from datetime import datetime
from rotator import Rotator


start_time = datetime.now()
print("rotation_START_time", start_time)

rotator = Rotator()
rotator.monitor_log_rotation()
rotator.alert_log_rotation()
rotator.log_rotator_log_rotation()
rotator.history_rotation()

end_time = datetime.now()
print("rotation_END_time", end_time)
