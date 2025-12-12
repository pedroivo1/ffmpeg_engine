import pytest
from unittest.mock import patch, MagicMock
from subprocess import CalledProcessError
from pympeg.runner import Runner
from pympeg.options import GlobalOptions, InputVideoOptions, OutputVideoOptions

# 1. TESTE DE ORDEM COMPLETA (O MAIS IMPORTANTE)
@patch('pympeg.runner.subprocess.run')
def test_runner_assembles_full_command_order(mock_subprocess):
    '''
    Garante que Global vem primeiro, depois Input Options, depois -i, depois Output.
    '''
    runner = Runner('in.mp4', 'out.mkv')
    
    # Mock do input
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.__str__.return_value = 'in.mp4'
    runner.input_path = mock_path

    # Adiciona todos os tipos de opções
    runner.add_global_options(GlobalOptions(overwrite=True))
    runner.add_input_options(InputVideoOptions(start_time=10))
    runner.add_output_options(OutputVideoOptions(codec='libx264'))

    runner.run()

    # Pega o comando executado
    cmd = mock_subprocess.call_args[0][0]
    
    # Índices
    idx_global = cmd.index('-y')
    idx_input_opt = cmd.index('-ss')
    idx_input_flag = cmd.index('-i')
    idx_output_opt = cmd.index('-c:v')

    # Validação da "Linha do Tempo" do comando
    assert idx_global < idx_input_opt, "Globais devem vir antes de Input Options"
    assert idx_input_opt < idx_input_flag, "Input Options devem vir antes de -i"
    assert idx_input_flag < idx_output_opt, "Output Options devem vir depois de -i"


# 2. TESTE DE ARQUIVO INEXISTENTE
def test_runner_raises_error_if_input_missing():
    '''
    O Runner não deve nem tentar chamar o subprocesso se o arquivo não existir.
    '''
    runner = Runner('fantasma.mp4', 'out.mp4')
    
    # Mock para dizer que arquivo NÃO existe
    mock_path = MagicMock()
    mock_path.exists.return_value = False
    runner.input_path = mock_path

    # Deve levantar FileNotFoundError
    with pytest.raises(FileNotFoundError):
        runner.run()


# 3. TESTE DE ERRO DO FFMPEG (PROCESS ERROR)
@patch('pympeg.runner.subprocess.run')
def test_runner_propagates_ffmpeg_errors(mock_subprocess):
    '''
    Se o FFmpeg retornar erro (exit code != 0), o Runner deve levantar a exceção.
    '''
    runner = Runner('corrupt.mp4', 'out.mp4')
    
    # Mock do arquivo existente
    mock_path = MagicMock()
    mock_path.exists.return_value = True
    mock_path.is_file.return_value = True
    mock_path.__str__.return_value = 'corrupt.mp4'
    runner.input_path = mock_path

    # Simula o FFmpeg falhando (ex: returncode 1)
    mock_subprocess.side_effect = CalledProcessError(1, ['ffmpeg', ...])

    with pytest.raises(CalledProcessError):
        runner.run()