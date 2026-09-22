from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
import shutil
import subprocess
import sys
import time

from rttdist.corpus import ProblemCorpusEntry

SUPPORTED_EXEC_LANGUAGES = frozenset({"c", "cpp", "java", "python", "scala", "haskell", "prolog"})


class ExecutionAdapterError(ValueError):
    pass


class ExecutionStatus(str, Enum):
    SUCCESS = "success"
    WRONG_ANSWER = "wrong_answer"
    COMPILE_ERROR = "compile_error"
    RUNTIME_ERROR = "runtime_error"
    TIMEOUT = "timeout"


@dataclass(frozen=True)
class ProcessResult:
    command: tuple[str, ...]
    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool
    duration_seconds: float


@dataclass(frozen=True)
class FixtureRunResult:
    fixture_stem: str
    input_path: Path
    output_path: Path
    status: ExecutionStatus
    stdout: str
    stderr: str
    exit_code: int | None
    duration_seconds: float
    stdout_log_path: Path
    stderr_log_path: Path
    message: str


@dataclass(frozen=True)
class ExecutionBatchResult:
    language: str
    problem_id: str
    status: ExecutionStatus
    work_directory: Path
    compile_log_path: Path
    compile_result: ProcessResult | None
    fixture_results: tuple[FixtureRunResult, ...]
    message: str
    details: dict = field(default_factory=dict)


class ExecutionAdapter:
    def __init__(self, *, language: str) -> None:
        self._language = language

    @property
    def language(self) -> str:
        return self._language

    def evaluate(
        self,
        *,
        source_path: Path,
        problem: ProblemCorpusEntry,
        workspace_root: Path,
        timeout_seconds: int,
    ) -> ExecutionBatchResult:
        normalized_source_path = Path(source_path).resolve()
        if not normalized_source_path.is_file():
            raise ExecutionAdapterError(
                f"`source_path` must point to an existing file: {normalized_source_path}"
            )
        if timeout_seconds < 1:
            raise ExecutionAdapterError("`timeout_seconds` must be >= 1.")

        work_directory = _build_clean_work_directory(
            workspace_root=workspace_root,
            problem_id=problem.problem_id,
            language=self.language,
        )
        compile_log_path = work_directory / "compile.log"

        prepared_source_path = self._prepare_source(
            source_path=normalized_source_path,
            work_directory=work_directory,
        )

        compile_result = self._compile(
            prepared_source_path=prepared_source_path,
            work_directory=work_directory,
            timeout_seconds=timeout_seconds,
        )

        if compile_result is None:
            compile_log_path.write_text("compile skipped\n", encoding="utf-8")
        else:
            _write_process_log(compile_log_path, compile_result)
            if compile_result.timed_out:
                return ExecutionBatchResult(
                    language=self.language,
                    problem_id=problem.problem_id,
                    status=ExecutionStatus.COMPILE_ERROR,
                    work_directory=work_directory,
                    compile_log_path=compile_log_path,
                    compile_result=compile_result,
                    fixture_results=tuple(),
                    message="Compilation exceeded timeout.",
                    details={"compile_timed_out": True},
                )
            if compile_result.exit_code != 0:
                missing_toolchain = _missing_executable_name(compile_result)
                return ExecutionBatchResult(
                    language=self.language,
                    problem_id=problem.problem_id,
                    status=ExecutionStatus.COMPILE_ERROR,
                    details={"missing_toolchain": missing_toolchain} if missing_toolchain else {},
                    work_directory=work_directory,
                    compile_log_path=compile_log_path,
                    compile_result=compile_result,
                    fixture_results=tuple(),
                    message=(
                        f"Missing toolchain executable: {missing_toolchain}."
                        if missing_toolchain is not None
                        else "Compilation failed."
                    ),
                )

        fixture_results: list[FixtureRunResult] = []
        for fixture_pair in problem.fixture_pairs:
            fixture_stem = fixture_pair.input_path.stem
            fixture_directory = work_directory / "fixtures" / fixture_stem
            fixture_directory.mkdir(parents=True, exist_ok=True)

            input_text = fixture_pair.input_path.read_text(encoding="utf-8")
            process_result = self._run(
                prepared_source_path=prepared_source_path,
                work_directory=work_directory,
                timeout_seconds=timeout_seconds,
                input_text=input_text,
            )

            stdout_log_path = fixture_directory / "stdout.log"
            stderr_log_path = fixture_directory / "stderr.log"
            stdout_log_path.write_text(process_result.stdout, encoding="utf-8")
            stderr_log_path.write_text(process_result.stderr, encoding="utf-8")

            status, message = _classify_fixture_result(
                process_result=process_result,
                expected_output=fixture_pair.output_path.read_text(encoding="utf-8"),
            )

            fixture_results.append(
                FixtureRunResult(
                    fixture_stem=fixture_stem,
                    input_path=fixture_pair.input_path,
                    output_path=fixture_pair.output_path,
                    status=status,
                    stdout=process_result.stdout,
                    stderr=process_result.stderr,
                    exit_code=process_result.exit_code,
                    duration_seconds=process_result.duration_seconds,
                    stdout_log_path=stdout_log_path,
                    stderr_log_path=stderr_log_path,
                    message=message,
                )
            )

        batch_status = _classify_batch_status(tuple(fixture_results))
        return ExecutionBatchResult(
            language=self.language,
            problem_id=problem.problem_id,
            status=batch_status,
            work_directory=work_directory,
            compile_log_path=compile_log_path,
            compile_result=compile_result,
            fixture_results=tuple(fixture_results),
            message=_batch_message(batch_status, tuple(fixture_results)),
        )

    def _prepare_source(self, *, source_path: Path, work_directory: Path) -> Path:
        destination_path = work_directory / self._source_filename()
        destination_path.write_text(
            source_path.read_text(encoding="utf-8"), encoding="utf-8"
        )
        return destination_path

    def _source_filename(self) -> str:
        raise NotImplementedError

    def _compile(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
    ) -> ProcessResult | None:
        raise NotImplementedError

    def _run(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
        input_text: str,
    ) -> ProcessResult:
        raise NotImplementedError


class CExecutionAdapter(ExecutionAdapter):
    def __init__(self) -> None:
        super().__init__(language="c")

    def _source_filename(self) -> str:
        return "Main.c"

    def _compile(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
    ) -> ProcessResult:
        executable_path = work_directory / "program"
        command = [
            "gcc",
            str(prepared_source_path),
            "-O2",
            "-std=c11",
            "-o",
            str(executable_path),
        ]
        return _run_subprocess(
            command=command,
            cwd=work_directory,
            timeout_seconds=timeout_seconds,
            input_text=None,
        )

    def _run(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
        input_text: str,
    ) -> ProcessResult:
        del prepared_source_path
        executable_path = work_directory / "program"
        return _run_subprocess(
            command=[str(executable_path)],
            cwd=work_directory,
            timeout_seconds=timeout_seconds,
            input_text=input_text,
        )


class CppExecutionAdapter(ExecutionAdapter):
    def __init__(self) -> None:
        super().__init__(language="cpp")

    def _source_filename(self) -> str:
        return "Main.cpp"

    def _compile(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
    ) -> ProcessResult:
        executable_path = work_directory / "program"
        command = [
            "g++",
            str(prepared_source_path),
            "-O2",
            "-std=c++17",
            "-o",
            str(executable_path),
        ]
        return _run_subprocess(
            command=command,
            cwd=work_directory,
            timeout_seconds=timeout_seconds,
            input_text=None,
        )

    def _run(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
        input_text: str,
    ) -> ProcessResult:
        del prepared_source_path
        executable_path = work_directory / "program"
        return _run_subprocess(
            command=[str(executable_path)],
            cwd=work_directory,
            timeout_seconds=timeout_seconds,
            input_text=input_text,
        )


class JavaExecutionAdapter(ExecutionAdapter):
    def __init__(self) -> None:
        super().__init__(language="java")

    def _source_filename(self) -> str:
        return "Main.java"

    def _compile(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
    ) -> ProcessResult:
        build_directory = work_directory / "build"
        build_directory.mkdir(parents=True, exist_ok=True)
        return _run_subprocess(
            command=[
                "javac",
                "-encoding",
                "UTF-8",
                "-d",
                str(build_directory),
                str(prepared_source_path),
            ],
            cwd=work_directory,
            timeout_seconds=timeout_seconds,
            input_text=None,
        )

    def _run(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
        input_text: str,
    ) -> ProcessResult:
        del prepared_source_path
        build_directory = work_directory / "build"
        return _run_subprocess(
            command=["java", "-cp", str(build_directory), "Main"],
            cwd=work_directory,
            timeout_seconds=timeout_seconds,
            input_text=input_text,
        )


class PythonExecutionAdapter(ExecutionAdapter):
    def __init__(self) -> None:
        super().__init__(language="python")

    def _source_filename(self) -> str:
        return "main.py"

    def _compile(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
    ) -> ProcessResult | None:
        del prepared_source_path
        del work_directory
        del timeout_seconds
        return None

    def _run(
        self,
        *,
        prepared_source_path: Path,
        work_directory: Path,
        timeout_seconds: int,
        input_text: str,
    ) -> ProcessResult:
        return _run_subprocess(
            command=[sys.executable, str(prepared_source_path)],
            cwd=work_directory,
            timeout_seconds=timeout_seconds,
            input_text=input_text,
        )


def get_execution_adapter(language: str) -> ExecutionAdapter:
    normalized_language = _normalize_language(language)
    if normalized_language == "c":
        return CExecutionAdapter()
    if normalized_language == "cpp":
        return CppExecutionAdapter()
    if normalized_language == "java":
        return JavaExecutionAdapter()
    if normalized_language in {"scala", "haskell", "prolog"}:
        from rttdist.exec.extended import ExtendedExecutionAdapter
        return ExtendedExecutionAdapter(normalized_language)
    return PythonExecutionAdapter()


def evaluate_source(
    *,
    language: str,
    source_path: Path,
    problem: ProblemCorpusEntry,
    workspace_root: Path,
    timeout_seconds: int,
) -> ExecutionBatchResult:
    adapter = get_execution_adapter(language)
    return adapter.evaluate(
        source_path=source_path,
        problem=problem,
        workspace_root=workspace_root,
        timeout_seconds=timeout_seconds,
    )


def _normalize_language(language: str) -> str:
    if not isinstance(language, str) or not language.strip():
        raise ExecutionAdapterError("`language` must be a non-empty string.")
    normalized = language.strip().lower()
    if normalized not in SUPPORTED_EXEC_LANGUAGES:
        supported = ", ".join(sorted(SUPPORTED_EXEC_LANGUAGES))
        raise ExecutionAdapterError(
            f"Unsupported execution language `{language}`. Supported: {supported}."
        )
    return normalized


def _build_clean_work_directory(
    *, workspace_root: Path, problem_id: str, language: str
) -> Path:
    normalized_workspace_root = Path(workspace_root).resolve()
    directory = normalized_workspace_root / "exec" / problem_id / language
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _run_subprocess(
    *,
    command: list[str],
    cwd: Path,
    timeout_seconds: int,
    input_text: str | None,
) -> ProcessResult:
    start = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            cwd=cwd,
            input=input_text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        elapsed = time.perf_counter() - start
        return ProcessResult(
            command=tuple(command),
            stdout=_normalize_timeout_stream(exc.stdout),
            stderr=_normalize_timeout_stream(exc.stderr),
            exit_code=None,
            timed_out=True,
            duration_seconds=elapsed,
        )
    except FileNotFoundError as exc:
        elapsed = time.perf_counter() - start
        return ProcessResult(
            command=tuple(command),
            stdout="",
            stderr=f"Executable not found: {command[0]} ({exc})\n",
            exit_code=127,
            timed_out=False,
            duration_seconds=elapsed,
        )

    elapsed = time.perf_counter() - start
    return ProcessResult(
        command=tuple(command),
        stdout=completed.stdout,
        stderr=completed.stderr,
        exit_code=completed.returncode,
        timed_out=False,
        duration_seconds=elapsed,
    )


def _normalize_timeout_stream(value: bytes | str | None) -> str:
    if value is None:
        return ""
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    return value


def _classify_fixture_result(
    *, process_result: ProcessResult, expected_output: str
) -> tuple[ExecutionStatus, str]:
    if process_result.timed_out:
        return ExecutionStatus.TIMEOUT, "Execution exceeded timeout."

    if process_result.exit_code != 0:
        return ExecutionStatus.RUNTIME_ERROR, "Program exited with a runtime error."

    expected = _canonicalize_output(expected_output)
    actual = _canonicalize_output(process_result.stdout)
    if actual != expected:
        return (
            ExecutionStatus.WRONG_ANSWER,
            "Program output did not match expected output.",
        )

    return ExecutionStatus.SUCCESS, "Program output matched expected output."


def _canonicalize_output(text: str) -> str:
    stripped = text.strip()
    if not stripped:
        return ""
    return "\n".join(line.rstrip() for line in stripped.splitlines())


def _classify_batch_status(
    fixture_results: tuple[FixtureRunResult, ...],
) -> ExecutionStatus:
    if not fixture_results:
        return ExecutionStatus.SUCCESS

    statuses = {item.status for item in fixture_results}
    if ExecutionStatus.TIMEOUT in statuses:
        return ExecutionStatus.TIMEOUT
    if ExecutionStatus.RUNTIME_ERROR in statuses:
        return ExecutionStatus.RUNTIME_ERROR
    if ExecutionStatus.WRONG_ANSWER in statuses:
        return ExecutionStatus.WRONG_ANSWER
    return ExecutionStatus.SUCCESS


def _batch_message(
    status: ExecutionStatus,
    fixture_results: tuple[FixtureRunResult, ...],
) -> str:
    if status == ExecutionStatus.SUCCESS:
        return "All fixture pairs passed."
    if status == ExecutionStatus.WRONG_ANSWER:
        return "At least one fixture produced wrong output."
    if status == ExecutionStatus.RUNTIME_ERROR:
        missing_runtime = _missing_runtime_executable_name(fixture_results)
        if missing_runtime is not None:
            return f"Missing runtime executable: {missing_runtime}."
        return "At least one fixture failed at runtime."
    if status == ExecutionStatus.TIMEOUT:
        return "At least one fixture exceeded timeout."
    return "Compilation failed."


def _missing_executable_name(result: ProcessResult) -> str | None:
    if result.exit_code != 127 or not result.command:
        return None

    stderr = result.stderr.strip()
    if stderr.startswith("Executable not found:"):
        remainder = stderr.removeprefix("Executable not found:").strip()
        if remainder:
            return remainder.split(" ", 1)[0]
    return Path(result.command[0]).name or result.command[0]


def _missing_runtime_executable_name(
    fixture_results: tuple[FixtureRunResult, ...],
) -> str | None:
    for result in fixture_results:
        if result.exit_code == 127:
            stderr = result.stderr.strip()
            if stderr.startswith("Executable not found:"):
                remainder = stderr.removeprefix("Executable not found:").strip()
                if remainder:
                    return remainder.split(" ", 1)[0]
    return None


def _write_process_log(log_path: Path, result: ProcessResult) -> None:
    command = " ".join(result.command)
    log_text = (
        f"command: {command}\n"
        f"exit_code: {result.exit_code}\n"
        f"timed_out: {result.timed_out}\n"
        f"duration_seconds: {result.duration_seconds:.6f}\n"
        "--- stdout ---\n"
        f"{result.stdout}"
        "\n--- stderr ---\n"
        f"{result.stderr}"
    )
    log_path.write_text(log_text, encoding="utf-8")
