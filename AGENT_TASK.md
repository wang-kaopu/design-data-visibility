# Agent 任务文档：将 Matlab 数据可视化实验改写为 Python 并自动运行

## 1. 任务目标

请在当前工作区创建一个 Python 项目，用 `numpy + matplotlib` 替代原 Matlab 实验代码，完成以下内容：

- 实验四：二维数据可视化，包括离散点、subplot、axis、grid、legend、hold on/off、双纵坐标等。
- 实验五：三维曲线、网格/曲面、统计图、散点图、动画。
- 实验六：K-means 聚类，包括简单二维版本和带中间过程记录的三维版本。

执行完成后，所有输出图片和 GIF 动画必须保存到 `outputs/` 目录。

## 2. Agent 执行规则

1. 不要改写本文的文件路径。
2. 在工作区根目录创建下面的文件树。
3. 如果依赖缺失，先执行 `python -m pip install -r requirements.txt`。
4. 执行 `python run_all.py`。
5. 运行完成后检查 `outputs/exp4/`、`outputs/exp5/`、`outputs/exp6/` 是否生成结果文件。
6. 如果 GIF 写入失败，不要中断；脚本会保存 PNG 备用帧。

## 3. 文件树

```text
.
├── requirements.txt
├── run_all.py
├── src/
│   ├── __init__.py
│   ├── exp4_2d_visualization.py
│   ├── exp5_3d_stats_animation.py
│   └── exp6_kmeans.py
└── outputs/
    ├── exp4/
    ├── exp5/
    └── exp6/
```

## 4. Matlab 到 Python 对应关系

| Matlab | Python |
|---|---|
| `plot` | `matplotlib.pyplot.plot` / `Axes.plot` |
| `subplot` | `plt.subplots` / `fig.add_subplot` |
| `axis([xmin xmax ymin ymax])` | `ax.set_xlim` + `ax.set_ylim` |
| `grid on/off` | `ax.grid(True/False)` |
| `box on` | 显示 `ax.spines` |
| `hold on/off` | 同一个 `Axes` 上连续调用 `ax.plot` |
| `plotyy` | `ax.twinx()` |
| `plot3` | `Axes3D.plot3D` |
| `mesh/meshc/meshz` | `plot_wireframe` + `contour` |
| `surf/surfl` | `plot_surface` |
| `bar/barh/bar3` | `bar` / `barh` / `bar3d` |
| `pie/pie3` | `pie`，`pie3` 用 exploded + shadow 近似 |
| `scatter/scatter3` | `scatter` / 3D `scatter` |
| `getframe/movie` | `matplotlib.animation.FuncAnimation` |
| `mvnrnd` | `numpy.random.Generator.multivariate_normal` |

## 5. 执行命令

```bash
python -m pip install -r requirements.txt
python run_all.py
```

## 6. 文件内容


### `requirements.txt`

```text
numpy>=1.24
matplotlib>=3.7

```

### `run_all.py`

```python
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

```

### `src/__init__.py`

```python

```

### `src/exp4_2d_visualization.py`

```python
"""
exp4_2d_visualization.py

Python replacement for Matlab Experiment 4: 2D data visualization.
Run directly:
    python src/exp4_2d_visualization.py

All figures are saved into outputs/exp4/.
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


OUT_DIR = Path(__file__).resolve().parents[1] / "outputs" / "exp4"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def save_fig(fig: plt.Figure, filename: str) -> None:
    path = OUT_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(f"[exp4] saved {path}")


def discrete_data_visualization() -> None:
    """Matlab: n=1:0.5:16; y=...; plot(n,y,'*')"""
    n = np.arange(1, 16.0 + 0.5, 0.5)
    y = 1 / ((n - 3) ** 2 + 1) - 1 / ((n - 9) ** 2 + 4)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(n, y, marker="*", linestyle="--")
    ax.set_title("Discrete Data Visualization")
    ax.set_xlabel("n")
    ax.set_ylabel("y")
    ax.grid(True)
    save_fig(fig, "01_discrete_plot.png")


def subplot_axis_grid_box_demo() -> None:
    """Matlab replacement for plot/subplot/set/axis/grid/box."""
    x = np.arange(0, 5.0 + 0.1, 0.1)
    y = np.sin(x)
    z = np.cos(x)

    fig, axes = plt.subplots(2, 1, figsize=(8, 6))
    axes[0].plot(x, y)
    axes[0].set_title("subplot(2,1,1): sin(x)")
    axes[0].grid(True, axis="x")
    axes[0].set_facecolor("#e6ffe6")

    axes[1].plot(x, z)
    axes[1].set_title("subplot(2,1,2): cos(x)")
    axes[1].set_xlim(0, 4)
    axes[1].set_ylim(-1.2, 1.2)
    axes[1].grid(True)
    for spine in axes[1].spines.values():
        spine.set_visible(True)

    save_fig(fig, "02_subplot_axis_grid_box.png")


def title_label_text_legend_demo() -> None:
    """Matlab replacement for title/xlabel/ylabel/text/legend."""
    x = np.arange(0, np.pi + np.pi / 100, np.pi / 100)
    y1 = 2 * np.exp(-0.5 * x)
    y2 = np.cos(4 * np.pi * x)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, y1, label="y1 = 2e^{-0.5x}")
    ax.plot(x, y2, label="y2 = cos(4πx)")
    ax.set_title("x from 0 to π")
    ax.set_xlabel("Variable X")
    ax.set_ylabel("Variable Y")
    ax.text(0.8, 1.5, "curve y1 = 2e^{-0.5x}")
    ax.text(1.8, 1.1, "curve y2 = cos(4πx)")
    ax.legend()
    ax.grid(True)

    save_fig(fig, "03_title_label_text_legend.png")


def hold_on_off_demo() -> None:
    """
    Matlab hold on/off replacement:
    In Matplotlib, repeated ax.plot(...) calls on the same Axes keep previous curves by default.
    """
    x = np.arange(0, 2 * np.pi + np.pi / 100, np.pi / 100)
    y1 = 0.2 * np.exp(-0.5 * x) * np.cos(4 * np.pi * x)
    y2 = 2 * np.exp(-0.5 * x) * np.cos(np.pi * x)

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.plot(x, y1, label="0.2e^{-0.5x}cos(4πx)")
    ax.plot(x, y2, label="2e^{-0.5x}cos(πx)")
    ax.set_title("hold on/off equivalent")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.legend()
    ax.grid(True)

    save_fig(fig, "04_hold_on_equivalent.png")


def concentric_circles_demo() -> None:
    """Matlab complex plot replacement: x=exp(i*t); y=[x;2*x;3*x]'."""
    t = np.arange(0, 2 * np.pi + 0.01, 0.01)
    x = np.exp(1j * t)
    circles = [x, 2 * x, 3 * x]

    fig, ax = plt.subplots(figsize=(6, 6))
    for idx, c in enumerate(circles, start=1):
        ax.plot(c.real, c.imag, label=f"radius {idx}")
    ax.set_title("Three Concentric Circles")
    ax.set_xlabel("Real")
    ax.set_ylabel("Imaginary")
    ax.axis("equal")
    ax.grid(True)
    ax.legend()
    ax.set_xticks([-3, -2, -1, 0, 1, 2, 3])
    ax.set_yticks([-3, -2, -1, 0, 1, 2, 3])

    save_fig(fig, "05_concentric_circles.png")


def double_y_axis_demo() -> None:
    """Matlab plotyy replacement: Matplotlib twinx()."""
    x = np.arange(0, 2 * np.pi + np.pi / 100, np.pi / 100)
    y1 = 0.2 * np.exp(-0.5 * x) * np.cos(4 * np.pi * x)
    y2 = 2 * np.exp(-0.5 * x) * np.cos(np.pi * x)

    fig, ax1 = plt.subplots(figsize=(8, 4.5))
    ax2 = ax1.twinx()

    line1 = ax1.plot(x, y1, label="y1 small scale")
    line2 = ax2.plot(x, y2, linestyle="--", label="y2 large scale")

    ax1.set_title("Double Y Axis: plotyy -> twinx")
    ax1.set_xlabel("x")
    ax1.set_ylabel("y1")
    ax2.set_ylabel("y2")
    ax1.grid(True)

    lines = line1 + line2
    labels = [line.get_label() for line in lines]
    ax1.legend(lines, labels, loc="upper right")

    save_fig(fig, "06_double_y_axis.png")


def main() -> None:
    discrete_data_visualization()
    subplot_axis_grid_box_demo()
    title_label_text_legend_demo()
    hold_on_off_demo()
    concentric_circles_demo()
    double_y_axis_demo()


if __name__ == "__main__":
    main()

```

### `src/exp5_3d_stats_animation.py`

```python
"""
exp5_3d_stats_animation.py

Python replacement for Matlab Experiment 5:
- 3D curves
- mesh/surf-like surfaces
- 3D view and surface control
- statistical charts
- frame/movie-style animation

Run directly:
    python src/exp5_3d_stats_animation.py

All figures are saved into outputs/exp5/.
"""

from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import animation
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401


OUT_DIR = Path(__file__).resolve().parents[1] / "outputs" / "exp5"
OUT_DIR.mkdir(parents=True, exist_ok=True)


def save_fig(fig: plt.Figure, filename: str) -> None:
    path = OUT_DIR / filename
    fig.tight_layout()
    fig.savefig(path, dpi=160)
    plt.close(fig)
    print(f"[exp5] saved {path}")


def matlab_peaks(n: int = 50):
    """
    Approximation of Matlab peaks(n).
    Returns X, Y, Z over [-3, 3] x [-3, 3].
    """
    x = np.linspace(-3, 3, n)
    y = np.linspace(-3, 3, n)
    X, Y = np.meshgrid(x, y)
    Z = (
        3 * (1 - X) ** 2 * np.exp(-(X ** 2) - (Y + 1) ** 2)
        - 10 * (X / 5 - X ** 3 - Y ** 5) * np.exp(-X ** 2 - Y ** 2)
        - (1 / 3) * np.exp(-(X + 1) ** 2 - Y ** 2)
    )
    return X, Y, Z


def plot3_curve_demo() -> None:
    """Matlab plot3 replacement."""
    t = np.arange(0, 10 * np.pi + np.pi / 100, np.pi / 100)
    x = np.cos(t)
    y = np.sin(t)
    z = (t + 1) ** t * np.sin(t) * np.cos(t)

    # Normalize z for readable plotting, because (t+1)^t grows very quickly.
    z_scaled = z / np.nanmax(np.abs(z))

    fig = plt.figure(figsize=(8, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.plot3D(x, y, z_scaled)
    ax.set_title("Line in 3-D Space")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("scaled Z")
    ax.grid(True)

    save_fig(fig, "01_plot3_curve.png")


def mesh_surface_demo() -> None:
    """Matlab mesh/meshc/meshz/surf replacement."""
    grid = np.arange(-7, 7.0 + 0.5, 0.5)
    X, Y = np.meshgrid(grid, grid)
    R = np.sqrt(X ** 4 + Y ** 4)
    Z = np.sin(R) / np.sqrt(X ** 4 + Y ** 4 + np.finfo(float).eps)

    fig = plt.figure(figsize=(11, 9))

    ax1 = fig.add_subplot(221, projection="3d")
    ax1.plot_wireframe(X, Y, Z, linewidth=0.6)
    ax1.set_title("mesh(x, y, z)")

    ax2 = fig.add_subplot(222, projection="3d")
    ax2.plot_wireframe(X, Y, Z, linewidth=0.6)
    ax2.contour(X, Y, Z, zdir="z", offset=np.nanmin(Z), levels=12)
    ax2.set_title("meshc-like: wireframe + contour")

    ax3 = fig.add_subplot(223, projection="3d")
    ax3.plot_wireframe(X, Y, Z, linewidth=0.6)
    ax3.contour(X, Y, Z, zdir="z", offset=np.nanmin(Z), levels=8)
    ax3.set_zlim(np.nanmin(Z), np.nanmax(Z))
    ax3.set_title("meshz-like: wireframe + base contour")

    ax4 = fig.add_subplot(224, projection="3d")
    ax4.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=True)
    ax4.set_title("surf(x, y, z)")

    save_fig(fig, "02_mesh_surface_demo.png")


def surface_control_demo() -> None:
    """Matlab view/rotate/colormap/shading/surfl-style surface controls."""
    X, Y, Z = matlab_peaks(40)

    fig = plt.figure(figsize=(12, 5))

    ax1 = fig.add_subplot(121, projection="3d")
    ax1.plot_surface(X, Y, Z, cmap="viridis", linewidth=0, antialiased=True)
    ax1.set_title("Default surface")

    ax2 = fig.add_subplot(122, projection="3d")
    ax2.plot_surface(X, Y, Z, cmap="plasma", linewidth=0, antialiased=True)
    ax2.view_init(elev=40, azim=0)
    ax2.set_title("view(0,40)-like")

    save_fig(fig, "03_surface_control_view.png")

    fig2 = plt.figure(figsize=(8, 5))
    ax = fig2.add_subplot(111, projection="3d")
    ax.plot_surface(X, Y, Z, cmap="jet", linewidth=0, antialiased=True)
    ax.view_init(elev=30, azim=45)
    ax.set_title("surfl-like shaded surface")
    save_fig(fig2, "04_surfl_like_surface.png")


def area_chart_demo() -> None:
    """Matlab area replacement: stackplot."""
    x = np.arange(-2, 3)
    Y = np.array([
        [3, 8, 9, 4, 1],
        [6, 3, 5, 2, 7],
        [5, 4, 3, 8, 6],
    ])

    fig, ax = plt.subplots(figsize=(8, 4.5))
    ax.stackplot(x, Y, labels=["Factor A", "Factor B", "Factor C"])
    ax.set_title("area -> stackplot")
    ax.set_xlabel("x")
    ax.set_ylabel("value")
    ax.legend(loc="upper left")
    ax.grid(True)

    save_fig(fig, "05_area_stackplot.png")


def bar_charts_demo() -> None:
    """Matlab bar/barh/bar3/bar3h replacement."""
    x = np.arange(-2, 3)
    Y = np.array([
        [3, 7, 2, 5, 1],
        [3, 7, 5, 2, 1],
        [5, 4, 1, 2, 5],
    ])

    fig = plt.figure(figsize=(11, 9))

    ax1 = fig.add_subplot(221)
    bottom = np.zeros_like(x, dtype=float)
    for row, label in zip(Y, ["Factor A", "Factor B", "Factor C"]):
        ax1.bar(x, row, bottom=bottom, label=label)
        bottom += row
    ax1.set_title("stacked bar")
    ax1.set_xlabel("x")
    ax1.set_ylabel("Σ y")
    ax1.legend()

    ax2 = fig.add_subplot(222)
    width = 0.25
    for i, row in enumerate(Y):
        ax2.bar(x + (i - 1) * width, row, width=width, label=f"Factor {chr(65+i)}")
    ax2.set_title("grouped bar")
    ax2.legend()

    ax3 = fig.add_subplot(223)
    y_pos = np.arange(len(x))
    left = np.zeros_like(x, dtype=float)
    for row, label in zip(Y, ["Factor A", "Factor B", "Factor C"]):
        ax3.barh(y_pos, row, left=left, label=label)
        left += row
    ax3.set_yticks(y_pos)
    ax3.set_yticklabels(x)
    ax3.set_title("stacked horizontal bar")

    ax4 = fig.add_subplot(224, projection="3d")
    xpos, ypos = np.meshgrid(np.arange(Y.shape[1]), np.arange(Y.shape[0]))
    xpos = xpos.ravel()
    ypos = ypos.ravel()
    zpos = np.zeros_like(xpos)
    dx = dy = 0.45 * np.ones_like(zpos, dtype=float)
    dz = Y.ravel()
    ax4.bar3d(xpos, ypos, zpos, dx, dy, dz)
    ax4.set_title("bar3d")
    ax4.set_xlabel("x index")
    ax4.set_ylabel("factor")
    ax4.set_zlabel("value")

    save_fig(fig, "06_bar_charts.png")


def pie_charts_demo() -> None:
    """Matlab pie/pie3 replacement. Matplotlib has 2D pie; pie3 is approximated with an exploded pie."""
    a = np.array([1, 1.6, 1.2, 0.8, 2.1])
    labels = ["Factor A", "Factor B", "Factor C", "Factor D", "Factor E"]

    fig, axes = plt.subplots(1, 2, figsize=(11, 5))
    axes[0].pie(a, explode=[0.1, 0, 0.1, 0, 0], labels=labels, autopct="%1.1f%%")
    axes[0].set_title("pie")

    explode_min = [0.15 if value == a.min() else 0 for value in a]
    axes[1].pie(a, explode=explode_min, labels=labels, autopct="%1.1f%%", shadow=True)
    axes[1].set_title("pie3-like: exploded + shadow")

    save_fig(fig, "07_pie_charts.png")


def scatter_demos() -> None:
    """Matlab scatter/scatter3/plotmatrix replacement."""
    rng = np.random.default_rng(42)

    X = np.arange(1, 11)
    Y = X ** 2 + rng.random(size=X.shape)

    fig, ax = plt.subplots(figsize=(6, 4.5))
    ax.scatter(X, Y)
    ax.set_facecolor("#fff8cc")
    ax.set_title("scatter")
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.grid(True)
    save_fig(fig, "08_scatter.png")

    x = np.array([4229042.63, 4230585.02, 4231384.96, 4231773.63, 4233028.58, 4233296.71, 4235869.68, 4236288.29])
    y = np.array([431695.4, 441585.8, 432745.6, 436933.7, 428734.4, 431946.3, 428705.0, 432999.5])
    z = np.array([1.019, 1.023, 1.011, 1.022, 1.020, 1.022, 1.022, 1.023])

    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(x, y, z)
    ax.set_title("scatter3")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    save_fig(fig, "09_scatter3.png")

    data = rng.standard_normal((100, 2))
    fig, axes = plt.subplots(2, 2, figsize=(7, 7))
    axes[0, 0].hist(data[:, 0], bins=15)
    axes[0, 0].set_title("x1 histogram")
    axes[1, 1].hist(data[:, 1], bins=15)
    axes[1, 1].set_title("x2 histogram")
    axes[0, 1].scatter(data[:, 1], data[:, 0], s=12)
    axes[0, 1].set_xlabel("x2")
    axes[0, 1].set_ylabel("x1")
    axes[1, 0].scatter(data[:, 0], data[:, 1], s=12)
    axes[1, 0].set_xlabel("x1")
    axes[1, 0].set_ylabel("x2")
    fig.suptitle("plotmatrix-like scatter matrix")
    save_fig(fig, "10_plotmatrix_like.png")


def movie_animation_demo() -> None:
    """Matlab getframe/movie replacement: save rotating surface as GIF."""
    X, Y, Z = matlab_peaks(50)
    fig = plt.figure(figsize=(7, 5))
    ax = fig.add_subplot(111, projection="3d")
    surface = ax.plot_surface(X, Y, Z, cmap="copper", linewidth=0, antialiased=True)
    ax.set_xlim(-3, 3)
    ax.set_ylim(-3, 3)
    ax.set_zlim(np.nanmin(Z), np.nanmax(Z))
    ax.set_title("Rotating peaks surface")
    ax.set_axis_off()

    def update(frame_idx: int):
        ax.view_init(elev=30, azim=-37.5 + frame_idx * 5)
        return (surface,)

    ani = animation.FuncAnimation(fig, update, frames=72, interval=80, blit=False)
    gif_path = OUT_DIR / "11_rotating_peaks.gif"

    try:
        ani.save(gif_path, writer=animation.PillowWriter(fps=12))
        print(f"[exp5] saved {gif_path}")
    except Exception as exc:
        fallback_path = OUT_DIR / "11_rotating_peaks_frame.png"
        update(0)
        fig.savefig(fallback_path, dpi=160)
        print(f"[exp5] GIF save failed: {exc!r}; saved fallback {fallback_path}")
    finally:
        plt.close(fig)


def main() -> None:
    plot3_curve_demo()
    mesh_surface_demo()
    surface_control_demo()
    area_chart_demo()
    bar_charts_demo()
    pie_charts_demo()
    scatter_demos()
    movie_animation_demo()


if __name__ == "__main__":
    main()

```

### `src/exp6_kmeans.py`

```python
"""
exp6_kmeans.py

Python replacement for Matlab Experiment 6:
- simple 2D K-means
- 3D K-means process with intermediate results
- optional GIF animation of clustering process

Run directly:
    python src/exp6_kmeans.py

All figures are saved into outputs/exp6/.
"""

from pathlib import Path
from dataclasses import dataclass
import numpy as np
import matplotlib
matplotlib.use("Agg")
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
    """
    Minimal K-means implementation, using only NumPy.
    data: shape (sample_count, feature_count)
    k: number of clusters
    """
    rng = np.random.default_rng(seed)
    n_samples = data.shape[0]
    initial_idx = rng.choice(n_samples, size=k, replace=False)
    centers = data[initial_idx].copy()
    history = []

    for iteration in range(max_iter):
        # distance matrix: shape (sample_count, k)
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
    """Replacement for the simple Matlab 2D K-means example."""
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
    ax.set_title("Simple 2D K-means")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()

    save_fig(fig, "01_simple_2d_kmeans.png")


def generate_3d_cluster_data(seed: int = 3) -> np.ndarray:
    """Replacement for Matlab mvnrnd-based 3D Gaussian data generation."""
    rng = np.random.default_rng(seed)

    mu1 = np.array([0, 0, 0])
    cov1 = np.diag([0.3, 0.35, 0.3])
    data1 = rng.multivariate_normal(mu1, cov1, size=100)

    mu2 = np.array([1.25, 1.25, 1.25])
    cov2 = np.diag([0.3, 0.35, 0.3])
    data2 = rng.multivariate_normal(mu2, cov2, size=100)

    mu3 = np.array([-1.25, 1.25, -1.25])
    cov3 = np.diag([0.3, 0.35, 0.3])
    data3 = rng.multivariate_normal(mu3, cov3, size=100)

    return np.vstack([data1, data2, data3])


def original_3d_data_demo(data: np.ndarray) -> None:
    """Plot original 3D data before clustering."""
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")
    ax.scatter(data[:100, 0], data[:100, 1], data[:100, 2], marker="+", label="group 1")
    ax.scatter(data[100:200, 0], data[100:200, 1], data[100:200, 2], marker="+", label="group 2")
    ax.scatter(data[200:, 0], data[200:, 1], data[200:, 2], marker="+", label="group 3")
    ax.set_title("Original 3D Gaussian Data")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.legend()
    ax.grid(True)

    save_fig(fig, "02_original_3d_data.png")


def kmeans_3d_final_demo(data: np.ndarray, result: KMeansResult) -> None:
    """Plot final 3D K-means result."""
    fig = plt.figure(figsize=(7, 6))
    ax = fig.add_subplot(111, projection="3d")

    for cluster_id in range(3):
        points = data[result.labels == cluster_id]
        ax.scatter(points[:, 0], points[:, 1], points[:, 2], marker="*", label=f"cluster {cluster_id + 1}")

    centers = result.centers
    ax.scatter(centers[:, 0], centers[:, 1], centers[:, 2], marker="x", s=160, linewidths=3, label="centers")
    ax.set_title(f"Final 3D K-means Result ({len(result.history)} iterations)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_zlabel("z")
    ax.legend()
    ax.grid(True)

    save_fig(fig, "03_final_3d_kmeans.png")


def kmeans_3d_process_animation(data: np.ndarray, result: KMeansResult) -> None:
    """Replacement for getframe/addframe-style K-means process recording."""
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
    finally:
        plt.close(fig)


def main() -> None:
    simple_2d_kmeans_demo()

    data = generate_3d_cluster_data()
    original_3d_data_demo(data)
    result = kmeans(data, k=3, seed=12)
    kmeans_3d_final_demo(data, result)
    kmeans_3d_process_animation(data, result)


if __name__ == "__main__":
    main()

```
