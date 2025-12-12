from pympeg import Builder, GlobalOptions, OutputImageOptions

(
    Builder(r"C:\Users\PRIME\Downloads\GitHub 1.jpg", r"C:\Users\PRIME\Downloads\GitHub 10.jpg")
    .with_global_options(GlobalOptions(overwrite=True, hide_banner=True))
    .with_output_options(OutputImageOptions(qscale=5))
    .run()
)
