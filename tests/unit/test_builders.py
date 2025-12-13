import pytest
from unittest.mock import patch
from pympeg import (
    Builder, GlobalOptions, InputVideoOptions, InputAudioOptions,
    OutputVideoOptions
)


# ===========================================================================
# FIXTURES
# ===========================================================================
@pytest.fixture
def mock_runner():
    with patch('pympeg.builder.Runner') as MockRunnerClass:
        mock_instance = MockRunnerClass.return_value
        yield mock_instance


@pytest.fixture
def builder(mock_runner):
    return Builder('input.mp4', 'output.mp4')


# ===========================================================================
# TESTES DE INICIALIZAÇÃO E FLUXO
# ===========================================================================
def test_builder_initialization(mock_runner):
    Builder('input.avi', 'output.mkv')
    assert mock_runner.input_path is not None


def test_fluent_interface_chaining(builder):
    global_opts = GlobalOptions(overwrite=True)
    returned_builder = builder.with_global_options(global_opts)
    assert returned_builder is builder
    assert isinstance(returned_builder, Builder)


def test_run_calls_runner_run(builder, mock_runner):
    builder.run()
    mock_runner.run.assert_called_once()


# ===========================================================================
# TESTES: GLOBAL OPTIONS
# ===========================================================================
def test_with_global_options_success(builder, mock_runner):
    opts = GlobalOptions(overwrite=True)
    builder.with_global_options(opts)
    mock_runner.add_global_options.assert_called_once_with(opts)


def test_with_global_options_invalid_type(builder):
    invalid_opt = InputVideoOptions() # Tipo errado
    with pytest.raises(TypeError) as excinfo:
        builder.with_global_options(invalid_opt)
    assert "Expected GlobalOptions" in str(excinfo.value)


# ===========================================================================
# TESTES: INPUT OPTIONS
# ===========================================================================
def test_with_input_options_success(builder, mock_runner):
    vid_opts = InputVideoOptions(fps=30)
    builder.with_input_options(vid_opts)
    mock_runner.add_input_options.assert_called_with(vid_opts)

    aud_opts = InputAudioOptions(codec='mp3')
    builder.with_input_options(aud_opts)
    mock_runner.add_input_options.assert_called_with(aud_opts)


def test_with_input_options_invalid_type(builder):
    invalid_opt = OutputVideoOptions()
    with pytest.raises(TypeError) as excinfo:
        builder.with_input_options(invalid_opt)
    assert "Expected input options" in str(excinfo.value)


# ===========================================================================
# TESTES: OUTPUT OPTIONS
# ===========================================================================
def test_with_output_options_success(builder, mock_runner):
    out_opts = OutputVideoOptions(codec='libx264')
    builder.with_output_options(out_opts)
    mock_runner.add_output_options.assert_called_once_with(out_opts)


def test_with_output_options_invalid_type(builder):
    invalid_opt = InputVideoOptions()
    with pytest.raises(TypeError) as excinfo:
        builder.with_output_options(invalid_opt)
    assert "Expected output options" in str(excinfo.value)


# ===========================================================================
# TESTE DE INTEGRAÇÃO (FLUXO COMPLETO MOCKADO)
# ===========================================================================
def test_full_chain_execution(builder, mock_runner):
    g_opts = GlobalOptions(hide_banner=True)
    i_opts = InputVideoOptions(start_time=10)
    o_opts = OutputVideoOptions(format='mp4')

    (
        builder
        .with_global_options(g_opts)
        .with_input_options(i_opts)
        .with_output_options(o_opts)
        .run()
    )

    mock_runner.add_global_options.assert_called_once_with(g_opts)
    mock_runner.add_input_options.assert_called_once_with(i_opts)
    mock_runner.add_output_options.assert_called_once_with(o_opts)
    mock_runner.run.assert_called_once()
