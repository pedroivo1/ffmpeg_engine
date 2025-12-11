import pytest
from datetime import timedelta
from pympeg import InputAudioOptions


# Structure: (attribute, input_value, expected_getter, expected_args)
VALID_ATTR_OPTIONS = [

    ('format',      'mp3',          'mp3',                  ['-f', 'mp3']),
    ('format',      'wav',          'wav',                  ['-f', 'wav']),
    ('format',      'pcm_s16le',    'pcm_s16le',            ['-f', 'pcm_s16le']),

    ('codec',       'aac',          'aac',                  ['-c:a', 'aac']),
    ('codec',       'mp3',          'mp3',                  ['-c:a', 'mp3']),
    ('codec',       'pcm_s16le',    'pcm_s16le',            ['-c:a', 'pcm_s16le']),

    ('start_time',  0,                                      '0.000',        ['-ss', '0.000']),
    ('start_time',  10.5,                                   '10.500',       ['-ss', '10.500']),
    ('start_time',  timedelta(minutes=1, seconds=30),       '00:01:30.000', ['-ss', '00:01:30.000']),

    ('duration',    5,                                      '5.000',        ['-t', '5.000']),
    ('duration',    timedelta(seconds=20),                  '00:00:20.000', ['-t', '00:00:20.000']),
    ('duration',    timedelta(hours=20, milliseconds=23),   '20:00:00.023', ['-t', '20:00:00.023']),

    ('n_channels',  1,              1,                      ['-ac', '1']),
    ('n_channels',  2,              2,                      ['-ac', '2']),
    ('n_channels',  6,              6,                      ['-ac', '6']),

    ('sample_rate', 44100,          44100,                  ['-ar', '44100']),
    ('sample_rate', 44100.0,        44100,                  ['-ar', '44100']),
    ('sample_rate', '48000',        48000,                  ['-ar', '48000']),
    ('sample_rate', '44.1k',        44100,                  ['-ar', '44100']),
    ('sample_rate', '48k',          48000,                  ['-ar', '48000']),

    ('stream_loop', -1,             -1,                     ['-stream_loop', '-1']),
    ('stream_loop',  0,              0,                     ['-stream_loop', '0']),
    ('stream_loop',  5,              5,                     ['-stream_loop', '5']),
]

# Structure: (attribute, invalid_value, expected_exception)
INVALID_ATTR_OPTIONS = [

    ('format',      'mp4',          ValueError),
    ('format',      123,            ValueError),

    ('codec',       'h264',         ValueError),

    ('n_channels',   0,             ValueError),
    ('n_channels',  -1,             ValueError),
    ('n_channels',  '2',            TypeError),

    ('sample_rate',  0,             ValueError),
    ('sample_rate', -44100,         ValueError),
    ('sample_rate', 'batata',       ValueError),
    ('sample_rate', '-48k',         ValueError),

    ('stream_loop', -5,             ValueError),
    ('stream_loop', '1',            TypeError),
]


@pytest.mark.parametrize('attr, input_val, expected_getter, _args', VALID_ATTR_OPTIONS)
def test_audio_setters_valid_storage(attr, input_val, expected_getter, _args):
    options = InputAudioOptions()

    setattr(options, attr, input_val)

    assert getattr(options, attr) == expected_getter


@pytest.mark.parametrize('attr, val_inv, exception_type', INVALID_ATTR_OPTIONS)
def test_audio_setters_invalid_raise_error(attr, val_inv, exception_type):
    options = InputAudioOptions()

    with pytest.raises(exception_type):
        setattr(options, attr, val_inv)

    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, _args', VALID_ATTR_OPTIONS)
def test_audio_deleters_functionality(attr, input_val, _expected, _args):
    options = InputAudioOptions()
    setattr(options, attr, input_val)
    
    delattr(options, attr)

    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, expected_args', VALID_ATTR_OPTIONS)
def test_audio_command_args_generation(attr, input_val, _expected, expected_args):
    input_args = {attr: input_val}
    options = InputAudioOptions(**input_args)
    
    flags = options.generate_command_args()

    assert flags == expected_args


def test_audio_full_initialization():
    opts = InputAudioOptions(
        format='s16le',
        codec='pcm_s16le',
        n_channels=2,
        sample_rate='44.1k'
    )

    expected_args = [
        '-f', 's16le',
        '-c:a', 'pcm_s16le',
        '-ac', '2',
        '-ar', '44100'
    ]
    assert opts.generate_command_args() == expected_args


def test_audio_empty_initialization():
    options = InputAudioOptions()
    
    assert options.generate_command_args() == []
