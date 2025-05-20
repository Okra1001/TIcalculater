import cupy as cp
import numpy as np
import os
import time
from tqdm import tqdm
import pandas as pd


def process_file_cuda(filepath):
    """
    使用 CuPy 加速计算时间积分尺度和空间积分尺度
    """
    try:
        # 从第126行开始读取文件内容
        data = np.loadtxt(filepath, skiprows=119)
    except Exception as e:
        print(f"文件 {filepath} 读取失败：{e}")
        return None, None, None

    # 检查数据是否包含至少两列
    if data.shape[1] < 2:
        print(f"文件 {filepath} 中数据格式错误（需要至少两列数据）！")
        return None, None, None

    # 提取时间和风速数据，并传输到 GPU
    time_array = cp.array(data[:, 0])  # 第一列是时间
    speed_array = cp.array(data[:, 1])  # 第二列是风速

    # 计算采样间隔和平均风速
    dt = cp.mean(cp.diff(time_array))  # 假设采样间隔均匀
    U_mean = cp.mean(speed_array)

    # 去均值（风速脉动）
    u_prime = speed_array - U_mean

    # 自相关函数计算
    N = len(u_prime)
    R = cp.correlate(u_prime, u_prime, mode='full') / cp.var(u_prime) / N
    R = R[N - 1:]  # 取非负滞后部分

    # 时间积分尺度计算
    T_L = cp.sum(R * dt).get()  # 从 GPU 获取结果

    # 空间积分尺度计算
    L = U_mean.get() * T_L

    return T_L, L


def process_folder_cuda(folder_path, output_excel="results.xlsx"):
    """
    遍历文件夹，处理所有 txt 文件，计算积分尺度并导出到 Excel
    """
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.txt')]

    # 初始化结果列表
    results = []
    start_time = time.time()

    for file in tqdm(files, desc="Processing files"):
        T_L, L = process_file_cuda(file)
        if T_L is not None and L is not None:
            results.append({"File": os.path.basename(file), "T_L (s)": T_L, "L (m)": L})

    # 计算总耗时
    total_time = time.time() - start_time
    print(f"所有文件处理完成，总耗时：{total_time:.2f} 秒")

    # 保存结果到 Excel
    df = pd.DataFrame(results)
    df.to_excel(output_excel, index=False)
    print(f"结果已保存到 {output_excel}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="使用 CuPy 加速计算时间积分尺度和空间积分尺度")
    parser.add_argument("folder", type=str, help="包含 txt 文件的文件夹路径")
    parser.add_argument("--output", type=str, default="results.xlsx", help="输出结果的 Excel 文件名")
    args = parser.parse_args()

    process_folder_cuda(args.folder, args.output)
