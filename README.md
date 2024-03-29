# CBPi4 Grouped Sensor Plugin

## Features
- This plugin allows to group up to 8 sensors into one sensor
- Supported modes are Average, Min and Max value of the sensors

## Use case
This Plugin will become handy if you have multiple sensors in your kettle and want to use their average/min/max value.

### Installation:

You can install it directly via pypi.org:	
- sudo pip3 install cbpi4_GroupedSensor 

Alternativeley you can install (or clone) it from the GIT Repo. In case of updates, you will find them here first:
- sudo pip3 install https://github.com/PiBrewing/cbpi4_GroupedSensor/archive/main.zip

Changelog:

- 10.03.23: (0.0.4) Transferred to new org and updated readme
- 20.07.22: (0.0.3) Fixed property issues (Actor <-> Sensor)
- 12.07.22: (0.0.2) Added min/max function (Contributed by Bernd Helm)
- 11.06.22: (0.0.1) Initial commit