from datetime import timedelta
from pympeg.interfaces import Options
from pympeg.utils.validation import (
    validate_choices, time_to_string, validate_int, 
    validate_positive_number, validate_video_size, 
    convert_bitrate, validate_dict, validate_number
)

class VideoOutputOptions(Options):

    VALID_FORMATS = {
        "mp4", "avi", "mov", "mkv", "webm", "flv", "mpeg", "3gp", 
        "ts", "ogv", "asf", "wmv", "gif", "matroska", "m4v"
    }
    VALID_VIDEO_CODECS = {
        "libx264", "h264", "libx265", "hevc", "vp9", "libvpx-vp9", 
        "vp8", "libvpx", "mpeg4", "mpeg2video", "prores", "dnxhd", 
        "ffv1", "copy", "mjpeg", "h264_nvenc", "hevc_nvenc", 
        "av1", "libaom-av1"
    }
    VALID_AUDIO_CODECS = {
        "aac", "libfdk_aac", "mp3", "libmp3lame", "opus", "libopus", 
        "vorbis", "libvorbis", "flac", "pcm_s16le", "copy", "ac3", "eac3"
    }
    VALID_PIX_FMTS = {
        "yuv420p", "yuv422p", "yuv444p", "rgb24", "bgr24", 
        "rgba", "bgra", "gray", "monow", "monob", 
        "yuyv422", "nv12", "nv21", "p010le", "p010be"
    }
    VALID_SIZES = {
        "sqcif", "qcif", "cif", "4cif", "16cif", "qqvga", "qvga", "vga", 
        "svga", "xga", "uxga", "qxga", "sxga", "qsxga", "qzxga", "wsxga", 
        "wuxga", "woxga", "wqsxga", "wquxga", "whsxfga", "hsxga", "cga", 
        "ega", "hd480", "hd720", "hd1080", "uhd2160", "8k", "ntsc", "pal", 
        "qntsc", "qpal", "sntsc", "spal", "film", "ntsc-film", "2k", 
        "2kflat", "2kscope", "4k", "4kflat", "4kscope"
    }
    VALID_PRESETS = {
        "ultrafast", "superfast", "veryfast", "faster", "fast", 
        "medium", "slow", "slower", "veryslow", "placebo"
    }
    VALID_MOVFLAGS = {
        "faststart", "frag_keyframe", "empty_moov", "default_base_moof", 
        "dash", "frag_custom", "separate_moof", "frag_every_frame"
    }
    VALID_TUNES = {
        "film", "animation", "grain", "stillimage", "fastdecode", 
        "zerolatency", "psnr", "ssim"
    }

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
        self._format = None
        self._video_codec = None
        self._audio_codec = None
        self._bitrate = None
        self._fps = None
        self._size = None
        self._pixel_format = None
        self._qscale = None
        self._duration = None
        self._preset = None
        self._crf = None
        self._metadata = None
        self._movflags = None
        self._tune = None

        if format is not None: self.format = format
        if video_codec is not None: self.video_codec = video_codec
        if audio_codec is not None: self.audio_codec = audio_codec
        if bitrate is not None: self.bitrate = bitrate
        if fps is not None: self.fps = fps
        if size is not None: self.size = size
        if pixel_format is not None: self.pixel_format = pixel_format
        if qscale is not None: self.qscale = qscale
        if duration is not None: self.duration = duration
        if preset is not None: self.preset = preset
        if crf is not None: self.crf = crf
        if metadata is not None: self.metadata = metadata
        if movflags is not None: self.movflags = movflags
        if tune is not None: self.tune = tune


    # ========== PROPERTIES ==========

    @property
    def format(self) -> str | None: return self._format
    @format.setter
    @validate_choices(VALID_FORMATS)
    def format(self, value: str): self._format = value
    @format.deleter
    def format(self): self._format = None

    @property
    def video_codec(self) -> str | None: return self._video_codec
    @video_codec.setter
    @validate_choices(VALID_VIDEO_CODECS)
    def video_codec(self, value: str): self._video_codec = value
    @video_codec.deleter
    def video_codec(self): self._video_codec = None

    @property
    def audio_codec(self) -> str | None: return self._audio_codec
    @audio_codec.setter
    @validate_choices(VALID_AUDIO_CODECS)
    def audio_codec(self, value: str): self._audio_codec = value
    @audio_codec.deleter
    def audio_codec(self): self._audio_codec = None

    @property
    def bitrate(self) -> int | None: return self._bitrate
    @bitrate.setter
    @convert_bitrate()
    def bitrate(self, value: str | int): self._bitrate = value
    @bitrate.deleter
    def bitrate(self): self._bitrate = None

    @property
    def fps(self) -> float | int | None: return self._fps
    @fps.setter
    @validate_positive_number()
    def fps(self, value: float | int): self._fps = value
    @fps.deleter
    def fps(self): self._fps = None

    @property
    def size(self) -> str | None: return self._size
    @size.setter
    @validate_video_size(VALID_SIZES)
    def size(self, value: str): self._size = value
    @size.deleter
    def size(self): self._size = None

    @property
    def pixel_format(self) -> str | None: return self._pixel_format
    @pixel_format.setter
    @validate_choices(VALID_PIX_FMTS)
    def pixel_format(self, value: str): self._pixel_format = value
    @pixel_format.deleter
    def pixel_format(self): self._pixel_format = None

    @property
    def qscale(self) -> int | float | None: return self._qscale
    @qscale.setter
    @validate_number(min_value=0)
    def qscale(self, value: int | float): self._qscale = value
    @qscale.deleter
    def qscale(self): self._qscale = None

    @property
    def duration(self) -> str | None: return self._duration
    @duration.setter
    @time_to_string()
    def duration(self, value: str): self._duration = value
    @duration.deleter
    def duration(self): self._duration = None

    @property
    def preset(self) -> str | None: return self._preset
    @preset.setter
    @validate_choices(VALID_PRESETS)
    def preset(self, value: str): self._preset = value
    @preset.deleter
    def preset(self): self._preset = None

    @property
    def crf(self) -> int | None: return self._crf
    @crf.setter
    @validate_int(min_value=0, max_value=51)
    def crf(self, value: int): self._crf = value
    @crf.deleter
    def crf(self): self._crf = None

    @property
    def metadata(self) -> dict | None: return self._metadata
    @metadata.setter
    @validate_dict()
    def metadata(self, value: dict): self._metadata = value
    @metadata.deleter
    def metadata(self): self._metadata = None

    @property
    def movflags(self) -> str | None: return self._movflags
    @movflags.setter
    @validate_choices(VALID_MOVFLAGS)
    def movflags(self, value: str): self._movflags = value
    @movflags.deleter
    def movflags(self): self._movflags = None

    @property
    def tune(self) -> str | None: return self._tune
    @tune.setter
    @validate_choices(VALID_TUNES)
    def tune(self, value: str): self._tune = value
    @tune.deleter
    def tune(self): self._tune = None


    # ========== MÉTODOS ==========
    def generate_command_args(self) -> list:
        args = []
        if self._format: args.extend(["-f", self._format])
        if self._video_codec: args.extend(["-c:v", self._video_codec])
        if self._audio_codec: args.extend(["-c:a", self._audio_codec])
        if self._bitrate: args.extend(["-b:v", str(self._bitrate)])
        if self._fps: args.extend(["-r", str(self._fps)])
        if self._size: args.extend(["-s", self._size])
        if self._pixel_format: args.extend(["-pix_fmt", self._pixel_format])
        if self._qscale is not None: args.extend(["-qscale:v", str(self._qscale)])
        if self._duration: args.extend(["-t", self._duration])
        if self._preset: args.extend(["-preset", self._preset])
        if self._crf is not None: args.extend(["-crf", str(self._crf)])
        
        if self._metadata:
            for key, value in self._metadata.items():
                if key and value:
                    args.extend(["-metadata", f"{key}={value}"])
        
        if self._movflags: args.extend(["-movflags", self._movflags])
        if self._tune: args.extend(["-tune", self._tune])

        return args
