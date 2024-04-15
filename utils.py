import os
import subprocess
import sys
import shutil
import platform
import json

def execute_ignore_stdout(argv, env=None, cwd=None):
    try:
        output = subprocess.check_output(argv, stderr=subprocess.STDOUT, env=env, cwd=cwd, text=True)
        return output
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e

def execute_stdout(argv, env=None, cwd=None, err=0):
    try:
        process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, cwd=cwd, text=True)
        out, err = process.communicate()
        
        if process.returncode != 0 and err==1:
            print(f"Something went wrong: {err}")
        return out
    except subprocess.CalledProcessError as e:
        print(e.output)
        raise e

def execute_and_redirect_stdout_to_file(argv, env=None, cwd=None, err=0, outfile=""):
    with open(outfile, 'w') as file:
        try:
            process = subprocess.Popen(argv, stdout=file, stderr=subprocess.PIPE, env=env, cwd=cwd, text=True)
            out, err = process.communicate()
            
            if process.returncode != 0 and err==1:
                print(f"Something went wrong: {err}")
            return out
        except subprocess.CalledProcessError as e:
            print(e.output)
            raise e

def execute(argv, env=os.environ, cwd=None, stdout=True, outfile="", root=False):
    if not isinstance(argv, list):
        argv = [argv]

    if root and platform.system() == 'Linux':
        argv = ["sudo"] + argv

    if stdout:
        return execute_stdout(argv, env, cwd)
    elif len(outfile)>0:
        return execute_and_redirect_stdout_to_file(argv, env, cwd, outfile=outfile)
    else:
        return execute_ignore_stdout(argv, env, cwd)
    
def file_exists(path):
    return os.path.exists(path)

def rmdir(path):
    shutil.rmtree(path, ignore_errors=True)

def dict_list_to_json(out):
    return json.dumps(out, indent=2)

def create_dir(path):
    if not os.path.exists(path):
        os.makedirs(path)