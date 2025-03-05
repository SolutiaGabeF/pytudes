import time
import random
from typing import Tuple, Dict
import matplotlib.pyplot as plt
from rich.console import Console
from rich.table import Table

COLOR_NAMES = {0: "ORANGE", 1: "GREEN", 2: "PURPLE"}

ORANGE = 0
GREEN = 1
PURPLE = 2
RUNS = 1000000


def rabbits_original(n: int) -> Tuple[float, Dict[int, int]]:
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


def rabbits_extra_credit(n: int, rabbits: int = 10):
    total_score = 0
    distribution = {}
    for _ in range(n):
        score = 0
        hat = {ORANGE: rabbits, GREEN: rabbits, PURPLE: rabbits}
        choices = {ORANGE: rabbits, GREEN: rabbits, PURPLE: rabbits}
        while hat:
            choice = max(choices, key=choices.get)
            color_list = []
            for color, count in hat.items():
                color_list.extend([color] * count)
            actual = random.choice(color_list)
            if actual == choice:
                choices[choice] -= 1
                hat[choice] -= 1
                if hat[choice] == 0:
                    del hat[choice]
                score += 1
            else:
                break
        total_score += score
        distribution[score] = distribution.get(score, 0) + 1
    avg = total_score / n
    return avg, dict(sorted(distribution.items()))


def format_simulation_results(
    name: str,
    avg: float,
    distribution: Dict[int, int],
    elapsed: float,
    runs: int,
    rabbits: int,
) -> str:
    """
    Format simulation results as a nicely styled string.

    Args:
        name: Name of the simulation
        avg: Average score
        distribution: Distribution of scores
        elapsed: Elapsed time in seconds
        runs: Number of simulation runs
        rabbits: Number of rabbits per color (for extra credit simulation)

    Returns:
        Formatted string with simulation results
    """
    console = Console(record=True, width=100)

    title = f"{name} Simulation Results "
    if rabbits:
        title += f" ({rabbits} rabbits per color)"

    table = Table(title=title, show_header=True, header_style="bold magenta")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")

    table.add_row("Simulation Runs", f"{runs:,}")
    table.add_row("Runtime", f"{elapsed:.2f} seconds")
    table.add_row("Average Score", f"{avg:.6f}")
    table.add_row("Iterations per Second", f"{runs/elapsed:,.2f}")

    console.print(table)

    dist_table = Table(title="Score Distribution", show_header=True)
    dist_table.add_column("Score", style="cyan")
    dist_table.add_column("Count", style="green")
    dist_table.add_column("Percentage", style="yellow")

    for score, count in sorted(distribution.items()):
        percentage = (count / runs) * 100
        dist_table.add_row(str(score), f"{count:,}", f"{percentage:.2f}%")

    console.print(dist_table)

    return console.export_text()


def plot_distribution(
    distribution: Dict[int, int], title: str, runs: int, save_path: str = None
):
    """
    Plot the distribution of scores from a simulation.

    Args:
        distribution: Dictionary mapping scores to counts
        title: Title for the plot
        runs: Total number of simulation runs
        save_path: Path to save the plot (optional)
    """
    scores = list(distribution.keys())
    counts = list(distribution.values())
    percentages = [count / runs * 100 for count in counts]

    plt.figure(figsize=(10, 6))
    bars = plt.bar(scores, percentages)

    colormap = plt.get_cmap("viridis")
    for i, bar in enumerate(bars):
        bar.set_color(colormap(i / len(bars)))

    plt.title(title)
    plt.xlabel("Score")
    plt.ylabel("Percentage (%)")
    plt.grid(axis="y", alpha=0.3)

    for i, p in enumerate(percentages):
        plt.text(scores[i], p + 0.5, f"{p:.1f}%", ha="center")

    if save_path:
        plt.savefig(save_path)

    plt.close()


def run_with_progress(simulation_func, runs, **kwargs):
    """ """
    console = Console()
    with console.status(f"Running {runs:,} simulations..."):
        start_time = time.time()
        result = simulation_func(runs, **kwargs)
        elapsed = time.time() - start_time

    return result, elapsed


if __name__ == "__main__":
    runs = 1000000

    (avg, distribution), elapsed = run_with_progress(rabbits_original, runs)
    format_simulation_results("Original Rabbits", avg, distribution, elapsed, runs, 2)
    plot_distribution(
        distribution, "Original Rabbits Score Distribution", runs, "p1.png"
    )

    (avg, distribution), elapsed = run_with_progress(
        rabbits_extra_credit, runs, rabbits=10
    )
    format_simulation_results(
        "Extra Credit Rabbits", avg, distribution, elapsed, runs, rabbits=10
    )
    plot_distribution(
        distribution, "Extra Credit Rabbits Score Distribution", runs, "p2.png"
    )
