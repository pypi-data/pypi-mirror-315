import subprocess
import sys
import os
import toml

def check_executable(executable):
    result = subprocess.run(['which', executable], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0

def run_testbench(testbench,path = "."):
    required_executables = ['iverilog', 'vvp', 'gtkwave']
    for exe in required_executables:
      if not check_executable(exe):
        print(f"Error: {exe} is not installed. Please install it and try again.")
        sys.exit(1)

    testbench_config_path = os.path.join(path, 'ivlogproject.toml')
    if not os.path.exists(testbench_config_path):
      print(f"Error: {testbench_config_path} does not exist.")
      sys.exit(1)

    with open(testbench_config_path, 'r') as config_file:
      config = toml.load(config_file)

    testbench_file = config.get('testbench').get(testbench)
    #print(testbench_file)
    if not os.path.exists(os.path.join(path,"simulation",testbench)):
      os.makedirs(os.path.join(path,"simulation",testbench))
    # Compile the testbench
    compile_command = ['iverilog', '-o',os.path.join(path,"simulation",testbench,testbench)+".vvp", os.path.join(path,"tests",testbench_file.get("tb_module"))] + [os.path.join(path,"src",source) for source in testbench_file.get("sources")]
    compile_result = subprocess.run(compile_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if compile_result.returncode != 0:
      print(f"Error: Compilation failed.\n{compile_result.stderr.decode()}")
      sys.exit(1)

    # Run the compiled testbench

    run_command = ['vvp', '-v', testbench+".vvp"]
    print(os.path.join(path,"simulation",testbench))
    #print(run_command)
    run_result = subprocess.run(run_command,cwd=os.path.join(path,"simulation",testbench), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run_result.returncode != 0:
      print(f"Error: Running testbench failed.\n{run_result.stderr.decode()}")
      sys.exit(1)

    run_command = ['gtkwave', "-g",testbench_file.get("dump_file")]
    run_result = subprocess.run(run_command,cwd=os.path.join(path,"simulation",testbench), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if run_result.returncode != 0:
      print(f"Error: Show wave failed.\n{run_result.stderr.decode()}")
      sys.exit(1)

if __name__ == '__main__':
    run_testbench('tb1')