import pytest
from pympeg import OutputImageOptions


# Structure: (atributo, valor_input, getter_esperado, args_esperados)
VALID_IMAGE_OPTIONS = [
    ('format',             'png',           'png',           ['-f', 'png']),
    ('format',             'image2',        'image2',        ['-f', 'image2']),
    ('format',             'jpeg',          'jpeg',          ['-f', 'jpeg']),

    ('codec',              'png',           'png',           ['-c:v', 'png']),
    ('codec',              'mjpeg',         'mjpeg',         ['-c:v', 'mjpeg']),
    ('codec',              'libwebp',       'libwebp',       ['-c:v', 'libwebp']),
    ('codec',              'copy',          'copy',          ['-c:v', 'copy']),

    ('qscale',             0,               0,               ['-qscale:v', '0']),
    ('qscale',             2,               2,               ['-qscale:v', '2']),
    ('qscale',             5.5,             5.5,             ['-qscale:v', '5.5']),

    ('frames',             1,               1,               ['-frames:v', '1']),
    ('frames',             10,              10,              ['-frames:v', '10']),

    ('framerate',          24,              24,              ['-r', '24']),
    ('framerate',          29.97,           29.97,           ['-r', '29.97']),

    ('size',               '1920x1080',     '1920x1080',     ['-s', '1920x1080']),
    ('size',               'hd720',         'hd720',         ['-s', 'hd720']),
    ('size',               'HD1080',        'hd1080',        ['-s', 'hd1080']), # Teste lowercase
    ('size',               '4k',            '4k',            ['-s', '4k']),

    ('pixel_format',       'yuv420p',       'yuv420p',       ['-pix_fmt', 'yuv420p']),
    ('pixel_format',       'rgb24',         'rgb24',         ['-pix_fmt', 'rgb24']),
    ('pixel_format',       'rgba',          'rgba',          ['-pix_fmt', 'rgba']),

    ('compression_level',  0,               0,               ['-compression_level', '0']),
    ('compression_level',  50,              50,              ['-compression_level', '50']),
    ('compression_level',  100,             100,             ['-compression_level', '100']),
]

# Structure: (atributo, valor_invalido, tipo_excecao)
INVALID_IMAGE_OPTIONS = [
    ('format',             'mp4',           ValueError),
    ('codec',              'h264',          ValueError),
    
    ('qscale',             -1,              ValueError),
    ('qscale',             '5',             TypeError),
    
    ('frames',             0,               ValueError),
    ('frames',             -5,              ValueError),
    ('frames',             1.5,             TypeError),
    
    ('framerate',          0,               ValueError),
    ('framerate',          -10,             ValueError),
    
    ('size',               'batata',        ValueError),
    ('size',               '100x',          ValueError),
    ('size',               '',              ValueError),
    
    ('pixel_format',       'invalid',       ValueError),
    
    ('compression_level',  -1,              ValueError),
    ('compression_level',  101,             ValueError),
    ('compression_level',  50.5,            TypeError),
]


@pytest.mark.parametrize('attr, input_val, expected_getter, _args', VALID_IMAGE_OPTIONS)
def test_image_setters_valid_storage(attr, input_val, expected_getter, _args):
    options = OutputImageOptions()
    setattr(options, attr, input_val)
    assert getattr(options, attr) == expected_getter


@pytest.mark.parametrize('attr, val_inv, exception_type', INVALID_IMAGE_OPTIONS)
def test_image_setters_invalid_raise_error(attr, val_inv, exception_type):
    options = OutputImageOptions()
    with pytest.raises(exception_type):
        setattr(options, attr, val_inv)
    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, expected_args', VALID_IMAGE_OPTIONS)
def test_image_command_args_generation(attr, input_val, _expected, expected_args):
    input_args = {attr: input_val}
    options = OutputImageOptions(**input_args)
    flags = options.generate_command_args()
    assert flags == expected_args


def test_image_full_initialization():
    opts = OutputImageOptions(
        format='png', codec='png', qscale=2, size='1920x1080',
        compression_level=90
    )

    assert opts.generate_command_args() == [
        '-f', 'png', '-c:v', 'png', '-qscale:v', '2', '-s', '1920x1080', 
        '-compression_level', '90'
    ]


def test_image_empty_initialization():
    options = OutputImageOptions()
    assert options.generate_command_args() == []
