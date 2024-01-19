import copy
def read_instructions(instructions=[], file_path='./Data/input1.txt'):

    with open(file_path, 'r') as file:
        lines = file.read().split("\n")
        for line in lines:
            instructions.append(line.split(" "))
    return instructions

def pretreat(instructions=[]):
    """
    对指令进行预处理
    """
    for i in range(len(instructions)):
        for j in range(len(instructions[i])):
            if instructions[i][j].isdigit():
                instructions[i][j] = int(instructions[i][j])
            else:
                instructions[i][j] = instructions[i][j]
    return instructions


def load_instructions_to_reorder_buffer(instructions, ROB, line, bottom):
    while  line < len(instructions) and  line < 6:
        ROB.buffers[line].instruction = instructions[line]
        ROB.buffers[line].destination = instructions[line][1]
        line += 1
        bottom += 1
    return  line, bottom


def find_proper_unit(op, loader, loads, fp_adders,fp_mults):
    unit = []
    if op == 'LD' or op == 'SD':
        loader = loads.find_no_busy()
        if loader != -1:
            unit = loads.buffers[loader]
    elif op == 'ADDD' or op == 'SUBD':
        loader = fp_adders.free_adders()
        if loader != -1:
            unit = fp_adders.buffers[loader]
    elif op == 'MULTD' or op == 'DIVD':
        loader = fp_mults.free_multipliers()
        if loader != -1:
            unit = fp_mults.buffers[loader]
    return unit, loader


def update_V_and_Q(V,Q,x,y,registers_state,registers,registers_name,rob):
    if type(x) == int:
        V = x
    elif y[0] == 'R' or registers_state[x] == 'No':
        V= copy.copy(registers[x])
    elif rob.buffers[registers_name[x]].value != '':
        V = copy.copy(
            rob.buffers[registers_name[x]].value)
    else:
        Q = registers_name[x]
    
    return V, Q


def display_status(cycle,rob,loads,fp_adders,fp_multipliers,registers_name,registers_state):
    print('cycle :', cycle)
    print("              busy  instruction                        states_name   dest  value")
    rob.display()
    print("        busy  op       Vj                              Vk                              Qj   Qk  dest")
    loads.display()
    fp_adders.display()
    fp_multipliers.display()
    print('registers_name : ', end='')
    for t in registers_name:
        print(str(t) + ':' + f'{str(registers_name[t]):<3}', end=', ')
    print('\nregisters_state : ', end='')
    for t in registers_state:
        print(str(t) + ':' + f'{str(registers_state[t]):<3}', end=', ')
    print()
    print()


def display_result(result):
    print("Finally result :")
    for i in range(len(result)):
        print(result[i][0], ':', result[i][1], result[i][2])


def handle_delete_sign(rob, top, bottom, delete_sign, insert_sign):
    if delete_sign:
        rob.buffers[top % 6].__init__(
            rob.buffers[top % 6].entry)
        top += 1
        delete_sign = 0
        insert_sign = 1
        if top == bottom:
            return None,None,None
    return top, delete_sign, insert_sign


def commit(rob, top, registers, registers_name, registers_state, result, delete_sign, cycle):
    if rob.buffers[top % 6].value != '':
        top_buffer = rob.buffers[top % 6]
        top_buffer.state = 3
        if top_buffer.instruction[0] != 'SD':
            registers[top_buffer.instruction[1]] = top_buffer.value
        top_buffer.busy = 'No'
        registers_name[top_buffer.destination] = ''
        registers_state[top_buffer.destination] = 'No'
        result.append([top_buffer.instruction,
                    top_buffer.states_num, top_buffer.value])
        delete_sign = 1
        top_buffer.states_num[3] = cycle
    return delete_sign


def write_result(cdb, rob, loads, fp_adders, fp_multipliers, cycle):
    if cdb.source_entry != -1:
        rob.buffers[cdb.source_entry].state = 2
        loads.write_in()
        fp_adders.write_in()
        fp_multipliers.write_in()
        rob.buffers[cdb.source_entry].value = copy.copy(
            cdb.data)
        rob.buffers[cdb.source_entry].states_num[2] = cycle
        cdb.source_entry = -1



def issue_instructions(rob, top, bottom, loads, fp_adders, fp_multipliers, registers_name, registers_state, registers, cycle):
    for i in range(top, bottom):
        _buffer = rob.buffers[i % 6]
        print()
        if (_buffer.busy == 'No' or _buffer.busy == False) and (_buffer.value == '' or _buffer.value == None):  # 不忙碌且 value 没算出来
            op = _buffer.instruction[0]
            flag_enable = -1
            unit = ()
            unit, flag_enable = find_proper_unit(op, flag_enable, loads, fp_adders, fp_multipliers)
            if flag_enable != -1:
                    _buffer.state = 0
                    _buffer.busy = 'Yes'
                    unit.busy = 'Yes'
                    unit.Op = op
                    unit.Dest = i % 6
                    registers_name[_buffer.instruction[1]] = i % 6
                    registers_state[_buffer.instruction[1]] = 'Yes'
                    x, y = _buffer.instruction[2], _buffer.instruction[3]

                    unit.Vj, unit.Qj = update_V_and_Q(
                        unit.Vj, unit.Qj, x, y, registers_state, registers, registers_name, rob)
                    unit.Vk, unit.Qk = update_V_and_Q(
                        unit.Vk, unit.Qk, y, y, registers_state, registers, registers_name, rob)
                    _buffer.states_num[0] = cycle
            break
    return top

def handle_insert_sign(line, bottom, instructions, rob, insert_sign):
    if insert_sign:
        if line < len(instructions):
            rob.buffers[bottom % 6].instruction = instructions[line]
            rob.buffers[bottom % 6].destination = instructions[line][1]
            line += 1
            bottom += 1
        insert_sign = 0
    return line, bottom, insert_sign
