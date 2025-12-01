import pytest
from src.builders import VideoCodecBuilder
# Importando os Enums que a gente criou, deixando o teste mais legível
from src.enums import VideoCodecType, Preset 

def test_builder_cria_codec_com_padroes_corretos():
    """
    Verifica se o método build() cria um codec com os valores default
    definidos na inicialização do VideoCodecBuilder.
    """
    # 1. Setup
    builder = VideoCodecBuilder()

    # 2. Execução
    codec = builder.build()

    # 3. Verificação (Assert)
    assert codec.video_codec == VideoCodecType.H264
    assert codec.crf == 23
    assert codec.preset == Preset.MEDIUM
    assert codec.scale is None

def test_builder_aceita_e_passa_valores_customizados():
    """
    Testa se o encadeamento de métodos do builder (fluency) funciona
    e se os valores customizados são repassados corretamente.
    """
    # 1. Setup e Execução
    builder = VideoCodecBuilder()
    codec = builder.set_codec(VideoCodecType.H265) \
                   .set_crf(30) \
                   .set_preset(Preset.SLOW) \
                   .resize(1920, 1080) \
                   .build()

    # 2. Verificação
    assert codec.video_codec == VideoCodecType.H265
    assert codec.crf == 30
    assert codec.preset == Preset.SLOW
    # O builder transforma em string no formato "largura:altura"
    assert codec.scale == "1920:1080"