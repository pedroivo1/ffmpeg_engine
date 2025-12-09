from .global_options import GlobalOptions

from .input_options import (
    ImageInputOptions,
    AudioInputOptions,
    VideoInputOptions
)

# 3. Classes de Output (Placeholder - Prontas para quando você criá-las)
# from .output_options import (
#     VideoOutputOptions,
#     AudioOutputOptions,
# )

__all__ = [
    "GlobalOptions", 
    "ImageInputOptions", 
    "AudioInputOptions", 
    "VideoInputOptions"
]
