import pytest
from datetime import timedelta
from pympeg import InputImageOptions

# Structure: (attribute, input_value, expected_getter, expected_args)
VALID_ATTR_OPTIONS = [

    ('format',      'png',       'png',       ['-f', 'png']),
    ('format',      'image2',    'image2',    ['-f', 'image2']),
    ('format',      'v4l2',      'v4l2',      ['-f', 'v4l2']),

    ('loop',         0,           0,          ['-loop', '0']),
    ('loop',         1,           1,          ['-loop', '1']),
    ('loop',        -1,          -1,          ['-loop', '-1']),

    ('framerate',    30,          30,         ['-framerate', '30']),
    ('framerate',    60,          60,         ['-framerate', '60']),
    ('framerate',    29.97,       29.97,      ['-framerate', '29.97']),

    ('start_time',   10,                                                              '10.000',       ['-ss', '10.000']),
    ('start_time',   1.5,                                                             '1.500',        ['-ss', '1.500']),
    ('start_time',   timedelta(seconds=90.5),                                         '00:01:30.500', ['-ss', '00:01:30.500']),
    ('start_time',   timedelta(hours=1),                                              '01:00:00.000', ['-ss', '01:00:00.000']),
    ('start_time',   timedelta(hours=1, minutes=32, seconds=45, milliseconds=287),    '01:32:45.287', ['-ss', '01:32:45.287']),
]


# Structure: (attribute, invalid_value, expected_exception)
INVALID_ATTR_OPTIONS = [

    ('format',      'mp4',                  ValueError),
    ('format',      123,                    ValueError),

    ('loop',        5,                      ValueError),
    ('loop',        '1',                    TypeError),

    ('framerate',   0,                      ValueError),
    ('framerate',  -10,                     ValueError),
    ('framerate',   '30',                   TypeError),

    ('start_time', -5,                      ValueError),
    ('start_time', 'agora',                 TypeError),
    ('start_time',  timedelta(days=-1),     ValueError),
]


@pytest.mark.parametrize('attr, input_val, expected_getter, _args', VALID_ATTR_OPTIONS)
def test_image_setters_valid_storage(attr, input_val, expected_getter, _args):
    '''Tests that valid values are stored correctly (including transformations).'''
    options = InputImageOptions()
    
    setattr(options, attr, input_val)
    
    assert getattr(options, attr) == expected_getter


@pytest.mark.parametrize('attr, val_inv, exception_type', INVALID_ATTR_OPTIONS)
def test_image_setters_invalid_raise_error(attr, val_inv, exception_type):
    '''Tests that invalid values raise the correct Exception type.'''
    options = InputImageOptions()
    
    with pytest.raises(exception_type):
        setattr(options, attr, val_inv)
    
    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, _args', VALID_ATTR_OPTIONS)
def test_image_deleters_functionality(attr, input_val, _expected, _args):
    '''Tests that deleters correctly reset attributes to None.'''
    options = InputImageOptions()
    setattr(options, attr, input_val)
    
    delattr(options, attr)
    
    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, expected_args', VALID_ATTR_OPTIONS)
def test_image_command_args_generation(attr, input_val, _expected, expected_args):
    '''Tests that the correct command line arguments are generated.'''
    input_args = {attr: input_val}
    options = InputImageOptions(**input_args)
    
    assert options.generate_command_args() == expected_args


def test_image_full_initialization():
    '''Tests initialization with multiple parameters combined.'''
    opts = InputImageOptions(
        format='png',
        start_time=timedelta(seconds=10),
        loop=1,
        framerate=30
    )
    
    expected_args = [
        '-f', 'png',
        '-ss', '00:00:10.000',
        '-loop', '1',
        '-framerate', '30'
    ]
    
    assert opts.generate_command_args() == expected_args


def test_image_empty_initialization():
    '''Tests that initializing with no arguments produces an empty command list.'''
    options = InputImageOptions()
    assert options.generate_command_args() == []
