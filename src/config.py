from configparser import ConfigParser
from os import path

ARDUINO_COM_PORT = "COM99"
ARDUINO_BAUD_RATE = 9600


def read_config_file():
    """

    :return:
    """
    global ARDUINO_COM_PORT
    global ARDUINO_BAUD_RATE
    config = ConfigParser()
    config.read('config.ini')
    ARDUINO_COM_PORT = config.get('main', 'com_port')
    ARDUINO_BAUD_RATE = config.get('main', 'baud_rate')


def init_config_file():
    """

    :return:
    """
    global ARDUINO_COM_PORT
    global ARDUINO_BAUD_RATE
    config = ConfigParser()
    config.read('config.ini')
    config.add_section('main')
    config.set('main', 'com_port', str(ARDUINO_COM_PORT))
    config.set('main', 'baud_rate', str(ARDUINO_BAUD_RATE))
    with open('config.ini', 'w') as f:
        config.write(f)
    read_config_file()


def write_config_file(com_port, baud_rate):
    """

    :param com_port:
    :param baud_rate:
    :return:
    """
    config = ConfigParser()
    config.read('config.ini')
    config.add_section('main')
    config.set('main', 'com_port', str(com_port))
    config.set('main', 'baud_rate', str(baud_rate))
    with open('config.ini', 'w') as f:
        config.write(f)
    read_config_file()


if path.exists('config.ini'):
    read_config_file()
else:
    init_config_file()
    read_config_file()
