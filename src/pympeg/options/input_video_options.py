from pympeg.interfaces import Options
from pympeg.constants import VIDEO_FORMATS, VIDEO_CODECS, VIDEO_SIZES, VIDEO_PIX_FMTS
from pympeg.descriptors import (
    ChoiceOption, 
    TimeOption, 
    FloatOption, 
    IntOption,
    VideoSizeOption
)

class InputVideoOptions(Options):

    format: str | None
    codec: str | None
    start_time: str | None
    duration: str | None
    fps: float | int | None
    size: str | None
    pixel_format: str | None
    stream_loop: int | None

    format = ChoiceOption(flag='-f', choices=VIDEO_FORMATS)
    codec = ChoiceOption(flag='-c:v', choices=VIDEO_CODECS)
    start_time = TimeOption(flag='-ss')
    duration = TimeOption(flag='-t')
    fps = FloatOption(flag='-r', min_val=0.00001)
    size = VideoSizeOption(flag='-s', valid_sizes=VIDEO_SIZES)
    pixel_format = ChoiceOption(flag='-pix_fmt', choices=VIDEO_PIX_FMTS)
    stream_loop = IntOption(flag='-stream_loop', min_val=-1)
