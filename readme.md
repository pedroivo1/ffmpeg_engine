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

```text
ffmpeg_engine/
├── src/
│   └── pympeg/
│       │
│       ├── options/
│       │   ├── __init__.py
│       │   ├── global_options.py
│       │   └── ...
│       │
│       ├── __init__.py
│       ├── builders.py
│       ├── interfaces.py
│       └── ...
│
├── tests/
│   └── unit/...
│
└── ...
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