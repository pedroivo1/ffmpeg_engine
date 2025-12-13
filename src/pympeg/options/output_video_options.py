from pympeg.interfaces import Options
from pympeg.constants import VIDEO_FORMATS, VIDEO_CODECS, VIDEO_SIZES, VIDEO_PIX_FMTS, VIDEO_PRESETS, VIDEO_MOVFLAGS, VIDEO_TUNES
from pympeg.descriptors import (
    ChoiceOption, 
    TimeOption, 
    IntOption, 
    FloatOption,
    VideoSizeOption,
    BitrateOption,
    DictOption
)

class OutputVideoOptions(Options):

    # VALID_FORMATS = {
    #     'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'mpeg', '3gp', 
    #     'ts', 'ogv', 'asf', 'wmv', 'gif', 'matroska', 'm4v'
    # }
    # CODECS = {
    #     'libx264', 'h264', 'libx265', 'hevc', 'vp9', 'libvpx-vp9', 
    #     'vp8', 'libvpx', 'mpeg4', 'mpeg2video', 'prores', 'dnxhd', 
    #     'ffv1', 'copy', 'mjpeg', 'h264_nvenc', 'hevc_nvenc', 
    #     'av1', 'libaom-av1'
    # }
    # VALID_PIX_FMTS = {
    #     'yuv420p', 'yuv422p', 'yuv444p', 'rgb24', 'bgr24', 
    #     'rgba', 'bgra', 'gray', 'monow', 'monob', 
    #     'yuyv422', 'nv12', 'nv21', 'p010le', 'p010be'
    # }
    # VALID_SIZES = {
    #     'sqcif', 'qcif', 'cif', '4cif', '16cif', 'qqvga', 'qvga', 'vga', 
    #     'svga', 'xga', 'uxga', 'qxga', 'sxga', 'qsxga', 'qzxga', 'wsxga', 
    #     'wuxga', 'woxga', 'wqsxga', 'wquxga', 'whsxfga', 'hsxga', 'cga', 
    #     'ega', 'hd480', 'hd720', 'hd1080', 'uhd2160', '8k', 'ntsc', 'pal', 
    #     'qntsc', 'qpal', 'sntsc', 'spal', 'film', 'ntsc-film', '2k', 
    #     '2kflat', '2kscope', '4k', '4kflat', '4kscope'
    # }


    format: str | None
    codec: str | None
    bitrate: int | None
    fps: float | int | None
    size: str | None
    pixel_format: str | None
    qscale: float | int | None
    duration: str | None
    preset: str | None
    crf: int | None
    metadata: dict[str, str] | None
    movflags: str | None
    tune: str | None

    format = ChoiceOption(flag='-f', choices=VIDEO_FORMATS)
    codec = ChoiceOption(flag='-c:v', choices=VIDEO_CODECS)
    bitrate = BitrateOption(flag='-b:v')
    fps = FloatOption(flag='-r', min_val=0.00001)
    size = VideoSizeOption(flag='-s', valid_sizes=VIDEO_SIZES)
    pixel_format = ChoiceOption(flag='-pix_fmt', choices=VIDEO_PIX_FMTS)
    qscale = FloatOption(flag='-qscale:v', min_val=0)
    duration = TimeOption(flag='-t')
    preset = ChoiceOption(flag='-preset', choices=VIDEO_PRESETS)
    crf = IntOption(flag='-crf', min_val=0, max_val=51)
    metadata = DictOption(flag='-metadata')
    movflags = ChoiceOption(flag='-movflags', choices=VIDEO_MOVFLAGS)
    tune = ChoiceOption(flag='-tune', choices=VIDEO_TUNES)
