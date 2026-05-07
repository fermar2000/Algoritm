import sys
from typing import TextIO

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

type Decision = tuple[int, int]     # Una decision: (jarras compradas, usos)
type Solution = list[Decision]
type Score = int
type ScoredSolution = tuple[Score, Solution]
type Result = ScoredSolution | None
type SParams = tuple[int, int]      # (litros pendientes, numero de tipos de jarra disponibles)

# --- FUNCIONES -----

def read_data(f: TextIO) -> Data:
    lines = [line.strip() for line in f if line.strip()]
    capacity = int(lines[0])
    jugs = [tuple(map(int, line.split())) for line in lines[1:]]
    return capacity, jugs

def process(data: Data) -> Result:
    capacity, jugs = data

    def bought_jugs(uses: int) -> int:
        return (uses + 2) // 3

    def S(liters: int, n: int) -> Score:
        if n == 0:
            return 0 if liters == 0 else infinity

        if (liters, n) not in mem:
            jug_capacity, jug_price = jugs[n - 1]
            best_score = infinity
            best_previous = (-1, -1)
            best_decision = (0, 0)

            for uses in range(liters // jug_capacity + 1):
                bought = bought_jugs(uses)
                previous_liters = liters - uses * jug_capacity
                previous_score = S(previous_liters, n - 1)
                current_score = previous_score + bought * jug_price

                if current_score < best_score:
                    best_score = current_score
                    best_previous = (previous_liters, n - 1)
                    best_decision = (bought, uses)

            mem[liters, n] = best_score, best_previous, best_decision

        return mem[liters, n][0]

    mem: dict[SParams, tuple[Score, SParams, Decision]] = {}
    score = S(capacity, len(jugs))

    if score == infinity:
        return None

    decisions: Solution = []
    liters, n = capacity, len(jugs)
    while n > 0:
        _, (liters, n), decision = mem[liters, n]
        decisions.append(decision)

    decisions.reverse()
    return score, decisions

def show_result(result: Result) -> None:
    if result is None:
        print("NO SOLUTION")
    else:
        score, solution = result
        print(score)
        for bought, uses in solution:
            print(bought, uses)

# --- PROGRAMA PRINCIPAL -----

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)
