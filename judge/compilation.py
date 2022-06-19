import shutil
import subprocess
from typing import List, Optional

import judge.constants as constants
import judge.extensions as extensions

from .language import Language


class CompilationError(Exception):
    pass


def prepare(language: Language, box_id: int, base_name: str, code: str, cleanup: bool) -> List[str]:
    if cleanup:
        subprocess.run(['isolate', '-b', str(box_id), '--silent', '--cleanup'])
        subprocess.run(['isolate', '-b', str(box_id), '--silent', '--init'], stdout=subprocess.PIPE)
    sandbox_path = f'/var/local/lib/isolate/{box_id}/box'
    code_filename = f'{base_name}.{extensions.file_extensions[language]}'
    executable_path = f'run/{base_name}'
    code_path = f'run/{code_filename}'
    with open(code_path, 'w') as f:
        f.write(code)

    compile_args = None
    run_args = None
    if language == Language.cpp:
        compile_args = ['g++', '-O2', '-o', executable_path, code_path, '--std=c++17' ]
    elif language == Language.c:
        compile_args = ['gcc', '-O2', '-o', executable_path, code_path]
    elif language == Language.ocaml:
        compile_args = ['ocamlopt', '-S', '-o', executable_path, code_path]
    elif language == Language.pas:
        compile_args = ['fpc', '-O2', '-Sg', '-v0', '-XS', code_path, '-o' + executable_path]
    elif language == Language.py:
        run_args = ['/usr/bin/python3', code_filename]

    if compile_args:
        compile_proc = subprocess.run(compile_args, text=True, stderr=subprocess.PIPE)
        if compile_proc.returncode != 0:
            raise CompilationError
        shutil.copy(executable_path, sandbox_path)  # copies executable to sandbox
        if not run_args:
            run_args = [base_name]  # run by directly calling the name of executable
    else:
        shutil.copy(code_path, sandbox_path)
    return run_args


def run(run_args: List[str], box_id: int, input_: str,
        metadata_path: Optional[str] = None,
        time_limit: Optional[float] = None,
        memory_limit: Optional[int] = None) -> subprocess.CompletedProcess:
    if constants.DEBUG:
        print(' '.join(['isolate', '-b', str(box_id)] +
                       (['-M', metadata_path] if metadata_path else []) +
                       (['-t', str(time_limit)] if time_limit else []) +
                       (['-w', str(20)] if time_limit else []) +  # wall time
                       (['-m', str(memory_limit * 1024)] if memory_limit else []) +  # in kilobytes
                       ['--silent', '--run', '--'] + run_args))
    return subprocess.run(['isolate'] +
                          (['-M', metadata_path] if metadata_path else []) +
                          (['-b', str(box_id)] if box_id else []) +
                          (['-t', str(time_limit)] if time_limit else []) +
                          (['-w', str(20)] if time_limit else []) +  # wall time
                          (['-m', str(memory_limit * 1024)] if memory_limit else []) +  # in kilobytes
                          ['--stderr-to-stdout', '--silent', '--run', '--'] + run_args,
                          input=input_,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          text=True)
