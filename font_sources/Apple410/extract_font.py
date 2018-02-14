#!/usr/bin/python3
"""
Extract the Apple 410 font as an SLFF.
"""

import sys
import math
import os

from slff import SLFF, PathBuilder

alpha_ft_start = 0x2569
point_ft_start = 0x3153

directory = os.path.dirname(__file__)
path = os.path.join(directory, "ROM.bin")
f = open(path, "rb")
data = f.read()


def eot(ft, off):
    "Returns true if the offset is at the end of the table."
    # Presumes that every table terminates in 0xff
    return data[ft + off*2] == 0xff

def get_char(ft,off):
    achar = chr(off+0x20)
    o1 = ft + (off*2)
    o2 = (data[o1+1]*256) + data[o1]
    o3 = o2
    while data[o3] != 0xff:
        o3 += 1
    return data[o2:o3]    

def unpack_byte(b):
    "convert two 4-bit signed packed numbers to a tuple"
    # this packing is... unusual.
    x = b >> 4
    y = b % 16
    if y > 8: # now the weird
        x -= 1
        y -= 16
    return (x,y)

# H:W for a char is 3:2
def unpack_coords(b):
    "convert two 4-bit signed packed numbers to cairo coordinates"
    (x,y) = unpack_byte(b)
    return (x, y)


def build_char_path(ft, offset):
    d = list(get_char(ft, offset))
    pb = PathBuilder()
    x,y = 0,0
    while d:
        cmd = d.pop(0)
        cn, ca = cmd >> 4, cmd % 16
        for _ in range(ca):
            (x,y) = unpack_coords(d.pop(0))
            if cn == 0:
                pb.move_to(x,y)
            elif cn == 2:
                pb.line_to(x,y)
    if (x, y) != (10,0):
        pb.move_to(10,0)
    return str(pb)

font = SLFF(name="Apple410")
off = 0
while not eot(alpha_ft_start, off):
    p = build_char_path(alpha_ft_start,off)
    c = chr(0x20 + off)
    font.add_glyph(c, p.strip())
    off += 1

font.save(sys.stdout)


