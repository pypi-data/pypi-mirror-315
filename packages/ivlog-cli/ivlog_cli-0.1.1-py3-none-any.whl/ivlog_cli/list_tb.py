import toml

def list_testbench(testbench = None, path = "."):
    with open(path+"/"+'ivlogproject.toml', 'r') as f:
        data = toml.load(f)
        project_name = data.get('project')
        print(f"Project {project_name}\n")
        testbenchs:dict = data.get('testbench')
        if not testbench:
            print("Testbenchs:")
            for tb in testbenchs:
                print(f"{tb}")
        else:
            print(f"Testbench:{testbench}\n")
            data = data.get('testbench').get(testbench)
            print(f"tb_module: {data.get('tb_module')}\n")
            print(f"source: {data.get('sources')}\n")
        
if __name__ == '__main__':
    list_testbench(testbench="test2")