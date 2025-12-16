import subprocess
import logging
from pathlib import Path

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
