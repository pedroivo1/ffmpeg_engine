import subprocess
from .interfaces import MediaFlags
import logging

logger = logging.getLogger(__name__)

class CommandRunner:
    def __init__(self, input_path: str, output_path: str) -> None:
        self.input_path = input_path
        self.output_path = output_path
        self._codecs: list[MediaFlags] = []

    def add_flags(self, codec: MediaFlags) -> None:
        self._codecs.append(codec)

    def run(self) -> None:
        command = ["ffmpeg", "-y", "-i", self.input_path]
        for codec in self._codecs:
            command.extend(codec.generate_command_args())
        command.append(self.output_path)

        logger.info(f"Executando: {' '.join(command)}")
        try:
            subprocess.run(command, check=True, capture_output=True, text=True)
            logger.info("Comando executado com sucesso.")
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg falhou com código {e.returncode}.")
            logger.error(f"Saída de erro (stderr):\n{e.stderr}")
            raise e
