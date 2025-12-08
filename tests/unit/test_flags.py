import pytest
import logging
from datetime import timedelta
from src.flags import GlobalOptions, ImageInputOptions, AudioInputOptions



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





VALID_IMAGE_IN_OPTIONS = [
    # none
    (ImageInputOptions, {}, []),

    # format
    (ImageInputOptions, {'format': 'png'}, ['-f', 'png']),
    (ImageInputOptions, {'format': 'image2'}, ['-f', 'image2']),
    (ImageInputOptions, {'format': 'v4l2'}, ['-f', 'v4l2']),

    # start time
    (ImageInputOptions, {'start_time': 0.0}, ['-ss', '0.000']),
    (ImageInputOptions, {'start_time': 10.5}, ['-ss', '10.500']),
    (ImageInputOptions, {'start_time': 1200.12345}, ['-ss', '1200.123']),
    (ImageInputOptions, {'start_time': timedelta(seconds=0)}, ['-ss', '00:00:00.000']),
    (ImageInputOptions, {'start_time': timedelta(seconds=90.5)}, ['-ss', '00:01:30.500']),
    (ImageInputOptions, {'start_time': timedelta(hours=3, minutes=45, seconds=5, milliseconds=567)}, ['-ss', '03:45:05.567']),

    # loop
    (ImageInputOptions, {'loop': -1}, ['-loop', '-1']),
    (ImageInputOptions, {'loop': 0}, ['-loop', '0']),
    (ImageInputOptions, {'loop': 1}, ['-loop', '1']),

    # framerate
    (ImageInputOptions, {'framerate': 24}, ['-framerate', '24']),
    (ImageInputOptions, {'framerate': 29.97}, ['-framerate', '29.97']),
    (ImageInputOptions, {'framerate': 0.5}, ['-framerate', '0.5']),

    # fps
    (ImageInputOptions, {'fps': 29.97}, ['-r', '29.97']),
    (ImageInputOptions, {'fps': 60}, ['-r', '60']),
    (ImageInputOptions, {'fps': 120}, ['-r', '120']),

    # all
    (ImageInputOptions,
        {'format': 'image2', 'start_time': 5.5, 'loop': 1, 'framerate': 30, 'fps': 15},
        ['-f', 'image2', '-ss', '5.500', '-loop', '1', '-framerate', '30', '-r', '15']),
    # all - fps
    (ImageInputOptions,
        {'format': 'v4l2', 'start_time': 0, 'framerate': 60},
        ['-f', 'v4l2', '-ss', '0.000', '-framerate', '60'])
]

INVALID_IMAGE_IN_OPTIONS = [
    (ImageInputOptions, {'format': 'mp4'}, []),
    (ImageInputOptions, {'start_time': '10:00'}, []),
    (ImageInputOptions, {'loop': 5}, []),
    (ImageInputOptions, {'framerate': 0}, []),
    (ImageInputOptions, {'framerate': -10}, []),
    (ImageInputOptions, {'framerate': 'slow'}, []),
    (ImageInputOptions, {'fps': 0}, []),
    (ImageInputOptions, {'fps': -5}, []),
    (ImageInputOptions, {'fps': 'fast'}, []),
]

@pytest.mark.parametrize('image_flags, input_args, expected_output', VALID_IMAGE_IN_OPTIONS)
def test_image_in_flags_parameters(image_flags, input_args, expected_output):
    flag_generator = image_flags(**input_args)

    flags = flag_generator.generate_command_args()

    assert flags == expected_output


@pytest.mark.parametrize('image_flags, input_args, expected_output', VALID_IMAGE_IN_OPTIONS)
def test_image_in_flags_logs_nothing_on_valid_input(caplog, image_flags, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = image_flags(**input_args)

    flag_generator.generate_command_args()

    assert not caplog.text


@pytest.mark.parametrize('image_flags, input_args, expected_output', INVALID_IMAGE_IN_OPTIONS)
def test_image_in_flags_logs_on_invalid_input(caplog, image_flags, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = image_flags(**input_args)
    attr_name, value_passed = list(input_args.items())[0]

    flag_generator.generate_command_args()
    expected_msg = f"Invalid value '{value_passed}' received for '{attr_name}' on ImageInputOptions."

    assert expected_msg in caplog.text





VALID_AUDIO_IN_OPTIONS = [
    # none
    (AudioInputOptions, {}, []),

    # format
    (AudioInputOptions, {'format': 'mp3'}, ['-f', 'mp3']),
    (AudioInputOptions, {'format': 'wav'}, ['-f', 'wav']),
    (AudioInputOptions, {'format': 'pcm_s16le'}, ['-f', 'pcm_s16le']),

    # codec
    (AudioInputOptions, {'codec': 'aac'}, ['-c:a', 'aac']),
    (AudioInputOptions, {'codec': 'mp3'}, ['-c:a', 'mp3']),
    (AudioInputOptions, {'codec': 'pcm_s16le'}, ['-c:a', 'pcm_s16le']),

    # start time
    (AudioInputOptions, {'start_time': 10.5}, ['-ss', '10.500']),
    (AudioInputOptions, {'start_time': timedelta(minutes=1, seconds=30)}, ['-ss', '00:01:30.000']),

    # duration
    (AudioInputOptions, {'duration': 5}, ['-t', '5.000']),
    (AudioInputOptions, {'duration': timedelta(seconds=20)}, ['-t', '00:00:20.000']),

    # number of channels
    (AudioInputOptions, {'n_channels': 1}, ['-ac', '1']),
    (AudioInputOptions, {'n_channels': 2}, ['-ac', '2']),
    (AudioInputOptions, {'n_channels': 6}, ['-ac', '6']),

    # sample rate
    (AudioInputOptions, {'sample_rate': 44100}, ['-ar', '44100']),
    (AudioInputOptions, {'sample_rate': 44100.00}, ['-ar', '44100']),
    (AudioInputOptions, {'sample_rate': '48000'}, ['-ar', '48000']),
    (AudioInputOptions, {'sample_rate': '44.1k'}, ['-ar', '44100']),
    (AudioInputOptions, {'sample_rate': '48k'}, ['-ar', '48000']),

    # stream loop
    (AudioInputOptions, {'stream_loop': -1}, ['-stream_loop', '-1']),
    (AudioInputOptions, {'stream_loop': 0}, ['-stream_loop', '0']),
    (AudioInputOptions, {'stream_loop': 5}, ['-stream_loop', '5']),

    # all
    (AudioInputOptions, 
        {'format': 's16le', 'n_channels': 2, 'sample_rate': 44100, 'codec': 'pcm_s16le'},
        ['-f', 's16le', '-c:a', 'pcm_s16le', '-ac', '2', '-ar', '44100'])
]


INVALID_AUDIO_IN_OPTIONS = [
    (AudioInputOptions, {'format': 'mp4'}, []),
    (AudioInputOptions, {'codec': 'h264'}, []),
    (AudioInputOptions, {'n_channels': 0}, []),
    (AudioInputOptions, {'n_channels': -1}, []),
    (AudioInputOptions, {'sample_rate': 0}, []),
    (AudioInputOptions, {'sample_rate': -44100}, []),
    (AudioInputOptions, {'sample_rate': 'batata'}, []),
    (AudioInputOptions, {'sample_rate': '-48k'}, []),
    (AudioInputOptions, {'stream_loop': -5}, []),
]


@pytest.mark.parametrize('audio_opts, input_args, expected_output', VALID_AUDIO_IN_OPTIONS)
def test_audio_in_options_parameters(audio_opts, input_args, expected_output):
    flag_generator = audio_opts(**input_args)
    flags = flag_generator.generate_command_args()
    assert flags == expected_output


@pytest.mark.parametrize('audio_opts, input_args, expected_output', VALID_AUDIO_IN_OPTIONS)
def test_audio_in_options_logs_nothing_on_valid_input(caplog, audio_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = audio_opts(**input_args)
    flag_generator.generate_command_args()
    assert not caplog.text


@pytest.mark.parametrize('audio_opts, input_args, expected_output', INVALID_AUDIO_IN_OPTIONS)
def test_audio_in_options_logs_on_invalid_input(caplog, audio_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = audio_opts(**input_args)
    
    # Nota: Aqui pegamos a chave do dicionário (ex: 'n_channels')
    attr_name, value_passed = list(input_args.items())[0]
    
    # Se o nome do atributo no init (n_channels) for diferente do nome no log ('channels'),
    # precisamos ajustar a expectativa. No seu código você loga como 'channels'.
    if attr_name == 'n_channels':
        expected_name = 'channels'
    else:
        expected_name = attr_name

    flag_generator.generate_command_args()
    
    expected_msg = f"Invalid value '{value_passed}' received for '{expected_name}' on AudioInputOptions."
    assert expected_msg in caplog.text
