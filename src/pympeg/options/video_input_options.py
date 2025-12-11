from datetime import timedelta
from pympeg.interfaces import Options
from pympeg.utils.validation import (
    validate_choices, time_to_string, validate_int, 
    validate_positive_number, validate_video_size
)

class VideoInputOptions(Options):

    VALID_FORMATS = {
        "mp4", "avi", "mov", "mkv", "webm", "flv", "mpeg", "3gp", 
        "ts", "ogv", "asf", "wmv", "rawvideo", "yuv4mpegpipe"
    }
    VALID_CODECS = {
        "libx264", "h264", "libx265", "hevc", "vp9", "vp8", "mpeg4", 
        "mpeg2video", "prores", "dnxhd", "ffv1", "rawvideo", "copy", "mjpeg"
    }
    VALID_PIX_FMTS = {
        "yuv420p", "yuv422p", "yuv444p", "rgb24", "bgr24", 
        "gray", "monow", "monob", "yuyv422"
    }
    VALID_SIZES = {
        "sqcif", "qcif", "cif", "4cif", "16cif", "qqvga", "qvga", "vga", 
        "svga", "xga", "uxga", "qxga", "sxga", "qsxga", "qzxga", "wsxga", 
        "wuxga", "woxga", "wqsxga", "wquxga", "whsxfga", "hsxga", "cga", 
        "ega", "hd480", "hd720", "hd1080", "uhd2160", "8k", "ntsc", "pal", 
        "qntsc", "qpal", "sntsc", "spal", "film", "ntsc-film", "2k", 
        "2kflat", "2kscope", "4k", "4kflat", "4kscope"
    }


    def __init__(
        self,
        format: str | None = None,
        codec: str | None = None,
        start_time: timedelta | float | int | None = None,
        duration: timedelta | float | int | None = None,
        fps: float | int | None = None,
        size: str | None = None,
        pixel_format: str | None = None,
        stream_loop: int | None = None,
    ) -> None:
        self._format = None
        self._codec = None
        self._start_time = None
        self._duration = None
        self._fps = None
        self._size = None
        self._pixel_format = None
        self._stream_loop = None

        if format is not None: self.format = format
        if codec is not None: self.codec = codec
        if start_time is not None: self.start_time = start_time
        if duration is not None: self.duration = duration
        if fps is not None: self.fps = fps
        if size is not None: self.size = size
        if pixel_format is not None: self.pixel_format = pixel_format
        if stream_loop is not None: self.stream_loop = stream_loop


    # ========== PROPERTY: format ==========
    @property
    def format(self) -> str | None:
        return self._format

    @format.setter
    @validate_choices(VALID_FORMATS)
    def format(self, value: str) -> None:
        self._format = value

    @format.deleter
    def format(self) -> None:
        self._format = None


    # ========== PROPERTY: codec ==========
    @property
    def codec(self) -> str | None:
        return self._codec

    @codec.setter
    @validate_choices(VALID_CODECS)
    def codec(self, value: str) -> None:
        self._codec = value

    @codec.deleter
    def codec(self) -> None:
        self._codec = None


    # ========== PROPERTY: start_time ==========
    @property
    def start_time(self) -> str | None:
        return self._start_time

    @start_time.setter
    @time_to_string()
    def start_time(self, value: str) -> None:
        self._start_time = value

    @start_time.deleter
    def start_time(self) -> None:
        self._start_time = None


    # ========== PROPERTY: duration ==========
    @property
    def duration(self) -> str | None:
        return self._duration

    @duration.setter
    @time_to_string()
    def duration(self, value: str) -> None:
        self._duration = value

    @duration.deleter
    def duration(self) -> None:
        self._duration = None


    # ========== PROPERTY: fps ==========
    @property
    def fps(self) -> float | int | None:
        return self._fps

    @fps.setter
    @validate_positive_number()
    def fps(self, value: float | int) -> None:
        self._fps = value

    @fps.deleter
    def fps(self) -> None:
        self._fps = None


    # ========== PROPERTY: size ==========
    @property
    def size(self) -> str | None:
        return self._size

    @size.setter
    @validate_video_size(VALID_SIZES)
    def size(self, value: str) -> None:
        self._size = value

    @size.deleter
    def size(self) -> None:
        self._size = None


    # ========== PROPERTY: pixel_format ==========
    @property
    def pixel_format(self) -> str | None:
        return self._pixel_format

    @pixel_format.setter
    @validate_choices(VALID_PIX_FMTS)
    def pixel_format(self, value: str) -> None:
        self._pixel_format = value

    @pixel_format.deleter
    def pixel_format(self) -> None:
        self._pixel_format = None


    # ========== PROPERTY: stream_loop ==========
    @property
    def stream_loop(self) -> int | None:
        return self._stream_loop

    @stream_loop.setter
    @validate_int(min_value=-1)
    def stream_loop(self, value: int) -> None:
        self._stream_loop = value

    @stream_loop.deleter
    def stream_loop(self) -> None:
        self._stream_loop = None


    # ========== MÉTODOS ==========
    def generate_command_args(self) -> list:
        args = []

        if self._format:
            args.extend(["-f", self._format])

        if self._codec:
            args.extend(["-c:v", self._codec])

        if self._start_time:
            args.extend(["-ss", self._start_time])

        if self._duration:
            args.extend(["-t", self._duration])

        if self._fps:
            args.extend(["-r", str(self._fps)])

        if self._size:
            args.extend(["-s", self._size])

        if self._pixel_format:
            args.extend(["-pix_fmt", self._pixel_format])

        if self._stream_loop is not None:
            args.extend(["-stream_loop", str(self._stream_loop)])

        return args
