# K-means 聚类过程可视化

这个项目只演示一个过程：使用 Python 生成三维重叠高斯数据，并用 K-means 算法逐轮完成聚类，最后保存 GIF 并弹出 Matplotlib 动画窗口展示迭代过程。

## 项目结构

```text
.
├── README.md
├── requirements.txt
├── run_all.py
├── src/
│   └── kmeans_process.py
└── outputs/
    └── kmeans_process/        # 运行后自动生成
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

```bash
python src/kmeans_process.py
```

或者：

```bash
python run_all.py
```

运行后会生成：

```text
outputs/kmeans_process/01_original_3d_data.png
outputs/kmeans_process/02_final_kmeans_result.png
outputs/kmeans_process/03_kmeans_process_first_frame.png
outputs/kmeans_process/04_kmeans_process.gif
```

保存 GIF 后，程序会继续弹出 Matplotlib 窗口展示 K-means 聚类迭代动画。

## 演示特点

- 只依赖 `numpy` 和 `matplotlib`。
- 数据使用三组三维高斯分布生成。
- 协方差设置为 `0.8 ~ 0.9`，让点云更分散。
- 聚类中心距离约为 `0.8`，让三个簇有一定重叠。
- K-means 收敛阈值 `tol=1e-8`，使迭代过程更完整。
- 动画中展示每轮的聚类结果、中心点位置和中心点移动量。

## 注意

弹窗展示依赖本机图形界面。请在 macOS、Windows 或 Linux 桌面环境中运行；如果在 SSH、Docker、无图形界面的服务器或 WSL 无显示配置环境中运行，GIF 可以正常保存，但窗口可能无法弹出。
