from collections import defaultdict
from pprint import pprint
import argparse
from t2f.utils import topo_sort
from t2f.stdlib import stdlib
from t2f.patched_asm import patched_asm
import os
import re


class Opcode(object):

    def __init__(self, opcode, params=None):
        self.opcode = opcode
        self.params = params

        if opcode == "XCHG" and len(params) == 1:
            self.opcode = "XCHG0"
    
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
        global DEBUG
        result_list = [Continuation()]
        
        for line in code_lines:
            if DEBUG: print(line)
            if line == "":
                continue
            if '<{' in line:
                cont_type = re.findall(r'([\w\d]+):<{', line)[0]
                # if cont_type == "IFELSE":
                #     result_list[-1].opcodes[-1].change_type("IF")
                
                result_list.append(Continuation(cont_type))
            elif '}>' in line:
                cont_0 = result_list.pop()
                cont_1 = result_list.pop()
                if cont_0.type == "CALLREF":
                    cont_1.opcodes += cont_0.opcodes
                elif cont_0.type == "PUSHSLICE":
                    new_opcode = Opcode("PUSHSLICE", ["x{}"])
                    if len(cont_0.opcodes):
                        slice_bits = cont_0.opcodes[0].params
                        new_opcode = Opcode("PUSHSLICE", slice_bits)
                    cont_1.opcodes.append(new_opcode)
                elif cont_0.type == "PUSHREF":
                    new_opcode = Opcode("PUSHREF", ["<b b>"])
                    if len(cont_0.opcodes):
                        ref_bits = cont_0.opcodes[0].params[0]
                        new_opcode = Opcode("PUSHREF", [f"<b {ref_bits} s, b>"])
                    cont_1.opcodes.append(new_opcode)
                elif cont_0.type == "IFELSE":
                    cont_0.change_type("IF")
                    cont_else = cont_1.opcodes.pop()
                    cont_else.change_type("ELSE")
                    cont_1.opcodes.append(cont_0)
                    cont_1.opcodes.append(cont_else)
                elif cont_0.type == "SECOND_":
                    cont_1.opcodes[-1].change_type("IF")
                    cont_0.change_type("ELSE")
                    cont_1.opcodes.append(cont_0)
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
                elif opcode_name in ["IF", "IFNOT", "REPEAT", "IFJMP", "IFNOTJMP"]:
                     result_list[-1].opcodes[-1].change_type(opcode_name)
                elif opcode_name == "WHILE":
                     result_list[-1].opcodes[-1].change_type("DO")
                     result_list[-1].opcodes[-2].change_type("WHILE")
                else:
                    cont_0 = result_list.pop()
                    cont_0.add_opcode(Opcode(opcode_name, params))
                    result_list.append(cont_0)
        cont_0 = result_list[0]
        proc_code = cont_0.build_body()
        proc_code = re.sub(r'}>\s*ELSE:<{', r'}>ELSE<{', proc_code)
        proc_code = re.sub(r'}>\s*DO:<{', r'}>DO<{', proc_code)
        return proc_code


class Program(object):   

    def __init__(self, procs, root=''):
        self.procs = procs
        self.root = root
    
    def declar_proc(r, proc_name):
        return f"{r}DECLPROC {proc_name}\n"
    
    def add_proc_body(r, proc):
        return f"{r}{proc.name} PROCINLINE:<{'{'}{proc.body}\n{'}'}>\n\n"
    
    def build(self):
        r = "<{\n\n"
        for proc_name in self.procs.keys():
            r = Program.declar_proc(r, proc_name)
        r += "\n"
        for proc in self.procs:
            r = Program.add_proc_body(r, self.procs[proc])
        internal = "recv_internal" in self.procs.keys()
        external = "recv_external" in self.procs.keys()
        ticktock = "run_ticktock" in self.procs.keys()
        if internal and not external and not ticktock:
            r += "IFNOT: recv_internal INLINECALL\n\n"
        else:
            if ticktock:
                r += "DUP -2 EQINT IFJMP:<{\n" \
                        "DROP run_ticktock INLINECALL\n" \
                    "}>\n\n"
            if internal:
                r += "DUP 0 EQINT IFJMP:<{\n" \
                        "DROP recv_internal INLINECALL\n" \
                    "}>\n\n"
            if external:
                r += "-1 EQINT IFJMP:<{\n" \
                        "recv_external INLINECALL\n" \
                    "}>\n\n"
                  
        return r + self.root + "}>"

    def return_cell(self):
        return self.build() + "c"
    
    def return_slice(self):
        return self.build() + "s"


def sort_procs(procedures):
    proc_names = procedures.keys()
    proc_inlines = {procedures[proc].name:re.findall(r'([\w\d]+) INLINECALL', procedures[proc].body) for proc in procedures}

    graph = defaultdict(list)
    for func in proc_names:
        graph[func] = []
        if func in proc_inlines:
            for called_func in proc_inlines[func]:
                graph[func].append(called_func)
    
    # remove unused funcs
    new_graph = defaultdict()
    funcs = []
    if "recv_internal" in graph:
        funcs.append("recv_internal")
    if "recv_external" in graph:
        funcs.append("recv_external")
    if "run_ticktock" in graph:
        funcs.append("run_ticktock")
    f_len = -1
    while (f_len != len(funcs)):
        f_len = len(funcs)
        new_funcs = funcs
        for f in funcs:
            new_graph[f] = graph[f]
            new_funcs = list(set(new_funcs + graph[f]))
        funcs = new_funcs
            
    sorted_functions = topo_sort(new_graph)
            
    sorted_functions.reverse()
    
    return {proc:procedures[proc] for proc in sorted_functions}


def translate(args):
    with open(args.filename) as file:
        code: str = file.read()
    
    code = stdlib + code
    
    # REPLACES BLOCK
    code = re.sub(r'\n\n[\n]*', r'\n\n', code)

    code_l = list(filter(lambda block: (".macro" in block) or (".internal-alias" in block), code.split('\n\n')))

    code = "\n\n".join(code_l)

    code = re.sub(r'\.loc.+\n', r'', code)
    code = re.sub(r'\.loc.+$', r'', code)

    code = code.replace(".internal-alias :main_internal, 0\n.internal :main_internal", "recv_internal")
    code = code.replace(".internal-alias :main_external, -1\n.internal :main_external", "recv_external")
    code = code.replace(".internal-alias :onTickTock, -2\n.internal :onTickTock", "run_ticktock")
    code = re.sub(r'.macro (\w+)', r'\1', code)

    if len(re.findall(r'onCodeUpgrade', code)):
        print("ERROR: onCodeUpgrade currently is not supported")
        exit(1)
        
    code = code.replace("\s$", "")
    code = code.replace("^\s", "")
    code = code.replace(" {", ":<{")
    code = code.replace(",", "")
    code = code.replace(".", "")
    code = code.replace("}", "}>")
    code = code.replace("PUSHCONT:<{", "CONT:<{")
    
    code = code.replace("IFREF", "IF")
    code = code.replace("ELSEREF", "ELSE")
    code = code.replace("IFJMPREF", "IFJMP")
    code = code.replace("IFNOTJMPREF", "IFNOTJMP")
    code = code.replace("PUSHREFSLICE", "PUSHSLICE")

    code = re.sub(r'S(\d+)', r's\1', code)
    code = re.sub(r'S(-\d+)', r's(\1)', code)
    code = re.sub(r'C([-]?\d+)', r'c\1', code)

    code = re.sub(r'CALL \$(.*?)\$', r'INLINECALL \1', code)

    code = re.sub(r'(STSLICECONST|PUSHSLICE|blob) x([\w_]*)', r'\1 x{\2}', code)
    code = re.sub(r'STSLICECONST 0', r'STZERO', code)
    code = re.sub(r'STSLICECONST 1', r'STONE', code)

    code = re.sub(r';.+', r'', code)

    code = re.sub(r'( *)(\w+ )([\w \-{}()]+)*', r'\1\3 \2', code)

    code = re.sub(r'(\d+ MODPOW2)', r'\1#', code)
    code = re.sub(r'(\d+ RSHIFT)', r'\1#', code)
    code = re.sub(r'(\d+ LSHIFT)', r'\1#', code)

    code = re.sub(r'\t+', r'', code)
    code = re.sub(r'[ ]+', r' ', code)
    code = re.sub(r'[ ]*(\n+)[ ]*', r'\1', code)

    code = code.replace("IFELSE\n{", "IFELSE_:<{")
    code = code.replace("\n{", "\nSECOND_:<{")

    # BUILD
    procs = {proc.name:proc for proc in [Procedure(proc_code) for proc_code in code.split("\n\n")]}

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

    prog_code = f"// Translated from TVM-asm: {os.path.basename(args.filename)}\n\n" + prog_code

    if args.asm:
        patched_asm_path = os.path.join(os.path.dirname(args.output), "PatchedAsm.fif")
        with open(patched_asm_path, 'w') as file:
            file.write(patched_asm)
        prog_code = '"PatchedAsm.fif" include\n\n' + prog_code

    if args.tvc:
        prog_code += f'\n\n<b b{{0011}} s, swap ref, <b b> ref, b>\n' \
                     f'2 boc+>B "{os.path.splitext(args.output)[0]}.tvc" B>file\n'

    with open(args.output, 'w') as file:
        file.write(prog_code)

DEBUG = False

def main():
    global DEBUG
    parser = argparse.ArgumentParser(
        prog='t2f',
        description='TVM Assembly to Fift Assembly Translator',
    )

    parser.add_argument('filename')
    parser.add_argument('-o', '--output', dest='output', default=None, help='output file name')
    parser.add_argument('-t', '--tvc', dest='tvc', default=False, help='add tvc generation', action='store_true')
    parser.add_argument('-a', '--asm-include', dest='asm', default=False, help='add PatchedAsm.fif', action='store_true')
    parser.add_argument('--debug', dest='debug', default=False, action='store_true')

    args = parser.parse_args()

    default_output = f'{os.path.splitext(args.filename)[0]}.fif'
    args.output = default_output if args.output is None else args.output
    DEBUG = args.debug
    translate(args)


if __name__ == '__main__':
    main()
