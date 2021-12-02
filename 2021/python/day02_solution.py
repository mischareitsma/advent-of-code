# https://adventofcode.com/2021/day/2
def exercise1():
    depth = 0
    x = 0

    with open('./day02_input.txt', 'r') as f:
        for l in f:
            direction, delta = l.strip().split()
            delta = int(delta)

            match direction:
                case "forward":
                    x += delta
                case "up":
                    depth -= delta
                case "down":
                    depth += delta

    print(f'Day 2, exercise 1: depth * x = {depth} * {x} = {depth * x}')


def exercise2():
    depth = 0
    x = 0
    aim = 0
    with open('./day02_input.txt', 'r') as f:
        for l in f:
            direction, delta = l.strip().split()
            delta = int(delta)

            match direction:
                case "forward":
                    x += delta
                    depth += (delta * aim)
                case "up":
                    aim -= delta
                case "down":
                    aim += delta

    print(f'Day 2, exercise 2: depth * x = {depth} * {x} = {depth * x}')


def main():
    exercise1()
    exercise2()


if __name__ == "__main__":
    main()
