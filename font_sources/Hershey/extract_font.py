#!/usr/bin/python3
"""
Script for exploring the Tempest vector roms.
"""

import sys
import math
import os

from slff import SLFF, PathBuilder

def hershey_to_glyph(hstr):
    "Convert a Hershey code to a character/path pair."
    def hconv(c):
        return ord(c) - ord('R')
    num = int(hstr[0:5])
    vcnt = int(hstr[5:8])
    lhs = hconv(hstr[8])
    rhs = hconv(hstr[9])
    vertices = hstr[10:]
    pendown = False
    pb = PathBuilder()
    for i in range(0,len(vertices),2):
        vertex = vertices[i:i+2]
        if vertex == " R":
            pendown = False
        else:
            x = hconv(vertex[0])
            y = -hconv(vertex[1])
            if pendown:
                pb.line_to(x,y)
            else:
                pb.move_to(x,y)
                pendown = True
    pb.move_to(rhs,0)
    if num == 12345:
        char = None
    else:
        char = chr(num)
    return (char, str(pb))

def convert_hershey(path, name=None):
    if not name:
        name = os.path.splitext(os.path.basename(path))[0]
    font = SLFF(name=name)
    i = 32
    for line in open(path,"r").readlines():
        line = line.rstrip()
        (c, p) = hershey_to_glyph(line)
        if not c:
            c = chr(i)
            i += 1
        font.add_glyph(c,p)
    return font

if len(sys.argv) > 1:
    path = sys.argv[1]
    convert_hershey(path).save(sys.stdout)

