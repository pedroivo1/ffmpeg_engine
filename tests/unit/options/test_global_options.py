import pytest
import logging
from pympeg import GlobalOptions


VALID_GLOBAL_OPTIONS = [
    # none
    (GlobalOptions, {}, []),

    # overwrite only
    (GlobalOptions, {'overwrite': 'no'}, ['-n']),
    (GlobalOptions, {'overwrite': 'yes'}, ['-y']),

    # hide_banner only
    (GlobalOptions, {'hide_banner': 'yes',}, ['-hide_banner']),

    # loglevel only
    (GlobalOptions, {'loglevel': 'quiet',}, ['-loglevel', 'quiet']),
    (GlobalOptions, {'loglevel': 'panic',}, ['-loglevel', 'panic']),
    (GlobalOptions, {'loglevel': 'fatal',}, ['-loglevel', 'fatal']),
    (GlobalOptions, {'loglevel': 'error',}, ['-loglevel', 'error']),
    (GlobalOptions, {'loglevel': 'warning',}, ['-loglevel', 'warning']),
    (GlobalOptions, {'loglevel': 'info',}, ['-loglevel', 'info']),
    (GlobalOptions, {'loglevel': 'verbose',}, ['-loglevel', 'verbose']),
    (GlobalOptions, {'loglevel': 'debug',}, ['-loglevel', 'debug']),
    (GlobalOptions, {'loglevel': 'trace',}, ['-loglevel', 'trace']),

    # stats only
    (GlobalOptions, {'stats': 'no',}, ['-nostats']),
    (GlobalOptions, {'stats': 'yes',}, ['-stats']),

    # all
    (GlobalOptions,
        {'overwrite': 'no', 'hide_banner': 'yes', 'loglevel': 'warning', 'stats': 'yes'},
        ['-n', '-hide_banner', '-loglevel', 'warning', '-stats'])
]

INVALID_GLOBAL_OPTIONS = [
    (GlobalOptions, {'overwrite': 'talvez'}, []),
    (GlobalOptions, {'hide_banner': 'maybe'}, []),
    (GlobalOptions, {'loglevel': 'super_alto'}, []),
    (GlobalOptions, {'stats': 'as vezes'}, []),
]


@pytest.mark.parametrize('global_flags, input_args, expected_output', VALID_GLOBAL_OPTIONS)
def test_global_flags_parameters(global_flags, input_args, expected_output):
    flag_generator = global_flags(**input_args)

    flags = flag_generator.generate_command_args()

    assert flags == expected_output


@pytest.mark.parametrize('global_flags, input_args, expected_output', VALID_GLOBAL_OPTIONS)
def test_global_flags_logs_nothing_on_valid_input(caplog, global_flags, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = global_flags(**input_args)

    flag_generator.generate_command_args()

    assert not caplog.text


@pytest.mark.parametrize('global_flags, input_args, expected_output', INVALID_GLOBAL_OPTIONS)
def test_global_flags_logs_on_invalid_input(caplog, global_flags, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = global_flags(**input_args)
    attr_name, value_passed = list(input_args.items())[0]

    flag_generator.generate_command_args()
    expected_msg = f'Invalid value \'{value_passed}\' received for \'{attr_name}\' on GlobalOptions.'

    assert expected_msg in caplog.text
