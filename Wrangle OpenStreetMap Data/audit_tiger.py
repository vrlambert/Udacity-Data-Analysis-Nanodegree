import xml.etree.cElementTree as ET
import pprint
import re
import audit_streetnames
from collections import defaultdict

filename = 'small_sample.osm'

def is_tiger_name(elem):
    """
    Takes in a tag and returns true if it is a tiger name base, otherwise false
    """
    return (elem.attrib['k'] == 'tiger:name_base')

def is_tiger_type(elem):
    """
    Takes in a tag and returns true if it is a tiger name type, otherwise false
    """
    return (elem.attrib['k'] == 'tiger:name_type')

def is_name(elem):
    """
    Checks if it is the way name element
    """
    return (elem.attrib['k'] == 'name')

def audit(osmfile):
    """
    Takes in an osm file and returns a list of tiger name/tiger type pairs
    for ways that have a tiger type but no updated name
    """

    # initialize a set default dict to hold the street names
    tiger_names = []
    for event, elem in ET.iterparse(osmfile, events=("start",)):
        has_name = False
        has_tiger = False
        # only look at nodes and ways
        if elem.tag == "node" or elem.tag == "way":

            # Iterate through the tags until you find a street or tiger name
            for tag in elem.iter("tag"):
                if is_name(tag):
                    # Check if it has a street
                    has_name = True
                if is_tiger_type(tag):
                    # Check if it has a tiger street type
                    tiger_type = tag.get('v')
                    has_tiger = True
                if is_tiger_name(tag):
                    tiger_name = tag.get('v')

            if has_tiger is True and has_name is False:
                tiger_names.append(tiger_name + '/' + tiger_type)

    return tiger_names

def update_tiger(parent_id, tiger_name, tiger_type):
    """
    Function takes in a parent id, tiger name, and tiger type and returns
    a dictionary with the appropriate name dictionary. Should only be called
    when the tiger name has not yet been compiled.
    """
    child_dict = {'id':parent_id
                  'type':'regular'
                  'key':'name'}
    street = tiger_name + tiger_type
    street_final = audit_streetnames.update_street_name(street)
    child_dict['value'] = street_final
    return child_dict

def main(output = False):
    names = audit(filename)
    if output is True:
        pprint.pprint(names)

    print 'There are {0} unformatted tiger streets'.format(len(names))

if __name__ == '__main__':
    main(output = True)
