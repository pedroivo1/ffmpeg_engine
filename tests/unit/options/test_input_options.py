import pytest
import logging
from datetime import timedelta
from pympeg import ImageInputOptions, AudioInputOptions, VideoInputOptions


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

    # all
    (ImageInputOptions,
        {'format': 'image2', 'start_time': 5.5, 'loop': 1, 'framerate': 30},
        ['-f', 'image2', '-ss', '5.500', '-loop', '1', '-framerate', '30']),
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
    expected_msg = f"Invalid value '{value_passed}' received for '{attr_name}' on ImageInputOptions."

    flag_generator.generate_command_args()

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
    (AudioInputOptions, {'start_time': 0}, ['-ss', '0.000']),
    (AudioInputOptions, {'start_time': 0}, ['-ss', '0.000']),
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
    attr_name, value_passed = list(input_args.items())[0]
    expected_msg = f"Invalid value '{value_passed}' received for '{attr_name}' on AudioInputOptions."

    flag_generator.generate_command_args()

    assert expected_msg in caplog.text



VALID_VIDEO_IN_OPTIONS = [
    # none
    (VideoInputOptions, {}, []),

    # format
    (VideoInputOptions, {'format': 'mp4'}, ['-f', 'mp4']),
    (VideoInputOptions, {'format': 'rawvideo'}, ['-f', 'rawvideo']),
    (VideoInputOptions, {'format': 'mov'}, ['-f', 'mov']),

    # codec
    (VideoInputOptions, {'codec': 'libx264'}, ['-c:v', 'libx264']),
    (VideoInputOptions, {'codec': 'copy'}, ['-c:v', 'copy']),
    (VideoInputOptions, {'codec': 'prores'}, ['-c:v', 'prores']),

    # start time
    (VideoInputOptions, {'start_time': 0}, ['-ss', '0.000']),
    (VideoInputOptions, {'start_time': 10.5}, ['-ss', '10.500']),
    (VideoInputOptions, {'start_time': timedelta(seconds=90)}, ['-ss', '00:01:30.000']),

    # duration
    (VideoInputOptions, {'duration': 10}, ['-t', '10.000']),
    (VideoInputOptions, {'duration': timedelta(minutes=1)}, ['-t', '00:01:00.000']),

    # fps
    (VideoInputOptions, {'fps': 24}, ['-r', '24']),
    (VideoInputOptions, {'fps': 29.97}, ['-r', '29.97']),
    (VideoInputOptions, {'fps': 60}, ['-r', '60']),

    # size
    (VideoInputOptions, {'size': '1920x1080'}, ['-s', '1920x1080']),
    (VideoInputOptions, {'size': '640x480'}, ['-s', '640x480']),
    (VideoInputOptions, {'size': 'hd720'}, ['-s', 'hd720']),
    (VideoInputOptions, {'size': 'HD1080'}, ['-s', 'hd1080']),
    (VideoInputOptions, {'size': '4k'}, ['-s', '4k']),
    (VideoInputOptions, {'size': 'pal'}, ['-s', 'pal']),

    # pixel format
    (VideoInputOptions, {'pixel_format': 'yuv420p'}, ['-pix_fmt', 'yuv420p']),
    (VideoInputOptions, {'pixel_format': 'rgb24'}, ['-pix_fmt', 'rgb24']),

    # stream loop
    (VideoInputOptions, {'stream_loop': -1}, ['-stream_loop', '-1']),
    (VideoInputOptions, {'stream_loop': 0}, ['-stream_loop', '0']),

    # all
    (VideoInputOptions, 
        {'format': 'mov', 'codec': 'prores', 'fps': 24, 'size': '1920x1080'},
        ['-f', 'mov', '-c:v', 'prores', '-r', '24', '-s', '1920x1080'])
]

INVALID_VIDEO_IN_OPTIONS = [
    (VideoInputOptions, {'format': 'mp3'}, []), 
    (VideoInputOptions, {'format': 'png'}, []),
    (VideoInputOptions, {'codec': 'aac'}, []),
    (VideoInputOptions, {'codec': 'h265'}, []),
    (VideoInputOptions, {'fps': 0}, []),
    (VideoInputOptions, {'fps': -30}, []),
    (VideoInputOptions, {'size': 'batata'}, []),
    (VideoInputOptions, {'size': '100x'}, []),
    (VideoInputOptions, {'size': 'x100'}, []),
    (VideoInputOptions, {'size': ''}, []),
    (VideoInputOptions, {'pixel_format': 'invalid_fmt'}, []),
    (VideoInputOptions, {'stream_loop': -5}, []),
]


@pytest.mark.parametrize('video_opts, input_args, expected_output', VALID_VIDEO_IN_OPTIONS)
def test_video_in_options_parameters(video_opts, input_args, expected_output):
    flag_generator = video_opts(**input_args)

    flags = flag_generator.generate_command_args()

    assert flags == expected_output


@pytest.mark.parametrize('video_opts, input_args, expected_output', VALID_VIDEO_IN_OPTIONS)
def test_video_in_options_logs_nothing_on_valid_input(caplog, video_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = video_opts(**input_args)

    flag_generator.generate_command_args()

    assert not caplog.text


@pytest.mark.parametrize('video_opts, input_args, expected_output', INVALID_VIDEO_IN_OPTIONS)
def test_video_in_options_logs_on_invalid_input(caplog, video_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = video_opts(**input_args)
    attr_name, value_passed = list(input_args.items())[0]
    expected_msg = f"Invalid value '{value_passed}' received for '{attr_name}' on VideoInputOptions."

    flag_generator.generate_command_args()

    assert expected_msg in caplog.text
