import toml
import os

def new_ivlog_project(project_name, path = '.'):
    data = {
        'project': project_name,
        'testbench': {}
    }
    if not os.path.exists(path+"/"+project_name):
        os.makedirs(path+"/"+project_name)
    os.makedirs(path+"/"+project_name+"/src")
    os.makedirs(path+"/"+project_name+"/tests")
    os.makedirs(path+"/"+project_name+"/simulation")
    with open(path+"/"+project_name+"/"+project_name+".v", 'w') as f:
        f.write(f"module {project_name}();\nendmodule\n")
    with open(path+"/"+project_name+"/ivlogproject.toml", 'w') as f:
        toml.dump(data, f)
    print(f"Created project {project_name}")

if __name__ == '__main__':
    new_ivlog_project('test1')