import argparse
import importlib

days = {}

# Import all aoc modules
for i in range(2):
    days[i+1] = importlib.import_module(f'd{i+1}')

def main():
    parser = argparse.ArgumentParser()

    # Which day do you want to run?
    parser.add_argument('-d', '--day', type='int', default=0,
        help='Which day do you want to run? Default is none.')
    parser.add_argument('-a', '--all', action='store_true',
        help='Run all days, should NOT pass the -d flag!!')
    parser.add_argument('-p', '--part', type='int', default=0,
        help='Which part do you want to run? Default is both.')
    parser.add_argument('-t', '--test', action='store_true',
        help='Do you want to run the test only?')
    parser.add_argument('-m', '--measure-time', action='store_true',
        help='Measure runtimes')

if __name__ == "__main__":
    main()
