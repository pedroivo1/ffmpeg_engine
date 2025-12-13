from pympeg.interfaces import Options
from pympeg.descriptors import (
    ChoiceOption, 
    TimeOption, 
    IntOption, 
    FloatOption,
    SampleRateOption,
    BitrateOption,
    DictOption
)

class OutputAudioOptions(Options):

    VALID_FORMATS = {
        'mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'aiff',
        'opus', 'ac3', 'eac3', 'dts',
        'pcm_s16le', 'pcm_s24le', 'pcm_f32le'
    }
    VALID_CODECS = {
        'mp3', 'libmp3lame', 'flac', 'aac', 'libfdk_aac',
        'opus', 'libopus', 'vorbis', 'libvorbis',
        'pcm_s16le', 'pcm_s24le', 'pcm_f32le',
        'ac3', 'eac3', 'dts', 'copy'
    }

    format: str | None
    codec: str | None
    bitrate: int | None
    sample_rate: int | None
    n_channels: int | None
    qscale: float | int | None
    duration: str | None
    metadata: dict[str, str] | None

    format = ChoiceOption(flag='-f', choices=VALID_FORMATS)
    codec = ChoiceOption(flag='-c:a', choices=VALID_CODECS)
    bitrate = BitrateOption(flag='-b:a')
    sample_rate = SampleRateOption(flag='-ar')
    n_channels = IntOption(flag='-ac', min_val=1)
    qscale = FloatOption(flag='-qscale:a', min_val=0)
    duration = TimeOption(flag='-t')
    metadata = DictOption(flag='-metadata')
