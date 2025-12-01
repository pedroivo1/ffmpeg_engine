from .strategies import VideoFlags

class VideoCodecBuilder:
    def __init__(self):
        self._video_codec = 'libx264'
        self._crf = 23
        self._preset = 'medium'
        self._scale = None

    def set_codec(self, codec: str):
        self._video_codec = codec
        return self

    def set_crf(self, crf: int):
        self._crf = crf
        return self

    def set_preset(self, preset: str):
        self._preset = preset
        return self

    def resize(self, width: int, height: int):
        self._scale = f"{width}:{height}"
        return self

    def build(self) -> VideoFlags:
        return VideoFlags(
            video_codec=self._video_codec,
            crf=self._crf,
            preset=self._preset,
            scale=self._scale
        )