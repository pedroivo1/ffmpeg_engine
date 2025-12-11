import pytest
import logging
from datetime import timedelta
from pympeg import VideoOutputOptions





VALID_VIDEO_OUT_OPTIONS = [
    # none
    (VideoOutputOptions, {}, []),

    # format
    (VideoOutputOptions, {'format': 'mp4'}, ['-f', 'mp4']),
    (VideoOutputOptions, {'format': 'webm'}, ['-f', 'webm']),
    (VideoOutputOptions, {'format': 'gif'}, ['-f', 'gif']),

    # video_codec
    (VideoOutputOptions, {'video_codec': 'libx264'}, ['-c:v', 'libx264']),
    (VideoOutputOptions, {'video_codec': 'libx265'}, ['-c:v', 'libx265']),
    (VideoOutputOptions, {'video_codec': 'copy'}, ['-c:v', 'copy']),

    # audio_codec
    (VideoOutputOptions, {'audio_codec': 'aac'}, ['-c:a', 'aac']),
    (VideoOutputOptions, {'audio_codec': 'libmp3lame'}, ['-c:a', 'libmp3lame']),
    (VideoOutputOptions, {'audio_codec': 'copy'}, ['-c:a', 'copy']),

    # bitrate
    (VideoOutputOptions, {'bitrate': 2000000}, ['-b:v', '2000000']),
    (VideoOutputOptions, {'bitrate': '2.5m'}, ['-b:v', '2.5m']),
    (VideoOutputOptions, {'bitrate': '500k'}, ['-b:v', '500k']),

    # fps
    (VideoOutputOptions, {'fps': 24}, ['-r', '24']),
    (VideoOutputOptions, {'fps': 29.97}, ['-r', '29.97']),
    (VideoOutputOptions, {'fps': 60}, ['-r', '60']),

    # size
    (VideoOutputOptions, {'size': '1920x1080'}, ['-s', '1920x1080']),
    (VideoOutputOptions, {'size': 'hd720'}, ['-s', 'hd720']),
    (VideoOutputOptions, {'size': '4k'}, ['-s', '4k']),

    # pixel_format
    (VideoOutputOptions, {'pixel_format': 'yuv420p'}, ['-pix_fmt', 'yuv420p']),
    (VideoOutputOptions, {'pixel_format': 'rgb24'}, ['-pix_fmt', 'rgb24']),

    # qscale
    (VideoOutputOptions, {'qscale': 0}, ['-qscale:v', '0']),
    (VideoOutputOptions, {'qscale': 5}, ['-qscale:v', '5']),

    # duration
    (VideoOutputOptions, {'duration': 10}, ['-t', '10.000']),
    (VideoOutputOptions, {'duration': timedelta(minutes=1)}, ['-t', '00:01:00.000']),

    # preset
    (VideoOutputOptions, {'preset': 'fast'}, ['-preset', 'fast']),
    (VideoOutputOptions, {'preset': 'slow'}, ['-preset', 'slow']),
    (VideoOutputOptions, {'preset': 'ultrafast'}, ['-preset', 'ultrafast']),

    # crf
    (VideoOutputOptions, {'crf': 0}, ['-crf', '0']),
    (VideoOutputOptions, {'crf': 23}, ['-crf', '23']),
    (VideoOutputOptions, {'crf': 51}, ['-crf', '51']),

    # metadata
    (VideoOutputOptions, {'metadata': {'title': 'My Video'}}, ['-metadata', 'title=My Video']),

    # movflags
    (VideoOutputOptions, {'movflags': 'faststart'}, ['-movflags', 'faststart']),
    (VideoOutputOptions, {'movflags': 'frag_keyframe'}, ['-movflags', 'frag_keyframe']),

    # tune
    (VideoOutputOptions, {'tune': 'film'}, ['-tune', 'film']),
    (VideoOutputOptions, {'tune': 'animation'}, ['-tune', 'animation']),

    # all
    (VideoOutputOptions,
        {'format': 'mp4', 'video_codec': 'libx264', 'audio_codec': 'aac', 
         'preset': 'fast', 'crf': 23, 'movflags': 'faststart'},
        ['-f', 'mp4', '-c:v', 'libx264', '-c:a', 'aac', 
         '-preset', 'fast', '-crf', '23', '-movflags', 'faststart']),
]

INVALID_VIDEO_OUT_OPTIONS = [
    (VideoOutputOptions, {'format': 'batata'}, []),
    (VideoOutputOptions, {'video_codec': 'h265'}, []),
    (VideoOutputOptions, {'audio_codec': 'h264'}, []),
    (VideoOutputOptions, {'bitrate': 0}, []),
    (VideoOutputOptions, {'bitrate': 'batata'}, []),
    (VideoOutputOptions, {'fps': 0}, []),
    (VideoOutputOptions, {'size': 'batata'}, []),
    (VideoOutputOptions, {'pixel_format': 'invalid'}, []),
    (VideoOutputOptions, {'qscale': -1}, []),
    (VideoOutputOptions, {'preset': 'invalid'}, []),
    (VideoOutputOptions, {'crf': -1}, []),
    (VideoOutputOptions, {'crf': 52}, []),
    (VideoOutputOptions, {'metadata': 'not a dict'}, []),
    (VideoOutputOptions, {'movflags': 'invalid'}, []),
    (VideoOutputOptions, {'tune': 'invalid'}, []),
]

@pytest.mark.parametrize('video_opts, input_args, expected_output', VALID_VIDEO_OUT_OPTIONS)
def test_video_out_options_parameters(video_opts, input_args, expected_output):
    flag_generator = video_opts(**input_args)

    flags = flag_generator.generate_command_args()

    assert flags == expected_output


@pytest.mark.parametrize('video_opts, input_args, expected_output', VALID_VIDEO_OUT_OPTIONS)
def test_video_out_options_logs_nothing_on_valid_input(caplog, video_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = video_opts(**input_args)

    flag_generator.generate_command_args()

    assert not caplog.text


@pytest.mark.parametrize('video_opts, input_args, expected_output', INVALID_VIDEO_OUT_OPTIONS)
def test_video_out_options_logs_on_invalid_input(caplog, video_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = video_opts(**input_args)
    attr_name, value_passed = list(input_args.items())[0]
    expected_msg = f"Invalid value '{value_passed}' received for '{attr_name}' on VideoOutputOptions."

    flag_generator.generate_command_args()

    assert expected_msg in caplog.text
