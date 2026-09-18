"""Explicit single-file entry points for the ABS language routes."""
from pathlib import Path
import os

from rttdist.exec.adapters import ExecutionAdapter, _run_subprocess

SCALA_HOME = Path(__file__).resolve().parents[3] / 'docs/abs/tools/scala-2.13.16'


class ExtendedExecutionAdapter(ExecutionAdapter):
    def __init__(self, language):
        super().__init__(language=language)

    def _source_filename(self):
        return {'scala': 'Main.scala', 'haskell': 'Main.hs', 'prolog': 'main.pl'}[self.language]

    def _compile(self, *, prepared_source_path, work_directory, timeout_seconds):
        if self.language == 'scala':
            build = work_directory / 'build'
            build.mkdir(exist_ok=True)
            command = ['java', '-cp', str(SCALA_HOME / 'lib/*'), 'scala.tools.nsc.Main',
                       '-usejavacp', '-encoding', 'UTF-8', '-d', str(build), str(prepared_source_path)]
        elif self.language == 'haskell':
            command = ['ghc', '-O2', '-outputdir', str(work_directory),
                       '-o', str(work_directory / 'program.exe'), str(prepared_source_path)]
        else:
            command = ['swipl', '-q', '--on-error=status', '-l', str(prepared_source_path), '-g', 'halt']
        return _run_subprocess(command=command, cwd=work_directory,
                               timeout_seconds=timeout_seconds, input_text=None)

    def _run(self, *, prepared_source_path, work_directory, timeout_seconds, input_text):
        if self.language == 'scala':
            classpath = os.pathsep.join((str(work_directory / 'build'), str(SCALA_HOME / 'lib/scala-library.jar')))
            command = ['java', '-cp', classpath, 'Main']
        elif self.language == 'haskell':
            command = [str(work_directory / 'program.exe')]
        else:
            command = ['swipl', '-q', '--on-error=status', '-l', str(prepared_source_path),
                       '-g', 'main', '-t', 'halt']
        return _run_subprocess(command=command, cwd=work_directory,
                               timeout_seconds=timeout_seconds, input_text=input_text)
