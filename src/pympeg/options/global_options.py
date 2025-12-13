from pympeg.interfaces import Options
from pympeg.descriptors import ChoiceOption, BoolOption

class GlobalOptions(Options):

    LOGLEVEL_VALUES = {
        'quiet', 'panic', 'fatal', 'error', 'warning', 
        'info', 'verbose', 'debug', 'trace'
    }

    overwrite: bool | None
    hide_banner: bool | None
    loglevel: str | None
    stats: bool | None

    overwrite = BoolOption(true_flag='-y', false_flag='-n')
    hide_banner = BoolOption(true_flag='-hide_banner')
    loglevel = ChoiceOption(flag='-loglevel', choices=LOGLEVEL_VALUES)
    stats = BoolOption(true_flag='-stats', false_flag='-nostats')
