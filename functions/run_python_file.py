import os
import subprocess

def run_python_file(working_directory, file_path):
    abs_working_directory = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(working_directory, file_path))
    
    if not os.path.isdir(abs_working_directory):
        return f'Error: "{working_directory}" is not a directory'
    elif not abs_file_path.startswith(abs_working_directory):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(abs_file_path):
        return f'Error: File "{file_path}" not found.'
    elif abs_file_path[-3:] != ".py":
        return f'Error: "{file_path}" is not a Python file.'

    try:
        results = subprocess.run(["python3", file_path], cwd=working_directory, timeout=30, capture_output="True", text=True)
        if results.stdout == "" and results.stderr == "" and results.returncode == 0:
            return "No output produced."
        output = f"STDOUT:{results.stdout}STDERR:{results.stderr}"
        if results.returncode != 0:
            output += f"\nProcess exited with code {results.returncode}"
        return output
    except Exception as e:
        return f"Error: executing Python file: {e}"