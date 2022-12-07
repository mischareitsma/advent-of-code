# https://adventofcode.com/2022/day/6
import os
file_path = os.path.abspath(os.path.dirname(__file__))

INPUT_FILE: str = f'{file_path}/input.dat'

TEST: bool = False
TEST_INPUT: list = [
    'mjqjpqmgbljsphdztnvjfqwrcgsmlb',
    'bvwbjplbgvbhsrlpgdmjqwftvncz',
    'nppdvjthqldpwncqszvftbrmjlhg',
    'nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg',
    'zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw'
]

STREAMS: list[str] = None

if TEST:
    STREAMS = TEST_INPUT
else:
    with open(INPUT_FILE, 'r') as f:
        STREAMS = [f.read().strip()]

def get_start_of_stream_marker(stream: str, marker_length: int) -> int:
    for i in range(len(stream)-marker_length):
        if len(set(stream[i:i+marker_length])) == marker_length:
            return i + marker_length

def get_start_of_package_marker(stream: str) -> int:
    return get_start_of_stream_marker(stream, 4)

def get_start_of_message_marker(stream: str) -> int:
    return get_start_of_stream_marker(stream, 14)

def main():
    for s in STREAMS:
        print(f'Start of packet marker: {get_start_of_package_marker(s)}')
        print(f'Start of message marker: {get_start_of_message_marker(s)}')

if __name__ == "__main__":
    main()
