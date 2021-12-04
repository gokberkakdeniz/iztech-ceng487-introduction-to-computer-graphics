# CENG 487 Assignment4 by
# Gokberk Akdeniz
# StudentId:250201041
# 12 2021

from functools import reduce
from typing import List
from OpenGL.GLUT import glutBitmapString
from OpenGL.GLUT.fonts import GLUT_BITMAP_HELVETICA_18, GLUT_BITMAP_9_BY_15


def create_ascii_table_header(text: str) -> bytes:
    text = (text+"\n").upper().encode("utf-8")

    def draw():
        glutBitmapString(GLUT_BITMAP_HELVETICA_18, text)

    return draw


def create_ascii_table(table: List[List[str]]) -> bytes:
    max_lengths = tuple(
        reduce(
            lambda curr, acc: tuple(map(max, zip(curr, acc))),
            map(lambda row: map(lambda cell: len(cell), row), table),
        )
    )

    def justify(x):
        index, cell = x

        if index+1 == len(max_lengths):
            return cell

        return cell.ljust(max_lengths[index+1])

    justified = list(
        map(
            lambda row: " ".join(map(
                justify,
                enumerate(row, 0)
            )),
            table
        )
    )

    justified.append("\n")

    text = "\n".join(justified).encode("utf-8")

    def draw():
        glutBitmapString(GLUT_BITMAP_9_BY_15, text)

    return draw
