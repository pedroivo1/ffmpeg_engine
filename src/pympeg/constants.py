# ===========================================================================
# GLOBAL
# ===========================================================================
LOGLEVEL_VALUES = {
    'quiet', 'panic', 'fatal', 'error', 'warning', 
    'info', 'verbose', 'debug', 'trace'
}


# ===========================================================================
# IMAGE
# ===========================================================================
IMAGE_FORMATS = {
    'image2', 'image2pipe', 'png', 'gif', 'bmp', 'tiff', 'jpeg',
    'webp', 'avif', 'v4l2', 'dshow', 'mjpeg'
}

IMAGE_CODECS = {
    'png', 'mjpeg', 'libwebp', 'av1', 'hevc', 'libx264', 
    'gif', 'bmp', 'tiff', 'copy'
}

IMAGE_PIX_FMTS = {
    'yuv420p', 'yuv422p', 'yuv444p', 'rgb24', 'bgr24', 
    'rgba', 'bgra', 'gray', 'monow', 'monob', 
    'yuyv422', 'pal8'
}

IMAGE_SIZES = {
    'sqcif', 'qcif', 'cif', '4cif', '16cif', 'qqvga', 'qvga', 'vga', 
    'svga', 'xga', 'uxga', 'qxga', 'sxga', 'qsxga', 'qzxga', 'wsxga', 
    'wuxga', 'woxga', 'wqsxga', 'wquxga', 'whsxfga', 'hsxga', 'cga', 
    'ega', 'hd480', 'hd720', 'hd1080', 'uhd2160', '8k', 'ntsc', 'pal', 
    'qntsc', 'qpal', 'sntsc', 'spal', 'film', 'ntsc-film', '2k', 
    '2kflat', '2kscope', '4k', '4kflat', '4kscope'
}


# ===========================================================================
# AUDIO
# ===========================================================================
AUDIO_FORMATS = {
    'mp3', 'wav', 'flac', 'aac', 'ogg', 'm4a', 'aiff',
    's16le', 'f32be', 'pcm_s16le', 'alsa', 'pulse',
    'opus', 'ac3', 'eac3', 'dts', 'pcm_s24le', 'pcm_f32le',
}

AUDIO_CODECS = {
    'mp3', 'flac', 'aac', 's16le', 'f32be', 'pcm_s16le',
    'libmp3lame', 'libfdk_aac', 'opus', 'libopus', 
    'vorbis', 'libvorbis', 'pcm_s24le', 'pcm_f32le',
    'ac3', 'eac3', 'dts'
}


# ===========================================================================
# VIDEO
# ===========================================================================
VIDEO_FORMATS = {
    'mp4', 'avi', 'mov', 'mkv', 'webm', 'flv', 'mpeg', '3gp', 
    'ts', 'ogv', 'asf', 'wmv', 'rawvideo', 'yuv4mpegpipe', 'gif'
}

VIDEO_CODECS = {
    'libx264', 'h264', 'libx265', 'hevc', 'vp9', 'vp8', 'mpeg4', 
    'mpeg2video', 'prores', 'dnxhd', 'ffv1', 'rawvideo', 'copy', 'mjpeg', 'gif'
}

VIDEO_PIX_FMTS = {
    'yuv420p', 'yuv422p', 'yuv444p', 'rgb24', 'bgr24', 
    'gray', 'monow', 'monob', 'yuyv422'
}

VIDEO_SIZES = {
    'sqcif', 'qcif', 'cif', '4cif', '16cif', 'qqvga', 'qvga', 'vga', 
    'svga', 'xga', 'uxga', 'qxga', 'sxga', 'qsxga', 'qzxga', 'wsxga', 
    'wuxga', 'woxga', 'wqsxga', 'wquxga', 'whsxfga', 'hsxga', 'cga', 
    'ega', 'hd480', 'hd720', 'hd1080', 'uhd2160', '8k', 'ntsc', 'pal', 
    'qntsc', 'qpal', 'sntsc', 'spal', 'film', 'ntsc-film', '2k', 
    '2kflat', '2kscope', '4k', '4kflat', '4kscope'
}

VIDEO_PRESETS = {
    'ultrafast', 'superfast', 'veryfast', 'faster', 'fast', 
    'medium', 'slow', 'slower', 'veryslow', 'placebo'
}

VIDEO_MOVFLAGS = {
    'faststart', 'frag_keyframe', 'empty_moov', 'default_base_moof', 
    'dash', 'frag_custom', 'separate_moof', 'frag_every_frame'
}

VIDEO_TUNES = {
    'film', 'animation', 'grain', 'stillimage', 'fastdecode', 
    'zerolatency', 'psnr', 'ssim'
}
