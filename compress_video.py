import logging
import re
import sys
from pathlib import Path
from pympeg import Builder, GlobalOptions, OutputVideoOptions, OutputAudioOptions

from utils.get_fps import get_fps
from utils.rename_videos import gerar_nome_formatado

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main(path: str):
    root_path = Path(path)

    if not root_path.exists():
        logger.error(f"❌ A pasta {root_path} não existe, meu!")
        return

    files = list(root_path.rglob('*.mp4'))
    logger.info(f"📂 Encontrados {len(files)} arquivos .mp4 para processar.")

    for video_file in files:
        novo_nome = gerar_nome_formatado(video_file)
        
        if not novo_nome:
            logger.warning(f"⚠️ Padrão 'Aula/Bloco' não encontrado em: {video_file.name}. Pulando...")
            continue
            
        output_file = video_file.with_name(novo_nome)

        if output_file.exists():
            if output_file.resolve() == video_file.resolve():
                continue
            logger.warning(f"⏭ O arquivo final já existe: {output_file.name}. Pulando conversão.")
            continue

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
            (
                Builder(video_file, output_file)
                .with_global_options(
                    GlobalOptions(hide_banner=True, loglevel='warning', stats=True, overwrite=False)
                )
                .with_output_options(
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
    main(r'/home/pedro/Videos/n')
