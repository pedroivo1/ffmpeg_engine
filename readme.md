# FFmpeg Engine

Uma biblioteca Python para construção e execução de comandos FFmpeg, utilizando dois Design Patterns, [Strategy](https://refactoring.guru/design-patterns/strategy) e [Builder](https://refactoring.guru/design-patterns/builder).

## 🎯 Motivação

Usar os comandos FFmpeg dá muita flexibilidade, mas exige muita prática, guardar comandos, lembrar de flags, etc.
Então por que não fazer um código para me ajudar e aproveitar para treinar uma matéria que acabei de aprender?

Por isso fiz uma mini biblioteca em python, usando [Design Patterns](https://refactoring.guru/design-patterns), para me ajudar converter vídeos, áudios e imagens sempre que eu precisar.

## 🏗 Arquitetura

O projeto utiliza 2 padrões de projeto para separar responsabilidades (buscar a atomicidade):

1.  **Strategy (`interfaces.py` e `strategies.py`):** Define **o que** são os Codecs (Vídeo, Áudio, Imagem). O `interfaces.py` é o contrato principal, e cada classe em `strategies.py` implementa a lógica para gerar seus próprios argumentos de linha de comando. (O `runner.py` é o Contexto que usa estas estratégias).
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
|   ├── __init__.py
│   ├── test_builders.py
│   └── ...
│
├── .gitignore
├── pyproject.toml
└── ...
```
.gitignore
## 🚀 Como Usar

### Exemplo Básico (Com Director)

Ideal para configurações padrão sem dor de cabeça. O Director aplica as "receitas" pré-definidas.

```python
from ffmpeg_engine import VideoCodecBuilder, CodecDirector, FFmpegRunner, AudioCodec

# 1. Configuração
builder = VideoCodecBuilder()
director = CodecDirector(builder)

# Aplica o preset de video no builder
director.make_video()
video_strategy = builder.build()

# 2. Execução
runner = FFmpegRunner("input.mp4", "output.mp4")
runner.add_strategy(video_strategy)            # Vídeo configurado
runner.add_strategy(AudioCodec())              # Áudio padrão (AAC)

runner.run()
```

### Exemplo Avançado (Builder Manual)

Ideal para quando você precisa de controle total sobre parâmetros específicos, sem usar presets.

```python
from ffmpeg_engine import VideoCodecBuilder, FFmpegRunner

# Construção manual fluente (Method Chaining)
custom_video = (VideoCodecBuilder()
                .set_codec("libvpx-vp9")
                .set_crf(30)
                .resize(1280, 720)
                .build())

runner = FFmpegRunner("input.mov", "output.webm")
runner.add_strategy(custom_video)
runner.run()
```

## 📋 Requisitos

* **Python 3.8+**: como [instalar Python](https://youtu.be/9_8YBRuC_ak)
* **FFmpeg** instalado e acessível no `PATH` do sistema: como [instalar FFmpeg](https://www.youtube.com/watch?v=K7znsMo_48I&pp=ygUPZG93bmxvYWQgZmZtcGVn) 
