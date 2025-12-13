import pytest
from datetime import timedelta
from pympeg import OutputAudioOptions


# Structure: (atributo, valor_input, getter_esperado, args_esperados)
VALID_AUDIO_OUT_OPTIONS = [
    ('format',       'mp3',           'mp3',           ['-f', 'mp3']),
    ('format',       'wav',           'wav',           ['-f', 'wav']),
    ('format',       'pcm_s16le',     'pcm_s16le',     ['-f', 'pcm_s16le']),

    ('codec',        'aac',           'aac',           ['-c:a', 'aac']),
    ('codec',        'libmp3lame',    'libmp3lame',    ['-c:a', 'libmp3lame']),
    ('codec',        'copy',          'copy',          ['-c:a', 'copy']),

    ('bitrate',      128000,          128000,          ['-b:a', '128000']),
    ('bitrate',      '128k',          128000,          ['-b:a', '128000']),
    ('bitrate',      '320K',          320000,          ['-b:a', '320000']),
    ('bitrate',      '1.5m',          1500000,         ['-b:a', '1500000']),
    ('bitrate',      '64000',         64000,           ['-b:a', '64000']),

    ('sample_rate',  44100,           44100,           ['-ar', '44100']),
    ('sample_rate',  44100.0,         44100,           ['-ar', '44100']),
    ('sample_rate',  '48k',           48000,           ['-ar', '48000']),

    ('n_channels',   1,               1,               ['-ac', '1']),
    ('n_channels',   2,               2,               ['-ac', '2']),
    ('n_channels',   6,               6,               ['-ac', '6']),

    ('qscale',       0,               0,               ['-qscale:a', '0']),
    ('qscale',       5,               5,               ['-qscale:a', '5']),
    ('qscale',       9.5,             9.5,             ['-qscale:a', '9.5']),

    ('duration',     5,               '5.000',         ['-t', '5.000']),
    ('duration',     timedelta(seconds=20), '00:00:20.000', ['-t', '00:00:20.000']),

    ('metadata',     {'title': 'Song'}, {'title': 'Song'}, ['-metadata', 'title=Song']),
    ('metadata',     {'a': '1', 'b': '2'}, {'a': '1', 'b': '2'}, ['-metadata', 'a=1', '-metadata', 'b=2']),
]

# Structure: (atributo, valor_invalido, tipo_excecao)
INVALID_AUDIO_OUT_OPTIONS = [
    ('format',       'mp4',           ValueError),
    ('format',       'invalid',       ValueError),
    
    ('codec',        'h264',          ValueError),
    
    ('bitrate',      0,               ValueError),
    ('bitrate',      -128,            ValueError),
    ('bitrate',      'batata',        ValueError),
    ('bitrate',      '128kbps',       ValueError),
    
    ('sample_rate',  0,               ValueError),
    ('sample_rate',  -44100,          ValueError),
    ('sample_rate',  'xyz',           ValueError),
    
    ('n_channels',   0,               ValueError),
    ('n_channels',   -1,              ValueError),
    
    ('qscale',       -1,              ValueError),
    
    ('metadata',     'not a dict',    TypeError),
    ('metadata',     123,             TypeError),
]


@pytest.mark.parametrize('attr, input_val, expected_getter, _args', VALID_AUDIO_OUT_OPTIONS)
def test_audio_out_setters_valid_storage(attr, input_val, expected_getter, _args):
    options = OutputAudioOptions()
    setattr(options, attr, input_val)
    assert getattr(options, attr) == expected_getter


@pytest.mark.parametrize('attr, val_inv, exception_type', INVALID_AUDIO_OUT_OPTIONS)
def test_audio_out_setters_invalid_raise_error(attr, val_inv, exception_type):
    options = OutputAudioOptions()
    with pytest.raises(exception_type):
        setattr(options, attr, val_inv)
    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, expected_args', VALID_AUDIO_OUT_OPTIONS)
def test_audio_out_command_args_generation(attr, input_val, _expected, expected_args):
    input_args = {attr: input_val}
    options = OutputAudioOptions(**input_args)
    flags = options.generate_command_args()

    if attr == 'metadata':
        assert sorted(flags) == sorted(expected_args)
    else:
        assert flags == expected_args


def test_audio_out_full_initialization():
    opts = OutputAudioOptions(
        format='mp3', codec='libmp3lame', bitrate='192k', sample_rate=44100,
        n_channels=2
    )

    assert opts.generate_command_args() == [
        '-f', 'mp3', '-c:a', 'libmp3lame', '-b:a', '192000', '-ar', '44100',
        '-ac', '2'
    ]


def test_audio_out_empty_initialization():
    options = OutputAudioOptions()
    
    assert options.generate_command_args() == []
