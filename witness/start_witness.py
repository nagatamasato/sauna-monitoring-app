from witness import Witness

witness = Witness()

# health check
witness.health_check('monitor_1')
witness.health_check('monitor_2')
witness.health_check('monitor_3')
witness.health_check('alert')

# check log rotation
witness.log_rotation('monitor')
witness.log_rotation('alert')

# check failure to get status
witness.sauna_error_count()
# check failure to chime
witness.chime_error_count()

# send report
witness.report()
