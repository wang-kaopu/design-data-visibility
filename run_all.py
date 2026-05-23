"""
run_all.py

Agent entrypoint:
    python run_all.py

This file runs all Python replacements for the Matlab visualization experiments.
"""

from src.exp4_2d_visualization import main as run_exp4
from src.exp5_3d_stats_animation import main as run_exp5
from src.exp6_kmeans import main as run_exp6


def main() -> None:
    print("Running Experiment 4 replacement...")
    run_exp4()

    print("Running Experiment 5 replacement...")
    run_exp5()

    print("Running Experiment 6 replacement...")
    run_exp6()

    print("Done. Check the outputs/ directory.")


if __name__ == "__main__":
    main()
