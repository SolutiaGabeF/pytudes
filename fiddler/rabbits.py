import random
from typing import Tuple, Dict

ORANGE = "orange"
GREEN = "green"
PURPLE = "purple"


def rabbits(n: int) -> Tuple[float, Dict[int, int]]:
    total_score = 0
    distribution = {0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    for _ in range(n):
        score = 0
        hat = [ORANGE, ORANGE, GREEN, GREEN, PURPLE, PURPLE]
        choices = {ORANGE: 2, GREEN: 2, PURPLE: 2}
        random.shuffle(hat)
        while hat:
            choice = max(choices, key=choices.get)
            actual = hat.pop()
            if actual == choice:
                choices[choice] -= 1
                score += 1
            else:
                break
        total_score += score
        distribution[score] += 1
    avg = total_score / n
    return avg, distribution


def main():
    rabbits(1000000)


if __name__ == "__main__":
    main()
