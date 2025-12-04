from unittest.mock import patch
from src.runner import CommandRunner
from src.flags import VideoFlags

@patch('src.runner.subprocess.run')
def test_runner_calls_subprocess_correctly(mock_subprocess):
    r = CommandRunner("input.mp4", "output.mp4")
    codec = VideoFlags(video_codec='libx264', crf=23, preset='fast')
    r.add_flags(codec)

    r.run()

    assert mock_subprocess.called

    args_list = mock_subprocess.call_args[0][0]

    assert args_list[0] == "ffmpeg"
    assert "input.mp4" in args_list
    assert "-c:v" in args_list
