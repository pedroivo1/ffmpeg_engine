from pympeg.interfaces import Options
from pympeg.descriptors import (
    ChoiceOption, 
    TimeOption, 
    IntOption, 
    SampleRateOption  # O novo que criamos acima
)

class InputAudioOptions(Options):
    
    # Constantes
    AUDIO_FORMATS = {
        'mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'aiff',
        's16le', 'f32be', 'pcm_s16le', 'alsa', 'pulse'
    }
    AUDIO_CODECS = {
        'mp3', 'flac', 'aac', 's16le', 'f32be', 'pcm_s16le'
    }

    format: str | None
    codec: str | None
    start_time: str | None
    duration: str | None
    n_channels: int | None
    sample_rate: int | None
    stream_loop: int | None

    format = ChoiceOption(flag='-f', choices=AUDIO_FORMATS)
    codec = ChoiceOption(flag='-c:a', choices=AUDIO_CODECS)
    start_time = TimeOption(flag='-ss')
    duration = TimeOption(flag='-t')
    n_channels = IntOption(flag='-ac', min_val=1)
    sample_rate = SampleRateOption(flag='-ar')
    stream_loop = IntOption(flag='-stream_loop', min_val=-1)
