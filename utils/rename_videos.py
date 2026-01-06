import re
from pathlib import Path

def renomear_videos(diretorio):
    pasta = Path(diretorio)
    
    # Verifica se o diretório existe
    if not pasta.exists():
        print(f"Opa, não achei a pasta: {diretorio}")
        return

    # Regex explicado:
    # AULA\s+(\d+) -> Procura a palavra AULA, espaços, e captura os números (Grupo 1)
    # .*?          -> Ignora qualquer coisa no meio
    # BLOCO\s+(\d+) -> Procura a palavra BLOCO, espaços, e captura os números (Grupo 2)
    padrao = re.compile(r"AULA\s+(\d+).*?BLOCO\s+(\d+)", re.IGNORECASE)

    # Itera sobre todos os arquivos .mp4 da pasta
    for arquivo in pasta.glob("*.mp4"):
        match = padrao.search(arquivo.name)
        
        if match:
            # Pega os grupos capturados pelo regex
            num_aula = int(match.group(1))
            num_bloco = int(match.group(2))
            
            # Monta o novo nome. O :02d garante o zero à esquerda (01, 02...)
            novo_nome = f"Aula {num_aula:02d} - Bloco {num_bloco}{arquivo.suffix}"
            
            novo_caminho = arquivo.with_name(novo_nome)
            
            # Mostra o que vai acontecer
            print(f"Renomeando: \nDE:   {arquivo.name}\nPARA: {novo_nome}\n---")
            
            # COMANDO REAL (Descomente a linha abaixo pra rodar de verdade)
            # arquivo.rename(novo_caminho)
            
        else:
            print(f"Pulei esse aqui (padrão não encontrado): {arquivo.name}")


def gerar_nome_formatado(arquivo: Path):
    """
    Usa a LÓGICA do seu renomear_videos, mas retorna o nome 
    para um único arquivo em vez de renomear a pasta toda.
    """
    padrao = re.compile(r"AULA\s+(\d+).*?BLOCO\s+(\d+)", re.IGNORECASE)
    match = padrao.search(arquivo.name)
    
    if match:
        num_aula = int(match.group(1))
        num_bloco = int(match.group(2))
        # Retorna ex: "Aula 02 - Bloco 1.mp4"
        return f"Aula {num_aula:02d} - Bloco {num_bloco}.mp4"
    
    return None
