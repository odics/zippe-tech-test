# Placeholder Python code for 'low-energy mode'
import os
import battery_info
import time
import logging
import threading
import datetime


logging.basicConfig(filename='low_energy_mode.log', level=logging.INFO)


class LowEnergyMode:
    def __init__(self):
        # Add variable to set frequency at which battery should be checked (in seconds)
        self.battery_polling_rate = 5
        # Add bool to toggle whether battery should be checked, in the event that battery polling needs to be disabled
        self.poll_battery = True
        # Set thresholds for battery levels if different action is needed based on different battery levels. Currently,
        # only the high threshold is being checked
        self.battery_thresholds = {"low": 30, "medium": 50, "high": 70}
        self.is_enabled = False
        self.gps_polling_rate = 60
        self.screen_brightness = 100

    def set_gps_polling_rate(self, rate):
        self.gps_polling_rate = rate

    def set_screen_brightness(self, brightness):
        self.screen_brightness = brightness

    def enable(self):
        # If low energy mode is enabled, reduce screen brightness and GPS polling frequency to conserve battery
        logging.info(f"{datetime.datetime.now()} Device entered low energy mode")
        self.set_screen_brightness(60)
        self.set_gps_polling_rate(20)

    def disable(self):
        # If low energy mode is disabled, reset values accordingly
        logging.info(f"{datetime.datetime.now()} Device exited low energy mode")
        self.screen_brightness = 100
        self.gps_polling_rate = 60

    def monitor_battery(self):
        # This loop runs in a separate thread and does not block execution of the remaining code
        while self.poll_battery:
            battery_state = battery_info.check_battery_level()
            # Check if device is plugged in, if it is, disable low energy mode
            if battery_state["plugged_in"]:
                if self.is_enabled:
                    self.is_enabled = False
                    self.disable()
            else:
                if battery_state["percent"] > self.battery_thresholds["high"]:
                    # If battery level rises above 70%, disable low energy mode and reset brightness and GPS polling
                    # frequency
                    self.is_enabled = False
                    self.disable()
                elif battery_state["percent"] < self.battery_thresholds["high"]:
                    # If battery level falls below high threshold, set low energy mode to enabled, and call appropriate
                    # method to reduce brightness and GPS polling frequency
                    self.is_enabled = True
                    self.enable()

            time.sleep(self.battery_polling_rate)


if __name__ == "__main__":
    monitor = LowEnergyMode()

    function_thread = threading.Thread(target=monitor.monitor_battery(), args=(monitor.battery_polling_rate,))
    function_thread.daemon = True
    function_thread.start()

    while True:
        # Do whatever else the app needs to do here
        time.sleep(1)
