"""
K-means clustering process visualization.

Run directly:
    python src/kmeans_process.py

The script saves the K-means process GIF and then opens a Matplotlib
window to show the clustering animation.
"""

from pathlib import Path
from dataclasses import dataclass

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation, font_manager
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


OUT_DIR = Path(__file__).resolve().parents[1] / "outputs" / "kmeans_process"
OUT_DIR.mkdir(parents=True, exist_ok=True)

WATERMARK_TEXT = "3123004758王坤平"
WATERMARK_FONT_CANDIDATES = [
    "Microsoft YaHei",
    "SimHei",
    "PingFang SC",
    "Heiti SC",
    "Songti SC",
    "Noto Sans CJK SC",
    "Source Han Sans SC",
    "WenQuanYi Zen Hei",
    "Arial Unicode MS",
]


def get_watermark_font() -> font_manager.FontProperties | None:
    """Pick an available CJK font so the Chinese watermark renders correctly."""
    available_fonts = {font.name for font in font_manager.fontManager.ttflist}
    for font_name in WATERMARK_FONT_CANDIDATES:
        if font_name in available_fonts:
            return font_manager.FontProperties(family=font_name)
    return None


WATERMARK_FONT = get_watermark_font()


def add_watermark(fig: plt.Figure) -> None:
    """Add a small watermark to the bottom-right corner of a figure."""
    fig.text(
        0.985,
        0.015,
        WATERMARK_TEXT,
        ha="right",
        va="bottom",
        fontsize=9,
        color="gray",
        alpha=0.65,
        fontproperties=WATERMARK_FONT,
    )


@dataclass
class KMeansResult:
    centers: np.ndarray
    labels: np.ndarray
    history: list


def save_fig(fig: plt.Figure, filename: str) -> None:
    path = OUT_DIR / filename
    fig.tight_layout()
    add_watermark(fig)
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(f"[kmeans] saved {path}")


def kmeans(data: np.ndarray, k: int, seed: int = 7, max_iter: int = 100, tol: float = 1e-8) -> KMeansResult:
    rng = np.random.default_rng(seed)
    n_samples = data.shape[0]
    centers = data[rng.choice(n_samples, size=k, replace=False)].copy()
    history = []

    for iteration in range(max_iter):
        distances = np.linalg.norm(data[:, None, :] - centers[None, :, :], axis=2)
        labels = np.argmin(distances, axis=1)

        new_centers = centers.copy()
        for cluster_id in range(k):
            cluster_points = data[labels == cluster_id]
            if len(cluster_points) > 0:
                new_centers[cluster_id] = cluster_points.mean(axis=0)

        shift = np.linalg.norm(new_centers - centers)
        history.append({
            "iteration": iteration + 1,
            "centers": new_centers.copy(),
            "labels": labels.copy(),
            "shift": shift,
        })

        centers = new_centers
        if shift < tol:
            break

    return KMeansResult(centers=centers, labels=labels, history=history)


def generate_cluster_data(seed: int = 3) -> np.ndarray:
    """Generate three overlapping 3D Gaussian clusters for K-means visualization."""
    rng = np.random.default_rng(seed)

    mu1 = np.array([0.0, 0.0, 0.0])
    mu2 = np.array([0.8, 0.8, 0.8])
    mu3 = np.array([-0.8, 0.8, -0.8])

    cov = np.diag([0.8, 0.9, 0.8])

    data1 = rng.multivariate_normal(mu1, cov, size=100)
    data2 = rng.multivariate_normal(mu2, cov, size=100)
    data3 = rng.multivariate_normal(mu3, cov, size=100)

    return np.vstack([data1, data2, data3])


def plot_original_data(data: np.ndarray) -> None:
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], marker="+", label="source data")
    ax.set(title="Original 3D Data", xlabel="x", ylabel="y", zlabel="z")
    ax.legend()
    ax.grid(True)
    save_fig(fig, "01_original_3d_data.png")


def plot_final_result(data: np.ndarray, result: KMeansResult) -> None:
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    for cluster_id in range(3):
        points = data[result.labels == cluster_id]
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker="*", label=f"cluster {cluster_id + 1}")

    centers = result.centers
    ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], marker="x", s=160, linewidths=3, label="centers")
    ax.set(
        title=f"Final K-means Result ({len(result.history)} iterations)",
        xlabel="x",
        ylabel="y",
        zlabel="z",
    )
    ax.legend()
    ax.grid(True)
    save_fig(fig, "02_final_kmeans_result.png")


def plot_center_shift(result: KMeansResult) -> None:
    """Plot how much the K-means centers move in each iteration."""
    if not result.history:
        return

    iterations = [state["iteration"] for state in result.history]
    shifts = [state["shift"] for state in result.history]

    fig, ax = plt.subplots(figsize=(7, 6))
    ax.plot(iterations, shifts, marker="o")
    ax.set_title("Center shift in each K-means iteration")
    ax.set_xlabel("iteration")
    ax.set_ylabel("center shift")
    ax.set_xticks(iterations)
    ax.grid(True)
    save_fig(fig, "05_center_shift.png")


def animate_kmeans_process(data: np.ndarray, result: KMeansResult) -> None:
    if not result.history:
        return

    fig = plt.figure(figsize=(7, 6))
    add_watermark(fig)
    ax = fig.add_subplot(111, projection="3d")

    xlim = (data[:, 0].min() - 0.5, data[:, 0].max() + 0.5)
    ylim = (data[:, 1].min() - 0.5, data[:, 1].max() + 0.5)
    zlim = (data[:, 2].min() - 0.5, data[:, 2].max() + 0.5)

    def update(frame_idx: int):
        ax.clear()
        state = result.history[frame_idx]
        labels = state["labels"]
        centers = state["centers"]

        for cluster_id in range(3):
            points = data[labels == cluster_id]
            ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker="*", label=f"cluster {cluster_id + 1}")

        ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], marker="x", s=160, linewidths=3, label="centers")
        ax.set_xlim(*xlim)
        ax.set_ylim(*ylim)
        ax.set_zlim(*zlim)
        ax.set_title(f"K-means iteration {state['iteration']} | center shift={state['shift']:.5f}")
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")
        ax.grid(True)
        ax.legend(loc="upper left")
        return []

    update(0)
    first_frame_path = OUT_DIR / "03_kmeans_process_first_frame.png"
    fig.savefig(first_frame_path, dpi=160)
    print(f"[kmeans] saved {first_frame_path}")

    ani = animation.FuncAnimation(fig, update, frames=len(result.history), interval=700, blit=False)
    gif_path = OUT_DIR / "04_kmeans_process.gif"

    try:
        ani.save(gif_path, writer=animation.PillowWriter(fps=1))
        print(f"[kmeans] saved {gif_path}")
    except Exception as exc:
        print(f"[kmeans] GIF save failed: {exc!r}; first frame already saved.")

    plt.show()
    plt.close(fig)


def main() -> None:
    data = generate_cluster_data()
    result = kmeans(data, k=3, seed=12, max_iter=50, tol=1e-8)

    plot_original_data(data)
    plot_final_result(data, result)
    plot_center_shift(result)
    animate_kmeans_process(data, result)


if __name__ == "__main__":
    main()
