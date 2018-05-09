import json
import requests
from datetime import datetime, timedelta
import os

class Gardena(object):
    """Class to take care of cummunication with Gardena Smart system"""
    def __init__(self, email_address=None, password=None, device_id=None):
        if email_address ==None or password==None:
            raise ValueError('Please provice, email, password')
        self.debug=True
        self.s = requests.session()
        self.email_address = email_address
        self.password = password
        self.device_id = device_id
        self.update()
    def update(self):
        self.update_authtokens()
        self.get_locations()
    def update_authtokens(self):
        """Get authentication token from servers"""
        data = '{"sessions":{"email":"' + self.email_address + '","password":"' + self.password + '"}}'
        url = 'https://smart.gardena.com/sg-1/sessions'
        headers = self.create_header()
        response = self.s.post(url, headers=headers, data=data)
        response_data = json.loads(response.content.decode('utf-8'))
        self.AuthToken = response_data['sessions']['token']
        self.refreshToken = response_data['sessions']['refresh_token']
        self.userID = response_data['sessions']['user_id']
    def get_locations(self):
        url = "https://smart.gardena.com/sg-1/locations/"
        params = (
            ('user_id', self.userID),
        )
        headers = self.create_header(Token=self.AuthToken)
        response = self.s.get(url, headers=headers, params=params)
        response_data = json.loads(response.content.decode('utf-8'))
        self.raw_locations_resp = response
        self.raw_locations = response_data
        self.locations = [(i['id'],i['name']) for i in response_data['locations']]
    def get_devices(self, locationID):
        url = "https://smart.gardena.com/sg-1/devices"
        params = (
            ('locationId', locationID),
        )
        headers = self.create_header(Token=self.AuthToken)
        response = self.s.get(url, headers=headers, params=params)
        response_data = json.loads(response.content.decode('utf-8'))
        self.raw_devices = response_data
        device_info = {}
        for i in self.raw_devices['devices']:
            device_info[i['id']]=i
        self.device_info = device_info
    def get_devices_in_catagory(self, category):
        """Return devices matching a category, should be mower, gateway, sensor """
        return [i['id'] for i in self.raw_devices['devices']  if i['category']==category]
    def get_mower_name(self, id):
        return self.device_info[id]['name']
    def get_mower_device_state(self, id):
        return self.device_info[id]['device_state']
    def get_mower_last_online(self, id):
        return self.device_info[id]['abilities'][0]['properties'][5]['value']
    def get_mower_battery_level(self, id):
        return self.device_info[id]['abilities'][1]['properties'][0]['value']
    def get_mower_charging_status(self, id):
        return self.device_info[id]['abilities'][1]['properties'][1]['value']
    def get_mower_radio_quality(self, id):
        return self.device_info[id]['abilities'][2]['properties'][0]['value']
    def get_mower_radio_status(self, id):
        return self.device_info[id]['abilities'][2]['properties'][2]['value']
    def get_mower_radio_connection_status(self, id):
        return self.device_info[id]['abilities'][2]['properties'][1]['value']
    def get_mower_manual_mode(self, id):
        return self.device_info[id]['abilities'][3]['properties'][0]['value']
    def get_mower_status(self, id):
        return self.device_info[id]['abilities'][3]['properties'][1]['value']
    def get_mower_error(self, id):
        """Return error and last ts"""
        error = self.device_info[id]['abilities'][3]['properties']
        return (error[2]['value'], error[7]['value'])
    def get_mower_last_error(self, id):
        return self.device_info[id]['abilities'][3]['properties'][3]['value']
    def get_mower_next_source_start(self, id):
        return self.device_info[id]['abilities'][3]['properties'][4]['value']
    def get_mower_next_start(self, id):
        return self.device_info[id]['abilities'][3]['properties'][5]['value']
    def get_mower_cutting_time(self, id):
        return self.device_info[id]['abilities'][4]['properties'][0]['value']
    def get_mower_charging_cycles(self, id):
        return self.device_info[id]['abilities'][4]['properties'][1]['value']
    def get_mower_collisions(self, id):
        return self.device_info[id]['abilities'][4]['properties'][2]['value']
    def get_mower_running_time(self, id):
        return self.device_info[id]['abilities'][4]['properties'][3]['value']
    def get_mower_info(self, id):
        mower_info = {}
        mower_info['name'] = self.get_mower_name(id)
        mower_info['dev_state'] = self.get_mower_device_state(id)
        mower_info['last_online'] = self.convert_python_dt(self.get_mower_last_online(id))
        mower_info['battery_level']  = self.get_mower_battery_level(id)
        mower_info['charging_satus'] = self.get_mower_charging_status(id)
        mower_info['radio_quality'] = self.get_mower_radio_quality(id)
        mower_info['radio_status'] = self.get_mower_radio_status(id)
        mower_info['radio_connection_status'] = self.get_mower_radio_connection_status(id)
        mower_info['in_manual_mode'] = self.get_mower_manual_mode(id)
        mower_info['status'] = self.get_mower_status(id)
        mower_info['error'] = self.get_mower_error(id)[0]
        mower_info['error_time'] = self.convert_python_dt(self.get_mower_error(id)[1])
        mower_info['last_error_msg'] = self.get_mower_last_error(id)
        mower_info['next_source_for_start']=self.get_mower_next_source_start(id)
        mower_info['next_start'] = self.get_mower_next_start(id)
        mower_info['cutting_time'] = self.convert_python_dt(self.get_mower_cutting_time(id))
        mower_info['charge_cycles'] = self.get_mower_charging_cycles(id)
        mower_info['collisions'] = self.get_mower_collisions(id)
        mower_info['running_time'] = self.get_mower_running_time(id)
        return mower_info
    def create_header(self, Token=None, ETag=None):
        headers={
        'Content-Type': 'application/json',
        }
        if Token is not None:
            headers['X-Session']=Token
        if ETag is not None:
            headers['If-None-Match'] = ETag
        return headers
    def convert_python_dt(dt_str):
        from dateutil import tz
        import datetime as dt
        from_zone = tz.tzutc()
        to_zone = tz.tzlocal()
        #We have two different formats:
        if len(dt_str) == 24:
            assert dt_str[-1] == 'Z'
            dt_str = dt_str[:-1] + '000UTC'
            gardena_dt = dt.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M:%S.%f%Z')
        elif len(dt_str) == 17:
            assert dt_str[-1] == 'Z'
            dt_str = dt_str[:-1] + 'UTC'
            gardena_dt = dt.datetime.strptime(dt_str, '%Y-%m-%dT%H:%M%Z')
        utc_dt = gardena_dt.replace(tzinfo=from_zone)
        local_dt = utc_dt.astimezone(to_zone)
        return local_dt
    def debug_print(self, string):
        if self.debug:
            print(string)
