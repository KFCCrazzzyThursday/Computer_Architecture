'''
ROB :
'''
from enum import Enum


class StateName(Enum):
    ISSUE = 0
    EXECUTE = 1
    WRITE_RESULT = 2
    COMMIT = 3

    @classmethod
    def get_state_name(cls, state):
        state_names = ['issue', 'execute', 'write result', 'commit']
        if isinstance(state, StateName):
            index = state.value
        elif isinstance(state, int):
            index = state
        else:
            raise TypeError("state must be a StateName enum or an int")
        return state_names[index]


class Reorder_Buffer:
    class Buffer_Unit:
        def __init__(self, entry=0) -> None:
            self.entry = entry
            self.busy = False
            self.instruction = []
            self.state = StateName.ISSUE  # 初始状态设为 ISSUE
            self.states_num = [0, 0, 0, 0]
            self.destination = ''
            self.value = '' 

        def update_state(self, state: StateName, cycle: int):
            self.state = state
            self.states_num[state.value] = cycle

        def display(self):
            print(f'entry{self.entry:<7}', end=' : ')
            print(f'{"Yes" if self.busy else "No":<4}', end=', ')
            output_ = ', '.join(str(x) for x in self.instruction)
            print(output_.ljust(32), end=', ')
            print(f'{StateName.get_state_name(self.state):<13}', end=', ')
            print(f'{self.destination:<4}', end=', ')
            print(f'{str(self.value):<4}' + ';')

    def __init__(self, size=6):
        self.buffers = [self.Buffer_Unit(entry=i+1) for i in range(size)]

    def display(self):
        for unit in self.buffers:
            unit.display()


if __name__ == '__main__':
    rob = Reorder_Buffer()
    rob.buffers[2].busy = True
    rob.buffers[2].instruction.append('MULTD')
    rob.buffers[2].instruction.append('F0')
    rob.buffers[2].instruction.append('F2')
    rob.buffers[2].instruction.append('F4')
    rob.buffers[0].update_state(StateName.EXECUTE, 1)
    rob.buffers[2].states_num = [3, 15, 0, 0]
    rob.buffers[2].destination = "F0"
    rob.display()