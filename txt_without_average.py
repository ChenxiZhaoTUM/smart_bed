import os
import re
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

folder_path = "dataset"
file_names = os.listdir(folder_path)

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

            # print(time_arr)  # test code
            # print(value_arr)  # test code
            # print(len(value_arr))  # test code

            # plot the dynamic picture
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


            dynamic_pic()
            # static_pic(20)
