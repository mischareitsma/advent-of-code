import os

TEST: bool = False

FILE_NAME = "day7_test_input.dat" if TEST else "day7_input.dat"
FILE_PATH = f'{os.path.dirname(os.path.realpath(__file__))}/{FILE_NAME}'

lines = [l.strip() for l in open(FILE_PATH).readlines()]

tot = 0

for line in lines:
    sum = int(line.split(":")[0])
    digits = tuple(int(i) for i in line.split(": ")[-1].split(" "))

    results = [([], digits[0])]

    for digit in digits[1:]:
        new_result = []
        for res in results:
            nr1 = (res[0][::] + ['+'], res[1] + digit)
            nr2 = (res[0][::] + ['*'], res[1] * digit)
            nr3 = (res[0][::] + ['|'], int(str(res[1]) + str(digit)))
            if nr1[1] <= sum:
                new_result.append(nr1)
            if nr2[1] <= sum:
                new_result.append(nr2)
            if nr3[1] <= sum:
                new_result.append(nr3)
        results = new_result

    # print(digits)
    for res in results:
        # print(res)
        if res[1] == sum:
            tot += sum
            break

print(tot)
