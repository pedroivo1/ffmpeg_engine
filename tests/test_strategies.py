import pytest
from src.strategies import VideoFlags

def test_video_codec_args_basic():
    codec = VideoFlags()

    # Execution
    args = codec.generate_command_args()

    # Verification (Assert)
    expected = ['-c:v', '', '-crf', '', '-preset', '']
    assert args == expected

def test_video_codec_args_with_scale():
    codec = VideoFlags(video_codec='libx264', crf=23, preset='fast', scale='1920:1080')
    args = codec.generate_command_args()

    # Verifica se a lista contêm os argumentos de filtro
    assert '-vf' in args
    assert 'scale=1920:1080' in args