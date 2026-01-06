import logging
import re
import sys
from pathlib import Path
from pympeg import Builder, GlobalOptions, OutputVideoOptions, OutputAudioOptions

# Importamos só o get_fps. A lógica de renomear a gente aplica direto na criação do arquivo
from utils.get_fps import get_fps
from utils.rename_videos import gerar_nome_formatado

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main(path: str):
    root_path = Path(path)

    if not root_path.exists():
        logger.error(f"❌ A pasta {root_path} não existe, meu!")
        return

    # Lista todos os mp4
    files = list(root_path.rglob('*.mp4'))
    logger.info(f"📂 Encontrados {len(files)} arquivos .mp4 para processar.")

    for video_file in files:
        # 1. Tenta descobrir o nome bonito
        novo_nome = gerar_nome_formatado(video_file)
        
        # Se o regex não bater, pula ou salva com nome padrão (aqui vou pular pra evitar duplicata errada)
        if not novo_nome:
            logger.warning(f"⚠️ Padrão 'Aula/Bloco' não encontrado em: {video_file.name}. Pulando...")
            continue
            
        # Define o arquivo de saída na mesma pasta
        output_file = video_file.with_name(novo_nome)

        # 2. Verifica se o arquivo de saída JÁ existe
        if output_file.exists():
            # Se for o mesmo arquivo, ignora
            if output_file.resolve() == video_file.resolve():
                continue
            logger.warning(f"⏭ O arquivo final já existe: {output_file.name}. Pulando conversão.")
            continue

        # 3. Pega o FPS (usando sua lib utils)
        fps = get_fps(video_file)
        if fps is None:
            logger.error(f"⛔ Pulando {video_file.name} (FPS não detectado).")
            continue

        fps_rounded = round(fps, 3)
        target_fps = 29.97 if fps_rounded in [59.94, 29.97] else 24

        logger.info(f"🎬 Comprimindo: {video_file.name}")
        logger.info(f"   └─> Destino: {output_file.name}")
        logger.info(f"   ⚙️ FPS: {fps_rounded} -> {target_fps}")

        try:
            # 4. A Mágica do PyMPEG (Compressão Forte)
            (
                Builder(video_file, output_file)
                .with_global_options(
                    GlobalOptions(hide_banner=True, loglevel='warning', stats=True, overwrite=False)
                )
                .with_output_options(
                    # CRF 32 é bem comprimido (bom pra video aula). libx265 é top.
                    OutputVideoOptions(codec='libx265', crf=32, fps=target_fps, x265_params='log-level=error')
                )
                .with_output_options(
                    OutputAudioOptions(codec='aac', bitrate='64k')
                )
                .run()
            )
            logger.info(f"✅ Sucesso! Vídeo novo criado.\n")
            
            # Opcional: Se quiser apagar o original pesado depois, descomente a linha abaixo:
            # video_file.unlink() 
            
        except Exception as e:
            logger.error(f"💥 Erro na conversão: {e}\n")

if __name__ == '__main__':
    main(r'/home/pedro/Videos/Aula 17')
