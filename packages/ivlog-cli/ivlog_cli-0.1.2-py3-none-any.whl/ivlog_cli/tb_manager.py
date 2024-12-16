import toml

def new_testbench(testbench, path = "."):
    with open(path+"/"+'ivlogproject.toml', 'r') as f:
        data = toml.load(f)
        project_name = data.get('project')
        testbenchs:dict = data.get('testbench')
        with open(path+"/"+"tests"+'/'+testbench+'.v', 'w') as f:
            f.write(f"module {testbench}();\n\nendmodule\n")
        data = {testbench:{"tb_module":testbench+".v","sources":[],"dump_file":testbench+".vcd"}}
        data = testbenchs | data
        data = {"project":project_name,"testbench":data}
    with open(path+"/"+'ivlogproject.toml', 'w') as f:
        toml.dump(data, f)
    print(f"Created testbench {testbench}")

if __name__ == '__main__':
    new_testbench('tb1')