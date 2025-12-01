from enum import Enum

class VideoCodecType(str, Enum):
    """
    Codecs de vídeo suportados.
    """
    H264 = "libx264"
    H265 = "libx265"
    VP9 = "libvpx-vp9"
    MPEG4 = "mpeg4"
    # Adicione outros conforme precisar

class AudioCodecType(str, Enum):
    """
    Codecs de áudio suportados.
    """
    AAC = "aac"
    MP3 = "libmp3lame"
    OPUS = "libopus"
    COPY = "copy" # Só copia o áudio sem reprocessar

class Preset(str, Enum):
    """
    Presets de velocidade de codificação do x264/x265.
    Quanto mais rápido, pior a compressão (arquivo maior).
    Use o mais lento que sua paciência permitir!
    """
    # ====== MAIS RÁPIDO (Menor Compressão, Rápido) ======
    ULTRAFAST = "ultrafast"
    SUPERFAST = "superfast"
    VERYFAST = "veryfast"
    FASTER = "faster"
    FAST = "fast"

    # ====== PADRÃO / EQUILIBRADO (Default) ======
    MEDIUM = "medium" 

    # ====== MAIS LENTO (Melhor Compressão, Lento) ======
    SLOW = "slow"
    SLOWER = "slower"
    VERYSlow = "veryslow"
    PLACEBO = "placebo"