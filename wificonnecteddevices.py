import urllib.request as url
import urllib.error as urlError
import re


class WifiConnectedDevices:
    """
    Gets the connected devices on the wifi network
    """

    def __init__(self, host, user, password):
        self._host = host
        self._user = user
        self._password = password

    def getDevices(self):
        """
        Gets the devices on the network
        :return: Array of Device class
        """
        auth_handler = url.HTTPBasicAuthHandler()
        auth_handler.add_password('Broadband Router',
                                  uri=self._host,
                                  user=self._user,
                                  passwd=self._password)
        opener = url.build_opener(auth_handler)
        # ...and install it globally so it can be used with urlopen.
        url.install_opener(opener)
        try:
            f = url.urlopen(self._host)
            html = f.read().decode()
            return self.__parse(html)
        except urlError.HTTPError as e:
            return

    def __parse(self, data):
        """
        Parses out the devices from html
        :param data: Html response from the wifi router
        :return:Array of Device class
        """
        match = re.search('attach_dev = \\\'([^\']*)', data)
        if match:
            lines = match.group(1).split('<lf>')
            devices = []
            for line in lines:
                d = line.split('<br>')
                device = Device(d[0], d[1], d[2])
                devices.append(device)
            return devices
        return


class Device:
    """
    Represent a wifi connected device
    """

    def __init__(self, ip, name, mac):
        self.name = name
        self.ip = ip
        self.mac = mac

    def __str__(self):
        return str(self.ip + ' ' + self.name + ' ' + self.mac)
