import pytest
from datetime import timedelta
from pympeg import InputVideoOptions

# Structure: (atributo, valor_input, getter_esperado, args_esperados)
VALID_VIDEO_OPTIONS = [
    ('format',       'mp4',           'mp4',                ['-f', 'mp4']),
    ('format',       'rawvideo',      'rawvideo',           ['-f', 'rawvideo']),

    ('codec',        'libx264',       'libx264',            ['-c:v', 'libx264']),
    ('codec',        'copy',          'copy',               ['-c:v', 'copy']),

    ('start_time',   0,               '0.000',              ['-ss', '0.000']),
    ('start_time',   10.5,            '10.500',             ['-ss', '10.500']),
    ('start_time',   timedelta(seconds=90), '00:01:30.000', ['-ss', '00:01:30.000']),

    ('duration',     10,              '10.000',             ['-t', '10.000']),
    ('duration',     timedelta(minutes=1), '00:01:00.000',  ['-t', '00:01:00.000']),

    ('fps',          24,              24,                   ['-r', '24']),
    ('fps',          29.97,           29.97,                ['-r', '29.97']),

    ('size',         '1920x1080',     '1920x1080',          ['-s', '1920x1080']),
    ('size',         'hd720',         'hd720',              ['-s', 'hd720']),
    ('size',         'HD1080',        'hd1080',             ['-s', 'hd1080']),
    ('size',         '4k',            '4k',                 ['-s', '4k']),

    ('pixel_format', 'yuv420p',       'yuv420p',            ['-pix_fmt', 'yuv420p']),

    ('stream_loop',  -1,              -1,                   ['-stream_loop', '-1']),
    ('stream_loop',  0,               0,                    ['-stream_loop', '0']),
]

# Structure: (atributo, valor_invalido, tipo_excecao)
INVALID_VIDEO_OPTIONS = [
    ('format',       'mp3',           ValueError),
    ('codec',        'aac',           ValueError),

    ('fps',          0,               ValueError),
    ('fps',          -30,             ValueError),
    ('fps',          '24',            TypeError),

    ('size',         'batata',        ValueError),
    ('size',         '100x',          ValueError),
    ('size',         'x100',          ValueError),
    ('size',         '',              ValueError),

    ('pixel_format', 'invalid_fmt',   ValueError),

    ('stream_loop',  -5,              ValueError),
]


@pytest.mark.parametrize('attr, input_val, expected_getter, _args', VALID_VIDEO_OPTIONS)
def test_video_setters_valid_storage(attr, input_val, expected_getter, _args):
    options = InputVideoOptions()

    setattr(options, attr, input_val)

    assert getattr(options, attr) == expected_getter


@pytest.mark.parametrize('attr, val_inv, exception_type', INVALID_VIDEO_OPTIONS)
def test_video_setters_invalid_raise_error(attr, val_inv, exception_type):
    options = InputVideoOptions()

    with pytest.raises(exception_type):
        setattr(options, attr, val_inv)

    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, expected_args', VALID_VIDEO_OPTIONS)
def test_video_command_args_generation(attr, input_val, _expected, expected_args):
    input_args = {attr: input_val}
    options = InputVideoOptions(**input_args)

    flags = options.generate_command_args()

    assert flags == expected_args


def test_video_full_initialization():
    opts = InputVideoOptions(
        format='mov',
        codec='prores',
        fps=24,
        size='1920x1080'
    )

    assert opts.generate_command_args() == [
        '-f', 'mov', '-c:v', 'prores', '-r', '24', '-s', '1920x1080']


def test_video_empty_initialization():
    options = InputVideoOptions()
    assert options.generate_command_args() == []
