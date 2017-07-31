import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

filename = 'rhode-island-latest.osm'

def is_postcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    postcodes = defaultdict(int)

    for event, elem in ET.iterparse(osmfile, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    postcodes[tag.attrib['v']] += 1
    return postcodes

def update_postcodes(code):
    if len(code) == 5:
        return code
    elif '-' in code:
        return code[:5]
    else:
        return None

def test():
    post_codes = audit(filename)
    pprint.pprint(dict(post_codes))
    print 'Length:', len(post_codes)

if __name__ == '__main__':
    test()
