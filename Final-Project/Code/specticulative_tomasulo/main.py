from CDB import CDB
from ROB import Reorder_Buffer, StateName
from Reservation_Station import *
import sys
import random
from Inst_IO import *

inpath = './Data/input2.txt'
outpath = './Data/output2.txt'

if __name__ == '__main__':

    
    sys.stdout = open(outpath, 'w')
    registers_name = {'F' + str(i): '' for i in range(0, 11)}
    registers_state = {'F' + str(i): 'No' for i in range(0, 11)}
    registers = {'R' + str(i): random.randint(1, 50)
                for i in range(1, 4)}
    registers.update({'F' + str(i): random.randint(1, 20)
                    for i in range(0, 11)})
    memory = [random.randint(1, 50) for _ in range(2048)]
    rob = Reorder_Buffer()

    cdb = CDB()
    loads = Load_Buffer(CDB=cdb, ROB=rob, register_states=registers_state,
                        memory=memory, registers=registers)  # 实例化
    fp_adders = FP_Adders(CDB=cdb, ROB=rob,
                        register_states=registers_state, memory=memory, registers=registers)  # 实例化
    fp_multipliers = FP_multipliers(CDB=cdb, ROB=rob,
                            register_states=registers_state, memory=memory, registers=registers)  # 实例化
    
    
    cycle = 1
    line = 0
    top = 0
    bottom = 0
    insert_sign = 0
    delete_sign = 0

    instructions = []
    result = []
    instructions=read_instructions(instructions,file_path=inpath)
    instructions=pretreat(instructions)

    line, bottom = load_instructions_to_reorder_buffer(
        instructions, rob, line, bottom)
    # Speculative Tomasulo
    while top != bottom:
        # 逆序执行
        # 删除标记
        top, delete_sign, insert_sign = handle_delete_sign(
            rob, top, bottom, delete_sign, insert_sign)
        if top == None: break
        
        # commit
        delete_sign = commit(rob, top, registers, registers_name,
                             registers_state, result, delete_sign, cycle)
        
        
        # 写结果                  
        write_result(cdb, rob, loads, fp_adders, fp_multipliers, cycle)
        #执行
        loads.execute(cycle)
        fp_adders.execute(cycle)
        fp_multipliers.execute(cycle)

        # 发射
        top = issue_instructions(rob, top, bottom, loads, fp_adders,
                                 fp_multipliers, registers_name, registers_state, registers, cycle)
        
        line, bottom, insert_sign = handle_insert_sign(
            line, bottom, instructions, rob, insert_sign)

        display_status(cycle, rob, loads, fp_adders,
                       fp_multipliers, registers_name, registers_state)
        cycle += 1

    display_result(result=result)
    sys.stdout.close()

