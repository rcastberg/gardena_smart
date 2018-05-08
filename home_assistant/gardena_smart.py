import logging
from datetime import timedelta
import json

import voluptuous as vol

from homeassistant.helpers.entity import Entity
import homeassistant.util as util
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_USERNAME, CONF_PASSWORD
import homeassistant.helpers.config_validation as cv

from deps.gardena_smart import *

#REQUIREMENTS = ['gardena_smart']


_LOGGER = logging.getLogger(__name__)

CONF_device_id = 'device_id'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_USERNAME): cv.string,
    vol.Required(CONF_PASSWORD): cv.string,
    vol.Optional(CONF_ID): cv.string
})

SCAN_INTERVAL = timedelta(seconds=300)
MIN_TIME_BETWEEN_SCANS = timedelta(seconds=600)
MIN_TIME_BETWEEN_FORCED_SCANS = timedelta(seconds=120)

def setup_platform(hass, config, add_devices, discovery_info=None):
    """Setup the sensor platform."""
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    device_id = config.get(CONF_ID)
    add_devices([gardena_smart(username, password, device_id)])


class gardena_smart(Entity):
    """Representation of a Sensor."""

    def __init__(self, username, password, device_id):
        """Initialize the sensor."""
        _LOGGER.debug('Initializing...')
        self.gardena = gardena(email_address=username, password=password)
        #Use first location
        self.devices = gardena.get_devices(locationID=gardena.locations[0][0])
        self.device_id = device_id
        self._state = None
        self._attributes = []
        self.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._attributes['name']

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return ''

    @util.Throttle(MIN_TIME_BETWEEN_SCANS, MIN_TIME_BETWEEN_FORCED_SCANS)
    def update(self):
        """Fetch new state data for the sensor.
        This is the only method that should fetch new data for Home Assistant.
        """
        _LOGGER.debug('Returning current state...')
        if self.device_id is not None:
            mower_info = gardena.get_mower_info(self.device_id)
        else:
            mower_info = gardena.get_mower_info(gardena.get_devices_in_catagory('mower')[0])
        _LOGGER.debug('State: ' + str(mower_info))
        self._state = json.dumps(mower_info)
        self._attributes = mower_info

    @property
    def state_attributes(self):
        """Return the attributes of the entity.

           Provide the parsed JSON data (if any).
        """

        return self._attributes
