# game of life - grid of cells, live or empty
# each cell has eight neighbors
#  if cell is live :
#      if cell has 2 or 3 neighbors -> live
#  if empty :
#      if cell has exactly 3 neighbors  - > live
#  else empty
#
#

from typing import Set, Tuple, List, Iterator
from time import sleep
from IPython.display import clear_output, display, HTML
import sys

Cell = Tuple[int, int]
World = Set[Cell]

LIVE = "@"
EMPTY = "."
PAD = " "


def neighbors(cell: Cell) -> List[Cell]:
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not i and not j:
                continue
            neighbors.append((cell[0] + i, cell[1] + j))
    return neighbors


def next_generation(world: World) -> World:
    counter = {}
    for cell in world:
        for neighbor in neighbors(cell):
            if neighbor in counter:
                counter[neighbor] += 1
            else:
                counter[neighbor] = 1
    new_world = set()
    for k, v in counter.items():
        if k in world and v in (2, 3):
            new_world.add(k)
        elif k not in world and v == 3:
            new_world.add(k)
    return new_world


def life(world: World, n: int) -> Iterator[World]:
    print(f"initial world: {world}")
    for g in range(n):
        yield world
        world = next_generation(world)
    return 0


def picture(world: World, Xs: range, Ys: range) -> str:
    def row(y):
        return PAD.join(LIVE if (x, y) in world else EMPTY for x in Xs)

    return "\n".join(row(y) for y in Ys)


def animate_life(world: World, n: int, Xs=range(10), Ys=range(10), pause=1 / 5):
    for g, world in enumerate(life(world, n)):
        clear_output(wait=True)
        population = len(world)
        generation_text = f"Generation: {g:2}, Population: {population:2}\n"
        world_picture = picture(world, Xs, Ys)
        print(generation_text)
        print(world_picture)
        # display(HTML(f"<pre>{generation_text}{world_picture}</pre>"))
        sleep(pause)


def main():
    # print(neighbors((1, 2)))
    world = {(3, 1), (1, 2), (1, 3), (2, 3)}
    print(picture(world, range(5), range(5)))
    # life({(3, 1), (1, 2), (1, 3), (2, 3)}, 5)
    animate_life(world, 4, range(5), range(5), 1)


if __name__ == "__main__":
    main()
