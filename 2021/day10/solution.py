# https://adventofcode.com/2021/day/10
import math

TEST: bool = False

if TEST:
    INPUT_FILE: str = './test_input.txt'

else:
    INPUT_FILE: str = './input.txt'

lines: list[str] = None

with open(INPUT_FILE, 'r') as f:
    lines = [l.strip() for l in f.readlines()]

SYNTAX_ERROR_SCORE_TABLE = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137,
}

AUTO_COMPLETE_SCORE_TABLE = {
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4,
}

OPEN_CHARS = ('(', '[', '{', '<')

CLOSE_CHARS = (')', ']', '}', '>')

CLOSE_TO_OPEN = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<',
}

OPEN_TO_CLOSE = {
    '(': ')',
    '[': ']',
    '{': '}',
    '<': '>',
}

def exercise():
    illegal_chars: list[str] = []
    incomplete_open_chars: list[list[str]] = []
    for line in lines:
        open_stack = []
        found_illegal_char = False
        for char in line:
            if char in OPEN_CHARS:
                open_stack.append(char)
            else:
                # Need to close the last one
                last_open = open_stack.pop()
                if last_open != CLOSE_TO_OPEN[char]:
                    illegal_chars.append(char)
                    found_illegal_char = True
                    break
        if not found_illegal_char:
            incomplete_open_chars.append(open_stack)

    illegal_char_highscore = 0
    for i in illegal_chars:
        illegal_char_highscore += (SYNTAX_ERROR_SCORE_TABLE[i])

    auto_complete_highscores: list[int] = []
    for line in incomplete_open_chars:
        score = 0
        for char in line[::-1]:
            score *= 5
            score += AUTO_COMPLETE_SCORE_TABLE[OPEN_TO_CLOSE[char]]
        auto_complete_highscores.append(score)

    idx: int = math.floor(len(auto_complete_highscores)/ 2)
    auto_complete_highscore: int = sorted(auto_complete_highscores)[idx]

    print(f'Illegal character high score: {illegal_char_highscore}')
    print(f'Auto-complete high score: {auto_complete_highscore}')

def main():
    exercise()


if __name__ == "__main__":
    main()
