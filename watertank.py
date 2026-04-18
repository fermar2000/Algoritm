import sys
from dataclasses import dataclass
from json.encoder import INFINITY
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
    l_total = int(lines[0])
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

    class WaterTank(BabDecisionSequence[int, Extra, int]):

        def calculate_opt_bound(self) -> int:
            liters = self.extra.liters
            cost = self.extra.cost

            for i in range(len(self), n):
                cap, price = jugs[i]
                if liters >= cap:
                    break
                f = min(1, (capacity - liters) / cap)
                liters += f * cap
                cost += f * price

            return cost

        def calculate_pes_bound(self) -> int:
            liters = self.extra.liters
            cost = self.extra.cost

            for i in range(len(self), n):
                cap, price = jugs[i]
                if liters + cap <= capacity:
                    liters += cap
                    cost += price

            if liters < capacity:
                return infinity

            return cost

        def is_solution(self) -> bool:
            return self.extra.liters == capacity

        def successors(self):
            i = len(self)
            if i >= n:
                return

            cap, price = jugs[i]

            if self.extra.liters + cap <= capacity:
                yield self.add_decision(1, Extra(self.extra.liters + cap,self.extra.cost + price))

            yield self.add_decision(0, self.extra)

        def state(self):
            return (len(self), self.extra.liters)

    initial = WaterTank(Extra(0,0))
    result = bab_min_solve(initial)

    if result is None:
        return None

    score, sol_ds = result
    return score, list(sol_ds.decisions())

def show_result(result: Result) -> None:
    if result is None:
        print("NO SOLUTION")
    else:
        score, solutions = result
        print(score)


# --- PROGRAMA PRINCIPAL -----

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)