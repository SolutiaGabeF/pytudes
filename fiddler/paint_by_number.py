import numpy as np


def generate_colored_array(n: int):
    return np.random.randint(0, 2, n)


def paint_by_colors(n: int) -> float:
    clusters = 0
    current = None
    painting = generate_colored_array(n)
    for i in range(n):
        if painting[i] != current:
            current = painting[i]
            clusters += 1
    return n / clusters
