from pympeg.interfaces import Options
from pympeg.descriptors import ChoiceOption, BoolOption
from pympeg.constants import LOGLEVEL_VALUES


class GlobalOptions(Options):

    overwrite: bool | None
    hide_banner: bool | None
    loglevel: str | None
    stats: bool | None

    overwrite = BoolOption(true_flag='-y', false_flag='-n')
    hide_banner = BoolOption(true_flag='-hide_banner')
    loglevel = ChoiceOption(flag='-loglevel', choices=LOGLEVEL_VALUES)
    stats = BoolOption(true_flag='-stats', false_flag='-nostats')
