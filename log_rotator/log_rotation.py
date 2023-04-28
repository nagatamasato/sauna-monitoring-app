from datetime import datetime
from rotator import Rotator


start_time = datetime.now()
print("rotation_START_time", start_time)

Rotator.monitor_log_rotation()
Rotator.alert_log_rotation()
Rotator.log_rotator_log_rotation()

end_time = datetime.now()
print("rotation_END_time", end_time)
