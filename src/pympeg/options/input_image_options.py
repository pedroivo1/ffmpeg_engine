from pympeg.interfaces import Options
from pympeg.descriptors import ChoiceOption, TimeOption, IntOption, FloatOption

class InputImageOptions(Options):
    
    FORMAT_VALUES = {
        'image2', 'image2pipe', 'png', 'gif', 'bmp', 'tiff', 'jpeg',
        'webp', 'avif', 'v4l2', 'dshow', 'mjpeg'
    }
    
    format: str | None
    start_time: str | None
    loop: int | None
    framerate: int | float | None

    format = ChoiceOption(flag='-f', choices=FORMAT_VALUES)
    start_time = TimeOption(flag='-ss')
    loop = IntOption(flag='-loop', min_val=-1, max_val=1)
    framerate = FloatOption(flag='-framerate', min_val=0.00001)
