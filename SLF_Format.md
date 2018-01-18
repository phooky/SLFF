# The Single-Line Font Format

SLFF is a simple format for representing single-line fonts, as used by CNC
machines, plotters, vector displays, and similar devices. It's a simple XML
format based on SVG's path descriptors. It's intended to be an intermediate
format from which other forms can be generated (DXF, HPGL, TTF, etc).

* Coordinate system is similar to TTF, plotters, etc: Y+ is up.
* Y=0 is the baseline.
* X=0 is the left edge of the character cell.
* Units should be the native unit of the font source. Do not scale if possible.
* Paths are in SVG Path format. All paths should be in relative format. At the 
  end of the path, the current position should be set to the start of the next
  character.
* The top-level slf-font object should define "cell-width" and "cell-height" in
  in terms of native units. These should describe the maximum width and height of
  ordinary character data. If the baseline is not at the bottom of the cells, the
  "descent" attribute should indicate how many native units the baseline is above
  the bottom of the cell.
  * In general it should be possible to work out the baseline by examining the extents
    of a few basic characters.
  * Most of these characteristics should be auto-extracted, in fact.
* Individual characters can define their own "cell-width" for variable-width fonts.
## Quick example

```<slf-font version="1.0" name="Tempest" encoding="utf-8" cell-width="12" cell-height="12">
<glyph symbol="A" path="l0 8 4 4 4 -4 0 -8 m-8 4 l8 0 m4 -4" />
<glyph symbol="B" path="l0 12 6 0 2 -2 0 -2 -2 -2 -6 0 m6 0 l2 -2 0 -2 -2 -2 -6 0 m12 0" />
<glyph symbol="C" path="l0 12 8 0 m-8 -12 l8 0 m4 0" />
<glyph symbol="D" path="l0 12 4 0 4 -4 0 -4 -4 -4 -4 0 m12 0" />
<glyph symbol="E" path="l0 12 8 0 m-2 -6 l-6 0 m0 -6 l8 0 m4 0" />
<glyph symbol="F" path="l0 12 8 0 m-2 -6 l-6 0 m0 -6 12 0" />
</slf-font>```

