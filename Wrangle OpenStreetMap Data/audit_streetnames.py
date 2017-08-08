import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

filename = 'small_sample.osm'

# regular expression that returns the final word or abbreviation of a string
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# List of normal street types to ignore when looking for shortened ones
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place",
            "Square", "Lane", "Road", "Trail", "Parkway", "Commons", "Highway",
            "Way", "Broadway", "Circle", "Pike"]

# mapping used to correct street name abbreviations
mapping = {
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "Blvd": "Boulevard",
            "Ct": "Court",
            "Ct.": "Court",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Hwy": "Highway",
            "HIGHWAY": "Highway",
            "Ln": "Lane",
            "PIKE": "Pike",
            "Rd": "Road",
            "Rd.": "Road",
            "Sq.": "Square",
            "St": "Street",
            "St.": "Street",
            "Wy": "Way"
}

def audit_street_type(street_types, street_name):
    """
    Takes in a dictionary of street types and a street name. Checks for an
    abnormal street name and adds it to the dictionary if it is abnormal
    """
    m = street_type_re.search(street_name) # extract the street name

    # If you find something, add it to the dictionary
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    """
    Takes in an element and returns true if the key corresponds to a street
    The key should be 'addr:street' otherwise returns false
    """
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    """
    Takes in an osm file and returns a dictionary with shortened or abnormal
    street names as the keys and the full street names as the values
    """

    # initialize a set default dict to hold the street names
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osmfile, events=("start",)):

        # only look at nodes and ways
        if elem.tag == "node" or elem.tag == "way":

            # Iterate through the tags until you find a street name
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    # Check the street type and save it if necessary
                    audit_street_type(street_types, tag.attrib['v'])
    return street_types

def update_street_name(name, mapping):
    """
    Takes in an abnormal street name and returns a corrected one
    """

    # Extract the street type and correct if possible
    street_type = re.search(street_type_re, name).group()
    if street_type in mapping:
        name = name.replace(street_type, mapping[street_type], 1)

    return name



def test():
    street_types = audit(filename)
    pprint.pprint(dict(street_types))


if __name__ == '__main__':
    test()
