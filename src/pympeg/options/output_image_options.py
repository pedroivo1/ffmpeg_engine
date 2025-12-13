from pympeg.interfaces import Options
from pympeg.descriptors import (
    ChoiceOption, 
    IntOption, 
    FloatOption, 
    VideoSizeOption
)

class OutputImageOptions(Options):

    VALID_FORMATS = {
        'image2', 'image2pipe', 'png', 'jpeg', 'jpg', 'gif', 
        'bmp', 'tiff', 'webp', 'avif', 'heif'
    }
    VALID_CODECS = {
        'png', 'mjpeg', 'libwebp', 'av1', 'hevc', 'libx264', 
        'gif', 'bmp', 'tiff', 'copy'
    }
    VALID_PIX_FMTS = {
        'yuv420p', 'yuv422p', 'yuv444p', 'rgb24', 'bgr24', 
        'rgba', 'bgra', 'gray', 'monow', 'monob', 
        'yuyv422', 'pal8'
    }
    VALID_SIZES = {
        'sqcif', 'qcif', 'cif', '4cif', '16cif', 'qqvga', 'qvga', 'vga', 
        'svga', 'xga', 'uxga', 'qxga', 'sxga', 'qsxga', 'qzxga', 'wsxga', 
        'wuxga', 'woxga', 'wqsxga', 'wquxga', 'whsxfga', 'hsxga', 'cga', 
        'ega', 'hd480', 'hd720', 'hd1080', 'uhd2160', '8k', 'ntsc', 'pal', 
        'qntsc', 'qpal', 'sntsc', 'spal', 'film', 'ntsc-film', '2k', 
        '2kflat', '2kscope', '4k', '4kflat', '4kscope'
    }

    format: str | None
    codec: str | None
    qscale: float | int | None
    frames: int | None
    framerate: float | int | None
    size: str | None
    pixel_format: str | None
    compression_level: int | None
    crf: int | None


    format = ChoiceOption(flag='-f', choices=VALID_FORMATS)
    codec = ChoiceOption(flag='-c:v', choices=VALID_CODECS)
    qscale = FloatOption(flag='-qscale:v', min_val=0)
    frames = IntOption(flag='-frames:v', min_val=1)
    framerate = FloatOption(flag='-r', min_val=0.00001)
    size = VideoSizeOption(flag='-s', valid_sizes=VALID_SIZES)
    pixel_format = ChoiceOption(flag='-pix_fmt', choices=VALID_PIX_FMTS)
    compression_level = IntOption(flag='-compression_level', min_val=0, max_val=100)
    crf = IntOption(flag='-crf', min_val=0, max_val=51)
