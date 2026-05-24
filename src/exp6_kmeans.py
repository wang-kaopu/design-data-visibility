from pathlib import Path
from dataclasses import dataclass
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

OUT_DIR = Path(__file__).resolve().parents[1] / "outputs" / "exp6"
OUT_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class KMeansResult:
    centers: np.ndarray
    labels: np.ndarray
    history: list


def save_fig(fig: plt.Figure, filename: str) -> None:
    path = OUT_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(f"[exp6] saved {path}")


def kmeans(data: np.ndarray, k: int, seed: int = 7, max_iter: int = 100, tol: float = 1e-3) -> KMeansResult:
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
            "iteration": iteration,
            "centers": new_centers.copy(),
            "labels": labels.copy(),
            "shift": shift,
        })

        centers = new_centers
        if shift < tol:
            break

    return KMeansResult(centers=centers, labels=labels, history=history)


def simple_2d_kmeans_demo() -> None:
    rng = np.random.default_rng(1)
    x1 = rng.random(100) * 5
    y1 = rng.random(100) * 5
    x2 = rng.random(100) * 5 + 3
    y2 = rng.random(100) * 5 + 3
    data = np.column_stack([np.concatenate([x1, x2]), np.concatenate([y1, y2])])
    result = kmeans(data, k=2, seed=10)

    fig, ax = plt.subplots(figsize=(7, 6))
    for cluster_id in range(2):
        points = data[result.labels == cluster_id]
        ax.scatter(points[:, 0], points[:, 1], marker="*", label=f"cluster {cluster_id + 1}")
    ax.scatter(result.centers[:, 0], result.centers[:, 1], marker="o", s=160, edgecolors="black", label="centers")
    ax.set(title="Simple 2D K-means", xlabel="x", ylabel="y")
    ax.grid(True)
    ax.legend()
    save_fig(fig, "01_simple_2d_kmeans.png")


def generate_3d_cluster_data(seed: int = 3) -> np.ndarray:
    rng = np.random.default_rng(seed)

    mu1 = np.array([0, 0, 0])
    cov1 = np.diag([0.8, 0.9, 0.8])
    data1 = rng.multivariate_normal(mu1, cov1, size=100)

    mu2 = np.array([0.8, 0.8, 0.8])
    cov2 = np.diag([0.8, 0.9, 0.8])
    data2 = rng.multivariate_normal(mu2, cov2, size=100)

    mu3 = np.array([-0.8, 0.8, -0.8])
    cov3 = np.diag([0.8, 0.9, 0.8])
    data3 = rng.multivariate_normal(mu3, cov3, size=100)

    return np.vstack([data1, data2, data3])


def original_3d_data_demo(data: np.ndarray) -> None:
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(data[:100, 0], data[:100, 1], data[:100, 2], marker="+", label="group 1")
    ax.scatter(data[100:200, 0], data[100:200, 1], data[100:200, 2], marker="+", label="group 2")
    ax.scatter(data[200:, 0], data[200:, 1], data[200:, 2], marker="+", label="group 3")
    ax.set(title="Original 3D Gaussian Data", xlabel="x", ylabel="y", zlabel="z")
    ax.legend()
    ax.grid(True)
    save_fig(fig, "02_original_3d_data.png")


def kmeans_3d_final_demo(data: np.ndarray, result: KMeansResult) -> None:
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    for cluster_id in range(3):
        points = data[result.labels == cluster_id]
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker="*", label=f"cluster {cluster_id + 1}")
    centers = result.centers
    ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], marker="x", s=160, linewidths=3, label="centers")
    ax.set(title=f"Final 3D K-means Result ({len(result.history)} iterations)", xlabel="x", ylabel="y", zlabel="z")
    ax.legend()
    ax.grid(True)
    save_fig(fig, "03_final_3d_kmeans.png")


def kmeans_3d_process_animation(data: np.ndarray, result: KMeansResult) -> None:
    fig = plt.figure(figsize=(7, 6))
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

    if not result.history:
        return

    update(0)
    first_frame_path = OUT_DIR / "04_kmeans_process_first_frame.png"
    fig.savefig(first_frame_path, dpi=160)
    print(f"[exp6] saved {first_frame_path}")

    ani = animation.FuncAnimation(fig, update, frames=len(result.history), interval=700, blit=False)
    gif_path = OUT_DIR / "05_kmeans_process.gif"
    try:
        ani.save(gif_path, writer=animation.PillowWriter(fps=1))
        print(f"[exp6] saved {gif_path}")
    except Exception as exc:
        print(f"[exp6] GIF save failed: {exc!r}; first frame already saved.")

    plt.show()
    plt.close(fig)


def main() -> None:
    simple_2d_kmeans_demo()
    data = generate_3d_cluster_data()
    original_3d_data_demo(data)
    result = kmeans(data, k=3, seed=12, max_iter=50, tol=1e-8)
    kmeans_3d_final_demo(data, result)
    kmeans_3d_process_animation(data, result)


if __name__ == "__main__":
    main()
