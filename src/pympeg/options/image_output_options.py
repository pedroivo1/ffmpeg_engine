from pympeg.interfaces import Options
import re


class ImageOutputOptions(Options):
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
        self.format = format
        self.codec = codec
        self.qscale = qscale
        self.frames = frames
        self.framerate = framerate
        self.size = size
        self.pixel_format = pixel_format
        self.compression_level = compression_level

    def generate_command_args(self) -> list:
        args = []

        if self.format is not None:
            valid_formats = {
                "image2",
                "image2pipe",
                "png",
                "jpeg",
                "jpg",
                "gif",
                "bmp",
                "tiff",
                "webp",
                "avif",
                "heif",
            }
            if self.format in valid_formats:
                args.extend(["-f", self.format])
            else:
                self._log_invalid_value("format", self.format)

        if self.codec is not None:
            valid_codecs = {
                "png",
                "mjpeg",
                "libwebp",
                "av1",
                "hevc",
                "libx264",
                "gif",
                "bmp",
                "tiff",
                "copy",
            }
            if self.codec in valid_codecs:
                args.extend(["-c:v", self.codec])
            else:
                self._log_invalid_value("codec", self.codec)

        if self.qscale is not None:
            if isinstance(self.qscale, (int, float)) and self.qscale >= 0:
                args.extend(["-qscale:v", str(self.qscale)])
            else:
                self._log_invalid_value("qscale", self.qscale)

        if self.frames is not None:
            if isinstance(self.frames, int) and self.frames > 0:
                args.extend(["-frames:v", str(self.frames)])
            else:
                self._log_invalid_value("frames", self.frames)

        if self.framerate is not None:
            if isinstance(self.framerate, (float, int)) and self.framerate > 0:
                args.extend(["-r", str(self.framerate)])
            else:
                self._log_invalid_value("framerate", self.framerate)

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
                "pal8",
            }
            if self.pixel_format in valid_pix_fmts:
                args.extend(["-pix_fmt", self.pixel_format])
            else:
                self._log_invalid_value("pixel_format", self.pixel_format)

        if self.compression_level is not None:
            if isinstance(self.compression_level, int) and 0 <= self.compression_level <= 100:
                args.extend(["-compression_level", str(self.compression_level)])
            else:
                self._log_invalid_value("compression_level", self.compression_level)

        return args
