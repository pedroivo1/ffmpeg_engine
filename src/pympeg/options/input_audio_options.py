from datetime import timedelta
from pympeg.interfaces import Options
from pympeg.utils.validation import (
    validate_choices, time_to_string, validate_int,
    convert_sample_rate
)

class InputAudioOptions(Options):
    
    AUDIO_FORMATS = {
        "mp3", "wav", "flac", "aac", "ogg", "m4a", "aiff",
        "s16le", "f32be", "pcm_s16le", "alsa", "pulse"
    }
    AUDIO_CODECS = {
        "mp3", "flac", "aac", "s16le", "f32be", "pcm_s16le"
    }

    def __init__(
        self,
        format: str | None = None,
        codec: str | None = None,
        start_time: timedelta | float | int | None = None,
        duration: timedelta | float | int | None = None,
        n_channels: int | None = None,
        sample_rate: int | float | str | None = None,
        stream_loop: int | None = None,
    ) -> None:
        self._format: str | None = None
        self._codec: str | None = None
        self._start_time: timedelta | float | int | None = None
        self._duration: timedelta | float | int | None = None
        self._n_channels: int | None = None
        self._sample_rate: int | float | str | None = None
        self._stream_loop: int | None = None

        if format is not None: self.format = format
        if codec is not None: self.codec = codec
        if start_time is not None: self.start_time = start_time
        if duration is not None: self.duration = duration
        if n_channels is not None: self.n_channels = n_channels
        if sample_rate is not None: self.sample_rate = sample_rate
        if stream_loop is not None: self.stream_loop = stream_loop


    # ========== PROPERTY: format ==========
    @property
    def format(self) -> str | None: return self._format

    @format.setter
    @validate_choices(AUDIO_FORMATS)
    def format(self, value: str) -> None: self._format = value

    @format.deleter
    def format(self) -> None: self._format = None


    # ========== PROPERTY: codec ==========
    @property
    def codec(self) -> str | None: return self._codec

    @codec.setter
    @validate_choices(AUDIO_CODECS)
    def codec(self, value: str) -> None: self._codec = value

    @codec.deleter
    def codec(self) -> None: self._codec = None


    # ========== PROPERTY: start_time ==========
    @property
    def start_time(self) -> str | None: return self._start_time

    @start_time.setter
    @time_to_string()
    def start_time(self, value: str) -> None: self._start_time = value

    @start_time.deleter
    def start_time(self) -> None: self._start_time = None


    # ========== PROPERTY: duration ==========
    @property
    def duration(self) -> str | None: return self._duration

    @duration.setter
    @time_to_string()
    def duration(self, value: str) -> None: self._duration = value

    @duration.deleter
    def duration(self) -> None: self._duration = None


    # ========== PROPERTY: n_channels ==========
    @property
    def n_channels(self) -> int | None: return self._n_channels

    @n_channels.setter
    @validate_int(min_value=1)
    def n_channels(self, value: int) -> None: self._n_channels = value

    @n_channels.deleter
    def n_channels(self) -> None: self._n_channels = None


    # ========== PROPERTY: sample_rate ==========
    @property
    def sample_rate(self) -> int | None: return self._sample_rate

    @sample_rate.setter
    @convert_sample_rate()
    def sample_rate(self, value: int | float | str) -> None: self._sample_rate = value

    @sample_rate.deleter
    def sample_rate(self) -> None: self._sample_rate = None


    # ========== PROPERTY: stream_loop ==========
    @property
    def stream_loop(self) -> int | None: return self._stream_loop

    @stream_loop.setter
    @validate_int(min_value=-1)
    def stream_loop(self, value: int) -> None: self._stream_loop = value

    @stream_loop.deleter
    def stream_loop(self) -> None: self._stream_loop = None


    # ========== MÉTODOS ==========
    def generate_command_args(self) -> list:
        args = []

        if self._format is not None:
            args.extend(["-f", self._format])

        if self._codec is not None:
            args.extend(["-c:a", self._codec])

        if self._start_time is not None:
            args.extend(["-ss", self._start_time])

        if self._duration is not None:
            args.extend(["-t", self._duration])

        if self._n_channels is not None:
            args.extend(["-ac", str(self._n_channels)])

        if self._sample_rate is not None:
            args.extend(["-ar", str(self._sample_rate)])

        if self._stream_loop is not None:
            args.extend(["-stream_loop", str(self._stream_loop)])

        return args
