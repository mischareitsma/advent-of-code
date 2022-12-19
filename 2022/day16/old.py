class Step:
    def __init__(self, valve: str, operation: str, minute: int):
        self.valve = valve
        self.operation = operation
        self.minute = minute

class Path:
    def __init__(self):
        self.steps: list[str] = []
        self.opened_valves: dict[str, int] = []

    def get_pressure_releases(self):
        return 0
    
    def copy(self):
        p = Path()
        p.steps = self.steps[::]
        for v, m in self.opened_valves.items():
            p.opened_valves[v] = m
        return p

"""
Use dfs? At every node, we can open, or walk. We don't open if opened or
if rate = 0 so at a node, for all options (o + w) do options
Then for the option: incr minutes + pressure then go through options
"""
def get_max_pressure() -> int:

    def dfs(v: str, o: str, m: int, p: int, cp: int, vv: list[str]):
        global max_pressure
        global paths_walked
        m += 1
        p += cp

        if m == 30:
            if (paths_walked % 10000 == 0):
                print(f'Paths walked: {paths_walked}, press: {p}, max: {max_pressure}')
            if p > max_pressure:
                max_pressure = p
            paths_walked += 1
            return

        if o == 'o':
            vv.append(v)
            cp += VALVES[v].rate

            for av in VALVES[v].adjacent:
                dfs(av, 'w', m, p, cp, vv[::])
        
        if not v in vv:
            dfs(v, 'o', m, p, cp, vv[::])
        
        for av in VALVES[v].adjacent:
                dfs(av, 'w', m, p, cp, vv[::])

    dfs('AA', 's', 0, 0, 0, [])

def get_best_target(pos, valves, minutes):
    l = []
    for v in valves:
        p = (30 - minutes - len(SHORTEST_ROUTE[(pos, v)])) * VALVES[v][0]
        l.append((v, p))
    l.sort(key=lambda x: x[1])
    
    return l[-1][0]

def get_max_pressure() -> int:
    pressure: int = 0

    rate: int = 0

    valves_with_rate: list[str] = []

    for k, v in VALVES.items():
        if v[0] > 0:
            valves_with_rate.append(k)

    minutes = 0

    pos = 'AA'

    while (minutes < 30 and len(valves_with_rate) > 0):
        minutes += 1
        target = get_best_target(pos, valves_with_rate, minutes)
        valves_with_rate.remove(target)
        steps = len(SHORTEST_ROUTE[(pos, target)])
        minutes += steps
        pressure += (rate * steps)

        # the += 1 at the start is for the opening of the valve.
        rate += VALVES[target][0]
        pos = target

    while minutes < 30:
        minutes += 1
        pressure += rate

    return pressure

