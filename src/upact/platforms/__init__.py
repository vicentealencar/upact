import sys

from upact.platforms.darwin import Darwin


sys.modules[__name__] = {
        'Darwin': Darwin()
}
