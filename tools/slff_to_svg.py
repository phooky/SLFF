#!/usr/bin/python3

import xml.dom.minidom
import sys
from slff import SLFF, parse_path

if len(sys.argv) < 2:
    print("Missing name of SLFF file.")
    sys.exit(1)

sfont = SLFF(sys.argv[1])
total_bounds = (0,0,0,0)
def add_bounds(b1,b2):
    return (min(b1[0],b2[0]), max(b1[1],b2[1]),
            max(b1[2],b2[2]), min(b1[3],b2[3]))
for glyph in sfont.glyph_map.values():
    total_bounds = add_bounds(total_bounds,glyph.bounds)

em_width = sfont.glyph_map['m'].bounds[2]
space_width = sfont.glyph_map[' '].bounds[2]


impl = xml.dom.minidom.getDOMImplementation('')
doctype = impl.createDocumentType('svg', '-//W3C//DTD SVG 1.1//EN', 'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd')
d = impl.createDocument('http://www.w3.org/2000/svg','svg',doctype)
defs = d.createElement('defs')
f = d.createElement('font')
f.setAttribute('id',sfont.name)
ff = d.createElement('font-face')
ff.setAttribute('font-family',sfont.name)
ff.setAttribute('units-per-em',str(em_width))
ff.setAttribute('ascent',str(total_bounds[1]))
ff.setAttribute('descent',str(total_bounds[3]))
f.appendChild(ff)
mg = d.createElement('missing-glyph')
mg.setAttribute('horiz-adv-x',str(space_width))
f.appendChild(mg)
for (key, glyph) in sfont.glyph_map.items():
    g = d.createElement('glyph')
    g.setAttribute('unicode',key)
    g.setAttribute('horiz-adv-x',str(glyph.bounds[2]))
    g.setAttribute('d',glyph.path)
    f.appendChild(g)
defs.appendChild(f)
d.documentElement.appendChild(defs)
d.writexml(sys.stdout,newl='\n',addindent='  ')
