import pytest
from src.flags import VideoFlags, AudioFlags 

# ============================================================= #
# ======================== VIDEO TESTS ======================== #
# ============================================================= #

@pytest.mark.parametrize(
    'codec_class, input_args, expected_output',
    [
        # Default Args
        (VideoFlags, 
            {'video_codec': 'libx264', 'crf': 23, 'preset': 'medium'},
            ['-c:v', 'libx264', '-crf', '23', '-preset', 'medium']),

        # All Args
        (VideoFlags, 
            {'video_codec': 'libx264', 'crf': 20, 'preset': 'fast', 'scale': '720:480', 'fps': 30},
            ['-c:v', 'libx264', '-crf', '20', '-preset', 'fast', '-vf', 'scale=720:480', '-r', '30']),

        # Default Args + scale
        (VideoFlags, 
            {'video_codec': 'mpeg4', 'crf': 20, 'preset': 'fast', 'scale': '720:480'},
            ['-c:v', 'mpeg4', '-crf', '20', '-preset', 'fast', '-vf', 'scale=720:480']),

        # Default Args + fps
        (VideoFlags, 
            {'video_codec': 'libx265', 'crf': 20, 'preset': 'fast', 'fps': 24},
            ['-c:v', 'libx265', '-crf', '20', '-preset', 'fast', '-r', '24']),
    ]
)

def test_video_command_generation_matches_expected(codec_class, input_args, expected_output):
    '''
    Do the generated flags, by VideoFlags, match the expected output?
    '''
    flags = codec_class(**input_args)

    result_args = flags.generate_command_args()

    print(result_args)

    assert result_args == expected_output


def test_optional_flags_are_not_added_when_none():
    '''
    Are flags that default to None correctly omitted from the command?
    '''
    flags = VideoFlags(video_codec='libx264', crf=23, preset='medium', scale=None, fps=None)

    result_args = flags.generate_command_args()

    assert '-r' not in result_args
    assert '-vf' not in result_args


# ============================================================= #
# ======================== AUDIO TESTS ======================== #
# ============================================================= #

@pytest.mark.parametrize(
    'codec_class, input_args, expected_output',
    [
        # Audio Transcoding (AAC with Bitrate)
        (AudioFlags, 
            {'audio_codec': 'aac', 'bitrate': '128k'},
            ['-c:a', 'aac', '-b:a', '128k']),

        # Audio Copy (No Bitrate)
        (AudioFlags, 
            {'audio_codec': 'copy', 'bitrate': None},
            ['-c:a', 'copy'])
    ]
)

def test_audio_command_generation_matches_expected(codec_class, input_args, expected_output):
    '''
    Do the generated flags, by AudioFlags, match the expected output?
    '''
    flags = codec_class(**input_args)
    
    result_args = flags.generate_command_args()

    assert result_args == expected_output
