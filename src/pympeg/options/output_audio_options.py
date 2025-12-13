from pympeg.interfaces import Options
from pympeg.constants import AUDIO_FORMATS, AUDIO_CODECS
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

    format: str | None
    codec: str | None
    bitrate: int | None
    sample_rate: int | None
    n_channels: int | None
    qscale: float | int | None
    duration: str | None
    metadata: dict[str, str] | None

    format = ChoiceOption(flag='-f', choices=AUDIO_FORMATS)
    codec = ChoiceOption(flag='-c:a', choices=AUDIO_CODECS | {'copy'})
    bitrate = BitrateOption(flag='-b:a')
    sample_rate = SampleRateOption(flag='-ar')
    n_channels = IntOption(flag='-ac', min_val=1)
    qscale = FloatOption(flag='-qscale:a', min_val=0)
    duration = TimeOption(flag='-t')
    metadata = DictOption(flag='-metadata')
