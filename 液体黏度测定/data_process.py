import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import linregress

# 读取CSV数据（假设文件名为"data.csv"）
df = pd.read_csv('data.csv')

# 常量设置
distance_per_interval = 3.43  # 相邻时间点间隔距离（cm）
g = 978.83  # 重力加速度 (cm/s^2)
rho_0 = 0.96  # 液体密度 (g/cm^3)

# 液柱参数
H_avg = 33.77  # cm
D_avg = 6.023  # cm

# 小球参数
ball_data = {
    'A': {'diameter_mm': 1.500},
    'B': {'diameter_mm': 1.999},
    'C': {'diameter_mm': 2.495}
}

rho_ball = 7.829

velocities = {}
viscosities = {}
reynolds_numbers = {}

# 创建大图框架
plt.figure(figsize=(15, 10))
plot_index = 1

# 遍历每个列名
for column in df.columns:
    ball_name = None
    if column.startswith('A'):
        ball_name = 'A'
    elif column.startswith('B'):
        ball_name = 'B'
    elif column.startswith('C'):
        ball_name = 'C'

    if ball_name:
        times = df[column].dropna().astype(float)
        if len(times) < 2:
            continue

        # 生成位移数组
        s = distance_per_interval * np.arange(1, len(times) + 1)

        t_fit = times[:].values
        s_fit = s[:]

        # 线性回归
        slope, intercept, r_value, _, _ = linregress(t_fit, s_fit)
        r_squared = r_value**2
        velocities[column] = slope

        # 绘制子图
        plt.subplot(3, 3, plot_index)
        plt.scatter(times, s, label='data', color='blue')
        plt.plot(t_fit, slope * t_fit + intercept, 'r--',
                 label=f'v={slope:.2f} cm/s\nR²={r_squared:.3f}')
        plt.xlabel('t (s)')
        plt.ylabel('s (cm)')
        plt.title(column)
        plt.legend()
        plt.grid(True)
        plot_index += 1

        # 计算黏度
        ball = ball_data[ball_name]
        d_cm = ball['diameter_mm'] / 10.0  # cm


        vf = slope  # cm/s
        D = D_avg  # cm
        H = H_avg  # cm

        eta = (1/18) * (d_cm**2 * g * (rho_ball - rho_0)) / (vf * (1 + 2.4 * d_cm / D) * (1 + 1.7 * d_cm / H))
        viscosities[column] = eta

        # 计算雷诺数
        re = (vf * rho_0 * d_cm) / eta
        reynolds_numbers[column] = re

plt.tight_layout()
plt.show()

print("\n计算得到的黏度 (每个测量):")
for column, eta in viscosities.items():
    print(f"黏度 η_{column}: {eta:.4f} g/(cm·s)")

print("\n计算得到的雷诺数 (每个测量):")
for column, re in reynolds_numbers.items():
    print(f"雷诺数 Re_{column}: {re:.4f}")

# 可以选择计算每个小球黏度和雷诺数的平均值
avg_viscosities = {}
avg_reynolds_numbers = {}
for ball_name in ball_data.keys():
    etas = [v for col, v in viscosities.items() if col.startswith(ball_name)]
    res = [v for col, v in reynolds_numbers.items() if col.startswith(ball_name)]
    if etas:
        avg_viscosities[ball_name] = np.mean(etas)
    if res:
        avg_reynolds_numbers[ball_name] = np.mean(res)

print("\n计算得到的平均黏度 (每个小球):")
for ball_name, avg_eta in avg_viscosities.items():
    print(f"平均黏度 η_{ball_name}: {avg_eta:.4f} g/(cm·s)")

print("\n计算得到的平均雷诺数 (每个小球):")
for ball_name, avg_re in avg_reynolds_numbers.items():
    print(f"平均雷诺数 Re_{ball_name}: {avg_re:.4f}")