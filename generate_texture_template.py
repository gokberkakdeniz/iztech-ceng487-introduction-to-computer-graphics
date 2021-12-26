#!/usr/bin/env python3
# CENG 487 Assignment6 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from sys import argv
from PIL import Image, ImageDraw


if len(argv) != 3:
    print(f'usage: {__file__} INPUT OUTPUT')
    print(f'generate texture template from obj file')
    exit(1)

width = 512
height = 512
uvs = []

img = Image.new('RGB', (width, height), color='black')

with open(argv[1]) as f:
    for line in f.readlines():
        if line.startswith("vt "):
            u, v = tuple(map(float, line.split(" ")[1:]))
            uvs.append((u * width, v * height))
        elif line.startswith("f "):
            try:
                vertices = tuple(map(lambda x: uvs[int(x[1])-1],
                                 filter(lambda x: x[0] % 3 == 1,
                                        enumerate(line[2:].replace(" ", "/").split("/")))))
                pdraw = ImageDraw.Draw(img)
                pdraw.polygon(vertices, fill='white', outline='red')
            except ValueError:
                pass  # no texture
img.save(argv[2])
