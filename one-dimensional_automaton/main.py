
from rich.console import Console
from algorithm import Computed


def f(neighbors: dict[int, bool]) -> bool:
    return ((not neighbors[-1]) or (neighbors[0]) or (neighbors[1])) and ((neighbors[-1]) or (not neighbors[0]) or (not neighbors[1])) and ((not neighbors[-1]) or (not neighbors[0]) or (neighbors[1]))


def main():
    console = Console()
    computed = Computed(state=[True], function=f, rang=1)
    console.print(computed)


if __name__ == '__main__':
    main()
