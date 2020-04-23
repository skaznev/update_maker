import xml.parsers.expat as expat

def StartElementHandler(name, attrs):
    print('Start element:', name, attrs)
def EndElementHandler(name):
    print('End element:', name)
def CharacterDataHandler(data):
    print('Character data:', repr(data))

parser = expat.ParserCreate()

parser.StartElementHandler = StartElementHandler
parser.EndElementHandler = EndElementHandler
parser.CharacterDataHandler = CharacterDataHandler
fajl = "Путь к файлу"
fl = open(file = fajl, mode = 'rb' )
parser.ParseFile(fl)
# parser.Parse("""<?xml version="1.0"?>
# <parent id="top"><child1 name="paul">Text goes here</child1>
# <child2 name="fred">More text</child2>
# </parent>""", 1)