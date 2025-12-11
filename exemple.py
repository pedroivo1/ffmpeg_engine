from pympeg import FFmpegBuilder, GlobalOptions, OutputImageOptions

(
    FFmpegBuilder(r"C:\Users\PRIME\Downloads\GitHub 1.jpg", r"C:\Users\PRIME\Downloads\GitHub 10.jpg")
    .with_global_options(GlobalOptions(overwrite=True, hide_banner=True))
    .with_output_options(OutputImageOptions(qscale=5))
    .run()
)
