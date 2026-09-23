"""Configured, auditable single-file execution for the FPS protocol."""
from dataclasses import asdict
from pathlib import Path
import os
import subprocess
import time

from rttdist.experiment_io import digest, read_json, write_json

# Python and Java are intermediate-only control languages (v1/abs_EXPERIMENT.md 1장);
# their runtime tool is the interpreter, respectively the javac compiler.
EXTENSIONS = {'cpp':'cpp', 'c':'c', 'haskell':'hs', 'prolog':'pl', 'python':'py', 'java':'java'}

def process(command, cwd, timeout, input_text=None, tool_directory=None):
    start = time.monotonic()
    env = os.environ.copy()
    env['PATH'] = str(tool_directory or Path(command[0]).parent) + os.pathsep + env.get('PATH','')
    try:
        p = subprocess.run(command, cwd=cwd, input=input_text, capture_output=True,
                           text=True, encoding='utf-8', errors='replace', timeout=timeout, env=env)
        return {'command':command, 'exit_code':p.returncode, 'stdout':p.stdout,
                'stderr':p.stderr, 'timed_out':False, 'seconds':time.monotonic()-start}
    except subprocess.TimeoutExpired as e:
        decode = lambda s: s.decode('utf-8',errors='replace') if isinstance(s,bytes) else (s or '')
        return {'command':command,'exit_code':None,'stdout':decode(e.stdout),
                'stderr':decode(e.stderr),'timed_out':True,'seconds':time.monotonic()-start}

def canonical_output(s):
    return '\n'.join(line.rstrip() for line in s.strip().splitlines())

def evaluate(source, language, problem, folder, runtime):
    problem, folder = Path(problem).resolve(), Path(folder).resolve()
    pairs = [(p,p.with_suffix('.out')) for p in sorted((problem/'evaluation').glob('*.inp'))]
    minimum = runtime.get('minimum_evaluation_cases', 10)
    if len(pairs) < minimum or any(not o.is_file() for _,o in pairs):
        raise ValueError(f'At least {minimum} complete evaluation pairs required')
    contract = {'source':digest(source.encode()), 'language':language, 'runtime':runtime,
                'inputs':{str(p):digest(p.read_bytes()) for pair in pairs for p in pair}}
    record = folder/'evaluation.json'
    if record.exists():
        old = read_json(record)
        if old['contract'] != contract: raise ValueError('Evaluation cache contract changed')
        return old
    folder.mkdir(parents=True, exist_ok=True)
    path = folder/('Main.'+EXTENSIONS[language])
    path.write_text(source,encoding='utf-8',newline='')
    executable = str(folder/('program.exe' if os.name=='nt' else 'program'))
    tool = runtime['tools'][language]
    if language in ('cpp', 'c'):
        compile_cmd = [tool,'-O2','-std=c++17' if language == 'cpp' else '-std=c11',str(path),'-o',executable]
        run_cmd = [executable]
    elif language == 'haskell':
        compile_cmd = [tool,'-O2','-outputdir',str(folder),'-o',executable,str(path)]
        run_cmd = [executable]
    elif language == 'prolog':
        compile_cmd = [tool,'-q','--on-error=status','-l',str(path),'-g','halt']
        run_cmd = [tool,'-q','--on-error=status','-l',str(path),'-g','main','-t','halt']
    elif language == 'python':
        compile_cmd = [tool,'-m','py_compile',str(path)]
        run_cmd = [tool,str(path)]
    elif language == 'java':
        java = str(Path(tool).with_name('java'+Path(tool).suffix))
        compile_cmd = [tool,'-encoding','UTF-8','-d',str(folder),str(path)]
        run_cmd = [java,'-cp',str(folder),'Main']
    else:
        raise ValueError(f'Unsupported evaluation language {language}')
    # Pass an isolated environment to each child. Parallel model workers must
    # never mutate the process-wide PATH, including compiler DLL lookup.
    compiled = process(compile_cmd,folder,runtime['compile_timeout'],tool_directory=Path(tool).parent)
    result = {'contract':contract,'compile':compiled,'cases':[], 'status':'success'}
    if compiled['timed_out']: result['status']='compile_timeout'
    elif compiled['exit_code'] != 0: result['status']='compile_error'
    if result['status']=='success':
        for inp,out in pairs:
            p = process(run_cmd,folder,runtime['fixture_timeout'],inp.read_text(encoding='utf-8'),tool_directory=Path(tool).parent)
            status = ('timeout' if p['timed_out'] else 'runtime_error' if p['exit_code'] != 0 else
                      'success' if canonical_output(p['stdout']) == canonical_output(out.read_text(encoding='utf-8')) else 'wrong_answer')
            result['cases'].append({'case':inp.stem,'status':status,**p})
            if status!='success' and result['status']=='success': result['status']=status
    write_json(record,result)
    return result
