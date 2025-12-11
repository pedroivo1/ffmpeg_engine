import subprocess
import logging
from pathlib import Path
from typing import List
from .interfaces import Options

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


class FFmpegRunner:
    def __init__(self, input_path: str | Path, output_path: str | Path) -> None:
        self.input_path = Path(input_path)
        self.output_path = Path(output_path)
        
        self._global_options: List[str] = []
        self._input_options: List[str] = []
        self._output_options: List[str] = []

    def add_global_options(self, options: Options) -> None:
        self._global_options.extend(options.generate_command_args())

    def add_input_options(self, options: Options) -> None:
        self._input_options.extend(options.generate_command_args())

    def add_output_options(self, options: Options) -> None:
        self._output_options.extend(options.generate_command_args())

    def _build_command(self, input_file: Path, output_file: Path) -> List[str]:
        """Constrói o comando final na ordem correta do FFmpeg."""
        cmd = ['ffmpeg']
        cmd.extend(self._global_options)
        cmd.extend(self._input_options)
        cmd.extend(['-i', str(input_file)])
        cmd.extend(self._output_options)
        cmd.append(str(output_file))
        return cmd

    def run(self) -> None:
        if not self.input_path.exists():
            raise FileNotFoundError(f'Arquivo não encontrado: {self.input_path}')

        if self.input_path.is_file():
            self.run_file(self.input_path, self.output_path)
        elif self.input_path.is_dir():
            self.run_batch()
        else:
            raise ValueError('O input deve ser um arquivo ou pasta.')

    def run_file(self, input_file: Path, output_file: Path) -> None:
        command = self._build_command(input_file, output_file)
        
        logger.info(f"Executando: {' '.join(command)}")
        try:
            subprocess.run(command, check=True, text=True)
            logger.info('Comando executado com sucesso.')
        except subprocess.CalledProcessError as e:
            logger.error(f'FFmpeg falhou com código {e.returncode}.')
            raise e
            
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
