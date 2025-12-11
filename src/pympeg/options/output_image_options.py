from pympeg.interfaces import Options
from pympeg.utils.validation import (
    validate_choices, validate_int, validate_video_size, 
    validate_number
)

class ImageOutputOptions(Options):

    VALID_FORMATS = {
        "image2", "image2pipe", "png", "jpeg", "jpg", "gif", 
        "bmp", "tiff", "webp", "avif", "heif"
    }
    VALID_CODECS = {
        "png", "mjpeg", "libwebp", "av1", "hevc", "libx264", 
        "gif", "bmp", "tiff", "copy"
    }
    VALID_PIX_FMTS = {
        "yuv420p", "yuv422p", "yuv444p", "rgb24", "bgr24", 
        "rgba", "bgra", "gray", "monow", "monob", 
        "yuyv422", "pal8"
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
        qscale: int | float | None = None,
        frames: int | None = None,
        framerate: float | int | None = None,
        size: str | None = None,
        pixel_format: str | None = None,
        compression_level: int | None = None,
    ) -> None:
        self._format = None
        self._codec = None
        self._qscale = None
        self._frames = None
        self._framerate = None
        self._size = None
        self._pixel_format = None
        self._compression_level = None

        if format is not None: self.format = format
        if codec is not None: self.codec = codec
        if qscale is not None: self.qscale = qscale
        if frames is not None: self.frames = frames
        if framerate is not None: self.framerate = framerate
        if size is not None: self.size = size
        if pixel_format is not None: self.pixel_format = pixel_format
        if compression_level is not None: self.compression_level = compression_level


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


    # ========== PROPERTY: qscale ==========
    @property
    def qscale(self) -> int | float | None:
        return self._qscale

    @qscale.setter
    @validate_number(min_value=0)
    def qscale(self, value: int | float) -> None:
        self._qscale = value

    @qscale.deleter
    def qscale(self) -> None:
        self._qscale = None


    # ========== PROPERTY: frames ==========
    @property
    def frames(self) -> int | None:
        return self._frames

    @frames.setter
    @validate_int(min_value=1)
    def frames(self, value: int) -> None:
        self._frames = value

    @frames.deleter
    def frames(self) -> None:
        self._frames = None


    # ========== PROPERTY: framerate ==========
    @property
    def framerate(self) -> float | int | None:
        return self._framerate

    @framerate.setter
    # Framerate deve ser estritamente maior que 0
    @validate_number(min_value=0.00001) 
    def framerate(self, value: float | int) -> None:
        self._framerate = value

    @framerate.deleter
    def framerate(self) -> None:
        self._framerate = None


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


    # ========== PROPERTY: compression_level ==========
    @property
    def compression_level(self) -> int | None:
        return self._compression_level

    @compression_level.setter
    @validate_int(min_value=0, max_value=100)
    def compression_level(self, value: int) -> None:
        self._compression_level = value

    @compression_level.deleter
    def compression_level(self) -> None:
        self._compression_level = None


    # ========== MÉTODOS ==========
    def generate_command_args(self) -> list:
        args = []

        if self._format:
            args.extend(["-f", self._format])

        if self._codec:
            args.extend(["-c:v", self._codec])

        if self._qscale is not None:
            args.extend(["-qscale:v", str(self._qscale)])

        if self._frames:
            args.extend(["-frames:v", str(self._frames)])

        if self._framerate:
            args.extend(["-r", str(self._framerate)])

        if self._size:
            args.extend(["-s", self._size])

        if self._pixel_format:
            args.extend(["-pix_fmt", self._pixel_format])

        if self._compression_level is not None:
            args.extend(["-compression_level", str(self._compression_level)])

        return args
