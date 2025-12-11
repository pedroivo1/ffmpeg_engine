import pytest
from datetime import timedelta
from pympeg import VideoOutputOptions

# Estrutura: (atributo, valor_input, getter_esperado, args_esperados)
VALID_VIDEO_OUT_OPTIONS = [
    # format
    ('format',       'mp4',           'mp4',           ['-f', 'mp4']),
    ('format',       'webm',          'webm',          ['-f', 'webm']),
    ('format',       'gif',           'gif',           ['-f', 'gif']),

    # video_codec
    ('video_codec',  'libx264',       'libx264',       ['-c:v', 'libx264']),
    ('video_codec',  'libx265',       'libx265',       ['-c:v', 'libx265']),
    ('video_codec',  'copy',          'copy',          ['-c:v', 'copy']),

    # audio_codec
    ('audio_codec',  'aac',           'aac',           ['-c:a', 'aac']),
    ('audio_codec',  'libmp3lame',    'libmp3lame',    ['-c:a', 'libmp3lame']),

    # bitrate
    ('bitrate',      2000000,         2000000,         ['-b:v', '2000000']),
    ('bitrate',      '2.5m',          2500000,         ['-b:v', '2500000']),
    ('bitrate',      '500k',          500000,          ['-b:v', '500000']),

    # fps
    ('fps',          24,              24,              ['-r', '24']),
    ('fps',          29.97,           29.97,           ['-r', '29.97']),
    ('fps',          60,              60,              ['-r', '60']),

    # size
    ('size',         '1920x1080',     '1920x1080',     ['-s', '1920x1080']),
    ('size',         'hd720',         'hd720',         ['-s', 'hd720']),
    ('size',         '4k',            '4k',            ['-s', '4k']),

    # pixel_format
    ('pixel_format', 'yuv420p',       'yuv420p',       ['-pix_fmt', 'yuv420p']),
    ('pixel_format', 'rgb24',         'rgb24',         ['-pix_fmt', 'rgb24']),

    # qscale
    ('qscale',       0,               0,               ['-qscale:v', '0']),
    ('qscale',       5,               5,               ['-qscale:v', '5']),
    ('qscale',       2.5,             2.5,             ['-qscale:v', '2.5']),

    # duration
    ('duration',     10,              '10.000',        ['-t', '10.000']),
    ('duration',     timedelta(minutes=1), '00:01:00.000', ['-t', '00:01:00.000']),

    # preset
    ('preset',       'fast',          'fast',          ['-preset', 'fast']),
    ('preset',       'slow',          'slow',          ['-preset', 'slow']),
    ('preset',       'ultrafast',     'ultrafast',     ['-preset', 'ultrafast']),

    # crf
    ('crf',          0,               0,               ['-crf', '0']),
    ('crf',          23,              23,              ['-crf', '23']),
    ('crf',          51,              51,              ['-crf', '51']),

    # metadata
    ('metadata',     {'title': 'My Video'}, {'title': 'My Video'}, ['-metadata', 'title=My Video']),

    # movflags
    ('movflags',     'faststart',     'faststart',     ['-movflags', 'faststart']),
    ('movflags',     'frag_keyframe', 'frag_keyframe', ['-movflags', 'frag_keyframe']),

    # tune
    ('tune',         'film',          'film',          ['-tune', 'film']),
    ('tune',         'animation',     'animation',     ['-tune', 'animation']),
]

# Estrutura: (atributo, valor_invalido, tipo_excecao)
INVALID_VIDEO_OUT_OPTIONS = [
    ('format',       'batata',        ValueError),
    ('video_codec',  'h265',          ValueError),
    ('audio_codec',  'h264',          ValueError),
    ('bitrate',      0,               ValueError),
    ('bitrate',      'batata',        ValueError),
    ('bitrate',      -500,            ValueError),
    ('fps',          0,               ValueError),
    ('fps',          -30,             ValueError),
    ('size',         'batata',        ValueError),
    ('size',         '',              ValueError),
    ('pixel_format', 'invalid',       ValueError),
    ('qscale',       -1,              ValueError),
    ('preset',       'invalid',       ValueError),
    ('crf',          -1,              ValueError),
    ('crf',          52,              ValueError),
    ('metadata',     'not a dict',    TypeError),
    ('movflags',     'invalid',       ValueError),
    ('tune',         'invalid',       ValueError),
]


@pytest.mark.parametrize('attr, input_val, expected_getter, _args', VALID_VIDEO_OUT_OPTIONS)
def test_video_out_setters_valid_storage(attr, input_val, expected_getter, _args):
    options = VideoOutputOptions()
    setattr(options, attr, input_val)
    assert getattr(options, attr) == expected_getter


@pytest.mark.parametrize('attr, val_inv, exception_type', INVALID_VIDEO_OUT_OPTIONS)
def test_video_out_setters_invalid_raise_error(attr, val_inv, exception_type):
    options = VideoOutputOptions()
    with pytest.raises(exception_type):
        setattr(options, attr, val_inv)
    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, expected_args', VALID_VIDEO_OUT_OPTIONS)
def test_video_out_command_args_generation(attr, input_val, _expected, expected_args):
    input_args = {attr: input_val}
    options = VideoOutputOptions(**input_args)
    flags = options.generate_command_args()
    assert flags == expected_args


def test_video_out_full_initialization():
    opts = VideoOutputOptions(
        format='mp4',
        video_codec='libx264',
        audio_codec='aac',
        preset='fast',
        crf=23,
        movflags='faststart'
    )

    assert opts.generate_command_args() == [
        '-f', 'mp4', 
        '-c:v', 'libx264', 
        '-c:a', 'aac', 
        '-preset', 'fast', 
        '-crf', '23', 
        '-movflags', 'faststart'
    ]


def test_video_out_empty_initialization():
    options = VideoOutputOptions()

    assert options.generate_command_args() == []
