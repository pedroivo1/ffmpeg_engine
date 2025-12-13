import pytest
from datetime import timedelta
from pympeg.descriptors import *


class MockFfmpegOptions:

    generic = BaseOption('-gen')
    codec = ChoiceOption('-c:v', choices={'h264', 'hevc'})
    overwrite = BoolOption(true_flag='-y', false_flag='-n')
    banner = BoolOption(true_flag='-hide_banner')
    fps = IntOption('-r', min_val=1, max_val=120)
    speed = FloatOption('-speed', min_val=0.1, max_val=10.0)
    start = TimeOption('-ss')
    ar = SampleRateOption('-ar')
    size = VideoSizeOption('-s', valid_sizes={'hd1080', '4k'})
    bitrate = BitrateOption('-b:v')
    metadata = DictOption('-metadata')


@pytest.fixture
def mock_opts():
    return MockFfmpegOptions()

# ===========================================================================
# BaseOption
# ===========================================================================
def test_base_option_lifecycle(mock_opts):
    assert mock_opts.generic is None

    mock_opts.generic = "teste"
    assert mock_opts.generic == "teste"
    
    assert mock_opts.__dict__['generic'] == "teste"

    descriptor = MockFfmpegOptions.generic
    assert descriptor.to_args("teste") == ['-gen', 'teste']

    del mock_opts.generic
    assert mock_opts.generic is None
    assert 'generic' not in mock_opts.__dict__


def test_base_option_set_none_removes_attr(mock_opts):
    mock_opts.generic = "algo"
    assert mock_opts.generic is not None
    
    mock_opts.generic = None
    assert mock_opts.generic is None
    assert 'generic' not in mock_opts.__dict__

# ===========================================================================
# ChoiceOption
# ===========================================================================
@pytest.mark.parametrize("value", ['h264', 'hevc'])
def test_choice_option_valid(mock_opts, value):
    mock_opts.codec = value
    assert mock_opts.codec == value


def test_choice_option_invalid(mock_opts):
    with pytest.raises(ValueError, match="not allowed"):
        mock_opts.codec = 'vp9'


# ===========================================================================
# BoolOption
# ===========================================================================
@pytest.mark.parametrize("input_val, expected_args", [
    (True, ['-y']),
    (False, ['-n']),
])
def test_bool_option_args_double_flag(mock_opts, input_val, expected_args):
    """Testa booleano que tem flag para True E para False (ex: overwrite)."""
    desc = MockFfmpegOptions.overwrite
    assert desc.to_args(input_val) == expected_args


@pytest.mark.parametrize("input_val, expected_args", [
    (True, ['-hide_banner']),
    (False, []),
])
def test_bool_option_args_single_flag(mock_opts, input_val, expected_args):
    desc = MockFfmpegOptions.banner
    assert desc.to_args(input_val) == expected_args


def test_bool_option_type_validation(mock_opts):
    with pytest.raises(TypeError, match="must be bool"):
        mock_opts.overwrite = "True"


# ===========================================================================
# IntOption
# ===========================================================================
@pytest.mark.parametrize("value", [1, 60, 120])
def test_int_option_valid(mock_opts, value):
    mock_opts.fps = value
    assert mock_opts.fps == value


@pytest.mark.parametrize("invalid_val, error_type", [
    (0, ValueError),
    (121, ValueError),
    ("60", TypeError),
    (60.5, TypeError),
    (True, TypeError),
])
def test_int_option_invalid(mock_opts, invalid_val, error_type):
    with pytest.raises(error_type):
        mock_opts.fps = invalid_val


# ===========================================================================
# FloatOption
# ===========================================================================
@pytest.mark.parametrize("value, expected_type", [
    (5.5, float),
    (5, int),
])
def test_float_option_valid_and_types(mock_opts, value, expected_type):
    mock_opts.speed = value
    assert mock_opts.speed == value
    assert isinstance(mock_opts.speed, expected_type)


@pytest.mark.parametrize("invalid_val, error_type", [
    (0.05, ValueError),
    (10.1, ValueError),
    ("5.5", TypeError),
])
def test_float_option_invalid(mock_opts, invalid_val, error_type):
    with pytest.raises(error_type):
        mock_opts.speed = invalid_val


# ===========================================================================
# TimeOption
# ===========================================================================
@pytest.mark.parametrize("input_val, expected_str", [
    (10, "10.000"),
    (10.5, "10.500"),
    (timedelta(seconds=10), "00:00:10.000"),
    (timedelta(hours=1, seconds=30.5), "01:00:30.500"),
    (0, "0.000"),
])
def test_time_option_formatting(mock_opts, input_val, expected_str):
    """Testa a lógica de formatação do validador."""
    mock_opts.start = input_val
    assert mock_opts.start == expected_str


@pytest.mark.parametrize("invalid_val, error_type", [
    (-10, ValueError),
    (timedelta(seconds=-1), ValueError),
    ("10:00", TypeError),
])
def test_time_option_errors(mock_opts, invalid_val, error_type):
    with pytest.raises(error_type):
        mock_opts.start = invalid_val


# ===========================================================================
# SampleRateOption
# ===========================================================================
@pytest.mark.parametrize("input_val, expected_int", [
    (44100, 44100),
    (48000.0, 48000),
    ("44100", 44100),
    ("44.1k", 44100),
    ("48k", 48000),
    ("44.1K", 44100),
])
def test_sample_rate_parsing(mock_opts, input_val, expected_int):
    mock_opts.ar = input_val
    assert mock_opts.ar == expected_int
    assert isinstance(mock_opts.ar, int)


@pytest.mark.parametrize("invalid_val", [
    "invalid",
    "44..1k",
    -100,
    0
])
def test_sample_rate_errors(mock_opts, invalid_val):
    with pytest.raises((ValueError, TypeError)):
        mock_opts.ar = invalid_val


# ===========================================================================
# VideoSizeOption
# ===========================================================================
@pytest.mark.parametrize("input_val, expected", [
    ('hd1080', 'hd1080'),
    ('4K', '4k'),
    ('1920x1080', '1920x1080'),
    ('320x240', '320x240'),
])
def test_video_size_valid(mock_opts, input_val, expected):
    mock_opts.size = input_val
    assert mock_opts.size == expected


@pytest.mark.parametrize("invalid_val", [
    'vga',
    '100',
    '100x',
    'x100',
    'widthxheight',
    1080
])
def test_video_size_invalid(mock_opts, invalid_val):
    with pytest.raises(ValueError, match="Invalid video size"):
        mock_opts.size = invalid_val


# ===========================================================================
# BitrateOption
# ===========================================================================
@pytest.mark.parametrize("input_val, expected_int", [
    (1000, 1000),
    ('1000', 1000),
    ('1k', 1000),
    ('1.5k', 1500),
    ('1M', 1000000),
    ('1.5M', 1500000),
    ('  2k  ', 2000),
])
def test_bitrate_valid(mock_opts, input_val, expected_int):
    mock_opts.bitrate = input_val
    assert mock_opts.bitrate == expected_int
    assert isinstance(mock_opts.bitrate, int)


@pytest.mark.parametrize("invalid_val, error_type", [
    (0, ValueError),
    (-100, ValueError),
    ('0k', ValueError),
    ('invalid', ValueError),
    (10.5, TypeError),
    ({}, TypeError),
])
def test_bitrate_invalid(mock_opts, invalid_val, error_type):
    with pytest.raises(error_type):
        mock_opts.bitrate = invalid_val


# ===========================================================================
# DictOption
# ===========================================================================
def test_dict_option_valid(mock_opts):
    data = {'title': 'My Video', 'year': '2024'}
    mock_opts.metadata = data
    assert mock_opts.metadata == data


def test_dict_option_to_args(mock_opts):
    """Testa se o dicionário é expandido em múltiplos argumentos."""
    data = {'title': 'Test', 'genre': ''}
    mock_opts.metadata = data
    
    desc = MockFfmpegOptions.metadata
    args = desc.to_args(data)
    
    assert args == ['-metadata', 'title=Test']


def test_dict_option_multiple_args(mock_opts):
    data = {'a': '1', 'b': '2'}
    desc = MockFfmpegOptions.metadata
    args = desc.to_args(data)
    
    assert len(args) == 4
    assert args[0] == '-metadata'
    assert args[2] == '-metadata'
    assert 'a=1' in args
    assert 'b=2' in args


def test_dict_option_invalid(mock_opts):
    with pytest.raises(TypeError, match="must be dict"):
        mock_opts.metadata = "not a dict"
    
    with pytest.raises(TypeError):
        mock_opts.metadata = [('key', 'value')]
