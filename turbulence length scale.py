import os
import pandas as pd
import numpy as np
import time
from tqdm import tqdm  # 进度条库


def process_file(filepath):
    """
    处理单个文件，计算时间积分尺度和空间积分尺度。
    """
    start_time = time.time()

    # 读取文件并查找数据起始行
    data_started = False
    time_list = []
    speed_list = []

    with open(filepath, 'r') as file:
        for line in file:
            # 跳过非数据行，直到发现两列数值
            try:
                values = list(map(float, line.split()))
                if len(values) == 2:  # 判断是否为两列数据
                    data_started = True
                    time_list.append(values[0])  # 第一列是时间
                    speed_list.append(values[1])  # 第二列是风速
            except ValueError:
                if data_started:
                    break  # 数据结束后退出

    if not time_list or not speed_list:
        print(f"文件 {filepath} 中未找到有效数据！")
        return None, None

    # 转换为 NumPy 数组
    time_array = np.array(time_list)
    speed_array = np.array(speed_list)

    # 计算采样间隔和平均风速
    dt = np.mean(np.diff(time_array))  # 假设采样间隔均匀
    U_mean = np.mean(speed_array)

    # 去均值（风速脉动）
    u_prime = speed_array - U_mean

    # 自相关函数计算
    N = len(u_prime)
    R = np.correlate(u_prime, u_prime, mode='full') / np.var(u_prime) / N
    R = R[N - 1:]  # 取非负滞后部分

    # 时间积分尺度计算
    T_L = np.sum(R * dt)

    # 空间积分尺度计算
    L = U_mean * T_L

    end_time = time.time()
    elapsed_time = end_time - start_time
    return T_L, L, elapsed_time


def process_folder(folder_path, output_excel="output.xlsx"):
    """
    处理文件夹下的所有 .txt 文件，将结果写入 Excel 文件。
    """
    result_data = []
    file_list = [f for f in os.listdir(folder_path) if f.endswith('.txt')]

    if not file_list:
        print("文件夹中没有找到 .txt 文件！")
        return

    print(f"正在处理文件夹：{folder_path}，共 {len(file_list)} 个文件")

    for file in tqdm(file_list, desc="处理进度"):
        filepath = os.path.join(folder_path, file)
        T_L, L, elapsed_time = process_file(filepath)

        if T_L is not None and L is not None:
            result_data.append({
                "文件名": file,
                "时间积分尺度 (T_L)": T_L,
                "空间积分尺度 (L)": L,
                "耗时 (秒)": elapsed_time
            })
        else:
            result_data.append({
                "文件名": file,
                "时间积分尺度 (T_L)": "无效数据",
                "空间积分尺度 (L)": "无效数据",
                "耗时 (秒)": "-"
            })

    # 将结果写入 Excel 文件
    result_df = pd.DataFrame(result_data)
    result_df.to_excel(output_excel, index=False)
    print(f"结果已保存到 {output_excel}")


# 主程序入口
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="计算湍流积分尺度的工具")
    parser.add_argument("folder", type=str, help="包含 .txt 文件的文件夹路径")
    parser.add_argument("-o", "--output", type=str, default="output.xlsx", help="输出的 Excel 文件名")
    args = parser.parse_args()

    folder_path = args.folder
    output_excel = args.output

    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        process_folder(folder_path, output_excel)
    else:
        print("提供的文件夹路径无效！")
