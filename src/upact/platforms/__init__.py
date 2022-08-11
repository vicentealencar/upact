import logging
import platform

from upact.platforms.darwin import Darwin
from upact.platforms.linux import Linux
from upact.platforms.windows import Windows

def current_platform(config):

    logging.basicConfig(
        format='%(asctime)s %(levelname)-8s %(message)s',
        level=logging.INFO,
        datefmt='%Y-%m-%d %H:%M:%S')

    available_platforms = {
            'Darwin': Darwin(config),
            'Linux': Linux(config),
            'Windows': Windows(config)
    }

    return available_platforms[platform.system()]
