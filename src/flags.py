from datetime import timedelta
from .interfaces import Flags



class GlobalOptions(Flags):
    def __init__(self,
                 overwrite: str | None = None,
                 hide_banner: str | None = None,
                 loglevel: str | None = None,
                 stats: str | None = None
    ) -> None:
        self.overwrite = overwrite
        self.hide_banner = hide_banner
        self.loglevel = loglevel
        self.stats = stats


    def generate_command_args(self) -> list:
        args = []

        if self.overwrite is not None:
            overwrite_map = {'no': '-n', 'yes': '-y'}
            if self.overwrite in overwrite_map:
                args.append(overwrite_map[self.overwrite])
            else:
                self._log_invalid_value('overwrite', self.overwrite)

        if self.hide_banner is not None:
            if self.hide_banner == 'yes':
                args.append('-hide_banner')
            else:
                self._log_invalid_value('hide_banner', self.hide_banner)

        if self.loglevel is not None:
            valid_levels = {'quiet', 'panic', 'fatal', 'error', 'warning',
                            'info', 'verbose', 'debug', 'trace'}
            if self.loglevel in valid_levels:
                args.extend(['-loglevel', self.loglevel])
            else:
                self._log_invalid_value('loglevel', self.loglevel)

        if self.stats is not None:
            stats_map = {'yes': '-stats', 'no': '-nostats'}
            if self.stats in stats_map:
                args.append(stats_map[self.stats])
            else:
                self._log_invalid_value('stats', self.stats)

        return args



class ImageInputOptions(Flags):
    def __init__(self,
                 format: str | None = None,
                 start_time: timedelta | float | int | None = None,
                 loop: int | None = None, 
                 framerate: float | int | None = None,
                 fps: float | int | None = None
    ) -> None:
        self.format = format
        self.start_time = start_time
        self.loop = loop
        self.framerate = framerate
        self.fps = fps


    def generate_command_args(self) -> list:
        args = []

        if self.format is not None:
            valid_formats = {"image2", "image2pipe", "png", "gif", "bmp",
                             "tiff", "jpeg", "webp", "avif", "heif", "v4l2",
                             "dshow", "mjpeg"}
            if self.format in valid_formats:
                args.extend(['-f', self.format])
            else:
                self._log_invalid_value('format', self.format)

        if self.start_time is not None:
            if isinstance(self.start_time, timedelta):
                total_seconds = self.start_time.total_seconds()
                
                H = int(total_seconds // 3600)
                R1 = total_seconds % 3600
                M = int(R1 // 60)
                S = R1 % 60
                
                time_arg = f"{H:02}:{M:02}:{S:06.3f}"
                args.extend(['-ss', time_arg])

            elif isinstance(self.start_time, (float, int)):
                time_arg = f"{self.start_time:.3f}"
                args.extend(['-ss', time_arg])

            else:
                self._log_invalid_value('start_time', self.start_time)

        if self.loop is not None:
            if self.loop in (-1, 0, 1):
                args.extend(['-loop', str(self.loop)])
            else:
                self._log_invalid_value('loop', self.loop)

        if self.framerate is not None:
            if isinstance(self.framerate, (float, int)) and self.framerate > 0:
                args.extend(['-framerate', str(self.framerate)])
            else:
                self._log_invalid_value('framerate', self.framerate)

        if self.fps is not None:
            if isinstance(self.fps, (float, int)) and self.fps > 0:
                args.extend(['-r', str(self.fps)])
            else:
                self._log_invalid_value('fps', self.fps)

        return args



class ImageFlagsOut(Flags):
    def __init__(self, codec: str, crf: int, preset: str, scale: str = None, fps: int = None):
        pass


    def generate_command_args(self):
        args = []


        return



class AudioFlags(Flags):
    def __init__(self, audio_codec: str = 'aac', bitrate: str = None) -> None:
        self.audio_codec = audio_codec
        self.bitrate = bitrate

    def generate_command_args(self) -> list:
        args = ['-c:a', self.audio_codec]
        
        if self.bitrate and self.audio_codec != 'copy':
            args.extend(['-b:a', self.bitrate])
            
        return args



class VideoFlags(Flags):
    def __init__(self, fps: int | None = None) -> None:

        self.fps = fps

    def generate_command_args(self) -> list:
        args = []

        if self.fps is not None:
            args.extend(['-r', str(self.fps)])

        return args


