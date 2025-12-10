import pytest
import logging
from pympeg import GlobalOptions


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
    # (classe, parâmetros inválidos)
    (GlobalOptions, {'overwrite': 'talvez'}),
    (GlobalOptions, {'hide_banner': 'maybe'}),
    (GlobalOptions, {'loglevel': 'super_alto'}),
    (GlobalOptions, {'stats': 'as vezes'}),
]


@pytest.mark.parametrize('global_flags, input_args, expected_output', VALID_GLOBAL_OPTIONS)
def test_global_flags_parameters(global_flags, input_args, expected_output):
    '''Testa criação com parâmetros válidos.'''
    flag_generator = global_flags(**input_args)
    flags = flag_generator.generate_command_args()
    assert flags == expected_output


@pytest.mark.parametrize('global_flags, input_args, expected_output', VALID_GLOBAL_OPTIONS)
def test_global_flags_logs_nothing_on_valid_input(caplog, global_flags, input_args, expected_output):
    '''Testa que não há logs de erro para entradas válidas.'''
    caplog.set_level(logging.ERROR, logger='src.interfaces')
    flag_generator = global_flags(**input_args)
    flag_generator.generate_command_args()
    assert not caplog.text


@pytest.mark.parametrize('global_flags, input_args', INVALID_GLOBAL_OPTIONS)
def test_global_flags_raises_value_error_on_invalid_input(global_flags, input_args):
    '''Testa que ValueError é levantado para entradas inválidas.
    
    Com o novo design com properties, valores inválidos causam
    ValueError imediato na criação do objeto.
    '''
    with pytest.raises(ValueError) as exc_info:
        flag_generator = global_flags(**input_args)
    
    # Verifica que a mensagem de erro é informativa
    assert exc_info.value.args
    error_msg = str(exc_info.value)
    
    # Verifica características comuns das mensagens de erro
    attr_name = list(input_args.keys())[0]
    invalid_value = input_args[attr_name]
    
    # Verifica se o valor inválido está na mensagem de erro
    assert str(invalid_value) in error_msg
    
    # Verifica se a mensagem menciona valores válidos
    if attr_name == 'overwrite':
        assert 'yes' in error_msg.lower() or 'no' in error_msg.lower()
    elif attr_name == 'hide_banner':
        assert 'yes' in error_msg.lower()
    elif attr_name == 'loglevel':
        valid_terms = ['quiet', 'info', 'verbose', 'debug', 'error', 'warning']
        assert any(term in error_msg.lower() for term in valid_terms)
    elif attr_name == 'stats':
        assert 'yes' in error_msg.lower() or 'no' in error_msg.lower()


def test_overwrite_setter_valid_values():
    '''Testa setters com valores válidos.'''
    opts = GlobalOptions()
    opts.overwrite = 'yes'
    assert opts.overwrite == 'yes'
    assert opts.generate_command_args() == ['-y']
    
    opts.overwrite = 'no'
    assert opts.overwrite == 'no'
    assert opts.generate_command_args() == ['-n']


def test_overwrite_setter_invalid_value():
    '''Testa que setter levanta ValueError para valor inválido.'''
    opts = GlobalOptions()
    with pytest.raises(ValueError, match='não permitido'):
        opts.overwrite = 'talvez'
    assert opts.overwrite is None


def test_hide_banner_setter_valid():
    '''Testa setter de hide_banner com valor válido.'''
    opts = GlobalOptions()
    opts.hide_banner = 'yes'
    assert opts.hide_banner == 'yes'
    assert opts.generate_command_args() == ['-hide_banner']


def test_hide_banner_setter_invalid():
    '''Testa que hide_banner só aceita 'yes'.'''
    opts = GlobalOptions()
    with pytest.raises(ValueError) as exc_info:
        opts.hide_banner = 'maybe'
    
    error_msg = str(exc_info.value)
    assert 'maybe' in error_msg
    assert 'yes' in error_msg
    assert opts.hide_banner is None


def test_loglevel_setter_valid():
    '''Testa setter de loglevel com valores válidos.'''
    opts = GlobalOptions()
    opts.loglevel = 'verbose'
    assert opts.loglevel == 'verbose'
    assert opts.generate_command_args() == ['-loglevel', 'verbose']


def test_loglevel_setter_invalid():
    '''Testa que loglevel valida contra lista de valores.'''
    opts = GlobalOptions()
    with pytest.raises(ValueError, match='não permitido'):
        opts.loglevel = 'super_alto'
    assert opts.loglevel is None


def test_stats_setter_valid():
    '''Testa setter de stats com valores válidos.'''
    opts = GlobalOptions()
    opts.stats = 'yes'
    assert opts.stats == 'yes'
    assert opts.generate_command_args() == ['-stats']
    
    opts.stats = 'no'
    assert opts.stats == 'no'
    assert opts.generate_command_args() == ['-nostats']


def test_stats_setter_invalid():
    '''Testa que stats valida contra yes/no.'''
    opts = GlobalOptions()
    with pytest.raises(ValueError, match='não permitido'):
        opts.stats = 'as vezes'
    assert opts.stats is None


def test_deleter_functionality():
    '''Testa que deleters funcionam corretamente.'''
    opts = GlobalOptions(overwrite='yes', loglevel='info')
    
    assert opts.overwrite == 'yes'
    assert opts.loglevel == 'info'
    
    # Testa deleter
    del opts.overwrite
    assert opts.overwrite is None
    assert opts.generate_command_args() == ['-loglevel', 'info']
    
    del opts.loglevel
    assert opts.loglevel is None
    assert opts.generate_command_args() == []


def test_property_getter():
    '''Testa que properties retornam valores corretos.'''
    opts = GlobalOptions(overwrite='yes', hide_banner='yes')
    
    # Testa getters
    assert opts.overwrite == 'yes'
    assert opts.hide_banner == 'yes'
    assert opts.loglevel is None
    assert opts.stats is None
    
    # Testa após modificação
    opts.loglevel = 'quiet'
    assert opts.loglevel == 'quiet'


def test_empty_initialization():
    '''Testa inicialização sem parâmetros.'''
    opts = GlobalOptions()
    assert opts.overwrite is None
    assert opts.hide_banner is None
    assert opts.loglevel is None
    assert opts.stats is None
    assert opts.generate_command_args() == []


def test_partial_initialization():
    '''Testa inicialização com alguns parâmetros.'''
    opts = GlobalOptions(overwrite='yes')
    assert opts.overwrite == 'yes'
    assert opts.hide_banner is None
    assert opts.generate_command_args() == ['-y']
    
    # Adiciona depois
    opts.hide_banner = 'yes'
    assert opts.generate_command_args() == ['-y', '-hide_banner']
