# https://adventofcode.com/2021/day/20
import os
file_path = os.path.abspath(os.path.dirname(__file__))

import sys
from functools import cache
from dataclasses import dataclass

TEST: bool = False
VERBOSE: bool = False

def _print(msg):
    if VERBOSE:
        print(msg)

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.txt'
else:
    INPUT_FILE: str = f'{file_path}/input.txt'

_lines: str = ''
with open(INPUT_FILE, 'r') as f:
    _lines = [line.strip() for line in f.readlines()]

PLAYER1_START: int = int(_lines[0].split()[-1])
PLAYER2_START: int = int(_lines[1].split()[-1])

@dataclass
class Player:
    id: int
    position: int
    score_to_win: int
    score: int = 0

    def move(self, spaces: int):
        _print(f'Moving player {self.id} a total of {spaces} spaces')
        _print(f'Position before moving: {self.position}')
        self.position += spaces
        _print(f'Position after moving: {self.position}')
        self.position = self.position % 10
        if self.position == 0:
            self.position = 10

        _print(f'Position after fixing for bord size: {self.position}')

        self.score += self.position

    def did_win(self) -> bool:
        return self.score >= self.score_to_win

@dataclass
class DeterministicDice:
    rolls: int = 0
    value: int = 1

    def roll(self, throws: int) -> list[int]:
        self.rolls += throws
        values = []
        for _ in range(throws):
            if self.value == 101:
                self.value = 1
            values.append(self.value)
            self.value += 1
        _print(f'Returning rolls: {values}')
        return values

def exercise1():

    player1 = Player(1, PLAYER1_START, 1000)
    player2 = Player(2, PLAYER2_START, 1000)

    die = DeterministicDice()

    while True:
        player1.move(sum(die.roll(3)))
        if player1.did_win():
            print(f'Player 1 wins with a score of {player1.score}')
            print(f'Player 2 score: {player2.score}, rolls: {die.rolls}')
            return player2.score * die.rolls

        player2.move(sum(die.roll(3)))
        if player2.did_win():
            print(f'Player 2 wins with a score of {player2.score}')
            print(f'Player 1 score: {player1.score}, rolls: {die.rolls}')
            return player1.score * die.rolls

DIRAC_DICE = [i + j + k for i in (1, 2, 3) for j in (1, 2, 3) for k in (1, 2, 3)]

def exercise2():
    p1, p2 = [int(line.split()[-1]) for line in _lines]
    s1 = s2 = 0

    @cache
    def check_wins(s1, p1, s2 ,p2):
        wins1 = 0
        wins2 = 0
        p1_init = p1
        s1_init = s1
        for throw in DIRAC_DICE:
            p1 = (p1_init + throw) % 10
            if p1 == 0:
                p1 = 10
            s1 = s1_init + p1
            if s1 >= 21:
                wins1 += 1
            else:
                # Flip order
                dwins2, dwins1 = check_wins(s2, p2, s1, p1)
                wins1 += dwins1
                wins2 += dwins2
        return wins1, wins2

    player1_wins, player2_wins = check_wins(s1, p1, s2, p2)
    print(f'Player 1 wins: {player1_wins}')
    print(f'Player 2 wins: {player2_wins}')

    return max((player1_wins, player2_wins))

if __name__ == "__main__":
    e1 = exercise1()
    e2 = exercise2()

    if e1:
        print(f'Solution exercise 1: {e1}')
    if TEST:
         print('Solution example exercise 1: 739785')
    if e2:
        print(f'Solution exercise 2: {e2}')
    if TEST:
        print('Solution example exercise 2: 444356092776315')
