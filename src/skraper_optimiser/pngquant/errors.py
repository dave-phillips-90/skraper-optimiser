from typing import final


_PNGQUANT_ERROR_CODES = {
    1: "An argument was missing while calling pngquant.",
    2: "Unable to read the input file.",
    4: "An argument was invalid while calling pngquant.",
    15: "The output file already exists, and force was not set.",
    16: "Unable to write to the output file.",
    17: "PngQuant ran out of memory while processing the file.",
    18: "The host CPU architecture is missing the required SSE instruction(s)",
    24: "LibPNG ran out of memory while processing the file.",
    25: "A fatal error occurred while calling LibPNG.",
    26: "The input color format is not supported.",
    35: "Error while initialising LibPNG.",
    45: (
        "Color conversion failed. This usually indicates a broken embedded ICC profile "
        "in the source image. Try stripping the color profile metadata or "
        "pre-converting the image to standard sRGB before processing."
    ),
    98: (
        "The output file was larger than the input file. Try reducing target quality "
        "settings, reducing speed, or enabling posterization"
    ),
    99: (
        "The target quality range could not be reached. Try reducing target quality "
        "settings, reducing speed, or enabling posterization"
    ),
}


class QuantizeError(Exception):
    """Raised during an exception when quantizing a file."""

    def __init__(self, message: str):
        super().__init__(message)


@final
class PngQuantError(QuantizeError):
    """Raised when PngQuant returns a non-zero error code"""

    def __init__(self, source: str, returncode: int, error_output: str):
        # Pass the message to the base Exception class
        message = f"{source}: " + _PNGQUANT_ERROR_CODES.get(
            returncode, "An unknown pngquant error occurred."
        )
        super().__init__(message)
        self.returncode = returncode
        self.error_output = error_output


__all__ = ["PngQuantError", "QuantizeError"]
