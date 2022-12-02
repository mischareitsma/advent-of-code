# https://adventofcode.com/2022/day/1
import os
from functools import lru_cache
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

POINTS_SIGN1 = {
    'X': 1, # Rock (A)
    'Y': 2, # Paper (B)
    'Z': 3, # Scissors (C)
}

POINTS_ROUND1 = {
    'A': {
        'X': 3,
        'Y': 6,
        'Z': 0,
    },
    'B': {
        'X': 0,
        'Y': 3,
        'Z': 6,
    },
    'C': {
        'X': 6,
        'Y': 0,
        'Z': 3,
    }
}

POINTS_SIGN2 = {
    'A': 1, # Rock, beats C, loses from B
    'B': 2, # Paper, beats A, loses from C
    'C': 3, # Scissors, beats B, loses from A
}


POINTS_ROUND2 = {
    'A': {
        'X': 3 + 0, # Chose C, Lose
        'Y': 1 + 3, # Chose A, Draw
        'Z': 2 + 6, # Chose B, Win
    },
    'B': {
        'X': 1 + 0, # Chose A, Lose
        'Y': 2 + 3, # Chose B, Draw
        'Z': 3 + 6, # Chose C, Win
    },
    'C': {
        'X': 2 + 0, # Chose B, Lose
        'Y': 3 + 3, # Chose C, Draw
        'Z': 1 + 6, # Chose A, Win
    }
}

@lru_cache
def get_score1(o: str, m: str):
    return POINTS_SIGN1[m] + POINTS_ROUND1[o][m]

def get_score2(o: str, m: str):
    return POINTS_ROUND2[o][m]

def main():
    score1 = 0
    score2 = 0
    with open(INPUT_FILE, 'r') as f:
        for l in [x.strip() for x in f.readlines()]:
            o, m = l.split(' ')
            score1 += get_score1(o, m)
            score2 += get_score2(o, m)

    print(f'Score 1: {score1}')
    print(f'Score 2: {score2}')

if __name__ == "__main__":
    main()
