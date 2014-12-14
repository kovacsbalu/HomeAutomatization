from TemperatureMonitor import TemperatureMonitor
import homeauto as ha
import time
import wificonnecteddevices
import AzureDataServices as azure
import logging
import os


def setup_log():
    logger = logging.getLogger(os.path.basename(__file__))
    logger.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter("%(asctime)s: %(message)s")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)
    file_formatter = logging.Formatter("%(asctime)s [%(name)s] [%(levelname)-5.5s]: %(message)s")
    file_handler = logging.FileHandler("presence.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    return logger


def update_presence(self):
        change = presence.get_presence_change()
        if change is not None:
            logger.info(change)
            data_service.insert_presence(change)


def update_temperature(self):
    o = tm.get_observation()
    temperature_data_service.insert_data(o)

if __name__ == '__main__':
    logger = setup_log()
    
    users = ha.init_users_from_file()
    wifi = wificonnecteddevices.WifiConnectedDevices('http://192.168.0.1/sky_attached_devices.html')
    
    data_service = azure.AzureDataServices('presence')
    data_service.create_table()

    temperature_data_service = azure.AzureDataServices('temperature')
    tm = TemperatureMonitor()
    
    presence = ha.Presence(users, wifi)
    i = 0
    while True:
        if i % 60 == 0:
            update_presence()
            update_temperature()
        i += 1
        if i >= 1000:
            i = 0
        time.sleep(10)