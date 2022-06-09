from PIL import Image
from typing import List, Type

import math
import os


def open_png_files() -> List[Type['Image']]:
    files_list = os.listdir('.')
    png_list = []
    open_png_list = []

    for one_file in files_list:
        if '.png' in one_file:
            png_list.append(one_file)

    for png_name in png_list:
        open_png_list.append(Image.open(png_name))
    return open_png_list


def cropping_legend(file_list: List[Type['Image']]) -> List[Type['Image']]:
    cropping_png = []

    for item in file_list:
        width, height = item.size
        area = (0, 0, width, height-127)
        item = item.crop(area)
        cropping_png.append(item)
    return cropping_png


def create_new_png(png_list: List[Type['Image']], color=(255, 255, 255)) -> Image:
    global highest
    highest = max(png_list, key=lambda png: png.height).height
    png_width = 0
    little_png_list = png_list

    for n in range(count_server // 2 + count_server % 2):
        try:
            img2 = png_list[n*2+1]
        except IndexError:
            img2 = new_img(0, 0)

        png_width += max(png_list[n*2].width, img2.width)

    dst = new_img(png_width, highest*2)
    return dst


def add_servers_in_new_png(new_png: Image, png_list: List[Type['Image']]) -> Image:
    width_png_all = 0

    for n in range(count_server // 2 + count_server % 2):
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

    return new_png.save('New_map_of_servers.jpg')


def new_img(weight: int, height: int) -> Image:
    return Image.new('RGB', (weight, height), color=(255, 255, 255))


if __name__ == '__main__':
    highest: int = 0
    server_list: List[Type['Image']] = open_png_files()
    count_server: int = len(server_list)
    server_list: List[Type['Image']] = cropping_legend(server_list)
    new_map: Image = create_new_png(server_list)
    add_servers_in_new_png(new_map, server_list)
