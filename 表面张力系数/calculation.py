import csv
import numpy as np

def calculate_surface_tension(delta_m_values, l_values, g):
    """
    计算表面张力系数。

    参数：
        delta_m_values: m2 - m3 值的列表 (单位: g)。
        l_values: 金属细丝横梁的长度列表 (单位: cm)。
        g: 重力加速度。

    返回：
        根据平均值计算的表面张力系数。
    """
    avg_delta_m = np.mean(delta_m_values)
    avg_l = np.mean(l_values)
    surface_tension = avg_delta_m * 0.001 * g / (2 * avg_l * 0.01) # Convert g to kg and cm to m
    return surface_tension

def calculate_uncertainty_mass_only(m2_values, m3_values, l_values, g):
    """
    计算表面张力系数的组合标准不确定度，仅考虑质量的不确定度。

    参数：
        m2_values: 电子天平最大示数m2的列表 (单位: g)。
        m3_values: 电子天平最终示数m3的列表 (单位: g)。
        l_values: 金属细丝横梁的长度列表 (单位: cm)。
        g: 重力加速度。

    返回：
        表面张力系数的组合标准不确定度和扩展不确定度。
    """
    m2_kg = np.array(m2_values) * 1e-3
    m3_kg = np.array(m3_values) * 1e-3
    l_m = np.array(l_values) * 1e-2
    delta_m = m2_kg - m3_kg
    mean_delta_m = np.mean(delta_m)
    mean_l = np.mean(l_m)

    # 标准不确定度 for mass (triangular distribution)
    u_m = (0.001 * 1e-3) / np.sqrt(6)  # 0.001 g = 0.001e-3 kg

    # 灵敏度系数 for mass
    c_delta_m = g / (2 * mean_l)

    # 合成标准不确定度 (仅考虑质量)
    u_c_sigma = np.abs(c_delta_m) * u_m

    # 扩展不确定度 (k=2 for approximately 95% confidence level)
    U_sigma = 2 * u_c_sigma

    return u_c_sigma, U_sigma

def read_data_from_csv(filename):
    """
    从CSV文件中读取m2、m3和l的值。

    参数：
        filename: CSV文件名。

    返回：
        m2值的列表、m3值的列表和l值的列表。
    """
    m2_values = []
    m3_values = []
    l_values = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # 跳过标题行
        for row in reader:
            if len(row) >= 3 and row[2]:
                try:
                    m2_values.append(float(row[0]))
                    m3_values.append(float(row[1]))
                    l_values.append(float(row[2]))
                except ValueError:
                    print(f"Skipping row due to invalid data: {row}")
            else:
                print(f"Skipping row due to missing length data: {row}")
    return m2_values, m3_values, l_values

# 示例用法
file_name = 'data.csv'
g = 9.7883

m2_values, m3_values, l_values = read_data_from_csv(file_name)

if m2_values and m3_values and l_values:
    delta_m_values_g = [m2 - m3 for m2, m3 in zip(m2_values, m3_values)]
    surface_tension_mean = calculate_surface_tension(delta_m_values_g, l_values, g)
    u_c_sigma, U_sigma = calculate_uncertainty_mass_only(m2_values, m3_values, l_values, g)

    print(f"表面张力系数：{surface_tension_mean:.4e} N/m")
    print(f"扩展不确定度 (仅考虑质量, 95%置信水平): {U_sigma:.4e} N/m")
    print(f"最终结果 (仅考虑质量不确定度): ({surface_tension_mean:.4e} ± {U_sigma:.4e}) N/m")
else:
    print("未能读取到有效数据，无法计算表面张力系数和不确定度。")