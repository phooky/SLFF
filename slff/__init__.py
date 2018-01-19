import xml.dom.minidom

class ParsedOp:
    def __init__(self, path_seg):
        self.code = path_seg[0]
        args = path_seg[1:].strip().split()
        self.args = list(map(float,args))

def parsePath(path):
    ops = []
    path = path.replace(',',' ').strip()
    op = path[0]
    for c in path[1:]:
        if c.isalpha():
            ops.append(ParsedOp(op))
            op = c
        else:
            op += c
    ops.append(ParsedOp(op))
    return ops

def path_bounds(path):
    "Return the bounding box of the path as a tuple (left, top, right, bottom)."
    bounds = (0,0,0,0)
    path = path.replace(","," ").strip()
    cx, cy = 0,0
    def add_to_bounds(bounds,x,y):
        left = min(bounds[0],x)
        top = max(bounds[1],y)
        right = max(bounds[2],x)
        bottom = min(bounds[3],y)
        return (left,top,right,bottom)
    for op in parsePath(path):
        assert op.code.islower()
        args = op.args
        if op.code in 'ml':
            while args:
                cx += args.pop(0)
                cy += args.pop(0)
                bounds = add_to_bounds(bounds, cx, cy)
        elif op.code == 'h':
            cx += args.pop(0)
            bounds = add_to_bounds(bounds, cx, cy)
        elif opcode == 'v':
            cy += args.pop(0)
        assert len(args) == 0
        bounds = add_to_bounds(bounds, cx, cy)
    return bounds



class SLFF:
    class Glyph:
        def __init__(self, path = None, xml = None):
            self.width = None
            if xml:
                self.load_from_xml(xml)
            elif path:
                self.load_from_path(path)

        def load_from_path(self,path):
            self.path = path
            self.bounds = path_bounds(path)

        def load_from_xml(self,element):
            self.path = element.getAttribute("path")
            self.bounds = path_bounds(self.path)

    def __init__(self, source=None, name=None):
        self.name = name
        self.glyph_map = {}
        if source:
            if type(source) == type(""):
                source = open(source,"r")
            self.load(source)
        if name:
            self.name = name
    
    def load(self,xml_src):
        dom = xml.dom.minidom.parse(xml_src)
        slff = dom.firstChild
        assert slff.nodeName == 'slff'
        self.name = slff.getAttribute("name")
        for gnode in slff.getElementsByTagName("glyph"):
            character = gnode.getAttribute("symbol")
            self.glyph_map[character] = self.Glyph(xml = gnode)

    def save(self,xml_dest):
        if type(xml_dest) == type(""):
            xml_dest = open(xml_dest,"w")
        self.build_doc().writexml(xml_dest,newl="\n",addindent="    ")

    def add_glyph(self, character, path, width=None):
        "Manually add a glyph to the font"
        glyph = self.Glyph(path)
        glyph.width = width
        self.glyph_map[character] = glyph

    def build_doc(self):
        doc = xml.dom.minidom.Document()
        slff = doc.createElement('slff')
        slff.setAttribute("name",self.name)
        for (character,glyph) in self.glyph_map.items():
            gnode = doc.createElement('glyph')
            gnode.setAttribute("path",glyph.path)
            gnode.setAttribute("symbol",character)
            slff.appendChild(gnode)
        doc.appendChild(slff)
        return doc

    def string_to_svg_path(self,s):
        return " ".join(map(lambda x:self.glyph_map[x].path,s))

