
# -*- coding: utf-8 -*-
#import os
#from aiohttp import web
import logging
#from unittest.mock import MagicMock, patch
import asyncio
from time import sleep
#import random
from cbpi.api import *
from cbpi.api.base import CBPiBase
from statistics import fmean

logger = logging.getLogger(__name__)


@parameters([Property.Select(label="Mode", options=['Average', 'Min', 'Max']),
            Property.Sensor(label="Sensor01", description="Select a sensor for this group."),
            Property.Sensor(label="Sensor02", description="Select a sensor for this group."),
            Property.Sensor(label="Sensor03", description="Select a sensor for this group."),
            Property.Sensor(label="Sensor04", description="Select a sensor for this group."),
            Property.Sensor(label="Sensor05", description="Select a sensor for this group."),
            Property.Sensor(label="Sensor06", description="Select a sensor for this group."),
            Property.Sensor(label="Sensor07", description="Select a sensor for this group."),
            Property.Sensor(label="Sensor08", description="Select a sensor for this group.")])

class GroupedSensor(CBPiSensor):


    def __init__(self, cbpi, id, props):
        super(GroupedSensor, self).__init__(cbpi, id, props)
        self.value = 0      
        self.sensors = []
        self.mode = self.props.get("Mode","Average")

        logging.info("GROUPED Sensor")
        if self.props.get("Sensor01", None) is not None:
            self.sensors.append(self.props.get("Sensor01"))
        if self.props.get("Sensor02", None) is not None:
            self.sensors.append(self.props.get("Sensor02"))
        if self.props.get("Sensor03", None) is not None:
            self.sensors.append(self.props.get("Sensor03"))
        if self.props.get("Sensor04", None) is not None:
            self.sensors.append(self.props.get("Sensor04"))
        if self.props.get("Sensor05", None) is not None:
            self.sensors.append(self.props.get("Sensor05"))
        if self.props.get("Sensor06", None) is not None:
            self.sensors.append(self.props.get("Sensor06"))
        if self.props.get("Sensor07", None) is not None:
            self.sensors.append(self.props.get("Sensor07"))
        if self.props.get("Sensor08", None) is not None:
            self.sensors.append(self.props.get("Sensor08"))
        pass

    def get_state(self):
        return dict(value=self.value)
   
    async def run(self):
        while self.running == True:
            values = []
            try:
                for sensor in self.sensors:
                    sensor_value = self.cbpi.sensor.get_sensor_value(sensor).get("value")
                    if sensor_value is not None:
                        values.append(float(sensor_value))
                
                if len(values) != 0:
                    if self.mode == 'Average':
                        self.value = round(fmean(values), 2)
                    elif self.mode == 'Min':
                        self.value = round(min(values), 2)
                    elif self.mode == 'Max':
                        self.value = round(max(values), 2)
                else:
                    logging.info("No values fetched from the selected child sensors, check connections and setup")

            except Exception as e:
                logging.info(e)
                pass 

            self.log_data(self.value)
            self.push_update(self.value)
            await asyncio.sleep(1)

        pass


def setup(cbpi):
    cbpi.plugin.register("Grouped Sensor", GroupedSensor)
    pass
