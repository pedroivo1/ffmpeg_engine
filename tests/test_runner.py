from unittest.mock import patch, MagicMock
from src.runner import CommandRunner
from src.strategies import VideoFlags

@patch('src.runner.subprocess.run')  # A gente "moca" o subprocess
def test_runner_calls_subprocess_correctly(mock_subprocess):
    # Setup
    runner = CommandRunner("input.mp4", "output.mp4")
    codec = VideoFlags(video_codec='libx264', crf=23, preset='fast')
    runner.add_flags(codec)
    
    runner.run()
    
    # Verification
    # Verifica se o subprocess.run foi chamado (não roda de verdade)
    assert mock_subprocess.called
    
    # Pega os argumentos que foram passados pro subprocess
    args_list = mock_subprocess.call_args[0][0]
    
    # Garante que a ordem tá certa
    assert args_list[0] == "ffmpeg"
    assert "input.mp4" in args_list
    assert "-c:v" in args_list