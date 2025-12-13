from pympeg.interfaces import Options
from pympeg.constants import IMAGE_FORMATS
from pympeg.descriptors import ChoiceOption, TimeOption, IntOption, FloatOption

class InputImageOptions(Options):
    
    format: str | None
    start_time: str | None
    loop: int | None
    framerate: int | float | None

    format = ChoiceOption(flag='-f', choices=IMAGE_FORMATS)
    start_time = TimeOption(flag='-ss')
    loop = IntOption(flag='-loop', min_val=-1, max_val=1)
    framerate = FloatOption(flag='-framerate', min_val=0.00001)
