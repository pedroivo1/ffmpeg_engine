from .interfaces import MediaFlags

class VideoFlags(MediaFlags):
    def __init__(self, video_codec: str, crf: int, preset: str, scale: str = None, fps: int = None) -> None:
        self.video_codec = video_codec
        self.crf = crf
        self.preset = preset
        self.scale = scale
        self.fps = fps

    def generate_command_args(self) -> list:
        args = ["-c:v", self.video_codec, "-crf", str(self.crf), "-preset", self.preset]

        if self.scale:
            args.extend(["-vf", f"scale={self.scale}"])

        if self.fps:
            args.extend(["-r", str(self.fps)])

        return args


class AudioFlags(MediaFlags):
    def __init__(self, audio_codec: str = 'aac', bitrate: str = None) -> None:
        self.audio_codec = audio_codec
        self.bitrate = bitrate

    def generate_command_args(self) -> list:
        args = ["-c:a", self.audio_codec]
        
        if self.bitrate and self.audio_codec != "copy":
            args.extend(["-b:a", self.bitrate])
            
        return args


class ImageFlags(MediaFlags):
    pass
