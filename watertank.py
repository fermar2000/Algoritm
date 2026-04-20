import sys
from dataclasses import dataclass
from typing import TextIO, Iterator, Self
from algoritmia.schemes.bab_scheme import BabDecisionSequence, bab_min_solve

# --- BEGIN Comprobar las versiones de Python y algoritmia ---

def _check_environment(min_py: tuple[int, ...], min_alg: tuple[int, ...]):
    # Comprueba la versión de Python
    if sys.version_info < min_py:
        print(f"ERROR: Se requiere Python {'.'.join(map(str, min_py))} o superior (detectado {sys.version.split()[0]})")
        sys.exit(1)
    # Comprueba la versión de algoritmia
    try:
        from algoritmia import TVERSION
    except ModuleNotFoundError:
        print("ERROR: La biblioteca algoritmia no está instalada.", file=sys.stderr)
        sys.exit(1)
    except ImportError:
        TVERSION = (0, 0, 0)
    if TVERSION < min_alg:
        print(f"ERROR: Se requiere algoritmia >= {'.'.join(map(str, min_alg))}", file=sys.stderr)
        print("Puedes instalarla/actualizarla desde el terminal de PyCharm con este comando:", file=sys.stderr)
        print("    pip install algoritmia --upgrade", file=sys.stderr)
        sys.exit(1)

_check_environment((3, 12), (4, 0, 6))  # Versiones mínimas: python 3.12 y algoritmia 4.0.6

# --- END Comprobar las versiones de Python y algoritmia ---

infinity = 10**10                   # Un entero suficientemente grande

# --- TIPOS -----

type Jug = tuple[int, int]          # Una jarra: (capacidad, precio)
type Data = tuple[int, list[Jug]]

type Decision = int                 # Debes obtenerlo de tu conjunto de soluciones (X)
type Solution = list[Decision]
type Score = int
type ScoredSolution = tuple[Score, Solution]
type Result = ScoredSolution | None

# --- FUNCIONES -----

def read_data(f: TextIO) -> Data:
    lines = [line.strip() for line in f if line.strip()]
    l_total = int(lines[0].lstrip('\ufeff'))
    jugs = []
    for line in lines[1:]:
        jugs.append(tuple(map(int, line.split())))
    return l_total, jugs


def process(data: Data) -> Result:
    capacity, jugs = data
    n = len(jugs)

    @dataclass
    class Extra:
        liters: int
        cost: int
        score: int

    score_factor = capacity + 1
    suffix_min = [[infinity] * (capacity + 1) for _ in range(n + 1)]
    suffix_min[n][0] = 0

    for i in range(n - 1, -1, -1):
        cap, price = jugs[i]
        row = suffix_min[i]
        next_row = suffix_min[i + 1]

        for remaining in range(capacity + 1):
            best = next_row[remaining]
            max_uses = remaining // cap

            for uses in range(1, max_uses + 1):
                bought = (uses + 2) // 3
                candidate = bought * price * score_factor + bought + next_row[remaining - uses * cap]
                if candidate < best:
                    best = candidate

            row[remaining] = best

    class WaterTank(BabDecisionSequence[int, Extra, int]):

        def calculate_opt_bound(self) -> int:
            remaining = capacity - self.extra.liters
            return self.extra.score + suffix_min[len(self)][remaining]

        def calculate_pes_bound(self) -> int:
            return self.calculate_opt_bound()

        def is_solution(self) -> bool:
            return self.extra.liters == capacity

        def successors(self):
            i = len(self)
            if i >= n:
                return

            cap, price = jugs[i]
            remaining = capacity - self.extra.liters
            children = []

            for uses in range(remaining // cap, -1, -1):
                bought = (uses + 2) // 3
                liters = self.extra.liters + uses * cap
                cost = self.extra.cost + bought * price
                score = self.extra.score + bought * price * score_factor + bought
                children.append(self.add_decision(uses, Extra(liters, cost, score)))

            children.sort(key=lambda child: child.opt())
            yield from children

        def state(self):
            return (len(self), self.extra.liters)

    initial = WaterTank(Extra(0, 0, 0))
    result = bab_min_solve(initial)

    if result is None:
        return None

    score, sol_ds = result
    decisions = list(sol_ds.decisions())
    while len(decisions) < n:
        decisions.append(0)
    return sol_ds.extra.cost, decisions

def show_result(result: Result) -> None:
    if result is None:
        print("NO SOLUTION")
    else:
        score, solutions = result
        print(score)
        for uses in solutions:
            print((uses + 2) // 3, uses)


# --- PROGRAMA PRINCIPAL -----

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)
