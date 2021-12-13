import sys

from upact.platforms.darwin import Darwin
from upact.platforms.linux import Linux


sys.modules[__name__] = {
        'Darwin': Darwin(),
        'Linux': Linux()
}
