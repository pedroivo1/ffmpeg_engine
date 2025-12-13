from .runner import Runner
from .interfaces import Options
from .options import *


class Builder:

    def __init__(self, input_path: str, output_path: str):
        self._runner = Runner(input_path, output_path)

    def with_global_options(self, options: GlobalOptions):
        if not isinstance(options, GlobalOptions):
            raise TypeError("Expected GlobalOptions instance")
        self._runner.add_global_options(options)
        return self

    def with_input_options(self, options: Options):
        valid_inputs = (InputVideoOptions, InputAudioOptions, InputImageOptions)
        if not isinstance(options, valid_inputs):
            raise TypeError(
                f"Expected input options, got {type(options).__name__}"
            )
        
        self._runner.add_input_options(options)
        return self

    def with_output_options(self, options: Options):
        valid_outputs = (OutputVideoOptions, OutputAudioOptions, OutputImageOptions)
        if not isinstance(options, valid_outputs):
            raise TypeError(
                f"Expected output options, got {type(options).__name__}"
            )
        
        self._runner.add_output_options(options)
        return self

    def run(self):
        self._runner.run()
