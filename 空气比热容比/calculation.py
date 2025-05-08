import csv
import math
import os

def calculate_gamma(P1_mV, P2_mV, P0_Pa):
    """
    根据电压读数和大气压计算空气比热容比 gamma。

    Args:
        P1_mV (float): 状态 I 的压力传感器电压读数 (mV)。
        P2_mV (float): 状态 III 的压力传感器电压读数 (mV)。
        P0_Pa (float): 环境大气压 (Pa)。

    Returns:
        float: 计算得到的比热容比 gamma 值。
    """
    # 将 mV 读数转换为相对于大气压的压强 (Pa)
    P1_gauge_Pa = P1_mV * 50
    P2_gauge_Pa = P2_mV * 50

    # 计算状态 I 和状态 III 的绝对压强 (Pa)
    P1_abs_Pa = P0_Pa + P1_gauge_Pa
    P2_abs_Pa = P0_Pa + P2_gauge_Pa

    # 确保 P1/P0 > 1 和 P1/P2 > 1，避免对非正数取对数
    if P1_abs_Pa <= P0_Pa or P1_abs_Pa <= P2_abs_Pa or P2_abs_Pa <= P0_Pa:
         print(f"Warning: Pressure values result in non-positive argument for log. P0={P0_Pa}, P1_abs={P1_abs_Pa}, P2_abs={P2_abs_Pa}")
         return None # Return None or handle appropriately

    # 计算比热容比 gamma
    gamma = math.log(P1_abs_Pa / P0_Pa) / math.log(P1_abs_Pa / P2_abs_Pa)
    return gamma

# 实验开始和结束时的平均大气压强 (Pa)
average_P0_Pa = 100345

# 读取 CSV 文件并计算 gamma
data_file = 'data.csv'
results = {}
all_data = []
fieldnames = []

# 首先读取所有数据和字段名
with open(data_file, mode='r', encoding='utf-8') as infile:
    reader = csv.DictReader(infile)
    fieldnames = reader.fieldnames
    
    for row in reader:
        condition = row['Condition']
        trial = int(row['Trial'])
        P1_mV = float(row['P1_mV'])
        P2_mV = float(row['P2_mV'])

        gamma = calculate_gamma(P1_mV, P2_mV, average_P0_Pa)
        
        # 将计算得到的gamma添加到原始行数据中
        row['Gamma'] = gamma
        all_data.append(row)

        if condition not in results:
            results[condition] = []

        results[condition].append({'Trial': trial, 'P1_mV': P1_mV, 'P2_mV': P2_mV, 'Gamma': gamma})

# 添加Gamma字段（如果不存在）
if 'Gamma' not in fieldnames:
    fieldnames.append('Gamma')

# 将数据写回到CSV文件
with open(data_file, mode='w', newline='', encoding='utf-8') as outfile:
    writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    writer.writeheader()
    for row in all_data:
        # 确保Gamma值格式化为字符串
        if row['Gamma'] is not None:
            row['Gamma'] = f"{row['Gamma']:.6f}"
        else:
            row['Gamma'] = "N/A"
        writer.writerow(row)

print(results)

# 打印计算结果
for condition, trials in results.items():
    print(f"--- {condition} ---")
    for trial_data in trials:
        # Format Gamma to a few decimal places, handle None case
        gamma_value = f"{trial_data['Gamma']:.4f}" if trial_data['Gamma'] is not None else "N/A"
        print(f"Trial {trial_data['Trial']}: P1_mV={trial_data['P1_mV']}, P2_mV={trial_data['P2_mV']}, Gamma={gamma_value}")
    print("-" * (len(condition) + 6)) # Separator line

# Optional: Calculate and print average gamma for each condition
print("\n--- 平均比热容比 ---")
for condition, trials in results.items():
    # Filter out None values before calculating average
    valid_gammas = [t['Gamma'] for t in trials if t['Gamma'] is not None]
    if valid_gammas:
        average_gamma = sum(valid_gammas) / len(valid_gammas)
        print(f"{condition} 平均 Gamma: {average_gamma:.4f}")
    else:
        print(f"{condition} 平均 Gamma: 无有效数据")