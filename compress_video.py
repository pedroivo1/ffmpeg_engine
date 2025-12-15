import subprocess
import logging
import sys
from pathlib import Path
from pympeg import Builder, GlobalOptions, OutputVideoOptions, OutputAudioOptions

# Configura o log
logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

def get_fps(file_path: Path) -> float | None:
    methods = ['avg_frame_rate', 'r_frame_rate']

    for entry in methods:
        cmd = [
            'ffprobe', 
            '-v', 'error', 
            '-select_streams', 'v:0', 
            '-show_entries', f'stream={entry}', 
            '-of', 'default=noprint_wrappers=1:nokey=1',
            str(file_path.resolve())
        ]

        try:
            output = subprocess.check_output(cmd, text=True, stderr=subprocess.STDOUT).strip()

            if '\n' in output:
                output = output.splitlines()[0].strip()
            # -----------------------------------

            if not output or output == '0/0':
                continue

            if '/' in output:
                parts = output.split('/')
                if len(parts) == 2:
                    num, den = parts
                    if float(den) == 0: continue
                    return float(num) / float(den)
            
            return float(output)

        except Exception as e:
            if entry == methods[-1]:
                msg = getattr(e, 'output', str(e)).strip()
                logger.error(f"❌ Falha ao ler FPS de '{file_path.name}':\n   --> {msg}")

    return None

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
