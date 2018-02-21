#!/usr/bin/python3
"""
Script for exploring the Tempest vector roms.
"""

import sys
import math
import os

from slff import SLFF, PathBuilder

# Convenient arrays
lc = map(chr,range(ord('a'),ord('z')+1))
uc = map(chr,range(ord('A'),ord('Z')+1))
num = map(chr,range(ord('0'),ord('9')+1))
ugr = list('ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩ')
lgr = list('αβγδεζηϑικλμνξοπρστυφχψω')

def zadd(d,keys,values):
    d.update(dict(zip(keys,values)))

# Set up mappings for each Hershey font
small_font = {}
zadd(small_font,uc,range(0x1,0x1b))
zadd(small_font,num,range(0xc8,0xd2))
zadd(small_font,ugr,range(0x1b,0x33))
zadd(small_font,list('.,:;!?\'"°$/()|-+=×*·‘’→ #&⌑'),range(0xd2,0xeb))
small_font[' '] = 0xc7

sans_font = {}
zadd(sans_font,uc,range(0x1f5,0x20f))
zadd(sans_font,ugr,range(0x20f,0x227))
zadd(sans_font,lgr,range(0x273,0x28b))
zadd(sans_font,lc,range(0x259,0x273))
zadd(sans_font,num,range(0x2bc,0x2c6))
sans_font[' '] = 0x2bb
sans_font['∇'] = 0x247
sans_font['ϵ'] = 0x2ac
sans_font['θ'] = 0x2ad
sans_font['ϕ'] = 0x2ae
sans_font['ϛ'] = 0x2af
sans_font['∂'] = 0x2ab
zadd(sans_font,list('.,:;!?\'"°$/()|-+=×*·‘’→ #&⌑'),range(0x2c6,0x2e0))
# glyph at 0x2a5 is unrecognized.

cursive_font = {}

eng_mappings = {
        'hershey_small':small_font,
        'hershey_sans':sans_font,
        }

# Prepare mappings for astronomy font
a = list(map(chr,range(32,128)))
a[1] = '♓'
a[3:8] = ['☉','☿','♀','⊕','♂']
a[10] = '♃'
a[11] = '♄'
a[13] = '⛢'
a[15] = '♆'
a[26:33] = ['♇','☽','☄ ','*','☊','☋,','♈']
a[59:65] = ['♉','\\', '♊','♋','♌','♍']
a[91:96] = ['♏','♐','♑','♒','~']

def hershey_to_glyph(hstr):
    "Convert a Hershey code to a character/path pair."
    def hconv(c):
        return ord(c) - ord('R')
    num = int(hstr[0:5])
    vcnt = int(hstr[5:8])
    # we are going to use the LHS information
    # to shift the X origin
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
            x = hconv(vertex[0]) - lhs
            y = -hconv(vertex[1])
            if pendown:
                pb.line_to(x,y)
            else:
                pb.move_to(x,y)
                pendown = True
    pb.move_to(rhs - lhs,0)
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
        font.add_glyph(hex(ord(c)),p)
    return font

if len(sys.argv) > 2:
    path = sys.argv[1]
    outpath = sys.argv[2]
    convert_hershey(path).save(open(outpath,"w"))

