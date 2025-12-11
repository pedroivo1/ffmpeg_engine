from datetime import timedelta
from pympeg.interfaces import Options
from pympeg.utils.validation import validate_choices, time_to_string 


class ImageInputOptions(Options):

    FORMAT_VALUES = {
        "image2", "image2pipe", "png", "gif", "bmp", "tiff", "jpeg",
        "webp", "avif", "v4l2", "dshow", "mjpeg"
    }
    LOOP_VALUES = {-1, 0, 1}


    def __init__(
        self,
        format: str | None = None,
        start_time: timedelta | float | int | None = None,
        loop: int | None = None,
        framerate: float | int | None = None,
    ) -> None:
        self._format: str | None = None
        self._start_time: str | None = None
        self._loop: int | None = None
        self._framerate: float | int | None = None

        if format is not None:
            self.format = format
        if start_time is not None:
            self.start_time = start_time
        if loop is not None:
            self.loop = loop
        if framerate is not None:
            self.framerate = framerate


    # ========== PROPERTY: format ==========
    @property
    def format(self) -> str | None:
        return self._format

    @format.setter
    @validate_choices(FORMAT_VALUES)
    def format(self, value: str) -> None:
        self._format = value

    @format.deleter
    def format(self) -> None:
        self._format = None


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


    # ========== PROPERTY: loop ==========
    @property
    def loop(self) -> int | None:
        return self._loop

    @loop.setter
    @validate_choices(LOOP_VALUES)
    def loop(self, value: int) -> None:
        self._loop = value

    @loop.deleter
    def loop(self) -> None:
        self._loop = None


    # ========== PROPERTY: framerate ==========
    @property
    def framerate(self) -> float | int | None:
        return self._framerate

    @framerate.setter
    def framerate(self, value: float | int) -> None:
        if not isinstance(value, (float, int)):
            raise TypeError(
                f"framerate must be float or int, got {type(value).__name__}"
            )
        if value <= 0:
            raise ValueError("framerate must be greater than 0")
        self._framerate = value

    @framerate.deleter
    def framerate(self) -> None:
        self._framerate = None


    # ========== MÉTODOS ==========
    def generate_command_args(self) -> list:
        args = []

        if self._format is not None:
            args.extend(["-f", self._format])

        if self._start_time is not None:
            args.extend(["-ss", self._start_time])

        if self._loop is not None:
            args.extend(["-loop", str(self._loop)])

        if self._framerate is not None:
            args.extend(["-framerate", str(self._framerate)])

        return args
