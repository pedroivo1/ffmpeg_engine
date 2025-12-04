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
    builder = VideoCodecBuilder()

    video_flags = (
        builder
        .set_codec("libx265")
        .set_crf(28)
        .set_preset("veryslow")
        .set_scale(1280, 720)
        .set_fps(60)
        .build()
    )

    assert video_flags.video_codec == "libx265"
    assert video_flags.crf == 28
    assert video_flags.preset == "veryslow"
    assert video_flags.scale == "1280:720" 
    assert video_flags.fps == 60


def test_builder_atualizacao_parcial():
    builder = VideoCodecBuilder()
    
    video_flags = builder.set_codec("libvpx-vp9").build()
    
    assert video_flags.video_codec == "libvpx-vp9"
    assert video_flags.crf == 23
    assert video_flags.preset == "medium"
