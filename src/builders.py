# from __future__ import annotations
# from .flags import VideoFlags

# class VideoCodecBuilder:
#     def __init__(self) -> None: 
#         self._video_codec = 'libx264'
#         self._crf = 23
#         self._preset = 'medium'
#         self._scale = None
#         self._fps = None

#     def set_codec(self, codec: str) -> VideoCodecBuilder:
#         self._video_codec = codec
#         return self

#     def set_crf(self, crf: int) -> VideoCodecBuilder:
#         self._crf = crf
#         return self

#     def set_preset(self, preset: str) -> VideoCodecBuilder:
#         self._preset = preset
#         return self

#     def set_scale(self, width: int, height: int = -1) -> VideoCodecBuilder:
#         self._scale = f"{width}:{height}"
#         return self

#     def set_fps(self, fps: int) -> VideoCodecBuilder:
#         self._fps = fps
#         return self

#     def build(self) -> VideoFlags:
#         return VideoFlags(
#             video_codec=self._video_codec,
#             crf=self._crf,
#             preset=self._preset,
#             scale=self._scale,
#             fps=self._fps
#         )
