from unittest.mock import patch, MagicMock
from src.runner import FFmpegRunner
from src.flags import VideoFlags

@patch('src.runner.subprocess.run')
def test_runner_calls_subprocess_correctly(mock_subprocess):
    runner = FFmpegRunner("input.mp4", "output.mp4")
    
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.__str__.return_value = "input.mp4"

    runner.input_path = mock_path

    codec = VideoFlags(video_codec='libx264', crf=23, preset='fast')
    runner.add_flags(codec)

    runner.run()

    assert mock_subprocess.called

    args_list = mock_subprocess.call_args[0][0]

    assert args_list[0] == "ffmpeg"
    assert "input.mp4" in args_list 
    assert "-c:v" in args_list
