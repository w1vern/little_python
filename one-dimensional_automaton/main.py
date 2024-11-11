
from rich.console import Console
from algorithm import Computed


def f(neighbors: dict[bool]) -> bool:
    return neighbors[-1] or neighbors[0] ^ neighbors[1]


def main():
    console = Console()
    computed = Computed(state=[True, False, False, True], function=f, rang=1)
    console.print(computed)


if __name__ == '__main__':
    main()
