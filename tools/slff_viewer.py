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

sz = (960,600)
chsz = (48,40)
th = 20

loff = 0

def OnDraw(w, cr):
    glyphs = list(font.glyph_map.items())
    cr.set_source_rgb(0, 0, 0)
    cr.set_line_width(2)
    cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cpl = int(w.get_allocated_width()/chsz[0])
    l1 = loff
    l2 = int(w.get_allocated_height()/(chsz[1]+th))
    for i in range(l1*cpl,min(len(glyphs),(l1+l2)*cpl)):
        (ch, gl) = glyphs[i]
        x = (i%cpl)
        y = math.floor(i/cpl) - loff
        cr.save()
        cr.translate(x*chsz[0],(y+1)*(chsz[1]+th))
        # draw name
        cr.move_to(0,chsz[1]-10)
        cr.set_source_rgb(0, 0, 0)
        cr.show_text(ch)
        cr.stroke()
        cr.set_source_rgb(1.0,0.5,0.5)
        cr.set_line_width(1)
        cr.move_to(0,0)
        cr.line_to(0,10)
        cr.stroke()
        cr.set_source_rgb(0, 0, 0)
        cr.set_line_width(2)
        cr.scale(1.,-1.)
        cr.move_to(0,0)
        ops = parse_path(gl.path)
        for op in ops:
            if op.code == 'm':
                cr.rel_move_to(op.args[0],op.args[1])
            elif op.code == 'l':
                while op.args:
                    cr.rel_line_to(op.args.pop(0), op.args.pop(0))
        p = cr.get_current_point()
        cr.stroke()
        cr.set_source_rgb(0.5,0.5,1.0)
        cr.set_line_width(1)
        cr.move_to(p[0],0)
        cr.line_to(p[0],-10)
        cr.stroke()
        cr.restore()

def OnKey(w, event):
    global loff
    n = Gdk.keyval_name(event.keyval)
    if n == 'q':
        print("QUIT")
        Gtk.main_quit()
    elif n == 'Down':
        loff += 1
        w.queue_draw()
    elif n == 'Up':
        if loff > 0:
            loff -= 1
            w.queue_draw()

w = Gtk.Window()
w.set_default_size(sz[0],sz[1])
a = Gtk.DrawingArea()
w.add(a)

w.connect('destroy', Gtk.main_quit)
a.connect('draw', OnDraw)
w.connect('key_press_event', OnKey)

w.show_all()

Gtk.main()



