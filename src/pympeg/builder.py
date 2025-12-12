from .runner import Runner
from .interfaces import Options
from .options import (
    GlobalOptions, InputAudioOptions, InputVideoOptions, InputImageOptions,
    OutputAudioOptions, OutputVideoOptions, OutputImageOptions
)

class Builder:
    """Implementa a interface fluente (Method Chaining) para configurar e executar comandos FFmpeg."""

    def __init__(self, input_path: str, output_path: str):
        self._runner = Runner(input_path, output_path)

    def with_global_options(self, options: GlobalOptions):
        """Aplica opções globais (ex: overwrite, hide_banner)."""
        if not isinstance(options, GlobalOptions):
            raise TypeError("Expected GlobalOptions instance")
        self._runner.add_global_options(options)
        return self

    def with_input_options(self, options: Options):
        """
        Aplica opções de entrada (flags que vêm ANTES do -i input).
        Aceita: InputVideoOptions, InputAudioOptions, InputImageOptions
        """
        valid_inputs = (InputVideoOptions, InputAudioOptions, InputImageOptions)
        if not isinstance(options, valid_inputs):
            raise TypeError(f"Expected input options, got {type(options).__name__}")
        
        self._runner.add_input_options(options)
        return self

    def with_output_options(self, options: Options):
        """
        Aplica opções de saída (codecs, bitrate, qscale, etc).
        Aceita: OutputVideoOptions, OutputAudioOptions, OutputImageOptions
        """
        valid_outputs = (OutputVideoOptions, OutputAudioOptions, OutputImageOptions)
        if not isinstance(options, valid_outputs):
            raise TypeError(f"Expected output options, got {type(options).__name__}")
        
        self._runner.add_output_options(options)
        return self

    def run(self):
        """Executa o comando final."""
        self._runner.run()
