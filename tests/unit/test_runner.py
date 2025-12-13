import pytest
from unittest.mock import patch, MagicMock
from subprocess import CalledProcessError
from pympeg.runner import Runner
from pympeg.options import GlobalOptions, InputVideoOptions, OutputVideoOptions


@patch('pympeg.runner.subprocess.run')
def test_runner_assembles_full_command_order(mock_subprocess):
    runner = Runner('in.mp4', 'out.mkv')
    
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.__str__.return_value = 'in.mp4'
    runner.input_path = mock_path

    runner.add_global_options(GlobalOptions(overwrite=True))
    runner.add_input_options(InputVideoOptions(start_time=10))
    runner.add_output_options(OutputVideoOptions(codec='libx264'))

    runner.run()

    cmd = mock_subprocess.call_args[0][0]
    
    idx_global = cmd.index('-y')
    idx_input_opt = cmd.index('-ss')
    idx_input_flag = cmd.index('-i')
    idx_output_opt = cmd.index('-c:v')

    assert idx_global < idx_input_opt, "Globais devem vir antes de Input Options"
    assert idx_input_opt < idx_input_flag, "Input Options devem vir antes de -i"
    assert idx_input_flag < idx_output_opt, "Output Options devem vir depois de -i"


def test_runner_raises_error_if_input_missing():
    runner = Runner('fantasma.mp4', 'out.mp4')
    
    mock_path = MagicMock()
    mock_path.exists.return_value = False
    runner.input_path = mock_path

    with pytest.raises(FileNotFoundError):
        runner.run()


@patch('pympeg.runner.subprocess.run')
def test_runner_propagates_ffmpeg_errors(mock_subprocess):
    runner = Runner('corrupt.mp4', 'out.mp4')
    
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.__str__.return_value = 'corrupt.mp4'
    runner.input_path = mock_path

    mock_subprocess.side_effect = CalledProcessError(1, ['ffmpeg', ...])

    with pytest.raises(CalledProcessError):
        runner.run()
