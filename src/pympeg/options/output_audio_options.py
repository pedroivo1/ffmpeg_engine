from datetime import timedelta
from pympeg.interfaces import Options
from pympeg.utils.validation import (
    validate_choices, time_to_string, validate_int, convert_sample_rate,
    validate_number, convert_bitrate, validate_dict, validate_audio_format
)

class OutputAudioOptions(Options):

    VALID_FORMATS = {
        "mp3", "wav", "flac", "aac", "ogg", "m4a", "aiff",
        "opus", "ac3", "eac3", "dts",
        "pcm_s16le", "pcm_s24le", "pcm_f32le"
    }
    VALID_CODECS = {
        "mp3", "libmp3lame", "flac", "aac", "libfdk_aac",
        "opus", "libopus", "vorbis", "libvorbis",
        "pcm_s16le", "pcm_s24le", "pcm_f32le",
        "ac3", "eac3", "dts", "copy"
    }

    def __init__(
        self,
        format: str | None = None,
        codec: str | None = None,
        bitrate: str | int | None = None,
        sample_rate: int | float | str | None = None,
        n_channels: int | None = None,
        qscale: int | float | None = None,
        duration: timedelta | float | int | None = None,
        metadata: dict[str, str] | None = None,
    ) -> None:
        self._format: str | None = None
        self._codec: str | None = None
        self._bitrate: str | int | None = None
        self._sample_rate: int | float | str | None = None
        self._n_channels: int | None = None
        self._qscale: int | float | None = None
        self._duration: timedelta | float | int | None = None
        self._metadata: dict[str, str] | None = None

        if format is not None: self.format = format
        if codec is not None: self.codec = codec
        if bitrate is not None: self.bitrate = bitrate
        if sample_rate is not None: self.sample_rate = sample_rate
        if n_channels is not None: self.n_channels = n_channels
        if qscale is not None: self.qscale = qscale
        if duration is not None: self.duration = duration
        if metadata is not None: self.metadata = metadata


    # ========== PROPERTY: format ==========
    @property
    def format(self) -> str | None: return self._format

    @format.setter
    @validate_audio_format(VALID_FORMATS)
    def format(self, value: str) -> None: self._format = value

    @format.deleter
    def format(self) -> None: self._format = None


    # ========== PROPERTY: codec ==========
    @property
    def codec(self) -> str | None: return self._codec

    @codec.setter
    @validate_choices(VALID_CODECS)
    def codec(self, value: str) -> None: self._codec = value

    @codec.deleter
    def codec(self) -> None: self._codec = None


    # ========== PROPERTY: bitrate ==========
    @property
    def bitrate(self) -> int | None: return self._bitrate

    @bitrate.setter
    @convert_bitrate()
    def bitrate(self, value: str | int) -> None: self._bitrate = value

    @bitrate.deleter
    def bitrate(self) -> None: self._bitrate = None


    # ========== PROPERTY: sample_rate ==========
    @property
    def sample_rate(self) -> int | None: return self._sample_rate

    @sample_rate.setter
    @convert_sample_rate()
    def sample_rate(self, value: int | float | str) -> None: self._sample_rate = value

    @sample_rate.deleter
    def sample_rate(self) -> None: self._sample_rate = None


    # ========== PROPERTY: n_channels ==========
    @property
    def n_channels(self) -> int | None: return self._n_channels

    @n_channels.setter
    @validate_int(min_value=1)
    def n_channels(self, value: int) -> None: self._n_channels = value

    @n_channels.deleter
    def n_channels(self) -> None: self._n_channels = None


    # ========== PROPERTY: qscale ==========
    @property
    def qscale(self) -> int | float | None: return self._qscale

    @qscale.setter
    @validate_number(min_value=0)
    def qscale(self, value: int | float) -> None: self._qscale = value

    @qscale.deleter
    def qscale(self) -> None: self._qscale = None


    # ========== PROPERTY: duration ==========
    @property
    def duration(self) -> str | None: return self._duration

    @duration.setter
    @time_to_string()
    def duration(self, value: str) -> None: self._duration = value

    @duration.deleter
    def duration(self) -> None: self._duration = None


    # ========== PROPERTY: metadata ==========
    @property
    def metadata(self) -> dict | None: return self._metadata

    @metadata.setter
    @validate_dict()
    def metadata(self, value: dict) -> None: self._metadata = value

    @metadata.deleter
    def metadata(self) -> None: self._metadata = None


    # ========== MÉTODOS ==========
    def generate_command_args(self) -> list:
        args = []

        if self._format:
            args.extend(["-f", self._format])

        if self._codec:
            args.extend(["-c:a", self._codec])

        if self._bitrate:
            args.extend(["-b:a", str(self._bitrate)])

        if self._sample_rate:
            args.extend(["-ar", str(self._sample_rate)])

        if self._n_channels:
            args.extend(["-ac", str(self._n_channels)])

        if self._qscale is not None:
            args.extend(["-qscale:a", str(self._qscale)])

        if self._duration:
            args.extend(["-t", self._duration])

        if self._metadata:
            for key, value in self._metadata.items():
                if key and value:
                    args.extend(["-metadata", f"{key}={value}"])

        return args
