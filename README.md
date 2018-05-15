# Gardena Smart mower
Python library for accessing the gardena smart system

Based on code and documentation by :
 - http://www.dxsdata.com/2016/07/php-class-for-gardena-smart-system-api/
 - http://www.roboter-forum.com/showthread.php?16777-Gardena-Smart-System-Analyse

**Implementation**
Currently only supports reading mower variables.
Only tested with my ownsetup, needs testing

**Usage:**
Basic usage, code below will grab the first mower:

    username='user@domain.com'
    password='password'
    gardena = Gardena(email_address=username, password=password)
    gardena.get_devices(locationID=gardena.locations[0][0])
    mower_info = gardena.get_mower_info(gardena.get_devices_in_catagory('mower')[0])
    
    mower_info
Output example:

    {'battery_level': 100,
     'charge_cycles': 17,
     'charging_satus': False,
     'collisions': 214,
     'cutting_time': 15,
     'dev_state': 'ok',
     'error': 'no_message',
     'error_time': datetime.datetime(1970, 1, 1, 1, 0, tzinfo=tzlocal()),
     'in_manual_mode': False,
     'last_error_msg': 'no_message',
     'last_online': datetime.datetime(2018, 5, 15, 11, 7, 22, 149000, tzinfo=tzlocal()),
     'name': 'SILENO',
     'next_source_for_start': 'week_timer',
     'next_start': datetime.datetime(2018, 5, 15, 12, 0, tzinfo=tzlocal()),
     'radio_connection_status': 'status_device_alive',
     'radio_quality': 40,
     'radio_status': 'poor',
     'running_time': 15,
     'status': 'parked_timer'}

