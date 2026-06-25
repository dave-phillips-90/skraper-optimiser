from dataclasses import dataclass


@dataclass
class PngQuantConfig:
    force: bool = False
    skip_if_larger: bool = True
    ext: str = ""
    quality_min: int = 50
    quality_max: int = 90
    speed: int = 4
    no_floyd_steinberg: bool = False
    posterize: int = 0
    strip: bool = False
    verbose: bool = False

    def get_config(self) -> list[str]:
        bool_flags = {
            "force": "--force",
            "skip_if_larger": "--skip-if-larger",
            "no_floyd_steinberg": "--nofs",
            "strip": "--strip",
            "verbose": "--verbose",
        }

        args = [
            "--quality",
            f"{self.quality_min}-{self.quality_max}",
            "--speed",
            str(self.speed),
            "--posterize",
            str(self.posterize),
        ]
        if self.ext:
            args.extend(["--ext", self.ext])

        args.extend([flag for attr, flag in bool_flags.items() if getattr(self, attr)])

        return args


default_config = PngQuantConfig()

__all__ = ["PngQuantConfig", "default_config"]
