import psutil
import logging
import datetime

logging.basicConfig(filename='low_energy_mode.log', level=logging.INFO)


class NoBatteryError(Exception):
    pass


def check_battery_level():
    battery = psutil.sensors_battery()
    if battery:
        battery_state = {"plugged_in": battery.power_plugged, "percent": battery.percent}
        return battery_state
    else:
        logging.error(f"{datetime.datetime.now()} Unable to get battery information")
        raise NoBatteryError("Cannot get battery information")
