import logging
import sys
from pathlib import Path
from pympeg import Builder, GlobalOptions, OutputVideoOptions, OutputAudioOptions
from utils.get_fps import get_fps

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def main():
    root_path = Path(r'/home/user/Videos')
    
    if not root_path.exists():
        logger.error(f"❌ A pasta {root_path} não existe!")
        return

    logger.info(f"🔍 Procurando arquivos .ts em: {root_path}...")
    files = list(root_path.rglob('*.ts'))
    logger.info(f"📂 Encontrados {len(files)} arquivos .ts")

    for video_file in files:
        output_file = video_file.with_suffix('.mp4')

        if output_file.exists():
            logger.warning(f"⏭ Pulinho: {output_file.name} já existe.")
            continue

        fps = get_fps(video_file)
        
        if fps is None:
            logger.error(f"⛔ Pulando {video_file.name} (FPS não detectado).")
            continue

        fps_rounded = round(fps, 3)
        target_fps = 29.97 if fps_rounded in [59.94, 29.97] else 24

        logger.info(f"🎬 Convertendo: {video_file.name}")
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
                    OutputAudioOptions(codec='aac', bitrate='48k')
                )
                .run()
            )
            logger.info(f"✅ Sucesso: {output_file.name}\n")
        except Exception as e:
            logger.error(f"💥 Erro na conversão: {e}\n")

if __name__ == '__main__':
    main()
