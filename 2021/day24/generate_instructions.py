"""Generate instructions from an input file
"""
import sys

def get_method_declaration(i: int):
    return f'@cache\ndef instruction{i}(z: int, w: int):\n'

def format_instruction(ins: str, a: str, b: str):
    if ins == 'mul':
        # print(f'In mul, a, b: {a}, {b}')
        if b == '0':
            return f'{a} = 0'
        else:
            return f'{a} *= {b}'

    if ins == 'add':
        return f'{a} += {b}'

    if ins == 'div':
        return f'{a} = int({a} / {b})'

    if ins == 'mod':
        return f'{a} = {a} % {b}'

    if ins == 'eql':
        return f'{a} = 1 if {a} == {b} else 0'

if __name__ == "__main__":
    try:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
    except:
        print(f'Usage: {sys.argv[0]} <intput file> <output file>')
        sys.exit(1)

    with open(input_file_name, 'r') as f:
        # Things to note in the instructions that are used in the generation
        # of the methods:
        # 1. Every `w` is only set with input, and then only used, never
        #    updated
        # 2. after every `inp w`, x and y are always multiplied with 0,
        #    resetting their value
        # 3. z continues on
        #
        # With these observations, the instructions can be cut up into 14
        # individual pieces, each taking an z and a w as input, and x and y
        # are set to 0, and their first `mut . 0` is ignored (or sets it to
        # zero there)
        instructions = [chunck.strip().split('\n') for chunck in f.read().strip().split('inp w\n')][1:]
        
    with open(output_file_name, 'w') as f:
        f.write('from functools import cache\n\n')
        for i, instruction_set in enumerate(instructions):
            f.write(get_method_declaration(i+1))

            for ins, a, b in [line.split() for line in instruction_set]:
                f.write('\t' + format_instruction(ins, a, b) + '\n')

            f.write('\treturn z\n\n')
        
        f.write('INSTRUCTIONS = {\n')
        for i in range(len(instructions)):
            f.write(f'\t{i+1}: instruction{i+1},\n')
        f.write('}\n')
