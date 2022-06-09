from PIL import Image

import math
import os


def open_png_files():
    files_list = os.listdir('.')
    png_list = []
    open_png_list = []

    for one_file in files_list:
        if '.png' in one_file:
            png_list.append(one_file)

    for png_name in png_list:
        open_png_list.append(Image.open(png_name))
    return open_png_list


def cropping_legend(file_list):
    cropping_png = []
    for item in file_list:
        width, height = item.size
        area = (0, 0, width, height-127)
        item = item.crop(area)
        cropping_png.append(item)
    return cropping_png


def create_new_png(png_list, color=(255, 255, 255)):
    global highest
    highest = max(png_list, key=lambda png: png.height).height
    png_width = 0
    little_png_list = png_list

    for n in range(count_server//2):
        try:
            img2 = png_list[n*2+1]
        except IndexError:
            img2 = new_img(0, 0)

        png_width += max(png_list[n*2].width, img2.width)

    dst = new_img(png_width, highest*2)
    return dst


def add_servers_in_new_png(new_png, png_list):
    width_png_all = 0

    for n in range(count_server//2):
        img1 = png_list[n*2]

        try:
            img2 = png_list[n*2+1]
        except IndexError:
            img2 = new_img(0, 0)

        width_png = abs(img1.width - img2.width)
        width1 = width_png_all
        width2 = math.ceil(width_png / 2) + width_png_all
        height1 = math.ceil((highest - img1.height)/2)
        height2 = math.ceil((highest - img2.height) / 2) + highest

        if img1.width > img2.width:
            new_png.paste(img1, (width1, height1))
            new_png.paste(img2, (width2, height2))
        else:
            new_png.paste(img1, (width2, height1))
            new_png.paste(img2, (width1, height2))
        width_png_all += max(img1.width, img2.width)

    new_png.save('New_map_of_servers.jpg')
    return print('done')


def new_img(weight, height):
    return Image.new('RGB', (weight, height), color=(255, 255, 255))


highest = 0

server_list = open_png_files()

count_server = len(server_list)

server_list = cropping_legend(server_list)

new_map = create_new_png(server_list)

add_servers_in_new_png(new_map, server_list)
