from platform import system
from ..bin.baxh import baxh
from ..bin.bazh import bazh

def _command(command,arguments):
    if system() == "Windows":
        return baxh(command,arguments)
    return bazh(command,arguments)