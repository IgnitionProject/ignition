"""
Ignition is a numerical code generator.

See README in top level for more details
"""

__version__ = "0.0.1-git"

def __ignition_debug():
    # helper function so we don't import os globally
    import os
    return eval(os.getenv('IGNITION_DEBUG', 'False'))
IGNITION_DEBUG = __ignition_debug()


from flame import *
from int_gen import *
from utils import *
