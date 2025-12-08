import pytest
import logging
from datetime import timedelta
from src.flags import GlobalOptions, ImageInputOptions



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


# @pytest.mark.parametrize(
#     'codec_class, input_args, expected_output',
#     [
#         # Default Args
#         (VideoFlags, 
#             {'video_codec': 'libx264', 'crf': 23, 'preset': 'medium'},
#             ['-c:v', 'libx264', '-crf', '23', '-preset', 'medium']),

#         # All Args
#         (VideoFlags, 
#             {'video_codec': 'libx264', 'crf': 20, 'preset': 'fast', 'scale': '720:480', 'fps': 30},
#             ['-c:v', 'libx264', '-crf', '20', '-preset', 'fast', '-vf', 'scale=720:480', '-r', '30']),

#         # Default Args + scale
#         (VideoFlags, 
#             {'video_codec': 'mpeg4', 'crf': 20, 'preset': 'fast', 'scale': '720:480'},
#             ['-c:v', 'mpeg4', '-crf', '20', '-preset', 'fast', '-vf', 'scale=720:480']),

#         # Default Args + fps
#         (VideoFlags, 
#             {'video_codec': 'libx265', 'crf': 20, 'preset': 'fast', 'fps': 24},
#             ['-c:v', 'libx265', '-crf', '20', '-preset', 'fast', '-r', '24']),
#     ]
# )

# def test_video_command_generation_matches_expected(codec_class, input_args, expected_output):
#     '''
#     Do the generated flags, by VideoFlags, match the expected output?
#     '''
#     flags = codec_class(**input_args)

#     result_args = flags.generate_command_args()

#     assert result_args == expected_output


# def test_optional_flags_are_not_added_when_none():
#     '''
#     Are flags that default to None correctly omitted from the command?
#     '''
#     flags = VideoFlags(video_codec='libx264', crf=23, preset='medium', scale=None, fps=None)

#     result_args = flags.generate_command_args()

#     assert '-r' not in result_args
#     assert '-vf' not in result_args


# # ============================================================= #
# # ======================== AUDIO TESTS ======================== #
# # ============================================================= #

# @pytest.mark.parametrize(
#     'codec_class, input_args, expected_output',
#     [
#         # Audio Transcoding (AAC with Bitrate)
#         (AudioFlags, 
#             {'audio_codec': 'aac', 'bitrate': '128k'},
#             ['-c:a', 'aac', '-b:a', '128k']),

#         # Audio Copy (No Bitrate)
#         (AudioFlags, 
#             {'audio_codec': 'copy', 'bitrate': None},
#             ['-c:a', 'copy'])
#     ]
# )

# def test_audio_command_generation_matches_expected(codec_class, input_args, expected_output):
#     '''
#     Do the generated flags, by AudioFlags, match the expected output?
#     '''
#     flags = codec_class(**input_args)
    
#     result_args = flags.generate_command_args()

#     assert result_args == expected_output
