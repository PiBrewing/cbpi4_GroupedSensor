
# -*- coding: utf-8 -*-
import logging
import asyncio
from cbpi.api import *
from statistics import fmean

logger = logging.getLogger("GroupedSensor")

@parameters([
            Property.Select(label="Mode", options=['Average', 'Min', 'Max']),
            Property.Sensor(label="Sensor01", description="Select an sensor for this group."),
            Property.Sensor(label="Sensor02", description="Select an sensor for this group."),
            Property.Sensor(label="Sensor03", description="Select an sensor for this group."),
            Property.Sensor(label="Sensor04", description="Select an sensor for this group."),
            Property.Sensor(label="Sensor05", description="Select an sensor for this group."),
            Property.Sensor(label="Sensor06", description="Select an sensor for this group."),
            Property.Sensor(label="Sensor07", description="Select an sensor for this group."),
            Property.Sensor(label="Sensor08", description="Select an sensor for this group.")])

class GroupedSensor(CBPiSensor):
    def __init__(self, cbpi, id, props):
        super(GroupedSensor, self).__init__(cbpi, id, props)
        self.running = True
        self.sensors = []
        self.value = 0
        self.mode = 'Average'
        self.errorReported = False

    async def start(self):
        await super().start()
        if self.props.get("Mode", None) is not None:
            self.mode = self.props.get("Mode")
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
        self.running = True
        self.errorReported = False

    async def stop(self):
        try:
            await super().stop()
            self.running = False
        except:
            pass

    async def run(self):
        while self.running is True:
            try:
                values = []
                for sensor in self.sensors:
                    sensorvalue = self.cbpi.sensor.get_sensor_value(sensor)['value']
                    if sensorvalue is not None and sensorvalue != 0:
                        values.append(self.cbpi.sensor.get_sensor_value(sensor)['value'])

                if len(values) == 0:
                    raise Exception("No values fetched from the selected child sensors, check connections and setup")

                if self.mode == 'Average':
                    self.value = round(fmean(values), 2)
                elif self.mode == 'Min':
                    self.value = round(min(values), 2)
                elif self.mode == 'Max':
                    self.value = round(max(values), 2)

                self.push_update(self.value)
                self.errorReported = False
            except Exception as e:
                if not self.errorReported:
                    logging.info(e)
                pass

            await asyncio.sleep(1)

    def get_state(self):
        return dict(value=self.value)

def setup(cbpi):
    cbpi.plugin.register("Grouped Sensor", GroupedSensor)
    pass
