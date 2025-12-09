from datetime import timedelta
import re
from pympeg.interfaces import Options


class ImageInputOptions(Options):
    def __init__(
        self,
        format: str | None = None,
        start_time: timedelta | float | int | None = None,
        loop: int | None = None,
        framerate: float | int | None = None,  # -framerate == -r on input
    ) -> None:
        self.format = format
        self.start_time = start_time
        self.loop = loop
        self.framerate = framerate

    def generate_command_args(self) -> list:
        args = []

        if self.format is not None:
            valid_formats = {
                "image2",
                "image2pipe",
                "png",
                "gif",
                "bmp",
                "tiff",
                "jpeg",
                "webp",
                "avif",
                "heif",
                "v4l2",
                "dshow",
                "mjpeg",
            }
            if self.format in valid_formats:
                args.extend(["-f", self.format])
            else:
                self._log_invalid_value("format", self.format)

        if self.start_time is not None:
            time = self.time_to_str(self.start_time, 0)
            if time is not None:
                args.extend(["-ss", time])
            else:
                self._log_invalid_value("start_time", self.start_time)

        if self.loop is not None:
            if self.loop in (-1, 0, 1):
                args.extend(["-loop", str(self.loop)])
            else:
                self._log_invalid_value("loop", self.loop)

        if self.framerate is not None:
            if isinstance(self.framerate, (float, int)) and self.framerate > 0:
                args.extend(["-framerate", str(self.framerate)])
            else:
                self._log_invalid_value("framerate", self.framerate)

        return args


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
                self._log_invalid_value("channels", self.n_channels)

        if self.sample_rate is not None:
            is_valid = False
            final_value = None  # Variável para guardar o valor limpo (sem .0 ou k)
            # CASO 1: Numérico (Int ou Float)
            # Aceita 44100 ou 44100.0
            if isinstance(self.sample_rate, (int, float)) and self.sample_rate > 0:
                is_valid = True
                final_value = int(self.sample_rate)  # Remove o .0 se for float
            # CASO 2: String (ex: '48k', '44.1k', '48000')
            elif isinstance(self.sample_rate, str):
                s_val = self.sample_rate.lower().strip()
                if s_val.endswith("k"):
                    try:
                        number_part = float(s_val[:-1])
                        if number_part > 0:
                            is_valid = True
                            # Multiplica por 1000 se tiver 'k' (ex: 44.1k -> 44100)
                            final_value = int(number_part * 1000)
                    except ValueError:
                        pass
                elif s_val.replace(".", "", 1).isdigit():
                    val_float = float(s_val)
                    if val_float > 0:
                        is_valid = True
                        final_value = int(val_float)
            # --- AÇÃO FINAL ---
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


class VideoInputOptions(Options):
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
        self.format = format
        self.codec = codec
        self.start_time = start_time
        self.duration = duration
        self.fps = fps
        self.size = size
        self.pixel_format = pixel_format
        self.stream_loop = stream_loop

    def generate_command_args(self) -> list:
        args = []

        if self.format is not None:
            valid_formats = {
                "mp4",
                "avi",
                "mov",
                "mkv",
                "webm",
                "flv",
                "mpeg",
                "3gp",
                "ts",
                "ogv",
                "asf",
                "wmv",
                "rawvideo",
                "yuv4mpegpipe",
            }
            if self.format in valid_formats:
                args.extend(["-f", self.format])
            else:
                self._log_invalid_value("format", self.format)

        if self.codec is not None:
            valid_codecs = {
                "libx264",
                "h264",
                "libx265",
                "hevc",
                "vp9",
                "vp8",
                "mpeg4",
                "mpeg2video",
                "prores",
                "dnxhd",
                "ffv1",
                "rawvideo",
                "copy",
                "mjpeg",
            }
            if self.codec in valid_codecs:
                args.extend(["-c:v", self.codec])
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

        if self.fps is not None:
            if isinstance(self.fps, (float, int)) and self.fps > 0:
                args.extend(["-r", str(self.fps)])
            else:
                self._log_invalid_value("fps", self.fps)

        if self.size is not None:
            valid_aliases = {
                "sqcif",
                "qcif",
                "cif",
                "4cif",
                "16cif",
                "qqvga",
                "qvga",
                "vga",
                "svga",
                "xga",
                "uxga",
                "qxga",
                "sxga",
                "qsxga",
                "qzxga",
                "wsxga",
                "wuxga",
                "woxga",
                "wqsxga",
                "wquxga",
                "whsxfga",
                "hsxga",
                "cga",
                "ega",
                "hd480",
                "hd720",
                "hd1080",
                "uhd2160",
                "8k",
                "ntsc",
                "pal",
                "qntsc",
                "qpal",
                "sntsc",
                "spal",
                "film",
                "ntsc-film",
                "2k",
                "2kflat",
                "2kscope",
                "4k",
                "4kflat",
                "4kscope",
            }
            if isinstance(self.size, str) and len(self.size) > 0:
                s_val = self.size.lower()

                is_wxh = re.match(r"^\d+x\d+$", s_val)

                is_alias = s_val in valid_aliases

                if is_wxh or is_alias:
                    args.extend(["-s", s_val])
                else:
                    self._log_invalid_value("size", self.size)
            else:
                self._log_invalid_value("size", self.size)

        if self.pixel_format is not None:
            valid_pix_fmts = {
                "yuv420p",
                "yuv422p",
                "yuv444p",
                "rgb24",
                "bgr24",
                "gray",
                "monow",
                "monob",
                "yuyv422",
            }
            if self.pixel_format in valid_pix_fmts:
                args.extend(["-pix_fmt", self.pixel_format])
            else:
                self._log_invalid_value("pixel_format", self.pixel_format)

        if self.stream_loop is not None:
            if isinstance(self.stream_loop, int) and self.stream_loop >= -1:
                args.extend(["-stream_loop", str(self.stream_loop)])
            else:
                self._log_invalid_value("stream_loop", self.stream_loop)

        return args
