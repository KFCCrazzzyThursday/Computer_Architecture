import copy
from CDB import CDB
from ROB import StateName

class Reservation_Station:
    def __init__(self, type="", id=0, CDB=None, ROB=None):
        self.type = type
        self.id = id
        self.busy = False
        self.Op = ''
        self.Vj = ''  # 拷贝可读取的数据
        self.Vk = ''
        self.Qj = ''  # 记录尚不能读取的数据将由哪条指令算出
        self.Qk = ''
        self.Dest = 0  # 目的ROB编号
        self.cdb = CDB
        self.rob = ROB

    def write_in(self):
        if self.busy == 'No':
            return
        if self.Qj == self.cdb.source_entry:
            self.Qj = ''
            self.Vj = copy.copy(self.cdb.data)
        if self.Qk == self.cdb.source_entry:
            self.Qk = ''
            self.Vk = copy.copy(self.cdb.data)

    def display(self):
        print(f'{self.type:<4}{self.id} : ', end= '')
        print(f'{"Yes" if self.busy else "No":<4}', end=', ')
        print(f'{self.Op:<8}', end=', ')
        print(f'{str(self.Vj):<30}', end=', ')
        print(f'{str(self.Vk):<30}', end=', ')
        print(f'{str(self.Qj):<3}', end=', ')
        print(f'{str(self.Qk):<3}', end=', ')
        print(f'{str(self.Dest):<4};')


class Load_Buffer:
    class Load_Buffer_Unit(Reservation_Station):
        def __init__(self,type='load',id=0, CDB=None, ROB=None, register_states_=None):
            super().__init__(type=type,id=id,CDB=CDB,ROB=ROB)
            self.address = ''
            self.flag = 0
            self.register_states = register_states_


        def execute(self,cycle):
            if not self.busy:
                return
            rob_entry = self.rob.buffers[self.Dest]
            rob_entry.update_state(StateName.EXECUTE, 1)
            '''print("asdddddddasdfa")
            print("asdddddddasdfa")'''
            print(self.Qj,self.Qk)
            print(self.Qj,self.Qk)
            print(self.Qj, self.Qk)
            print(self.Qj, self.Qk)
            if self.Qj == '' and self.Qk == '' :
                self.address = self.Vj+self.Vk
                '''print("asdddddddasdfa")
                print("asdddddddasdfa")
                print(self.Op == "LD" or (
                    self.Op == "SD" and self.register_states[f'F{self.Dest}'] == "No"))
                print(self.Op == "LD" or (
                    self.Op == "SD" and self.register_states[f'F{self.Dest}'] == "No"))
                print(self.Op == "LD" or (
                    self.Op == "SD" and self.register_states[f'F{self.Dest}'] == "No"))
                print(self.Op == "LD" or (self.Op == "SD" and self.register_states[f'F{self.Dest}']=="No"))
                print(self.Op == "LD" or (self.Op == "SD" and self.register_states[f'F{self.Dest}']=="No"))
                print(self.Op == "LD" or (self.Op == "SD" and self.register_states[f'F{self.Dest}']=="No"))'''
                if self.Op == "LD" or (self.Op == "SD" and self.register_states[f'F{self.Dest+1}']=="No"):
                    '''print("SDSDSDSDSDSD")
                    print("SDSDSDSDSDSD")
                    print("SDSDSDSDSDSD")
                    print("SDSDSDSDSDSD")
                    print("SDSDSDSDSDSD")'''
                    self.flag = 1

    def __init__(self, CDB=None, ROB=None, register_states=None, memory=None, registers=None):
        self.buffers = [self.Load_Buffer_Unit(id=i, CDB=CDB,ROB=ROB,register_states_=register_states) for i in range(1,3)]
        self.head = 0
        self.memory = memory
        self.ROB = ROB
        self.CDB = CDB
        self.register_states = register_states
        self.registers = registers
        self.count=0
    def write_in(self):
        for i in range(2): self.buffers[i].write_in() 

    def execute(self,cycle):
        # print('cycle',cycle)
        if self.count==6: self.head = 1-self.head
        running_buffer = self.buffers[self.head]
        # flag标志位为1（表示地址计算已完成）
        #if running_buffer.Op == 'SD' and cycle >30 : running_buffer.flag = 1
        if running_buffer.flag:
            
            if running_buffer.Op == 'LD':
                #for i in range(CDB.source_entry):
                if running_buffer.Dest > self.CDB.source_entry:
                    '''
                    如果头部加载单元是一个加载指令 并且该指令的目的地小于通用数据总线（CDB）上当前的源指令索引，那么进行以下操作：
                    
                    从内存地址中读取数据并将其写入CDB
                    设置CDB的数据来源为当前加载单元的目的地
                    更新执行阶段结束的周期数
                    重新初始化当前加载单元并更新头部指针
                    '''
                    '''print("asdddddddasdfa")
                    print("asdddddddasdfa")
                    print("asdddddddasdfa")
                    print("asdddddddasdfa")
                    print("asdddddddasdfa")
                    print("asdddddddasdfa")
                    print("asdddddddasdfa")
                    print("asdddddddasdfa")'''
                    self.CDB.data = self.memory[running_buffer.address]
                    self.CDB.source_entry = running_buffer.Dest
                    

            elif running_buffer.Op == 'SD':
                print("SDSDSDSDSDSD")
                print("SDSDSDSDSDSD")
                print("SDSDSDSDSDSD")
                print("SDSDSDSDSDSD")
                print("SDSDSDSDSDSD")
                temp = self.ROB.buffers[running_buffer.Dest].instruction[1]
                if type(temp) != int:
                    temp = self.registers[temp]
                self.memory[running_buffer.address] = temp
                self.ROB.buffers[running_buffer.Dest].value = 0

            self.ROB.buffers[running_buffer.Dest].states_num[1] = cycle
            running_buffer.__init__(id=running_buffer.id,CDB=self.CDB,ROB=self.ROB,register_states_=self.register_states)

            self.head = 1 - self.head 
            self.count+=1
        self.buffers[0].execute(cycle)
        self.buffers[1].execute(cycle)

    def display(self):
        self.buffers[0].display()
        self.buffers[1].display()

    def find_no_busy(self):
        for i in range(2):
            if not self.buffers[i].busy:
                return  i
        return -1

class FP_Adders:
    class FP_add_unit(Reservation_Station):
        def __init__(self,type='add',id=0, CDB=None, ROB=None, register_states_=None):
            super().__init__(type=type,id=id,CDB=CDB,ROB=ROB)
            self.address = ''
            self.flag = 0
            self.delay = 0
            self.register_states = register_states_
        def execute(self,cycle):
            if not self.busy:
                return
            print("aAAAAAAA",self.Dest)
            rob_entry = self.rob.buffers[self.Dest]
            rob_entry.update_state(StateName.EXECUTE, 1)
            if self.Qj == '' and self.Qk == '' :
                if self.delay < 2:
                    self.delay += 1
                    return
            
                rob_entry.states_num[1] = cycle

                if self.Op == 'ADDD': 
                    self.cdb.data = self.Vj+self.Vk
                    self.cdb.source_entry = self.Dest
                    self.flag = 1
                
                elif self.Op == 'SUBD':
                    self.cdb.data = self.Vj-self.Vk
                    self.cdb.source_entry = self.Dest
                    self.flag = 1


    def __init__(self, CDB=None, ROB=None, register_states=None, memory=None, registers=None):
        self.buffers = [self.FP_add_unit(id=i, CDB=CDB,ROB=ROB,register_states_=register_states) for i in range(1,4)]

    def write_in(self):
        for adders in self.buffers:
            adders.write_in()

    def execute(self,cycle):
        for adders in self.buffers:
            if adders.flag:
                adders.__init__(id=adders.id,CDB=adders.cdb,ROB=adders.rob,register_states_=adders.register_states)
            adders.execute(cycle)

    def free_adders(self):
        for i in range(3):
            if not self.buffers[i].busy:
                return i
            
        return -1
    
    def display(self):
        for adders in self.buffers:
            adders.display()

class FP_multipliers:
    class FP_mul_unit(Reservation_Station):
        def __init__(self, type='mult', id=0, CDB=None, ROB=None, register_states_=None):
            super().__init__(type=type, id=id, CDB=CDB, ROB=ROB)
            self.address = ''
            self.flag = 0
            self.delay = 0
            self.register_states = register_states_

        def execute(self,cycle):
            if not self.busy:
                return

            rob_entry = self.rob.buffers[self.Dest]
            rob_entry.update_state(StateName.EXECUTE, 1)
            if self.Qj == '' and self.Qk == '':
                if self.Op == 'MULTD':
                    if self.delay < 10:
                        print("delay",self.delay)
                        print("delay",self.delay)
                        print("delay",self.delay)
                        print("delay", self.delay)
                        print("delay", self.delay)
                        print("delay", self.delay)
                        print("delay", self.delay)
                        self.delay += 1
                        return

                    rob_entry.states_num[1] = cycle
                    if self.Dest > self.cdb.source_entry:
                        self.cdb.data = self.Vj * self.Vk
                        self.cdb.source_entry = self.Dest
                        self.flag = 1
                
                else :
                    if self.delay < 20:
                        self.delay +=1
                        return
                    rob_entry.states_num[1] = cycle

                    if self.Dest>self.cdb.source_entry:
                        self.cdb.data = self.Vj / self.Vk
                        self.cdb.source_entry = self.Dest
                        self.flag = 1


    def __init__(self, CDB=None, ROB=None, register_states=None, memory=None, registers=None):
        self.buffers = [self.FP_mul_unit(
            id=i, CDB=CDB, ROB=ROB, register_states_=register_states) for i in range(1, 3)]

    def write_in(self):
        for multiers in self.buffers:
            multiers.write_in()

    def execute(self,cycle):
        for multiers in self.buffers:
            if multiers.flag:
                multiers.__init__(id=multiers.id, CDB=multiers.cdb, ROB=multiers.rob,
                                  register_states_=multiers.register_states)
            multiers.execute(cycle)

    def free_multipliers(self):
        for i in range(2):
            if not self.buffers[i].busy:
                return i

        return -1
    
    def display(self):
        for multier in self.buffers:
            multier.display()









if __name__ == "__main__":
    lb = Load_Buffer()
    lb.display()
    ad = FP_Adders()
    ad.display()
    mul = FP_multipliers()
    mul.display()

