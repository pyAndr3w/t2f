from collections import defaultdict
from pprint import pprint
import argparse
from t2f.utils import topo_sort
import os
import re


class Opcode(object):

    def __init__(self, opcode, params=None):
        self.opcode = opcode
        self.params = params
    
    def build(self):
        if self.params is None:
            return self.opcode
        else:
            params_str = " ".join(self.params)
            return f"{params_str} {self.opcode}"
    

class Continuation(object):

    def __init__(self, cont_type="ordinary"):
        self.opcodes = []
        self.type = cont_type

    def change_type(self, new_type):
        self.type = new_type
        
        
    def add_opcode(self, opcode):
        if opcode is not None:
            self.opcodes.append(opcode)
    
    def build(self):
        result = f"{self.type}:<" + "{"
        result += self.build_body()
        return result + "\n}>"

    def build_body(self):
        result = ""
        for idx, opcode in enumerate(self.opcodes):
            if opcode != None:
                result += "\n" + opcode.build()
        return result


class Procedure(object):

    def __init__(self, code):
        code_lines = code.split('\n')
        self.name = code_lines[0]
        self.body = Procedure.process_code(code_lines[1:])
    
    def process_code(code_lines):
        result_list = [Continuation()]
        
        for line in code_lines:
            if '<{' in line:
                cont_type = re.findall(r'([\w\d]+):<{', line)[0]
                if cont_type == "IFELSE":
                    cont_type = "ELSE"
                    result_list[-1].opcodes[-1].change_type("IF")
                result_list.append(Continuation(cont_type))
            elif '}>' in line:
                cont_0 = result_list.pop()
                cont_1 = result_list.pop()
                if cont_0.type == "CALLREF":
                    cont_1.opcodes += cont_0.opcodes
                    result_list.append(cont_1)
                else:
                    cont_1.add_opcode(cont_0)
                    result_list.append(cont_1)
            else:
                ll = line.split(" ")
                opcode_name = ll[-1]
                params = None
                if len(ll) > 1:
                    params = ll[0:-1]
                if opcode_name == "IFELSE":
                     result_list[-1].opcodes[-1].change_type("ELSE")
                     result_list[-1].opcodes[-2].change_type("IF")
                else:
                    cont_0 = result_list.pop()
                    cont_0.add_opcode(Opcode(opcode_name, params))
                    result_list.append(cont_0)
        cont_0 = result_list[0]
        proc_code = cont_0.build_body()
        proc_code = re.sub(r'}>\s*ELSE:<{', r'}>ELSE<{', proc_code)
        return proc_code


class Program(object):   

    def __init__(self, procs, root=''):
        self.procs = procs
        self.root = root
    
    def declar_proc(r, proc):
        return f"{r}DECLPROC {proc.name}\n"
    
    def add_proc_body(r, proc):
        return f"{r}{proc.name} PROCINLINE:<{'{'}{proc.body}\n{'}'}>\n\n"
    
    def build(self):
        r = "<{\n\n"
        for proc in self.procs:
            r = Program.declar_proc(r, proc)
        r += "\n"
        for proc in self.procs:
            r = Program.add_proc_body(r, proc)
        r += "IFNOT: recv_internal INLINECALL\n\n"
        return r + self.root + "}>"

    def return_cell(self):
        return self.build() + "c"
    
    def return_slice(self):
        return self.build() + "s"


def sort_procs(procedures):
    procedures = {proc.name:proc for proc in procedures}

    proc_names = procedures.keys()
    proc_inlines = {procedures[proc].name:re.findall(r'([\w\d]+) INLINECALL', procedures[proc].body) for proc in procedures}

    graph = defaultdict(list)
    for func in proc_names:
        graph[func] = []
        if func in proc_inlines:
            for called_func in proc_inlines[func]:
                graph[func].append(called_func)

    sorted_functions = topo_sort(graph)
    sorted_functions.reverse()
    
    return [procedures[proc] for proc in sorted_functions]


def translate(in_path, out_path):
    with open(in_path) as file:
        code: str = file.read()
    
    # REPLACES BLOCK
    code = code.replace(".internal-alias :main_internal, 0\n.internal :main_internal", "recv_internal")
    code = re.sub(r'.macro (\w+)', r'\1', code)

    code = code.replace("\s$", "")
    code = code.replace("^\s", "")
    code = code.replace(" {", ":<{")
    code = code.replace(",", "")
    code = code.replace("}", "}>")
    code = code.replace("PUSHCONT:<{", "CONT:<{")
    code = code.replace("IFREF", "IF")
    code = code.replace("IFJMPREF", "IFJMP")
    code = code.replace("IFNOTJMPREF", "IFNOTJMP")

    code = re.sub(r'S(\d+)', r's\1', code)
    code = re.sub(r'C(\d+)', r'c\1', code)

    code = re.sub(r'CALL \$(.*?)\$', r'INLINECALL \1', code)

    code = re.sub(r'(STSLICECONST|PUSHSLICE) x([\w_]+)', r'\1 x{\2}', code)
    code = re.sub(r';.+', r'', code)

    code = re.sub(r'( *)(\w+ )([\w \-{}]+)*', r'\1\3 \2', code)

    code = re.sub(r'(\d+ MODPOW2)', r'\1#', code)

    code = re.sub(r'\t+', r'', code)
    code = re.sub(r'[ ]+', r' ', code)
    code = re.sub(r'[ ]*(\n+)[ ]*', r'\1', code)

    # BUILD
    procs = [Procedure(proc_code) for proc_code in code.split("\n\n")[1:]]

    prog = Program(sort_procs(procs))
    prog_code = prog.return_cell()


    lvl = 0
    proc_rows = prog_code.split("\n")
    for idx, row in enumerate(proc_rows):
        if "}>" in row:
            lvl -= 1
        if lvl > 0:
            new_row = "    " * lvl + row
            proc_rows[idx] = new_row
        if "<{" in row:
            lvl += 1
    prog_code = "\n".join(proc_rows)

    with open(out_path, 'w') as file:
        file.write(prog_code)


def main():

    parser = argparse.ArgumentParser(
        prog='t2f',
        description='TVM Assembly to Fift Assembly Translator',
    )

    parser.add_argument('filename')
    parser.add_argument('-o', '--output', dest='output', default=None, help='output file name')
    args = parser.parse_args()

    default_output = f'{os.path.splitext(args.filename)[0]}.fif'
    args.output = default_output if args.output is None else args.output
    
    translate(args.filename, args.output)


if __name__ == '__main__':
    main()
