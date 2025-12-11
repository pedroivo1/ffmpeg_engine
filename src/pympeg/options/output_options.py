from datetime import timedelta
import re
from pympeg.interfaces import Options




class AudioOutputOptions(Options):
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
        self.format = format
        self.codec = codec
        self.bitrate = bitrate
        self.sample_rate = sample_rate
        self.n_channels = n_channels
        self.qscale = qscale
        self.duration = duration
        self.metadata = metadata

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
                "opus",
                "ac3",
                "eac3",
                "dts",
                "pcm_s16le",
                "pcm_s24le",
                "pcm_f32le",
            }
            if self.format in valid_audio_formats or self.format.startswith("pcm"):
                args.extend(["-f", self.format])
            else:
                self._log_invalid_value("format", self.format)

        if self.codec is not None:
            valid_audio_codecs = {
                "mp3",
                "libmp3lame",
                "flac",
                "aac",
                "libfdk_aac",
                "opus",
                "libopus",
                "vorbis",
                "libvorbis",
                "pcm_s16le",
                "pcm_s24le",
                "pcm_f32le",
                "ac3",
                "eac3",
                "dts",
                "copy",
            }
            if self.codec in valid_audio_codecs:
                args.extend(["-c:a", self.codec])
            else:
                self._log_invalid_value("codec", self.codec)

        if self.bitrate is not None:
            is_valid = False
            if isinstance(self.bitrate, int) and self.bitrate > 0:
                args.extend(["-b:a", f"{self.bitrate}"])
                is_valid = True
            elif isinstance(self.bitrate, str):
                s_val = self.bitrate.lower().strip()
                if s_val.endswith("k") or s_val.endswith("m"):
                    try:
                        number_part = float(s_val[:-1])
                        if number_part > 0:
                            args.extend(["-b:a", s_val])
                            is_valid = True
                    except ValueError:
                        pass
                elif s_val.replace(".", "", 1).isdigit():
                    val_float = float(s_val)
                    if val_float > 0:
                        args.extend(["-b:a", f"{int(val_float)}"])
                        is_valid = True
            
            if not is_valid:
                self._log_invalid_value("bitrate", self.bitrate)

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

        if self.n_channels is not None:
            if isinstance(self.n_channels, int) and self.n_channels > 0:
                args.extend(["-ac", str(self.n_channels)])
            else:
                self._log_invalid_value("n_channels", self.n_channels)

        if self.qscale is not None:
            if isinstance(self.qscale, (int, float)) and self.qscale >= 0:
                args.extend(["-qscale:a", str(self.qscale)])
            else:
                self._log_invalid_value("qscale", self.qscale)

        if self.duration is not None:
            time = self.time_to_str(self.duration, 0)
            if time is not None:
                args.extend(["-t", time])
            else:
                self._log_invalid_value("duration", self.duration)

        if self.metadata is not None:
            if isinstance(self.metadata, dict):
                for key, value in self.metadata.items():
                    if key and value:
                        args.extend(["-metadata", f"{key}={value}"])
            else:
                self._log_invalid_value("metadata", self.metadata)

        return args


class VideoOutputOptions(Options):
    def __init__(
        self,
        format: str | None = None,
        video_codec: str | None = None,
        audio_codec: str | None = None,
        bitrate: str | int | None = None,
        fps: float | int | None = None,
        size: str | None = None,
        pixel_format: str | None = None,
        qscale: int | float | None = None,
        duration: timedelta | float | int | None = None,
        preset: str | None = None,
        crf: int | None = None,
        metadata: dict[str, str] | None = None,
        movflags: str | None = None,
        tune: str | None = None,
    ) -> None:
        self.format = format
        self.video_codec = video_codec
        self.audio_codec = audio_codec
        self.bitrate = bitrate
        self.fps = fps
        self.size = size
        self.pixel_format = pixel_format
        self.qscale = qscale
        self.duration = duration
        self.preset = preset
        self.crf = crf
        self.metadata = metadata
        self.movflags = movflags
        self.tune = tune

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
                "gif",
                "matroska",
                "flv",
                "m4v",
            }
            if self.format in valid_formats:
                args.extend(["-f", self.format])
            else:
                self._log_invalid_value("format", self.format)

        if self.video_codec is not None:
            valid_codecs = {
                "libx264",
                "h264",
                "libx265",
                "hevc",
                "vp9",
                "libvpx-vp9",
                "vp8",
                "libvpx",
                "mpeg4",
                "mpeg2video",
                "prores",
                "dnxhd",
                "ffv1",
                "copy",
                "mjpeg",
                "h264_nvenc",
                "hevc_nvenc",
                "av1",
                "libaom-av1",
            }
            if self.video_codec in valid_codecs:
                args.extend(["-c:v", self.video_codec])
            else:
                self._log_invalid_value("video_codec", self.video_codec)

        if self.audio_codec is not None:
            valid_audio_codecs = {
                "aac",
                "libfdk_aac",
                "mp3",
                "libmp3lame",
                "opus",
                "libopus",
                "vorbis",
                "libvorbis",
                "flac",
                "pcm_s16le",
                "copy",
                "ac3",
                "eac3",
            }
            if self.audio_codec in valid_audio_codecs:
                args.extend(["-c:a", self.audio_codec])
            else:
                self._log_invalid_value("audio_codec", self.audio_codec)

        if self.bitrate is not None:
            is_valid = False
            if isinstance(self.bitrate, int) and self.bitrate > 0:
                args.extend(["-b:v", f"{self.bitrate}"])
                is_valid = True
            elif isinstance(self.bitrate, str):
                s_val = self.bitrate.lower().strip()
                if s_val.endswith("k") or s_val.endswith("m"):
                    try:
                        number_part = float(s_val[:-1])
                        if number_part > 0:
                            args.extend(["-b:v", s_val])
                            is_valid = True
                    except ValueError:
                        pass
                elif s_val.replace(".", "", 1).isdigit():
                    val_float = float(s_val)
                    if val_float > 0:
                        args.extend(["-b:v", f"{int(val_float)}"])
                        is_valid = True
            
            if not is_valid:
                self._log_invalid_value("bitrate", self.bitrate)

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
                "rgba",
                "bgra",
                "gray",
                "monow",
                "monob",
                "yuyv422",
                "nv12",
                "nv21",
                "p010le",
                "p010be",
            }
            if self.pixel_format in valid_pix_fmts:
                args.extend(["-pix_fmt", self.pixel_format])
            else:
                self._log_invalid_value("pixel_format", self.pixel_format)

        if self.qscale is not None:
            if isinstance(self.qscale, (int, float)) and self.qscale >= 0:
                args.extend(["-qscale:v", str(self.qscale)])
            else:
                self._log_invalid_value("qscale", self.qscale)

        if self.duration is not None:
            time = self.time_to_str(self.duration, 0)
            if time is not None:
                args.extend(["-t", time])
            else:
                self._log_invalid_value("duration", self.duration)

        if self.preset is not None:
            valid_presets = {
                "ultrafast",
                "superfast",
                "veryfast",
                "faster",
                "fast",
                "medium",
                "slow",
                "slower",
                "veryslow",
                "placebo",
            }
            if self.preset in valid_presets:
                args.extend(["-preset", self.preset])
            else:
                self._log_invalid_value("preset", self.preset)

        if self.crf is not None:
            if isinstance(self.crf, int) and 0 <= self.crf <= 51:
                args.extend(["-crf", str(self.crf)])
            else:
                self._log_invalid_value("crf", self.crf)

        if self.metadata is not None:
            if isinstance(self.metadata, dict):
                for key, value in self.metadata.items():
                    if key and value:
                        args.extend(["-metadata", f"{key}={value}"])
            else:
                self._log_invalid_value("metadata", self.metadata)

        if self.movflags is not None:
            valid_movflags = {
                "faststart",
                "frag_keyframe",
                "empty_moov",
                "default_base_moof",
                "dash",
                "frag_custom",
                "separate_moof",
                "frag_every_frame",
            }
            if self.movflags in valid_movflags:
                args.extend(["-movflags", self.movflags])
            else:
                self._log_invalid_value("movflags", self.movflags)

        if self.tune is not None:
            valid_tunes = {
                "film",
                "animation",
                "grain",
                "stillimage",
                "fastdecode",
                "zerolatency",
                "psnr",
                "ssim",
            }
            if self.tune in valid_tunes:
                args.extend(["-tune", self.tune])
            else:
                self._log_invalid_value("tune", self.tune)

        return args
