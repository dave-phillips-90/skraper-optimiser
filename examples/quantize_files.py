from pathlib import Path

from skraper_optimiser.pngquant import PngQuantConfig, quantize_file


configs = [
    PngQuantConfig(quality_max=80, speed=1, strip=True),
    PngQuantConfig(quality_max=80, speed=1, no_floyd_steinberg=True, strip=True),
    PngQuantConfig(ext="-default.png"),
]

for config in configs:
    file_path = Path("examples/file_example_PNG.png")
    quantize_file(file_path, config=config)
