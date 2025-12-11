from datetime import timedelta
from pympeg.interfaces import Options


class AudioInputOptions(Options):
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
        self.format = format
        self.codec = codec
        self.start_time = start_time
        self.duration = duration
        self.n_channels = n_channels
        self.sample_rate = sample_rate
        self.stream_loop = stream_loop

    def generate_command_args(self) -> list:
        args = []

        if self.format is not None:
            valid_audio_formats = {
                "mp3",
                "wav",
                "flac",
                "aac",
                "ogg",
                "m4a",
                "aiff",
                "s16le",
                "f32be",
                "pcm_s16le",
                "alsa",
                "pulse",
            }
            if self.format in valid_audio_formats or self.format.startswith("pcm"):
                args.extend(["-f", self.format])
            else:
                self._log_invalid_value("format", self.format)

        if self.codec is not None:
            valid_audio_codecs = {"mp3", "flac", "aac", "s16le", "f32be", "pcm_s16le"}
            if self.codec in valid_audio_codecs:
                args.extend(["-c:a", self.codec])
            else:
                self._log_invalid_value("codec", self.codec)

        if self.start_time is not None:
            time = self.time_to_str(self.start_time, 0)
            if time is not None:
                args.extend(["-ss", time])
            else:
                self._log_invalid_value("start_time", self.start_time)

        if self.duration is not None:
            time = self.time_to_str(self.duration, 0)
            if time is not None:
                args.extend(["-t", time])
            else:
                self._log_invalid_value("duration", self.duration)

        if self.n_channels is not None:
            if isinstance(self.n_channels, int) and self.n_channels > 0:
                args.extend(["-ac", str(self.n_channels)])
            else:
                self._log_invalid_value("n_channels", self.n_channels)

        if self.sample_rate is not None:
            is_valid = False
            final_value = None
            if isinstance(self.sample_rate, (int, float)) and self.sample_rate > 0:
                is_valid = True
                final_value = int(self.sample_rate)
            elif isinstance(self.sample_rate, str):
                s_val = self.sample_rate.lower().strip()
                if s_val.endswith("k"):
                    try:
                        number_part = float(s_val[:-1])
                        if number_part > 0:
                            is_valid = True
                            final_value = int(number_part * 1000)
                    except ValueError:
                        pass
                elif s_val.replace(".", "", 1).isdigit():
                    val_float = float(s_val)
                    if val_float > 0:
                        is_valid = True
                        final_value = int(val_float)
            if is_valid and final_value is not None:
                args.extend(["-ar", str(final_value)])
            else:
                self._log_invalid_value("sample_rate", self.sample_rate)

        if self.stream_loop is not None:
            if isinstance(self.stream_loop, int) and self.stream_loop >= -1:
                args.extend(["-stream_loop", str(self.stream_loop)])
            else:
                self._log_invalid_value("stream_loop", self.stream_loop)

        return args
