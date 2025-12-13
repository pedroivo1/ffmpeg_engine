from pympeg.interfaces import Options
from pympeg.descriptors import (
    ChoiceOption, 
    TimeOption, 
    FloatOption, 
    IntOption,
    VideoSizeOption
)

class InputVideoOptions(Options):

    VALID_FORMATS = {
        'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'mpeg', '3gp', 
        'ts', 'ogv', 'asf', 'wmv', 'rawvideo', 'yuv4mpegpipe'
    }
    VALID_CODECS = {
        'libx264', 'h264', 'libx265', 'hevc', 'vp9', 'vp8', 'mpeg4', 
        'mpeg2video', 'prores', 'dnxhd', 'ffv1', 'rawvideo', 'copy', 'mjpeg'
    }
    VALID_PIX_FMTS = {
        'yuv420p', 'yuv422p', 'yuv444p', 'rgb24', 'bgr24', 
        'gray', 'monow', 'monob', 'yuyv422'
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
    start_time: str | None
    duration: str | None
    fps: float | int | None
    size: str | None
    pixel_format: str | None
    stream_loop: int | None

    format = ChoiceOption(flag='-f', choices=VALID_FORMATS)
    codec = ChoiceOption(flag='-c:v', choices=VALID_CODECS)
    start_time = TimeOption(flag='-ss')
    duration = TimeOption(flag='-t')
    fps = FloatOption(flag='-r', min_val=0.00001)
    size = VideoSizeOption(flag='-s', valid_sizes=VALID_SIZES)
    pixel_format = ChoiceOption(flag='-pix_fmt', choices=VALID_PIX_FMTS)
    stream_loop = IntOption(flag='-stream_loop', min_val=-1)
