# FFmpeg Engine

Uma biblioteca Python para construção e execução de comandos FFmpeg, utilizando dois Design Patterns: [Strategy](https://refactoring.guru/design-patterns/strategy) e [Builder](https://refactoring.guru/design-patterns/builder).



## 🎯 Motivação

Usar os comandos FFmpeg dá muita flexibilidade, mas exige muita prática, guardar comandos, lembrar de *flags*, etc.
Então, por que não fazer um código para me ajudar e aproveitar para treinar uma matéria que acabei de aprender?

Por isso fiz uma mini biblioteca em Python, usando [Design Patterns](https://refactoring.guru/design-patterns), para me ajudar a converter vídeos, áudios e imagens sempre que eu precisar.



## 🏗 Arquitetura

O projeto utiliza 2 padrões de projeto para separar responsabilidades (buscar a atomicidade):

1.  **Strategy (`interfaces.py`):** Define **o que** são os Codecs (Vídeo, Áudio, Imagem). O `interfaces.py` é o contrato principal, e as classes concretas (Estratégias) implementam a lógica para gerar seus próprios argumentos de linha de comando. (O `runner.py` é o Contexto que usa estas estratégias).
2.  **Builder (`builders.py` e `director.py`):** Define **como** criar esses *codecs* complexos passo-a-passo. O `builders.py` monta o objeto, e o `director.py` (Diretor) aplica as "receitas" pré-definidas.

### 📂 Estrutura do Pacote

A estrutura do projeto segue o padrão `src/` e inclui as pastas de cache ignoradas pelo Git:

```text
FFMPEG_ENGINE/
├── .pytest_cache/     # Cache do Pytest
├── .ruff_cache/       # Cache de linters (Ruff)
├── .venv/             # Ambiente Virtual Python
│
├── src/
│   └── pympeg/        # Pacote principal
│       ├── data/
│       │   ├── flags.json
│       │   └── read_json.py
│       │
│       ├── options/   # Subpacote para Classes de Opções
│       │   ├── __init__.py
│       │   ├── global_options.py
│       │   ├── input_options.py
│       │   └── output_options.py
│       │
│       ├── __init__.py
│       ├── builders.py  # Implementa o Builder
│       ├── director.py  # Implementa o Director
│       ├── interfaces.py # Contrato para Estratégias (Strategy)
│       ├── options.py    # Módulo de Opções/Flags
│       └── runner.py    # Executa o comando FFmpeg
│
├── tests/
│   ├── integration/
│   └── unit/
│
├── pyproject.toml
├── .gitignore
└── README.md
```



## 🚀 Como Usar

O exemplo a seguir mostra como usar o padrão **Builder** para configurar um *codec* de vídeo e uma *flag* de áudio, e executá-los com o `CommandRunner`.

**Note:** O comando de importação deve usar o nome do pacote, que é `pympeg`.

```python
from pympeg.builders import VideoCodecBuilder
from pympeg.runner import CommandRunner
from pympeg.interfaces import AudioFlags # Assumindo que AudioFlags está em interfaces.py

def main():
    builder = VideoCodecBuilder()

    # Configurando vídeo (H.265, CRF 30)
    video_flags = builder.set_codec('libx265').set_crf(30).build()
    
    # Configurando áudio (AAC 48k)
    # A classe AudioFlags representa a Estratégia
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
Execute no terminal para clonar o repositório:
```bash
git clone [https://github.com/pedroivo1/ffmpeg_engine.git](https://github.com/pedroivo1/ffmpeg_engine.git)
```

Em seguida, navegue para o diretório e instale o pacote em modo editável (`-e`), o que também resolve as dependências listadas no `pyproject.toml`:
```bash
cd ffmpeg_engine
pip install -e .
```

### 📋 Requisitos

| Requisito | Como Instalar |
| :--- | :--- |
| **Python 3.10+** | [Python](https://youtu.be/9_8YBRuC_ak) |
| **FFmpeg** | [FFmpeg](https://www.youtube.com/watch?v=K7znsMo_48I&pp=ygUPZG93bmxvYWQgZmZtcGVn) |