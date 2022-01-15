import argparse
import aoc

def p1():
    print('d1.p1')

def p2():
    print('d1.p2')


def main():
    print('d1.main')
    p1()
    p2()


def run():
    pass

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    aoc.add_generic_options(parser)

    opts = parser.parse_args()

    
