# https://adventofcode.com/2021/day/16
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False
TEST_NUMBER: int = 3

BITS_MESSAGE: str = ''

if not TEST:
    INPUT_FILE: str = f'{file_path}/input.dat'
    with open(INPUT_FILE, 'r') as f:
        BITS_MESSAGE = f.readline().strip()

hex2bin: dict[str, str] = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'A': '1010',
    'B': '1011',
    'C': '1100',
    'D': '1101',
    'E': '1110',
    'F': '1111',
}

def hex_to_bin(hex):
    return ''.join(hex2bin[h] for h in hex)

def get_header(msg):
    return int(msg[0:3],2)

def get_type(msg):
    return int(msg[3:6],2)

class Message:

    def __init__(self, message: str, is_bin: bool = True):
        if not is_bin:
            message = hex_to_bin(message)
        self.message = message
        self.iter = 0
        self.version = int(message[self.iter:self.iter+3], 2)
        self.iter += 3
        self.type = int(message[self.iter:self.iter+3], 2)
        self.iter += 3
        self.subpackets_length_type = int(message[6]) if self.type != 4 else -1
        if self.subpackets_length_type > -1:
            self.iter += 1
            read_length = 15 if self.subpackets_length_type == 0 else 11
            self.subpackets_length = int(message[self.iter:self.iter+read_length], 2)
            self.iter += read_length
            self.has_subpackets = True

        else:
            self.subpackets_length = -1
            self.has_subpackets = False
        self.value = -1
        self.subpackets: list['Message'] = []

    def parse(self):
        if self.has_subpackets:
            self.parse_subpackets()
        else:
            self.calc_value()

    def calc_value(self):
        bits = ''
        msb = '1'
        while msb == '1':
            msb = self.message[self.iter]
            bits += self.message[self.iter+1:self.iter+5]
            self.iter += 5
        self.value = int(bits,2)

    def parse_subpackets(self):
        if self.subpackets_length_type == 0:
            curr_length = self.iter
            while (self.iter - curr_length < self.subpackets_length):
                self.process_next_subpacket()
        else:
            for _ in range(self.subpackets_length):
                self.process_next_subpacket()

    def process_next_subpacket(self):
        subpacket = Message(self.message[self.iter:])
        subpacket.parse()
        self.subpackets.append(subpacket)
        self.iter += subpacket.iter

    def get_value(self):
        # Depends on the type
        value = 0
        if self.type == 0:
            value = sum([m.get_value() for m in self.subpackets])
        elif self.type == 1:
            value = 1
            for m in self.subpackets:
                value *= m.get_value()
        elif self.type == 2:
            value = min([m.get_value() for m in self.subpackets])
        elif self.type == 3:
            value = max([m.get_value() for m in self.subpackets])
        elif self.type == 4:
            value = self.value
        elif self.type == 5:
            value = 1 if self.subpackets[0].get_value() > self.subpackets[1].get_value() else 0
        elif self.type == 6:
            value = 1 if self.subpackets[0].get_value() < self.subpackets[1].get_value() else 0
        elif self.type == 7:
            value = 1 if self.subpackets[0].get_value() == self.subpackets[1].get_value() else 0

        return value

def sum_versions(m: Message):
    sum_version = m.version
    for _m in m.subpackets:
        sum_version+=sum_versions(_m)
    return sum_version

def exercise():
    message = Message(BITS_MESSAGE, False)
    message.parse()
    print(f'Sum of versions: {sum_versions(message)}')
    print(f'Value: {message.get_value()}')

if __name__ == "__main__":
    if TEST:
        print('Exercise 1 test:')
        with open('test_part1.dat') as f:
            for _in in [l.strip() for l in f.readlines()]:
                m = Message(_in, False)
                m.parse()
                print(f'Input message: {_in}, sum of versions: {sum_versions(m)}')
        print('Exercise 2 test:')
        with open('test_part2.dat') as f:
            for _in in [l.strip() for l in f.readlines()]:
                m = Message(_in, False)
                m.parse()
                print(f'Input message: {_in}, value: {m.get_value()}')
    else:
        exercise()
