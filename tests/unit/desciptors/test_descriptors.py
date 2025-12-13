import pytest
from datetime import timedelta
from pympeg.descriptors.base_option import (
    BaseOption,
    ChoiceOption,
    BoolOption,
    IntOption,
    FloatOption,
    TimeOption,
    SampleRateOption
)

# --- 1. CLASSE DE MOCK PARA TESTES ---
# O descriptor precisa morar numa classe para o __set_name__ e __get__ funcionarem
class MockFfmpegOptions:
    # Base
    generic = BaseOption('-gen')
    
    # Choice
    codec = ChoiceOption('-c:v', choices={'h264', 'hevc'})
    
    # Bool
    overwrite = BoolOption(true_flag='-y', false_flag='-n')
    banner = BoolOption(true_flag='-hide_banner') # Sem flag falsa
    
    # Int
    fps = IntOption('-r', min_val=1, max_val=120)
    
    # Float
    speed = FloatOption('-speed', min_val=0.1, max_val=10.0)
    
    # Time
    start = TimeOption('-ss')
    
    # Sample Rate
    ar = SampleRateOption('-ar')

@pytest.fixture
def mock_opts():
    return MockFfmpegOptions()

# ==============================================================================
# TESTES: BASE OPTION (Protocolo de Descriptor)
# ==============================================================================

def test_base_option_lifecycle(mock_opts):
    """Testa o ciclo completo: set, get, to_args e delete."""
    # 1. Getter inicial (valor padrão None)
    assert mock_opts.generic is None

    # 2. Setter
    mock_opts.generic = "teste"
    assert mock_opts.generic == "teste"
    
    # 3. Verificação no __dict__ interno
    assert mock_opts.__dict__['generic'] == "teste"

    # 4. Geração de Argumentos
    # Precisamos acessar o descriptor na classe para chamar to_args
    descriptor = MockFfmpegOptions.generic
    assert descriptor.to_args("teste") == ['-gen', 'teste']

    # 5. Deleter
    del mock_opts.generic
    assert mock_opts.generic is None
    assert 'generic' not in mock_opts.__dict__

def test_base_option_set_none_removes_attr(mock_opts):
    """Setar None deve limpar o atributo do dicionário."""
    mock_opts.generic = "algo"
    assert mock_opts.generic is not None
    
    mock_opts.generic = None
    assert mock_opts.generic is None
    assert 'generic' not in mock_opts.__dict__

# ==============================================================================
# TESTES: CHOICE OPTION
# ==============================================================================

@pytest.mark.parametrize("value", ['h264', 'hevc'])
def test_choice_option_valid(mock_opts, value):
    mock_opts.codec = value
    assert mock_opts.codec == value

def test_choice_option_invalid(mock_opts):
    with pytest.raises(ValueError, match="not allowed"):
        mock_opts.codec = 'vp9' # Não está no set de choices

# ==============================================================================
# TESTES: BOOL OPTION
# ==============================================================================

@pytest.mark.parametrize("input_val, expected_args", [
    (True, ['-y']),
    (False, ['-n']),
])
def test_bool_option_args_double_flag(mock_opts, input_val, expected_args):
    """Testa booleano que tem flag para True E para False (ex: overwrite)."""
    # Acessa o descriptor direto da classe
    desc = MockFfmpegOptions.overwrite
    assert desc.to_args(input_val) == expected_args

@pytest.mark.parametrize("input_val, expected_args", [
    (True, ['-hide_banner']),
    (False, []), # False não gera nada
])
def test_bool_option_args_single_flag(mock_opts, input_val, expected_args):
    """Testa booleano que só tem flag para True (ex: hide_banner)."""
    desc = MockFfmpegOptions.banner
    assert desc.to_args(input_val) == expected_args

def test_bool_option_type_validation(mock_opts):
    with pytest.raises(TypeError, match="must be bool"):
        mock_opts.overwrite = "True" # String não vale

# ==============================================================================
# TESTES: INT OPTION
# ==============================================================================

@pytest.mark.parametrize("value", [1, 60, 120])
def test_int_option_valid(mock_opts, value):
    mock_opts.fps = value
    assert mock_opts.fps == value

@pytest.mark.parametrize("invalid_val, error_type", [
    (0, ValueError),        # Abaixo do min (1)
    (121, ValueError),      # Acima do max (120)
    ("60", TypeError),      # String
    (60.5, TypeError),      # Float
    (True, TypeError),      # Bool (Python trata True como 1, mas bloqueamos)
])
def test_int_option_invalid(mock_opts, invalid_val, error_type):
    with pytest.raises(error_type):
        mock_opts.fps = invalid_val

# ==============================================================================
# TESTES: FLOAT OPTION
# ==============================================================================

@pytest.mark.parametrize("value, expected_type", [
    (5.5, float),
    (5, int),  # Deve preservar INT se for passado INT
])
def test_float_option_valid_and_types(mock_opts, value, expected_type):
    mock_opts.speed = value
    assert mock_opts.speed == value
    # Garante que ele não converteu int 5 para float 5.0 desnecessariamente
    assert isinstance(mock_opts.speed, expected_type)

@pytest.mark.parametrize("invalid_val, error_type", [
    (0.05, ValueError),     # Abaixo do min
    (10.1, ValueError),     # Acima do max
    ("5.5", TypeError),     # String
])
def test_float_option_invalid(mock_opts, invalid_val, error_type):
    with pytest.raises(error_type):
        mock_opts.speed = invalid_val

# ==============================================================================
# TESTES: TIME OPTION
# ==============================================================================

@pytest.mark.parametrize("input_val, expected_str", [
    (10, "10.000"),
    (10.5, "10.500"),
    (timedelta(seconds=10), "00:00:10.000"),
    (timedelta(hours=1, seconds=30.5), "01:00:30.500"),
    (0, "0.000"),
])
def test_time_option_formatting(mock_opts, input_val, expected_str):
    """Testa a lógica de formatação do validador."""
    # Como o validador roda no __set__, verificamos o valor salvo
    mock_opts.start = input_val
    assert mock_opts.start == expected_str

@pytest.mark.parametrize("invalid_val, error_type", [
    (-10, ValueError),              # Negativo Int
    (timedelta(seconds=-1), ValueError), # Negativo Timedelta
    ("10:00", TypeError),           # String direta (não suportada por enquanto)
])
def test_time_option_errors(mock_opts, invalid_val, error_type):
    with pytest.raises(error_type):
        mock_opts.start = invalid_val

# ==============================================================================
# TESTES: SAMPLE RATE OPTION
# ==============================================================================

@pytest.mark.parametrize("input_val, expected_int", [
    (44100, 44100),
    (48000.0, 48000),       # Float para Int
    ("44100", 44100),       # String numérica
    ("44.1k", 44100),       # Sufixo k com ponto
    ("48k", 48000),         # Sufixo k inteiro
    ("44.1K", 44100),       # Case insensitive
])
def test_sample_rate_parsing(mock_opts, input_val, expected_int):
    mock_opts.ar = input_val
    assert mock_opts.ar == expected_int
    assert isinstance(mock_opts.ar, int)

@pytest.mark.parametrize("invalid_val", [
    "invalid",
    "44..1k",
    -100,
    0
])
def test_sample_rate_errors(mock_opts, invalid_val):
    # Pode ser ValueError (string ruim, negativo) ou TypeError (objeto errado)
    # Vamos pegar qualquer Exception para simplificar, ou especificar as duas
    with pytest.raises((ValueError, TypeError)):
        mock_opts.ar = invalid_val
