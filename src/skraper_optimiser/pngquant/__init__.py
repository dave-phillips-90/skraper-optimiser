import logging
import subprocess
from io import BytesIO
from pathlib import Path

from skraper_optimiser.pngquant.errors import PngQuantError, QuantizeError
from skraper_optimiser.pngquant.pngquantconfig import PngQuantConfig, default_config


logger = logging.getLogger(__name__)


def quantize_file(
    input_file: Path,
    output_file: Path | None = None,
    config: PngQuantConfig = default_config,
):
    """
    Executes pngquant and writes the output to either the given path or the
    original+suffix as defined in PngQuantConfig
    """
    if not input_file.exists() or input_file.suffix.lower() != ".png":
        logger.error(
            "quantize_file: Input file type is not correct or the file does not exist"
        )
        raise QuantizeError(
            "quantize_file: Input file type is not correct or the file does not exist"
        )

    command = ["pngquant", *config.get_config()]
    if output_file:
        logger.info(f"output_file specified, adding '-o {output_file!s}' to command")
        command.extend(["-o", str(output_file)])
    command.append(str(input_file))

    result = subprocess.run(command, stderr=subprocess.PIPE, check=False)  # noqa: S603

    stderr_output = result.stderr.decode("utf-8", errors="replace")

    if result.returncode != 0:
        logger.error(
            "quantize_file: pngquant returned a non-zero return code: "
            f"{result.returncode}"
        )
        raise PngQuantError("quantize_file", result.returncode, stderr_output)


def quantize_bytes(
    stdin_bytes: BytesIO, config: PngQuantConfig = default_config
) -> BytesIO:
    """
    Executes pngquant and writes the output to a byte array
    """
    command = ["pngquant", *config.get_config()]
    png_magic = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])

    if stdin_bytes.getvalue()[:8] != png_magic:
        logger.error("quantize_bytes: stdin_bytes does not contain PNG data")
        raise QuantizeError("quantize_stream: stdin_bytes does not contain PNG data")

    result = subprocess.run(  # noqa: S603
        command,
        input=stdin_bytes.getvalue(),
        capture_output=True,
        check=False,
    )

    stdout = BytesIO()
    stdout.write(result.stdout)
    stderr = result.stderr.decode("utf-8", errors="replace")

    if result.returncode != 0:
        logger.error(
            "quantize_bytes: pngquant returned a non-zero return code: "
            f"{result.returncode}"
        )
        raise PngQuantError("quantize_bytes", result.returncode, stderr)

    return stdout


__all__ = [
    "PngQuantConfig",
    "PngQuantError",
    "QuantizeError",
    "quantize_bytes",
    "quantize_file",
]
