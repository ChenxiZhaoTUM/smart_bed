import os
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime

folder_path = "dataset"
file_names = os.listdir(folder_path)
np.set_printoptions(threshold=np.inf)


# average the time by second
def parse_time_string(time_string):
    return datetime.strptime(time_string, "%H:%M:%S.%f")


def format_time_string(time):
    return time.strftime("%H:%M:%S")


def average_by_sec(time_arr, value_arr):
    time_objs = [parse_time_string(time_str) for time_str in time_arr]
    time_objs = [format_time_string(time_obj) for time_obj in time_objs]

    # create dictionary to save time and corresponding values
    sum_dict = {}
    count_dict = {}
    new_time_arr = []

    for i in range(len(time_objs)):
        new_time_str = time_objs[i]

        if new_time_str in sum_dict:
            sum_dict[new_time_str] += value_arr[i]
            count_dict[new_time_str] += 1
        else:
            sum_dict[new_time_str] = value_arr[i]
            # print(type(value_arr[i]))  # test code
            count_dict[new_time_str] = 1
            new_time_arr.append(new_time_str)

    avg_value_arr = [sum_dict[new_time_str] / count_dict[new_time_str] for new_time_str in new_time_arr]
    return new_time_arr, avg_value_arr


def plot_3D(new_time_arr, avg_value_arr):
    # Convert time strings to datetime objects
    timestamps = [datetime.strptime(ts, '%H:%M:%S') for ts in new_time_arr]
    # Convert datetime objects to numeric values
    numeric_timestamps = mdates.date2num(timestamps)

    # plot
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    group_index = list(range(1, 21))
    for i, index in enumerate(group_index):
        ax.plot3D(numeric_timestamps, [index] * len(numeric_timestamps), [value[i] for value in avg_value_arr])

    ax.set_xlabel('Time')
    ax.set_ylabel('Index')
    ax.set_zlabel('Value')
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M:%S'))

    plt.show()


for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    if file_path.endswith(".TXT"):
        with open(file_path, 'r') as file:
            lines = file.readlines()

            time_arr = []
            value_arr = []

            for line in lines:
                line = line.strip()

                # ignore the line not including []
                if "[" not in line and "]" not in line:
                    continue

                time_start = line.find("[")
                time_end = line.find("]")

                value_str = line[time_end + 1:]
                value_str = re.sub(r'[^a-zA-Z0-9\s]', '', value_str)
                values = value_str.split()

                if len(values) != 20:
                    continue

                time_str = line[time_start + 1:time_end]
                time_str = re.sub(r'[^a-zA-Z0-9:.]', '', time_str)
                time_arr.append(time_str)

                value_per_time = [int(value, 16) for value in values]
                value_arr.append(value_per_time)

            value_arr = np.array(value_arr)


            # print(time_arr)  # test code
            # print(value_arr)  # test code
            # print(len(value_arr))  # test code

            ######## plot dynamic or static pictures #######
            def dynamic_pic():
                fig, ax = plt.subplots()
                x = np.arange(1, 21)
                bars = ax.bar(x, np.zeros(20))

                def update(frame):
                    y = value_arr[frame]  # get the values for the current frame
                    for i, bar in enumerate(bars):
                        bar.set_height(y[i])

                ani = animation.FuncAnimation(fig, update, frames=len(value_arr), interval=500)
                plt.xticks(x)
                plt.ylim(0, 250)
                plt.show()


            def static_pic(index):
                x = np.arange(1, 21)
                y = value_arr[index]
                plt.bar(x, y)
                plt.xticks(x)
                plt.ylim(0, 250)
                plt.show()


            # dynamic_pic()
            # static_pic(20)

            ######## do time average #######
            new_time_arr, avg_value_arr = average_by_sec(time_arr, value_arr)
            # print(new_time_arr)
            plot_3D(new_time_arr, avg_value_arr)
