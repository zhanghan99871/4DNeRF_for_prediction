import re
from matplotlib import pyplot as plt 
import numpy as np

def read_data(path, threshold=100, mode="avg"):
    # Initialize an empty dictionary to store the data
    data_dict = {}
    avg_dict = {}

    # Open the file and process each line
    with open(path, 'r') as file:
        for line in file:
            # Regular expression pattern to extract index and tensor value
            pattern = r"index: (\d+), PSNR: tensor\(\[(.*?)\]\)"

            # Use regex to extract the index and tensor value
            match = re.search(pattern, line)

            if match:
                # Extract the index (as integer) and PSNR value (as float)
                index = int(match.group(1))
                psnr_value = float(match.group(2))

                if index < threshold: 

                    if index in data_dict:
                        data_dict[index].append(psnr_value) 
                    else: 
                        data_dict[index] = [psnr_value]
        if mode == "avg":
            for key, value in data_dict.items():
                avg_dict[key] = sum(data_dict[key]) / len(data_dict[key])
        else: 
            for key, value in data_dict.items():
                avg_dict[key] = data_dict[key][-1]

    return data_dict, avg_dict


def avg_by_index(data_dict):
    avg_list = []
    size = len(data_dict[49])
    num = len(data_dict.keys())


    for i in range(size):
        avg = 0
        for key, value in data_dict.items():
            avg += data_dict[key][i]
        avg_list.append(avg / num)
    return avg_list

def total_avg(avg_dict):
    total = 0
    length = 0
    for key, value in avg_dict.items():
        total += value 
        length += 1
    return total / length
    
def pad_with_zero(refer, to_pad, default=0):
    for key in refer.keys():
        if key not in to_pad:
            to_pad[key] = default
    to_pad = dict(sorted(to_pad.items()))
    return to_pad

def extract_max(data_dict_list):
    result = {}
    for key, value in data_dict_list[0].items():
        max = 0
        for i in range(len(data_dict_list)):
            if max < data_dict_list[i][key]:
                max = data_dict_list[i][key]
        result[key] = max
    return result

def main():
    data_dict, avg_dict = read_data("log_new.txt", threshold=50, mode="avg")
    data_dict1, avg_dict1 = read_data("log_new1.txt", threshold=50, mode="avg")
    data_dict2, avg_dict2 = read_data("log_new2.txt", threshold=50, mode="avg")
    data_dict3, avg_dict3 = read_data("log_new3.txt", threshold=50, mode="avg")

    avg_dict1 = pad_with_zero(avg_dict, avg_dict1)
    avg_dict2 = pad_with_zero(avg_dict, avg_dict2)
    avg_dict3 = pad_with_zero(avg_dict, avg_dict3)

    # avg_list = avg_by_index(data_dict)
    # print(avg_list)
    # plt.plot(avg_list)
    # plt.show()

    # Print the data dictionary

    x = list(avg_dict.keys())
    y = list(avg_dict.values())
    y1 = list(avg_dict1.values())
    y2 = list(avg_dict2.values())
    y3 = list(avg_dict3.values())

    # Set the width for each bar and position offset
    width = 0.2  # Width of each bar
    x_indices = np.arange(len(x))  # X locations for the groups

    # Plotting the grouped bar chart
    plt.figure(figsize=(15, 7))
    plt.bar(x_indices - width,     y,  width/2, label='Train', color='skyblue')
    plt.bar(x_indices - width / 2, y1, width/2, label='Train + 40-41', color='salmon')
    plt.bar(x_indices,             y2, width/2, label='Train + 40-44', color='red')
    plt.bar(x_indices + width / 2, y3, width/2, label='Train + 40-46', color='green')

    # Labeling
    plt.xlabel('Image index')
    plt.ylabel('PSNR')
    plt.title('PSNR for different stages')
    plt.xticks(x_indices, x)  # Set the x-ticks to the keys
    plt.legend()

    # Display
    plt.tight_layout()
    # plt.show()
    plt.savefig("./Tensor4d.png")

def main2():
    data_dict, avg_dict = read_data("log_100000.txt", threshold=50, mode="avg")
    data_dict1, avg_dict1 = read_data("log_new.txt", threshold=50, mode="avg")
    # data_dict2, avg_dict2 = read_data("log_new2.txt", threshold=50, mode="avg")
    # data_dict3, avg_dict3 = read_data("log_new3.txt", threshold=50, mode="avg")

    # avg_dict1 = pad_with_zero(avg_dict, avg_dict1)
    # avg_dict2 = pad_with_zero(avg_dict, avg_dict2)
    # avg_dict3 = pad_with_zero(avg_dict, avg_dict3)
    # max_dict = extract_max([avg_dict, avg_dict1, avg_dict2, avg_dict3])
    # avg = total_avg(avg_dict)
    # print(avg)
    # return 

    # avg_list = avg_by_index(data_dict)
    # print(avg_list)
    # plt.plot(avg_list)
    # plt.show()

    # Print the data dictionary

    x = list(avg_dict.keys())
    y = list(avg_dict.values())
    y1 = list(avg_dict1.values())
    

    # Set the width for each bar and position offset
    width = 0.3  # Width of each bar
    x_indices = np.arange(len(x))  # X locations for the groups

    # Plotting the grouped bar chart
    plt.figure(figsize=(15, 7))
    plt.bar(x_indices,     y,  width/2, label='Train', color='skyblue')
    plt.bar(x_indices + width / 2, y1, width/2, label='Train + 40-41', color='salmon')

    # Labeling
    plt.xlabel('Image index')
    plt.ylabel('PSNR')
    plt.title('PSNR for different images')
    plt.xticks(x_indices, x)  # Set the x-ticks to the keys
    plt.legend()

    # Display
    plt.tight_layout()
    plt.show()
    # plt.savefig("./NeRF-T.png")

if __name__ == "__main__":
    main2()
