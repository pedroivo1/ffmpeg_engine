import subprocess
import sys
import logging
from pathlib import Path

# Configuração básica de log pra ficar bonito no terminal
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def comprimir_pdf_ghostscript(entrada, saida, qualidade='/ebook'):
    """Executa o comando do Ghostscript."""
    comando = [
        "gs", "-sDEVICE=pdfwrite", "-dCompatibilityLevel=1.4",
        f"-dPDFSETTINGS={qualidade}",
        "-dNOPAUSE", "-dQUIET", "-dBATCH",
        f"-sOutputFile={saida}",
        str(entrada)
    ]
    try:
        subprocess.run(comando, check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"💥 Erro interno do Ghostscript: {e}")
        return False

def processar_arquivo(arquivo_alvo: Path):
    """Aplica a lógica de renomear e comprimir em um único arquivo."""
    
    # Pulo do gato: Se o arquivo já termina com ' - o', ignora pra não comprimir backup
    if arquivo_alvo.stem.endswith(" - o"):
        return

    # Define o nome do backup (ex: boleto.pdf -> boleto - o.pdf)
    arquivo_backup = arquivo_alvo.with_name(f"{arquivo_alvo.stem} - o{arquivo_alvo.suffix}")

    # Se já existe o backup, pula pra não fazer caca (ou avisa)
    if arquivo_backup.exists():
        logger.warning(f"⏭ Pulinho: Já existe backup para {arquivo_alvo.name}. Ignorando.")
        return

    logger.info(f"🔄 Processando: {arquivo_alvo.name}")

    try:
        # 1. Renomeia o original para " - o"
        arquivo_alvo.rename(arquivo_backup)
        
        # 2. Tenta comprimir (Entrada: backup, Saída: nome original)
        sucesso = comprimir_pdf_ghostscript(entrada=arquivo_backup, saida=arquivo_alvo)

        if sucesso:
            logger.info(f"✅ Sucesso! Original salvo como '{arquivo_backup.name}'")
        else:
            # Se falhar, desfaz a renomeação
            logger.error("❌ Falha na compressão. Revertendo nome do arquivo...")
            if arquivo_backup.exists():
                arquivo_backup.rename(arquivo_alvo)

    except OSError as e:
        logger.error(f"💥 Erro de permissão ou disco: {e}")

def main(caminho_inicial=None):
    # LÓGICA HÍBRIDA:
    # 1. Se você passou o caminho direto na chamada da função (lá embaixo), usa ele.
    if caminho_inicial:
        entrada_str = caminho_inicial
    
    # 2. Se não, tenta pegar o argumento do terminal (sys.argv)
    elif len(sys.argv) > 1:
        entrada_str = sys.argv[1]
        
    # 3. Se não tem nenhum dos dois, chora.
    else:
        logger.info("Uso: python script.py <arquivo_ou_pasta>")
        return

    entrada = Path(entrada_str).resolve()

    if not entrada.exists():
        logger.error(f"❌ O caminho informado não existe: {entrada}")
        return

    # MODO PASTA (Recursivo)
    if entrada.is_dir():
        logger.info(f"📂 Varrendo a pasta: {entrada}")
        logger.info("-" * 40)
        
        # rglob pega todas as subpastas
        arquivos = list(entrada.rglob("*.pdf"))
        total = len(arquivos)
        
        if total == 0:
            logger.info("Nenhum PDF encontrado nessa pasta.")
            return

        for i, pdf in enumerate(arquivos, 1):
            processar_arquivo(pdf)
            
        logger.info("-" * 40)
        logger.info("🏁 Processamento em lote finalizado.")

    # MODO ARQUIVO ÚNICO
    elif entrada.is_file():
        if entrada.suffix.lower() == ".pdf":
            processar_arquivo(entrada)
        else:
            logger.error("❌ Isso não é um PDF, parça.")

if __name__ == "__main__":
    # Agora sim! Pode passar o caminho aqui ou deixar vazio pra usar o terminal
    main(r'/home/pedro/Videos/Aula 06')

