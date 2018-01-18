#!/usr/bin/python3
"""
Script for exploring the Tempest vector roms.
"""

import sys
import math

path="136002-138.np3"
if len(sys.argv) > 1:
    path = sys.argv[1]
f = open(path,"rb")
data_raw = f.read()
data = [ data_raw[i ^ 0x01] for i in range(len(data_raw)) ]

sz = (300,300)

glyph_spans = [('A',0,26),
        (' ',0x168,1),
        ('1',0x16c,9),
        ('-',0x236,1),
        ('©',0x23e,1),
        ('/',0x25c,1),
        ]


class PathBuilder:
    def __init__(self):
        self.op = "" 
        self.path = ""
    def add_op(self,op,x,y):
        if self.op != op:
            self.path += op
            self.op = op
        self.path += f"{x} {y} "

def vecproc_run(pc, stack = []):
    pb = PathBuilder()
    cur_op = -1
    while pc < len(data):
        op = (data[pc] >> 5) & 0x07
        if op == 2: # SDRAW
            yy = data[pc] & 0x0f
            if data[pc] & 0x10:
                yy = -(0x10 - yy)
            zz = (data[pc+1] >> 5) & 0x07
            xx = data[pc+1] & 0x0f
            if data[pc+1] & 0x10:
                xx = -(0x10 - xx)
            if zz == 0:
                pb.add_op("m",xx,yy)
            else:
                pb.add_op("l",xx,yy)
            pc += 2
        elif op == 0: #LDRAW
            yy = ((data[pc] & 0x1f) << 8) | data[pc+1]
            xx = ((data[pc+2] & 0x1f) << 8) | data[pc+3]
            if yy & 0x1000:
                yy = -(0x2000 - yy)
            if xx & 0x1000:
                xx = -(0x2000 - xx)
            zz = (data[pc+2] >> 5) & 0x07
            if zz == 0:
                pb.add_op("m",xx,yy)
            else:
                pb.add_op("l",xx,yy)
            pc += 4
        elif op == 1: # HALT
            #print("HALT")
            pc += 2
            break
        elif op == 3: # SCALE/STAT
            #print("SCALE/STAT")
            pc += 2
        elif op == 4: # CENTER
            cr.move_to(sz[0]/2,sz[1]/2)
            pc += 2
        elif op == 5: # JSR
            jaddr = ((data[pc] & 0x1f) << 8) | data[pc+1]
            jaddr = jaddr << 1
            #print("JSR to {:04x}".format(jaddr))
            pc += 2
            break
        elif op == 6: # RTS
            #print("Return")
            pc += 2
            break
        elif op == 7: # JMP
            jaddr = ((data[pc] & 0x1f) << 8) | data[pc+1]
            #print("Jump to {:04x}".format(jaddr))
            pc += 2
            break
    #print("Path '{}'".format(glyph_path))
    #print("Cell size: {} x {}".format(cw,ch))
    return (pb.path.strip(),pc)

import slff
font = slff.SLFF(name="Tempest")
for (ch, idx, count) in glyph_spans:
    pc = idx
    for i in range(count):
        (path, pc) = vecproc_run(pc)
        newch = chr(ord(ch)+i)
        font.add_glyph(newch,path)

font.add_glyph('0',font.glyph_map['O'].path)
font.save(sys.stdout)


