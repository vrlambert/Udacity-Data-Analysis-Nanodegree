import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

filename = 'rhode-island-latest.osm'

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Highway",
            "Way", "Broadway", "Circle", "Pike"]

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit(osmfile):
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osmfile, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def update_street_name(name):

    mapping = {
                "Ave":"Avenue",
                "Ave.":"Avenue",
                "Blvd":"Boulevard",
                "Ct":"Court",
                "Ct.": "Court",
                "Dr":"Drive",
                "Dr.":"Drive",
                "Hwy":"Highway",
                "HIGHWAY":"Highway",
                "Ln":"Lane",
                "PIKE":"Pike",
                "Rd":"Road",
                "Rd.": "Road",
                "Sq.":"Square",
                "St": "Street",
                "St.": "Street",
                "Wy":"Way"
                }

    street_type = re.search(street_type_re, name).group()
    if street_type in mapping:
        name = name.replace(street_type, mapping[street_type], 1)

    return name

def test():
    street_types = audit(filename)
    pprint.pprint(dict(street_types))

if __name__ == '__main__':
    test()
