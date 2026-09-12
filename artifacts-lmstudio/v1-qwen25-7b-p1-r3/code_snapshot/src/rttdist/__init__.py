from __future__ import annotations

from importlib import import_module

__all__ = ["__version__", "ensure_dependency"]

__version__ = "0.1.0"


def ensure_dependency(module_name: str, package_name: str | None = None) -> None:
    try:
        import_module(module_name)
    except ModuleNotFoundError as exc:
        requested_package = package_name or module_name
        raise RuntimeError(
            "Missing runtime dependency "
            f"'{requested_package}'. Install project dependencies with "
            "`python -m pip install -e .[dev]`."
        ) from exc
