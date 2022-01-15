import argparse
import importlib
import sys
import os
import re

FILE_PATH = os.path.abspath(os.path.dirname(__file__))
FILES = os.listdir(FILE_PATH)

DAY_MODULE_RE = re.compile(r'd\d+\.py')

days = {}

# Import all aoc day modules (dN)
for m in [f.split('.')[0] for f in FILES if DAY_MODULE_RE.match(f)]:
    days[int(m[1:])] = importlib.import_module(m)


def print_unsupported_combo(opt1: str, opt2: str):
    print(
        'Unsupported combination of arguments: '
        f'\'{opt1}\' and \'{opt2}\''
    )


class Day:
    


def run_day(i:int):
    getattr(days[i], 'main')()


def add_generic_options(parser: argparse.ArgumentParser):
    parser.add_argument(
        '-p', '--part', type=int, default=0,
        help='Which part do you want to run? Default is both.'
    )
    parser.add_argument(
        '-t', '--test', action='store_true',
        help='Do you want to run the test only?'
    )
    parser.add_argument(
        '-m', '--measure-time', action='store_true',
        help='Measure runtimes'
    )
    parser.add_argument(
        '-v', '--verbose', action='store_true',
        help='Verbose output'
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '-d', '--day', type=int, default=0,
        help='Which day do you want to run? Default is all.'
    )

    add_generic_options(parser)

    opts = parser.parse_args()

    if opts.day == 0:
        for i in days:
            run_day(i)
    else:
        run_day(opts.day)

if __name__ == "__main__":
    main()
