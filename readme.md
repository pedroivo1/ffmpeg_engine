# FFmpeg Engine

Uma biblioteca Python para construção e execução de comandos FFmpeg, utilizando dois Design Patterns, [Strategy](https://refactoring.guru/design-patterns/strategy) e [Builder](https://refactoring.guru/design-patterns/builder).

## 🎯 Motivação

Usar os comandos FFmpeg dá muita flexibilidade, mas exige muita prática, guardar comandos, lembrar de flags, etc.
Então por que não fazer um código para me ajudar e aproveitar para treinar uma matéria que acabei de aprender?

Por isso fiz uma mini biblioteca em python, usando [Design Patterns](https://refactoring.guru/design-patterns), para me ajudar converter vídeos, áudios e imagens sempre que eu precisar.

## 🏗 Arquitetura

O projeto utiliza 2 padrões de projeto para separar responsabilidades (buscar a atomicidade):

1.  **Strategy (`interfaces.py` e `flags.py`):** Define **o que** são os Codecs (Vídeo, Áudio, Imagem). O `interfaces.py` é o contrato principal, e cada classe em `flags.py` implementa a lógica para gerar seus próprios argumentos de linha de comando. (O `runner.py` é o Contexto que usa estas estratégias).
2.  **Builder (`builders.py` e `director.py`):** Define **como** criar esses codecs complexos passo-a-passo. O `builders.py` monta o objeto, e o `director.py` (Diretor) aplica as "receitas" pré-definidas.

### 📂 Estrutura do Pacote

```text
ffmpeg_engine/
│
├── src/
|   ├── __init__.py
│   ├── builders.py
│   ├── strategies.py
│   └── ...
│
├── tests/
│   ├── integration/
│   └── unit/...
│
├── pyproject.toml
└── ...
```

## 🚀 Como Usar

```python
from ffmpeg_engine.src.builders import VideoCodecBuilder
from ffmpeg_engine.src.runner import CommandRunner
from ffmpeg_engine.src.strategies import AudioFlags

def main():
    builder = VideoCodecBuilder()

    # Configurando vídeo (H.265, CRF 30)
    video_flags = builder.set_codec('libx265').set_crf(30).build()
    
    # Configurando áudio (AAC 48k)
    audio_flags = AudioFlags(audio_codec='aac', bitrate='48k')

    # Caminhos relativos ou absolutos
    runner = CommandRunner("video_aula_01.mp4", "video_aula_01_otimizado.mp4")
    runner.add_flags(video_flags)
    runner.add_flags(audio_flags)

    print("🚀 Iniciando conversão...")
    runner.run()
    print("✅ Processo finalizado!")

if __name__ == "__main__":
    main()
```



## 📦 Instalação

### Como Instalar a Biblioteca
Execute no terminal:
```bash
git clone https://github.com/pedroivo1/ffmpeg_engine.git
```

Em seguida, execute:
```bash
cd ffmpeg-engine
pip install .
```

### 📋 Requisitos

| Requisito | Como Instalar |
| :--- | :--- |
| **Python 3.10+** | [Python](https://youtu.be/9_8YBRuC_ak) |
| **FFmpeg** | [FFmpeg](https://www.youtube.com/watch?v=K7znsMo_48I&pp=ygUPZG93bmxvYWQgZmZtcGVn) |
