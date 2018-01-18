import xml.dom.minidom

def path_bounds(path):
    "Return the bounding box of the glyph as a tuple (left, top, right, bottom)."
    bounds = (0,0,0,0)
    path = path.replace(","," ").strip()
    cx, cy = 0,0
    def get_op(path):
        opcode = path[0]
        idx = 1
        while idx < len(path) and not path[idx].isalpha():
            idx += 1
        args = list(map(float,path[1:idx].strip().split()))
        return (opcode, args, path[idx:])
    def add_to_bounds(bounds,x,y):
        left = min(bounds[0],x)
        top = max(bounds[1],y)
        right = max(bounds[2],x)
        bottom = min(bounds[3],y)
        return (left,top,right,bottom)
    while path:
        opcode, args, path = get_op(path)
        if opcode in 'ml':
            while args:
                cx += args.pop(0)
                cy += args.pop(0)
                bounds = add_to_bounds(bounds, cx, cy)
        elif opcode in 'ML':
            while args:
                cx = args.pop(0)
                cy = args.pop(0)
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
            self.path = element.attributes["path"].value
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
        self.name = slff.attributes["name"].value
        for gnode in slff.getElementsByTagName("glyph"):
            character = gnode.attributes["symbol"].value
            self.glyph_map[character] = self.Glyph(xml = gnode)

    def add_glyph(self, character, path, width=None):
        "Manually add a glyph to the font"
        glyph = self.Glyph(path)
        glyph.width = width
        self.glyph_map[character] = glyph


