from datetime import timedelta
from .interfaces import Options



class GlobalOptions(Options):
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



class ImageInputOptions(Options):
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
            valid_formats = {
                "image2", "image2pipe", "png", "gif", "bmp", "tiff", 
                "jpeg", "webp", "avif", "heif", "v4l2", "dshow", "mjpeg"}
            if self.format in valid_formats:
                args.extend(['-f', self.format])
            else:
                self._log_invalid_value('format', self.format)

        if self.start_time is not None:
            if isinstance(self.start_time, timedelta):
                total_seconds = self.start_time.total_seconds()
                H, R = divmod(total_seconds, 3600)
                M, S = divmod(R, 60)
                args.extend(['-ss', f"{int(H):02}:{int(M):02}:{S:06.3f}"])
            elif isinstance(self.start_time, (float, int)):
                args.extend(['-ss', f"{self.start_time:.3f}"])
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



class AudioInputOptions(Options):
    def __init__(self,
                 format: str | None = None,
                 codec: str | None = None,
                 start_time: timedelta | float | int | None = None,
                 duration: timedelta | float | int | None = None,
                 n_channels: int | None = None,
                 sample_rate: int | None = None,
                 stream_loop: int | None = None
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
                "mp3", "wav", "flac", "aac", "ogg", "m4a", "aiff", 
                "s16le", "f32be", "pcm_s16le", "alsa", "pulse"}
            if self.format in valid_audio_formats or self.format.startswith("pcm"):
                args.extend(['-f', self.format])
            else:
                self._log_invalid_value('format', self.format)

        if self.codec is not None:
            valid_audio_codecs = {
                "mp3", "flac", "aac", "s16le", "f32be","pcm_s16le"}
            if self.codec in valid_audio_codecs:
                args.extend(['-c:a', self.codec])
            else:
                self._log_invalid_value('codec', self.codec)

        if self.start_time is not None:
            if isinstance(self.start_time, timedelta):
                total_seconds = self.start_time.total_seconds()
                H, R = divmod(total_seconds, 3600)
                M, S = divmod(R, 60)
                args.extend(['-ss', f"{int(H):02}:{int(M):02}:{S:06.3f}"])
            elif isinstance(self.start_time, (float, int)):
                args.extend(['-ss', f"{self.start_time:.3f}"])
            else:
                self._log_invalid_value('start_time', self.start_time)

        if self.duration is not None:
            if isinstance(self.duration, timedelta):
                total_seconds = self.duration.total_seconds()
                H, R = divmod(total_seconds, 3600)
                M, S = divmod(R, 60)
                args.extend(['-t', f"{int(H):02}:{int(M):02}:{S:06.3f}"])
            elif isinstance(self.duration, (float, int)) and self.duration > 0:
                args.extend(['-t', f"{self.duration:.3f}"])
            else:
                self._log_invalid_value('duration', self.duration)

        if self.n_channels is not None:
            if isinstance(self.n_channels, int) and self.n_channels > 0:
                args.extend(['-ac', str(self.n_channels)])
            else:
                self._log_invalid_value('channels', self.n_channels)

        if self.sample_rate is not None:
            is_valid = False
            final_value = None # Variável para guardar o valor limpo (sem .0 ou k)
            # CASO 1: Numérico (Int ou Float)
            # Aceita 44100 ou 44100.0
            if isinstance(self.sample_rate, (int, float)) and self.sample_rate > 0:
                is_valid = True
                final_value = int(self.sample_rate) # Remove o .0 se for float
            # CASO 2: String (ex: "48k", "44.1k", "48000")
            elif isinstance(self.sample_rate, str):
                s_val = self.sample_rate.lower().strip()
                if s_val.endswith('k'):
                    try:
                        number_part = float(s_val[:-1])
                        if number_part > 0:
                            is_valid = True
                            # Multiplica por 1000 se tiver 'k' (ex: 44.1k -> 44100)
                            final_value = int(number_part * 1000) 
                    except ValueError:
                        pass
                elif s_val.replace('.', '', 1).isdigit():
                     val_float = float(s_val)
                     if val_float > 0:
                        is_valid = True
                        final_value = int(val_float)
            # --- AÇÃO FINAL ---
            if is_valid and final_value is not None:
                args.extend(['-ar', str(final_value)])
            else:
                self._log_invalid_value('sample_rate', self.sample_rate)

        if self.stream_loop is not None:
            if isinstance(self.stream_loop, int) and self.stream_loop >= -1:
                args.extend(['-stream_loop', str(self.stream_loop)])
            else:
                self._log_invalid_value('stream_loop', self.stream_loop)

        return args
