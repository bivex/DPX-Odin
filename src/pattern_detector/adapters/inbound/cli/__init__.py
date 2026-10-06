"""Inbound CLI adapter exports."""

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from pattern_detector.adapters.inbound.cli.main import app, main


def __getattr__(name: str) -> Any:
    if name in ("app", "main"):
        from pattern_detector.adapters.inbound.cli import main as _main_module

        return getattr(_main_module, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


__all__ = ["app", "main"]
