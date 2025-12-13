import pytest
from pympeg import GlobalOptions


# Structure: (attribute, input_value, expected_getter, expected_args)
VALID_ATTR_OPTIONS = [
    ('overwrite',   True,       True,       ['-y']),
    ('overwrite',   False,      False,      ['-n']),

    ('hide_banner', True,       True,       ['-hide_banner']),

    ('loglevel',    'quiet',    'quiet',    ['-loglevel', 'quiet']),
    ('loglevel',    'panic',    'panic',    ['-loglevel', 'panic']),
    ('loglevel',    'fatal',    'fatal',    ['-loglevel', 'fatal']),
    ('loglevel',    'error',    'error',    ['-loglevel', 'error']),
    ('loglevel',    'warning',  'warning',  ['-loglevel', 'warning']),
    ('loglevel',    'info',     'info',     ['-loglevel', 'info']),
    ('loglevel',    'verbose',  'verbose',  ['-loglevel', 'verbose']),
    ('loglevel',    'debug',    'debug',    ['-loglevel', 'debug']),
    ('loglevel',    'trace',    'trace',    ['-loglevel', 'trace']),

    ('stats',       True,       True,       ['-stats']),
    ('stats',       False,      False,      ['-nostats']) 
]

# Structure: (attribute, invalid_value, expected_exception)
INVALID_ATTR_OPTIONS = [
    ('overwrite',   'invalid value', TypeError),
    ('hide_banner', 'invalid value', TypeError),
    ('loglevel',    'invalid value', ValueError),
    ('stats',       'invalid value', TypeError),
]


@pytest.mark.parametrize('attr, input_val, expected_getter, _args', VALID_ATTR_OPTIONS)
def test_global_setters_valid_storage(attr, input_val, expected_getter, _args):
    options = GlobalOptions()
    setattr(options, attr, input_val)
    assert getattr(options, attr) == expected_getter


@pytest.mark.parametrize('attr, val_inv, exception_type', INVALID_ATTR_OPTIONS)
def test_global_setters_invalid_raise_error(attr, val_inv, exception_type):
    options = GlobalOptions()
    with pytest.raises(exception_type):
        setattr(options, attr, val_inv)
    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, _args', VALID_ATTR_OPTIONS)
def test_global_deleters_functionality(attr, input_val, _expected, _args):
    options = GlobalOptions()

    setattr(options, attr, input_val)
    delattr(options, attr)

    assert getattr(options, attr) is None


@pytest.mark.parametrize('attr, input_val, _expected, expected_args', VALID_ATTR_OPTIONS)
def test_global_command_args_generation(attr, input_val, _expected, expected_args):
    input_args = {attr: input_val}
    flag_generator = GlobalOptions(**input_args)
    flags = flag_generator.generate_command_args()
    assert flags == expected_args


def test_global_multiple_attrs_combined():
    opts = GlobalOptions(
        overwrite=True,
        hide_banner=True, 
        loglevel='info',
        stats=False
    )

    assert opts.generate_command_args() == [
        '-y', '-hide_banner', '-loglevel', 'info', '-nostats'
    ]


def test_global_empty_initialization():
    options = GlobalOptions()
    assert options.generate_command_args() == []
