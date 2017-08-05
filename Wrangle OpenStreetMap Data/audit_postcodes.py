import xml.etree.cElementTree as ET
import pprint
from collections import defaultdict

filename = 'rhode-island-latest.osm'

def is_postcode(elem):
    """
    Checks if the element's key is a poscode, 'addr:postcode'
    """
    return (elem.attrib['k'] == "addr:postcode")

def audit(osmfile):
    """
    Checks each element in a osm file for postcodes and returns a
    dictionary of  potentially problematic postcodes
    """
    postcodes = defaultdict(int)

    # Iterate through all start elements of the file
    for event, elem in ET.iterparse(osmfile, events=("start",)):

        # if it's a node or way, check for a postcode tag and increment
        # the count
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_postcode(tag):
                    postcodes[tag.attrib['v']] += 1
    return postcodes

def update_postcodes(code):
    """
    Takes a postcode and updates it to a valid 5 digit postcode
    """
    # If the postcode is the proper length, return it
    if len(code) == 5:
        return code
    # Otherwise, if the postcode has a dash only return the first five digits
    elif '-' in code:
        return code[:5]
    # If the postcode does not fall in to these catigories, return None
    else:
        return None

def test():
    post_codes = audit(filename)
    pprint.pprint(dict(post_codes))
    print 'Length:', len(post_codes)

if __name__ == '__main__':
    test()
