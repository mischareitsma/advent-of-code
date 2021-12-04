# https://adventofcode.com/2021/day/4

input_file: str = './day04_input.txt'

bingo_numbers = []
bingo_cards = []
n_bingo_cards = 0

def load_file():
    global bingo_numbers
    global bingo_cards
    global n_bingo_cards

    with open(input_file, 'r') as f:
        lines = [i for i in f.read().splitlines() if i != '']

    bingo_numbers = [int(i) for i in lines[0].split(',')]
    # print(bingo_numbers)
    del lines[0]

    # for i in lines:
    #     print(i)

    n_bingo_cards = len(lines) // 5
    # print(n_bingo_cards)

    bingo_cards = []

    for i in range(n_bingo_cards):
        bingo_cards.append([])
        for j in range(5):
            bingo_cards[i].append([int(n) for n in lines[5 * i + j].split()])
            
    # print(bingo_cards)

def mark_number(n):
    for card_number, card in enumerate(bingo_cards):
        for row_number, row in enumerate(card):
            for digit_number, digit in enumerate(row):
                if digit == n:
                    bingo_cards[card_number][row_number][digit_number] = 0

def has_bingo() -> int:
    for card_number, card in enumerate(bingo_cards):
        has_bingo: bool = False
        # Check rows:
        for row in card:
            if sum(row) == 0:
                return card_number
        for i in range(5):
            _sum = 0
            for j in range(5):
                _sum += card[j][i]
            
            if _sum == 0:
                return card_number

    return -1

def exercise1():
    winner: int = -1
    i: int = -1
    n: int = -1

    while (winner == -1):
        i += 1
        n = bingo_numbers[i]
        mark_number(n)
        winner = has_bingo()

    print(f'Bingo for card number {winner}')

    remainder = 0

    for row in bingo_cards[winner]:
        for digit in row:
            remainder += digit

    print(f'Remainder: {remainder}')
    print(f'Last bingo digit: {n}')
    print(f'Result: {remainder * n}')

def exercise2():
    last_card: int = -1
    n_winners = 0

    i = -1
    n = -1

    winner = -1

    while True:
        i += 1
        n = bingo_numbers[i]
        print(f'i: {i}, n: {n}, n_winners: {n_winners} / {n_bingo_cards}')
        mark_number(n)
        winner = has_bingo()
        while (winner != -1):
            n_winners += 1
            if (n_bingo_cards == n_winners):
                break
            del bingo_cards[winner]
            winner = has_bingo()
        winner = -1
        if (n_bingo_cards == n_winners):
            break

    print('Remaining bingo cards:')
    print(bingo_cards)

    remainder = 0

    for row in bingo_cards[0]:
        for digit in row:
            remainder += digit

    print(f'Remainder: {remainder}')
    print(f'Last bingo digit: {n}')
    print(f'Result: {remainder * n}')


def main():
    load_file()
    # TODO: Can only run one exercise at a time, improve this
    # exercise1()
    exercise2()


if __name__ == "__main__":
    main()
