import pytest
import logging
from datetime import timedelta
from pympeg import ImageOutputOptions, AudioOutputOptions, VideoOutputOptions


VALID_IMAGE_OUT_OPTIONS = [
    # none
    (ImageOutputOptions, {}, []),

    # format
    (ImageOutputOptions, {'format': 'png'}, ['-f', 'png']),
    (ImageOutputOptions, {'format': 'image2'}, ['-f', 'image2']),
    (ImageOutputOptions, {'format': 'jpeg'}, ['-f', 'jpeg']),

    # codec
    (ImageOutputOptions, {'codec': 'png'}, ['-c:v', 'png']),
    (ImageOutputOptions, {'codec': 'mjpeg'}, ['-c:v', 'mjpeg']),
    (ImageOutputOptions, {'codec': 'libwebp'}, ['-c:v', 'libwebp']),
    (ImageOutputOptions, {'codec': 'copy'}, ['-c:v', 'copy']),

    # qscale
    (ImageOutputOptions, {'qscale': 0}, ['-qscale:v', '0']),
    (ImageOutputOptions, {'qscale': 2}, ['-qscale:v', '2']),
    (ImageOutputOptions, {'qscale': 5.0}, ['-qscale:v', '5.0']),

    # frames
    (ImageOutputOptions, {'frames': 1}, ['-frames:v', '1']),
    (ImageOutputOptions, {'frames': 10}, ['-frames:v', '10']),

    # framerate
    (ImageOutputOptions, {'framerate': 24}, ['-r', '24']),
    (ImageOutputOptions, {'framerate': 29.97}, ['-r', '29.97']),

    # size
    (ImageOutputOptions, {'size': '1920x1080'}, ['-s', '1920x1080']),
    (ImageOutputOptions, {'size': 'hd720'}, ['-s', 'hd720']),
    (ImageOutputOptions, {'size': 'HD1080'}, ['-s', 'hd1080']),
    (ImageOutputOptions, {'size': '4k'}, ['-s', '4k']),

    # pixel_format
    (ImageOutputOptions, {'pixel_format': 'yuv420p'}, ['-pix_fmt', 'yuv420p']),
    (ImageOutputOptions, {'pixel_format': 'rgb24'}, ['-pix_fmt', 'rgb24']),
    (ImageOutputOptions, {'pixel_format': 'rgba'}, ['-pix_fmt', 'rgba']),

    # compression_level
    (ImageOutputOptions, {'compression_level': 0}, ['-compression_level', '0']),
    (ImageOutputOptions, {'compression_level': 50}, ['-compression_level', '50']),
    (ImageOutputOptions, {'compression_level': 100}, ['-compression_level', '100']),

    # all
    (ImageOutputOptions,
        {'format': 'png', 'codec': 'png', 'qscale': 2, 'size': '1920x1080', 'compression_level': 90},
        ['-f', 'png', '-c:v', 'png', '-qscale:v', '2', '-s', '1920x1080', '-compression_level', '90']),
]

INVALID_IMAGE_OUT_OPTIONS = [
    (ImageOutputOptions, {'format': 'mp4'}, []),
    (ImageOutputOptions, {'codec': 'h264'}, []),
    (ImageOutputOptions, {'qscale': -1}, []),
    (ImageOutputOptions, {'frames': 0}, []),
    (ImageOutputOptions, {'framerate': 0}, []),
    (ImageOutputOptions, {'size': 'batata'}, []),
    (ImageOutputOptions, {'size': '100x'}, []),
    (ImageOutputOptions, {'pixel_format': 'invalid'}, []),
    (ImageOutputOptions, {'compression_level': -1}, []),
    (ImageOutputOptions, {'compression_level': 101}, []),
]

@pytest.mark.parametrize('image_opts, input_args, expected_output', VALID_IMAGE_OUT_OPTIONS)
def test_image_out_options_parameters(image_opts, input_args, expected_output):
    flag_generator = image_opts(**input_args)

    flags = flag_generator.generate_command_args()

    assert flags == expected_output


@pytest.mark.parametrize('image_opts, input_args, expected_output', VALID_IMAGE_OUT_OPTIONS)
def test_image_out_options_logs_nothing_on_valid_input(caplog, image_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = image_opts(**input_args)

    flag_generator.generate_command_args()

    assert not caplog.text


@pytest.mark.parametrize('image_opts, input_args, expected_output', INVALID_IMAGE_OUT_OPTIONS)
def test_image_out_options_logs_on_invalid_input(caplog, image_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = image_opts(**input_args)
    attr_name, value_passed = list(input_args.items())[0]
    expected_msg = f"Invalid value '{value_passed}' received for '{attr_name}' on ImageOutputOptions."

    flag_generator.generate_command_args()

    assert expected_msg in caplog.text



VALID_AUDIO_OUT_OPTIONS = [
    # none
    (AudioOutputOptions, {}, []),

    # format
    (AudioOutputOptions, {'format': 'mp3'}, ['-f', 'mp3']),
    (AudioOutputOptions, {'format': 'wav'}, ['-f', 'wav']),
    (AudioOutputOptions, {'format': 'pcm_s16le'}, ['-f', 'pcm_s16le']),

    # codec
    (AudioOutputOptions, {'codec': 'aac'}, ['-c:a', 'aac']),
    (AudioOutputOptions, {'codec': 'libmp3lame'}, ['-c:a', 'libmp3lame']),
    (AudioOutputOptions, {'codec': 'copy'}, ['-c:a', 'copy']),

    # bitrate
    (AudioOutputOptions, {'bitrate': 128000}, ['-b:a', '128000']),
    (AudioOutputOptions, {'bitrate': '128k'}, ['-b:a', '128k']),
    (AudioOutputOptions, {'bitrate': '320k'}, ['-b:a', '320k']),
    (AudioOutputOptions, {'bitrate': '1.5m'}, ['-b:a', '1.5m']),

    # sample_rate
    (AudioOutputOptions, {'sample_rate': 44100}, ['-ar', '44100']),
    (AudioOutputOptions, {'sample_rate': 44100.00}, ['-ar', '44100']),
    (AudioOutputOptions, {'sample_rate': '48000'}, ['-ar', '48000']),
    (AudioOutputOptions, {'sample_rate': '44.1k'}, ['-ar', '44100']),
    (AudioOutputOptions, {'sample_rate': '48k'}, ['-ar', '48000']),

    # n_channels
    (AudioOutputOptions, {'n_channels': 1}, ['-ac', '1']),
    (AudioOutputOptions, {'n_channels': 2}, ['-ac', '2']),
    (AudioOutputOptions, {'n_channels': 5}, ['-ac', '5']),

    # qscale
    (AudioOutputOptions, {'qscale': 0}, ['-qscale:a', '0']),
    (AudioOutputOptions, {'qscale': 5}, ['-qscale:a', '5']),
    (AudioOutputOptions, {'qscale': 9.0}, ['-qscale:a', '9.0']),

    # duration
    (AudioOutputOptions, {'duration': 5}, ['-t', '5.000']),
    (AudioOutputOptions, {'duration': timedelta(seconds=20)}, ['-t', '00:00:20.000']),

    # metadata
    (AudioOutputOptions, {'metadata': {'title': 'My Song'}}, ['-metadata', 'title=My Song']),
    (AudioOutputOptions, {'metadata': {'artist': 'Artist', 'album': 'Album'}}, 
        ['-metadata', 'artist=Artist', '-metadata', 'album=Album']),

    # all
    (AudioOutputOptions,
        {'format': 'mp3', 'codec': 'libmp3lame', 'bitrate': '192k', 'sample_rate': 44100, 'n_channels': 2},
        ['-f', 'mp3', '-c:a', 'libmp3lame', '-b:a', '192k', '-ar', '44100', '-ac', '2']),
]

INVALID_AUDIO_OUT_OPTIONS = [
    (AudioOutputOptions, {'format': 'mp4'}, []),
    (AudioOutputOptions, {'codec': 'h264'}, []),
    (AudioOutputOptions, {'bitrate': 0}, []),
    (AudioOutputOptions, {'bitrate': -128}, []),
    (AudioOutputOptions, {'bitrate': 'batata'}, []),
    (AudioOutputOptions, {'sample_rate': 0}, []),
    (AudioOutputOptions, {'sample_rate': -44100}, []),
    (AudioOutputOptions, {'sample_rate': 'batata'}, []),
    (AudioOutputOptions, {'n_channels': 0}, []),
    (AudioOutputOptions, {'qscale': -1}, []),
    (AudioOutputOptions, {'metadata': 'not a dict'}, []),
]

@pytest.mark.parametrize('audio_opts, input_args, expected_output', VALID_AUDIO_OUT_OPTIONS)
def test_audio_out_options_parameters(audio_opts, input_args, expected_output):
    flag_generator = audio_opts(**input_args)

    flags = flag_generator.generate_command_args()

    assert flags == expected_output


@pytest.mark.parametrize('audio_opts, input_args, expected_output', VALID_AUDIO_OUT_OPTIONS)
def test_audio_out_options_logs_nothing_on_valid_input(caplog, audio_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = audio_opts(**input_args)

    flag_generator.generate_command_args()

    assert not caplog.text


@pytest.mark.parametrize('audio_opts, input_args, expected_output', INVALID_AUDIO_OUT_OPTIONS)
def test_audio_out_options_logs_on_invalid_input(caplog, audio_opts, input_args, expected_output):
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = audio_opts(**input_args)
    attr_name, value_passed = list(input_args.items())[0]
    expected_msg = f"Invalid value '{value_passed}' received for '{attr_name}' on AudioOutputOptions."

    flag_generator.generate_command_args()

    assert expected_msg in caplog.text



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
