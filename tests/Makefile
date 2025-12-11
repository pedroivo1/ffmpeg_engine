.PHONY: test-unit
.PHONY: test-ordered
.PHONY: test-global-options
.PHONY: test-image-in-options

test-unit:
	python -m pytest tests/unit/

test-ordered:
	python -m pytest tests/unit/test_flags.py tests/unit/test_builders.py tests/unit/test_runner.py

test-global-options:
	python -m pytest .\tests\unit\options\test_global_options.py

test-image-in-options:
	python -m pytest .\tests\unit\options\test_image_input_options.py

test-audio-in-options:
	python -m pytest .\tests\unit\options\test_audio_input_options.py

test-video-in-options:
	python -m pytest .\tests\unit\options\test_video_input_options.py
