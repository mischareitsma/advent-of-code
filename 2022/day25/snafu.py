import sys
from collections import OrderedDict

SNAFU_DIGIT: dict[str, int] = {
    '=': -2,
    '-': -1,
    '0': 0,
    '1': 1,
    '2': 2
}

REV_SNAFU_DIGIT: dict[int, str] = {v:k for k,v in SNAFU_DIGIT.items()}

def _snafu_min_digits():
    x: int = 0
    i: int = 0
    d: OrderedDict[int, int] = OrderedDict()

    while x < sys.maxsize:
        x += 2 * (5**i)
        d[i] = x
        i += 1

    return d

SNAFU_MIN_DIGITS: OrderedDict[int, int] = _snafu_min_digits()

def get_max_power_of_five(dec: int):
    _dec = -dec if dec < 0 else dec
    for k, v in SNAFU_MIN_DIGITS.items():
        if _dec <= v:
            return k

def snafu_to_dec(snafu: str) -> int:
    result: int = 0

    for c in snafu:
        result *= 5
        result += SNAFU_DIGIT[c]

    return result


def dec_to_snafu(dec: int) -> str:
    max_power: int = get_max_power_of_five(dec)

    if max_power == 0:
        return str(dec)

    digits: list[int] = ['0'] * (max_power + 1)

    while (dec != 0):
        # if negative, need to do something else...
        curr_power = get_max_power_of_five(dec)

        if curr_power == 0:
            digits[curr_power] = valid_sum_two_snafus(digits[curr_power], REV_SNAFU_DIGIT[dec])
            dec = 0
            break

        curr_max = SNAFU_MIN_DIGITS[curr_power]
        next_max = SNAFU_MIN_DIGITS[curr_power - 1]

        if dec > 0:
            digit: int = 2 if dec > next_max + ((curr_max - next_max) // 2) else 1
        else:
            digit: int = -2 if -dec > next_max + ((curr_max - next_max) // 2) else -1

        digits[curr_power] = valid_sum_two_snafus(digits[curr_power], REV_SNAFU_DIGIT[digit])

        dec -= digit * (5 ** curr_power)

    return ''.join(reversed(digits))


def valid_sum_two_snafus(a: str, b: str):
    result: int = SNAFU_DIGIT[a] + SNAFU_DIGIT[b]

    # Algorithm in other methods should never get to this condition, but
    # keep it here to not get KeyErrors

    if not result in REV_SNAFU_DIGIT:
        raise ValueError(f'Cannot add snafu digits {a} and {b}')

    return REV_SNAFU_DIGIT[result]


def _run_brochure():
    snafu_dec_brochure = {
        1: '1',
        2: '2',
        3: '1=',
        4: '1-',
        5: '10',
        6: '11',
        7: '12',
        8: '2=',
        9: '2-',
        10: '20',
        15: '1=0',
        20: '1-0',
        2022: '1=11-2',
        12345: '1-0---0',
        314159265: '1121-1110-1=0',
    }

    print(f'Testing snafu_to_dec():')
    for dec, snafu in snafu_dec_brochure.items():
        print(f'Snafu: {snafu}, dec: {snafu_to_dec(snafu)}, should be: {dec}')

    print()

    print(f'Testing dec_to_snafu():')
    for dec, snafu in snafu_dec_brochure.items():
        print(f'Dec: {dec}, snafu: {dec_to_snafu(dec)}, should be: {snafu}')


if __name__ == "__main__":
    _run_brochure()
