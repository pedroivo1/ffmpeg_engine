import pytest
from src.builders import VideoCodecBuilder

def test_builder_inicializa_com_defaults_seguros():
    """
    Sem mexer em nada, o Builder deve entregar o padrão 'safe' (H.264/Medium).
    """
    builder = VideoCodecBuilder()
    video_flags = builder.build()

    assert video_flags.video_codec == "libx264"
    assert video_flags.crf == 23
    assert video_flags.preset == "medium"
    assert video_flags.scale is None
    assert video_flags.fps is None

def test_builder_aceita_valores_customizados_e_encadeamento():
    """
    Testa se o .set_... funciona e se o Builder formata o scale corretamente.
    """
    # 1. Arrange
    builder = VideoCodecBuilder()

    # 2. Act (Encadeamento / Fluent Interface)
    video_flags = (
        builder
        .set_codec("libx265")       # Passando string direto
        .set_crf(28)                # Passando int direto
        .set_preset("veryslow")     # String direta
        .set_scale(1280, 720)       # Ints que viram string formatada
        .set_fps(60)
        .build()
    )

    # 3. Assert
    assert video_flags.video_codec == "libx265"
    assert video_flags.crf == 28
    assert video_flags.preset == "veryslow"
    
    # O PULO DO GATO: O Builder recebe (1280, 720) e guarda "1280:720"
    assert video_flags.scale == "1280:720" 
    assert video_flags.fps == 60

def test_builder_atualizacao_parcial():
    """
    Se eu mudar só o Codec, o CRF e o Preset devem continuar os originais.
    """
    builder = VideoCodecBuilder()
    
    # Mudando só uma coisa
    video_flags = builder.set_codec("libvpx-vp9").build()
    
    assert video_flags.video_codec == "libvpx-vp9"
    assert video_flags.crf == 23
    assert video_flags.preset == "medium"
