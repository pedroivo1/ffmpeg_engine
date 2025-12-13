from pympeg.interfaces import Options
from pympeg.constants import IMAGE_FORMATS, IMAGE_CODECS, IMAGE_SIZES, IMAGE_PIX_FMTS
from pympeg.descriptors import (
    ChoiceOption, 
    IntOption, 
    FloatOption, 
    VideoSizeOption
)

class OutputImageOptions(Options):

    format: str | None
    codec: str | None
    qscale: float | int | None
    frames: int | None
    framerate: float | int | None
    size: str | None
    pixel_format: str | None
    compression_level: int | None
    crf: int | None


    format = ChoiceOption(flag='-f', choices=IMAGE_FORMATS)
    codec = ChoiceOption(flag='-c:v', choices=IMAGE_CODECS)
    qscale = FloatOption(flag='-qscale:v', min_val=0)
    frames = IntOption(flag='-frames:v', min_val=1)
    framerate = FloatOption(flag='-r', min_val=0.00001)
    size = VideoSizeOption(flag='-s', valid_sizes=IMAGE_SIZES)
    pixel_format = ChoiceOption(flag='-pix_fmt', choices=IMAGE_PIX_FMTS)
    compression_level = IntOption(flag='-compression_level', min_val=0, max_val=100)
    crf = IntOption(flag='-crf', min_val=0, max_val=51)
