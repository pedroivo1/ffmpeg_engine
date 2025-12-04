from src.builders import VideoCodecBuilder

def test_builder_initializes_with_safe_defaults():
    '''
    Does the builder.build work with default values?
    '''
    builder = VideoCodecBuilder()

    video_flags = builder.build()

    assert video_flags.video_codec == 'libx264'
    assert video_flags.crf == 23
    assert video_flags.preset == 'medium'
    assert video_flags.scale is None
    assert video_flags.fps is None


def test_builder_accepts_custom_values_and_chaining():
    '''
    Do the builder's setters work correctly?
    '''
    builder = VideoCodecBuilder()

    video_flags = (
        builder
        .set_codec('libx265')
        .set_crf(28)
        .set_preset('veryslow')
        .set_scale(1280, 720)
        .set_fps(60)
        .build()
    )

    assert video_flags.video_codec == 'libx265'
    assert video_flags.crf == 28
    assert video_flags.preset == 'veryslow'
    assert video_flags.scale == '1280:720' 
    assert video_flags.fps == 60


def test_builder_partial_update():
    '''
    Can I use only one of the builder's setters?
    '''
    builder = VideoCodecBuilder()
    
    video_flags = builder.set_codec('libvpx-vp9').build()
    
    assert video_flags.video_codec == 'libvpx-vp9'
    assert video_flags.crf == 23
    assert video_flags.preset == 'medium'
