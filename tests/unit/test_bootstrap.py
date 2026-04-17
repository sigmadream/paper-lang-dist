from __future__ import annotations

import importlib
import io
import unittest
from contextlib import redirect_stdout


class BootstrapTests(unittest.TestCase):
    def test_package_imports(self) -> None:
        package = importlib.import_module("rttdist")

        self.assertEqual(package.__version__, "0.1.0")

    def test_cli_help_path(self) -> None:
        cli = importlib.import_module("rttdist.cli")
        stdout = io.StringIO()

        with redirect_stdout(stdout):
            with self.assertRaises(SystemExit) as excinfo:
                cli.main(["--help"])

        self.assertEqual(excinfo.exception.code, 0)
        self.assertIn("Bootstrap CLI for RTT distance experiments.", stdout.getvalue())
        self.assertEqual(cli.build_parser().prog, "rttdist")

    def test_missing_dependency_guard(self) -> None:
        package = importlib.import_module("rttdist")

        with self.assertRaises(RuntimeError) as excinfo:
            package.ensure_dependency(
                "module_that_does_not_exist", package_name="example-package"
            )

        self.assertIn("python -m pip install -e .[dev]", str(excinfo.exception))
        self.assertIn("example-package", str(excinfo.exception))
