import subprocess
import logging
from pathlib import Path
from .interfaces import Options

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

class FFmpegRunner:
    def __init__(self, input_path: str | Path, output_path: str | Path) -> None:
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        self._codecs: list[Options] = []


    def add_flags(self, codec: Options) -> None:
        self._codecs.append(codec)


    def run(self) -> None:
        if not self.input_path.exists():
            raise FileNotFoundError(f'Arquivo não encontrado: {self.input_path}')

        if self.input_path.is_file():
            self.run_file(self.input_path, self.output_path)

        elif self.input_path.is_dir():
            self.run_batch()

        else:
            raise ValueError('O input deve ser um arquivo ou pasta.')


    def run_batch(self) -> None:
        
        extensions = ['*.mp4', '*.mkv', '*.mov', '*.avi', '*.webm']
        files = []
        for ext in extensions:
            files.extend(self.input_path.glob(ext))

        total = len(files)
        if total:
            self.output_path.mkdir(parents=True, exist_ok=True)

        logger.info(f'{total} arquivos encontrados.')

        for i, video_file in enumerate(files, start=1):
            target_file = self.output_path / video_file.name

            logger.info(f'--- Processando [{i}/{total}]: {video_file.name} ---')
            try:
                self.run_file(video_file, target_file)
            except Exception as e:
                logger.error(f'Erro ao converter {video_file.name}: {e}')


    def run_file(self, input_file: Path, output_file: Path) -> None:
        command = ['ffmpeg', '-y', '-i', str(input_file)]

        for codec in self._codecs:
            command.extend(codec.generate_command_args())
        command.append(str(output_file))

        logger.info(f'Executando: {' '.join(command)}')
        try:
            print(command)
            subprocess.run(command, check=True, text=True)
            logger.info('Comando executado com sucesso.')
        except subprocess.CalledProcessError as e:
            logger.error(f'FFmpeg falhou com código {e.returncode}.')
            raise e
