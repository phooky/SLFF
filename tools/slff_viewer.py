#!/usr/bin/python3
"""
A tool for quickly verifying an SLFF font.
"""

import sys
import math

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk
import cairo

from slff import SLFF, parse_path

if len(sys.argv) < 2:
    print("Missing name of SLFF file.")
    sys.exit(1)

font = SLFF(sys.argv[1])

sz = (600,500)
chsz = (20,20)
def OnDraw(w, cr):
    global slff
    glyphs = list(font.glyph_map.items())
    glyphs.sort()
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(2)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(len(glyphs)):
        (ch, gl) = glyphs[i]
        cpl = sz[0]/chsz[0]
        x = (i%cpl)
        y = math.floor(i/cpl)
        cr.save()
        cr.translate(x*chsz[0],(y+1)*chsz[1])
        cr.scale(1.,-1.)
        cr.move_to(0,0)
        ops = parse_path(gl.path)
        for op in ops:
            if op.code == 'm':
                cr.rel_move_to(op.args[0],op.args[1])
            elif op.code == 'l':
                while op.args:
                    cr.rel_line_to(op.args.pop(0), op.args.pop(0))
        cr.stroke()
        cr.restore()

def OnKey(w, event):
    n = Gdk.keyval_name(event.keyval)
    if n == 'q':
        print("QUIT")
        Gtk.main_quit()

w = Gtk.Window()
w.set_default_size(sz[0],sz[1])
a = Gtk.DrawingArea()
w.add(a)

w.connect('destroy', Gtk.main_quit)
a.connect('draw', OnDraw)
w.connect('key_press_event', OnKey)

w.show_all()

Gtk.main()



