from .builders import VideoCodecBuilder
from .strategies import VideoFlags # Opcional, para tipagem

class CodecDirector:
    def __init__(self, builder: VideoCodecBuilder):
        self._builder = builder

    def make_video_codec(self) -> VideoFlags:
        return (self._builder
            .set_codec("libx264")
            .set_preset("fast")
            .set_crf(23)
            .build())
