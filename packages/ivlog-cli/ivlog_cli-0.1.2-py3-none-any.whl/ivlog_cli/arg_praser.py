import argparse
import os
import toml
from .new_ivlog_project import new_ivlog_project
from .tb_manager import new_testbench
from .list_tb import list_testbench
from .run_iverilog import run_testbench

class Ivlog_Praser():
    def __init__(self):
        self.path = None         # 项目路径
        self.project_name = None # 项目名称
        self.testbench = None    # 测试点名称
        self.load_project()      # 加载项目

    def load_project(self):
        if os.path.exists('ivlogproject.toml'):
            with open('ivlogproject.toml', 'r') as f:
                data = toml.load(f)
                self.project_name = data.get('project')
                self.testbench = data.get('testbench')
                self.path = os.path.abspath('.')
                print(f"Loaded project {self.project_name} at {self.path}")
        else:
            self.path = os.path.abspath('.')



    def ivlog_praser(self):

        parser = argparse.ArgumentParser(description="Verilog Project Manager")
        subparsers = parser.add_subparsers(dest='command')

        parser_new = subparsers.add_parser('new', help='Create new project') # 创建新项目
        parser_new.add_argument('project_name', type=str, help='Project name')

        parser_tb = subparsers.add_parser('tb', help='Create new testbench') # 创建新tb
        parser_tb.add_argument('testbench', type=str, help='testbench name')

        parser_list = subparsers.add_parser('list', help='list testbench') # 展示tb
        parser_list.add_argument('testbench', nargs='?',default=None, help='specfic testbench')

        parser_run = subparsers.add_parser('run', help='run testbench') # 运行tb
        parser_run.add_argument('testbench', help='specfic testbench')
        args = parser.parse_args()

        match args.command:
            case 'new':
                new_ivlog_project(args.project_name, self.path)
            case 'tb':
                new_testbench(args.testbench,self.path)
            case 'list':
                list_testbench(args.testbench,self.path)
            case 'run':
                run_testbench(args.testbench,self.path)
            case _:
                parser.print_help()
    

def run():
    praser = Ivlog_Praser()
    praser.ivlog_praser()