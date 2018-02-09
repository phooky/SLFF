#!/usr/bin/python3
"""
Extract the Apple 410 font as an SLFF.
"""

import sys
import math

print("TODO: fix endpoint of paths (and ensure space advances properly)")
sys.exit(1)

alpha_ft_start = 0x2569
point_ft_start = 0x3153

f = open("ROM.bin","rb")
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
    return (x, (8 - y))

class PathBuilder:
    def __init__(self):
        self.op = "" 
        self.path = ""
    def add_op(self,op,x,y):
        if self.op != op:
            self.path += op
            self.op = op
        self.path += f"{x} {y} "

def build_char_path(ft, offset):
    d = list(get_char(ft, offset))
    pb = PathBuilder()
    cx, cy = 0, 0
    while d:
        cmd = d.pop(0)
        cn, ca = cmd >> 4, cmd % 16
        for _ in range(ca):
            (x,y) = unpack_coords(d.pop(0))
            dx,dy = x-cx,y-cy
            cx,cy = x,y
            if cn == 0:
                pb.add_op('m',dx,dy)
            elif cn == 2:
                pb.add_op('l',dx,dy)
    return pb.path

import slff
font = slff.SLFF(name="Apple410")
off = 1
while not eot(alpha_ft_start, off):
    p = build_char_path(alpha_ft_start,off)
    c = chr(0x20 + off)
    font.add_glyph(c, p.strip())
    off += 1

font.save(sys.stdout)


