import pytest
from pympeg import GlobalOptions


VALID_ATTR_OPTIONS = [
    ('overwrite',   'yes',      ['-y']),
    ('overwrite',   'no',       ['-n']),
    ('hide_banner', 'yes',      ['-hide_banner']),
    ('loglevel',    'quiet',    ['-loglevel', 'quiet']),
    ('loglevel',    'panic',    ['-loglevel', 'panic']),
    ('loglevel',    'fatal',    ['-loglevel', 'fatal']),
    ('loglevel',    'error',    ['-loglevel', 'error']),
    ('loglevel',    'warning',  ['-loglevel', 'warning']),
    ('loglevel',    'info',     ['-loglevel', 'info']),
    ('loglevel',    'verbose',  ['-loglevel', 'verbose']),
    ('loglevel',    'debug',    ['-loglevel', 'debug']),
    ('loglevel',    'trace',    ['-loglevel', 'trace']),
    ('stats',       'yes',      ['-stats']),
    ('stats',       'no',       ['-nostats']) 
]

INVALID_ATTR_OPTIONS = [
    ('overwrite',   'invalid default'),
    ('hide_banner', 'invalid default'),
    ('loglevel',    'invalid default'),
    ('stats',       'invalid default'),
]


@pytest.mark.parametrize('attr, val, _args', VALID_ATTR_OPTIONS)
def test_setters_with_valid_attr(attr, val, _args):
    options = GlobalOptions()

    setattr(options, attr, val)

    assert getattr(options, attr) == val


@pytest.mark.parametrize('attr, val_inv', INVALID_ATTR_OPTIONS)
def test_setters_with_invalid_attr(attr, val_inv):
    opts = GlobalOptions()

    with pytest.raises(ValueError):
        setattr(opts, attr, val_inv)

    assert getattr(opts, attr) is None



@pytest.mark.parametrize('attr, val, _args', VALID_ATTR_OPTIONS)
def test_deleters_with_valid_attr(attr, val, _args):
    options = GlobalOptions()

    setattr(options, attr, val)
    delattr(options, attr)

    assert getattr(options, attr) is None



@pytest.mark.parametrize('attr, val, args', VALID_ATTR_OPTIONS)
def test_generate_command_args_with_valid_attr(attr, val, args):
    input_args = {attr: val}
    flag_generator = GlobalOptions(**input_args)
    
    flags = flag_generator.generate_command_args()

    assert flags == args


def test_multiple_attrs_combined():
    """Testa combinação de vários atributos."""
    opts = GlobalOptions(
        overwrite='yes',
        hide_banner='yes', 
        loglevel='info',
        stats='no'
    )
    
    assert opts.overwrite == 'yes'
    assert opts.hide_banner == 'yes'
    assert opts.loglevel == 'info'
    assert opts.stats == 'no'
    assert opts.generate_command_args() == [
        '-y', '-hide_banner', '-loglevel', 'info', '-nostats'
    ]
