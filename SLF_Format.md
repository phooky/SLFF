# A Single-Line Font Format

SLFF is a simple format for representing single-line fonts, as used by CNC
machines, plotters, vector displays, and similar devices. It's a simple XML
format based on SVG's path descriptors. It's intended to be an intermediate
format from which other forms can be generated (DXF, HPGL, TTF, etc).

## Coordinate system

The Y+ axis is oriented towards the _top_ of the page.
The X+ axis is oriented towards the _right_ of the page.

All glyphs are described relative to an origin 0,0 which is considered the _start position_
of the glyph. Subsequent glyphs are drawn starting at the point at which the previous
glyph left the pen. We can interpret the origin as follows:

* Y=0 at the baseline of the font (if the font has a "baseline"; otherwise, the bottom of
  the character cell).
* X=0 at the left edge of the character cell (in a font that is drawn left-to-right; in fonts
  that are drawn right-to-left, X=0 is at the _right_ edge of the character cell).

Keep in mind that although the path format is based on the SVG path format, the Y axis is
inverted from what you'd expect in a standard SVG path.

## Units

The system of units used should be that of the original source material. Some optional
attributes ("line-height", "cell-height") can be consulted to help the client decide how
to scale the font.

## Drawing the glyph

Each glyph contains a path attribute which describes how the glyph should be drawn. 
This sequence of moves and draws should approximate the source material as closely as possible.
At the end of the glyph, a move command should be added to locate the pen at the starting point
for the next glyph (if needed).

The 'space' character should always be implemented and move the pen to the starting position
for the next character after the space.

### The path attribute

SLFF paths are defined as a the subset of SVG path commands that correspond to relative, rather
than absolute, motion. Most SLFF paths will consist entirely of the `m` (relative move to) and
`l` (relative line to) commands.

* The top-level slf-font object should define "cell-width" and "cell-height" in
  in terms of native units. These should describe the maximum width and height of
  ordinary character data. If the baseline is not at the bottom of the cells, the
  "descent" attribute should indicate how many native units the baseline is above
  the bottom of the cell.
  * In general it should be possible to work out the baseline by examining the extents
    of a few basic characters.
  * Most of these characteristics should be auto-extracted, in fact.

## Quick example

```<slf-font version="1.0" name="Tempest" encoding="utf-8" cell-width="12" cell-height="12">
<glyph symbol="A" path="l0 8 4 4 4 -4 0 -8 m-8 4 l8 0 m4 -4" />
<glyph symbol="B" path="l0 12 6 0 2 -2 0 -2 -2 -2 -6 0 m6 0 l2 -2 0 -2 -2 -2 -6 0 m12 0" />
<glyph symbol="C" path="l0 12 8 0 m-8 -12 l8 0 m4 0" />
<glyph symbol="D" path="l0 12 4 0 4 -4 0 -4 -4 -4 -4 0 m12 0" />
<glyph symbol="E" path="l0 12 8 0 m-2 -6 l-6 0 m0 -6 l8 0 m4 0" />
<glyph symbol="F" path="l0 12 8 0 m-2 -6 l-6 0 m0 -6 12 0" />
</slf-font>```

