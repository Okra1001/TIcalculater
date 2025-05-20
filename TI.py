import os
import numpy as np
import pandas as pd

def read_data_from_file(file_path, start_row):
    """
    从文件中读取数据，从指定的行开始
    :param file_path: 文件路径
    :param start_row: 开始读取的行数
    :return: 时间列表和风速列表
    """
    times = []
    wind_speeds = []
    with open(file_path, 'r') as file:
        for _ in range(start_row - 1):
            next(file)  # 跳过前面的行
        for line in file:
            parts = line.strip().split()
            if len(parts) >= 2:
                times.append(float(parts[0]))
                wind_speeds.append(float(parts[1]))
    return times, wind_speeds

def calculate_turbulence_intensity(wind_speeds):
    """
    计算湍流度
    :param wind_speeds: 风速列表
    :return: 湍流度
    """
    wind_speeds = np.array(wind_speeds)
    mean_wind_speed = np.mean(wind_speeds)
    std_wind_speed = np.std(wind_speeds)
    turbulence_intensity = std_wind_speed / mean_wind_speed
    return turbulence_intensity, mean_wind_speed

def process_files_in_folder(folder_path, start_row):
    """
    处理文件夹中的所有txt文件
    :param folder_path: 文件夹路径
    :param start_row: 开始读取的行数
    :return: 包含文件名、湍流度和平均风速的DataFrame
    """
    results = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            times, wind_speeds = read_data_from_file(file_path, start_row)
            turbulence_intensity, mean_wind_speed = calculate_turbulence_intensity(wind_speeds)
            results.append([file_name, turbulence_intensity, mean_wind_speed])
    return pd.DataFrame(results, columns=['文件名', '湍流度', '平均风速'])

def main():
    folder_path = 'E:/desk/tubulence/1227/1227'  # 替换为你的文件夹路径
    start_row = 126

    results_df = process_files_in_folder(folder_path, start_row)
    results_df.to_excel('湍流度结果1227.xlsx', index=False)

if __name__ == "__main__":
    main()
