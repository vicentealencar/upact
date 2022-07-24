import sys

from upact.platforms.darwin import Darwin
from upact.platforms.linux import Linux
from upact.platforms.windows import Windows


sys.modules[__name__] = {
        'Darwin': Darwin(),
        'Linux': Linux(),
        'Windows': Windows()
}
