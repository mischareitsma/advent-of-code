# https://adventofcode.com/2021/day/22
from functools import cache
import os
file_path = os.path.abspath(os.path.dirname(__file__))
import sys
TEST: bool = True
VERBOSE: bool = False

# count = 0

def _print(msg):
    # global count
    # count += 1
    # if count > 20:
    #     sys.exit(1)
    if VERBOSE:
        print(msg)

ROOMS_INIT: list[list[str]]

if TEST:
    HALL_INIT = ['.', '.', 'BA', '.', 'CD', '.', 'BC', '.', 'DA', '.', '.']
else:
    HALL_INIT = ['.', '.', 'DD', '.', 'CA', '.', 'BA', '.', 'CB', '.', '.']

HALL_LENGTH: int = len(HALL_INIT)

ENERGY = {
    'A': 1,
    'B': 10,
    'C': 100,
    'D': 1000
}

ROOM = {
    'A': 2,
    'B': 4,
    'C': 6,
    'D': 8
}

PODS = { v: k for k, v in ROOM.items()}

ROOMS = list(ROOM.values())

ROOM_SIZE = 2

def is_solved(state: list[str]) -> bool:
    return (
        state[2] == 'AA' and
        state[4] == 'BB' and
        state[6] == 'CC' and
        state[8] == 'DD'
    )

def get_energy(amphipod: str, steps: int) -> int:
    return ENERGY[amphipod] * steps

def is_movable(pos, pods) -> bool:
    if pods == '.':
        return False
    # pos not a room, and the pods is not a ., so this one can move
    if pos not in [2, 4, 6, 8]:
        return True

    # if we are here, the pods is not a dot, and we are in a room
    if pos == 2 and (pods != 'AA' or pods != 'A'):
        return 

    if pos == 4 and (pods != 'BB' or pods != 'B'):
        return True

    if pos == 6 and (pods != 'CC' or pods != 'C'):
        return True

    if pos == 8 and (pods != 'DD' or pods != 'D'):
        return True


def can_reach_room(state, pos, pod):
    room_pos = ROOM[pod]
    # Cannot reach if room is full
    if len(state[room_pos]) == ROOM_SIZE:
        return False
    step = 1 if room_pos > pos else -1
    for i in range(pos, room_pos, step):
        if i in ROOMS or i == pos:
            continue
        if state[i] != '.':
            return False
    return True

def get_amphipods(state):
    amphipods = []

    for pos, pod in enumerate(state):
        if pod == '.':
            continue
        
        # rooms are special:
        if pos in ROOMS:
            room_owner = PODS[pos]
            # Room is done
            if pod.count(room_owner) == len(pod):
                continue
            
            # Can only move if either side is empty
            if state[pos-1] == '.' or state[pos+1] == '.':
                amphipods.append((pos, pod[0]))

        else:
            if can_reach_room(state, pos, pod):
                amphipods.append((pos, pod))

    return amphipods

def get_new_states(state, pod, pos) -> list[tuple[list, int]]:
    """Get new states, returns a list of tuples, which have the
    new state (as a list) and the energy it took to get to there.
    """
    pod_in_room = pos in ROOMS
    e: int = 0

    _print(f'\t\tGetting new states for {pod} at {pos} in {state}, pod in room: {pod_in_room}')

    # If the pod is not in a room, it can only move to its own room,
    # so only one possible move
    if not pod_in_room:
        # Check if the path is clear, meaning no pods between current pos
        # and pod's room
        room_number = ROOM[pod]

        _print(f'Trying to get to room {room_number}, state of that room: {state[room_number]}')

        # if room is occupied with another, cannot move
        if state[room_number] not in ['.', pod]:
            return []

        step = 1
        if room_number < pos:
            step = -1

        _print(f'start, end and step for range: {pos}, {room_number + step}, {step}')

        for i in range(pos + step, room_number + step, step):
            e += ENERGY[pod]
            if i in ROOMS:
                continue
            if state[i] != '.':
                return []

        new_state = state[::]
        new_state[pos] = '.'
        # Was empty, extra step needed
        if new_state[room_number] == '.':
            e += ENERGY[pod]
            new_state[room_number] = pod
        # Was not empty
        else:
            new_state[room_number] += pod

        return [(new_state, e)]

    new_states = []
    # Stepping out of the room energy
    init_energy = ENERGY[pod]
    new_room_content = state[pos][-1]
    if len(state[pos]) == 1:
        # Room now empty, extra step + now empty
        init_energy += ENERGY[pod]
        new_room_content = '.'

    # _print(f'Starting energy: {init_energy}, new room content: {new_room_content}')

    e = init_energy
    for i in range(pos-1, -1, -1):
        # Cannot move any further
        if i not in ROOMS and state[i] != '.':
            break
        e += ENERGY[pod]
        # passing a room, cannot stop here
        if i in ROOMS:
            continue
        new_state = state[::]
        new_state[i] = pod
        new_state[pos] = new_room_content
        new_states.append((new_state, e))

    e = init_energy
    for i in range(pos + 1, HALL_LENGTH):
        # Cannot move any further
        if i not in ROOMS and state[i] != '.':
            break
        e += ENERGY[pod]
        # passing a room, cannot stop here
        if i in ROOMS:
            continue
        new_state = state[::]
        new_state[i] = pod
        new_state[pos] = new_room_content
        new_states.append((new_state, e))

    return new_states

def invalid_state(state):
    s = ''.join(state)
    return sum([s.count(c) for c in 'ABCD']) != 8

def solve(state, energy, depth=0) -> list[int]:
    energies = []

    _print(f'Solving for {state} with energy {energy}, depth: {depth}')

    depth += 1

    # Catching weird states here
    if invalid_state(state):
        print('CURRENT STATE INVALID')
        print(state)
        sys.exit()

    if is_solved(state):
        return [energy]

    # This while used to be here, but we have recurions in the moves, so no need???
    # # Solve for a particular state
    # while not is_solved(state):
    #     # copy_state = state[::]
    #     # bit hacky, start at -2 so while kicks in
    # Selection of all pods goes with a loop
    # TODO: Could also just do a list, and select all 'movable' pods
    for pos, pod in get_amphipods(state):
        
        _print(f'\tGoing to use pod {pod} at position {pos}')
        new_states = get_new_states(state, pod, pos)
        for i, (s, e) in enumerate(new_states):
            _print(f'\tNew state {i} with energy {e}: {s}')
        # _print(f'New states: {new_states}')
        for s, e in new_states:
            energies += solve(s, energy + e, depth)

    return energies

def exercise1():
    energies = solve(HALL_INIT, 0)
    return min(energies)

def exercise2():
    pass

if __name__ == "__main__":
    e1 = exercise1()
    e2 = exercise2()

    if e1:
        print(f'Solution exercise 1: {e1}')
    if TEST:
         print('Solution example exercise 1: 12521')
    if e2:
        print(f'Solution exercise 2: {e2}')
    if TEST:
        print('Solution example exercise 2: ...')
