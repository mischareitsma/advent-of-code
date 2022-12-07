# https://adventofcode.com/2022/day/7
import os
file_path = os.path.abspath(os.path.dirname(__file__))

TEST: bool = False

if TEST:
    INPUT_FILE: str = f'{file_path}/test_input.dat'
else:
    INPUT_FILE: str = f'{file_path}/input.dat'

with open(INPUT_FILE, 'r') as f:
    LINES = [l.strip() for l in f.readlines()]

SPACES: str = '  '

SMALL_SIZE: int = 100000
TOTAL_SPACE: int = 70000000
SPACE_REQUIRED: int = 30000000

class File:
    def __init__(self, name: str, size: int = 0):
        self.name = name
        self.size = size

    def get_size(self):
        return self.size

    def print(self, current_indent = 0):
        print(f'{SPACES * current_indent}- {self.name} (file, {self.size})')


class Directory(File):
    def __init__(self, name: str, parent: 'Directory' = None):
        super().__init__(name, 0)

        self.parent = parent
        self.children: list[File|Directory] = []

    def get_files(self) -> list[File]:
        return [c for c in self.children if type(c) == File]

    def get_directories(self) -> list['Directory']:
        return [c for c in self.children if type(c) == Directory]

    def get_dir_by_name(self, name: str) -> 'Directory':
        for d in self.get_directories():
            if d.name == name:
                return d

    def get_file_by_name(self, name: str) -> File:
        for f in self.get_files():
            if f.name == name:
                return f

    def add_directory(self, directory: 'Directory'):
        # only add if not added:
        if not self.get_dir_by_name(directory.name):
            self.children.append(directory)

    def add_file(self, _file: File):
        if not self.get_file_by_name(_file.name):
            self.children.append(_file)

    def get_size(self):
        if self.size > 0:
            return self.size

        size = 0

        for c in self.children:
            size += c.get_size()

        self.size = size
        return self.size

    def print(self, current_depth: int = 0):

        print(f'{SPACES * current_depth}- {self.name} (dir) ({self.get_size()})')

        current_depth += 1

        for c in self.children:
            c.print(current_depth)

        current_depth -= 1


def main():
    root: Directory = Directory('/', None)

    all_dirs: list[Directory] = []

    cur_dir = root

    idx: int = -1

    while (idx < len(LINES)):
        try:
            idx += 1
            line = LINES[idx]
        except:
            # TODO: Just ignore fix later
            pass

        if line == '$ cd /':
            cur_dir = root
            continue

        if line == '$ cd ..':
            cur_dir = cur_dir.parent
            continue

        if line.startswith('$ cd'):
            name = line.split(' ')[-1]
            cur_dir = cur_dir.get_dir_by_name(name)
            continue

        if line == '$ ls':
            # only do one `ls` per dir, so add to list of all dirs:
            all_dirs.append(cur_dir)
            idx += 1
            line = LINES[idx]
            while not line.startswith('$'):
                if line.startswith('dir'):
                    cur_dir.add_directory(Directory(line.split()[-1], cur_dir))
                else:
                    cur_dir.add_file(File(line.split()[1], int(line.split()[0])))
                idx += 1
                if idx >= len(LINES):
                    break
                line = LINES[idx]
            idx -= 1

    total = 0

    for d in all_dirs:
        size = d.get_size()
        if size < SMALL_SIZE:
            total += size
    
    print(f'Total size of dir sizes under {SMALL_SIZE}: {total}')

    space_to_free: int = SPACE_REQUIRED - (TOTAL_SPACE - root.get_size())

    smallest_size = root.get_size()

    for d in all_dirs:
        size = d.get_size()
        diff = space_to_free - size
        if diff > 0:
            continue
        else:
            if smallest_size > size:
                smallest_size = size
    
    print(f'Smallest size to delete: {smallest_size}')


if __name__ == "__main__":
    main()
