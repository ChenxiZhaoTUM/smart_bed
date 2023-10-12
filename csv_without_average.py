import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import colors
from scipy.ndimage import correlate

folder_path = "dataset"
file_names = os.listdir(folder_path)


def add_filter(value_arr):
    # filter operator
    h = np.ones((3, 3)) / 9.0
    f = np.ones((7, 7)) / 49.0
    filter = correlate(value_arr, h, mode='nearest')

    delta_value_arr = np.copy(value_arr)
    delta_value_arr[value_arr < 0.5] = 0
    delta_filter = np.copy(filter)
    delta_filter[delta_value_arr > 0] = delta_value_arr[delta_value_arr > 0]
    delta_filter[delta_value_arr == 0] *= 1.2

    def update(frame):
        image0 = np.reshape(value_arr[frame], (32, 64))
        image1 = np.reshape(filter[frame], (32, 64))
        image2 = np.reshape(delta_filter[frame], (32, 64))
        image3 = np.reshape(delta_filter[frame], (32, 64))
        im0.set_array(image0)
        im1.set_array(image1)
        im2.set_array(image2)
        im3.set_array(image3)

    fig, axs = plt.subplots(1, 5, figsize=(12, 4))

    for ax in axs:
        ax.set_aspect('equal', 'box')
        ax.axis('off')

    image0 = np.reshape(value_arr[0], (32, 64))
    image1 = np.reshape(filter[0], (32, 64))
    image2 = np.reshape(delta_filter[0], (32, 64))
    image3 = np.reshape(delta_filter[0], (32, 64))

    im0 = axs[0].imshow(image0, cmap='jet', norm=colors.Normalize(vmin=0, vmax=1))
    axs[0].set_title('original data')

    im1 = axs[1].imshow(image1, cmap='jet', norm=colors.Normalize(vmin=0, vmax=1))
    axs[1].set_title('original data filter')

    im2 = axs[2].imshow(image2, cmap='jet', norm=colors.Normalize(vmin=0, vmax=1))
    axs[2].set_title('recovery peak data')

    im3 = axs[3].imshow(image3, cmap='jet', interpolation='bilinear', norm=colors.Normalize(vmin=0, vmax=1))
    axs[3].set_title('interpolated data')

    cax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cbar = plt.colorbar(im0, cax=cax)

    plt.subplots_adjust(wspace=0.05)

    ani = animation.FuncAnimation(fig, update, frames=len(value_arr), interval=500, blit=False)

    plt.show()


def dynamic_pic(value_arr):
    def update(frame):
        image = np.reshape(value_arr[frame], (32, 64))
        im.set_array(image)

    fig, ax = plt.subplots()

    ax.set_aspect('equal', 'box')
    image = np.reshape(value_arr[0], (32, 64))
    im = ax.imshow(image, cmap='jet', interpolation='bilinear', norm=colors.Normalize(vmin=0, vmax=1))
    ax.axis('off')

    ani = animation.FuncAnimation(fig, update, frames=len(value_arr), interval=500, blit=False)
    cbar = plt.colorbar(im)

    plt.show()


def static_pic(value_arr, index):
    fig, ax = plt.subplots()

    ax.set_aspect('equal', 'box')
    image = np.reshape(value_arr[index], (32, 64))
    im = ax.imshow(image, cmap='jet', interpolation='bicubic', norm=colors.Normalize(vmin=0, vmax=1))
    ax.axis('off')
    cbar = plt.colorbar(im)

    plt.show()


def pressure_norm(value_arr):
    value_arr = np.array(value_arr)

    min_value = np.min(value_arr)
    max_value = np.max(value_arr)

    value_arr = (value_arr - min_value) / (max_value - min_value)
    return value_arr


for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    if file_path.endswith(".CSV"):
        with open(file_path, 'r') as file:

            time_arr = []
            value_arr = []

            lines = file.readlines()[1:]

            for line in lines:
                line = line.strip()
                line = line.split(',')

                time_str = line[0].split(' ')[1]
                time_arr.append(time_str)

                value_str = line[1:]
                value_per_time = [int(value) for value in value_str]
                value_arr.append(value_per_time)

            value_arr = pressure_norm(value_arr)
            # print(time_arr)  # test code

            # dynamic_pic(value_arr)
            # static_pic(value_arr, 50)
            add_filter(value_arr)

            # np.set_printoptions(threshold=np.inf)  # test code
            # print(value_arr[50])
