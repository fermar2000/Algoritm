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

type Decision = ...                 # Debes obtenerlo de tu conjunto de soluciones (X)
type Solution = list[Decision]
type Score = int
type ScoredSolution = tuple[Score, Solution]
type Result = ScoredSolution | None

# --- FUNCIONES -----

def read_data(f: TextIO) -> Data:
    pass

def process(data: Data) -> Result:
    pass

def show_result(result: Result) -> None:
    pass

# --- PROGRAMA PRINCIPAL -----

if __name__ == '__main__':
    data0 = read_data(sys.stdin)
    result0 = process(data0)
    show_result(result0)