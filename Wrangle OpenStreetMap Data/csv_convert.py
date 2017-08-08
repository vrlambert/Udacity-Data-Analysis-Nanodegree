#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import codecs
import pprint
import re
import xml.etree.cElementTree as ET
import cerberus

# The schema file is used to double check our exported csv
import schema

# Import the audit scripts with useful update functions
import audit_streetnames
import audit_postcodes
import audit_tiger

# The path to the OSM file to be analyzed
OSM_PATH = "rhode-island-latest.osm"

# The filenames for the output csvs
NODES_PATH = "nodes.csv"
NODE_TAGS_PATH = "nodes_tags.csv"
WAYS_PATH = "ways.csv"
WAY_NODES_PATH = "ways_nodes.csv"
WAY_TAGS_PATH = "ways_tags.csv"

LOWER_COLON = re.compile(r'^([a-z]|_)+:([a-z]|_)+')
PROBLEMCHARS = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

SCHEMA = schema.schema

# Make sure the fields order in the csvs matches the column order in the sql table schema
NODE_FIELDS = ['id', 'lat', 'lon', 'user',
               'uid', 'version', 'changeset', 'timestamp']
NODE_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_FIELDS = ['id', 'user', 'uid', 'version', 'changeset', 'timestamp']
WAY_TAGS_FIELDS = ['id', 'key', 'value', 'type']
WAY_NODES_FIELDS = ['id', 'node_id', 'position']


def get_attribs(fields, element):
    """
    Given an element and fields to fetch from that element, returns a dictionary
    of the field and the fields attributes
    """
    out_dict = {}
    for field in fields:
        out_dict[field] = element.get(field)
    return out_dict


def get_tags(element):
    """
    Get tags function takes in an element and returns a list of dictionaries,
    where each dictionary is
    """
    tags = []
    parent_id = element.get('id') # extract the id of the parent tag

    # Extract the street name mapping for fixing abbreviations
    mapping = audit_streetnames.mapping

    # Used for checking if the tiger name needs to be converted
    has_name = False
    has_tiger = False

    # Iterate through all of the tag elements in the parent element
    for child in element.iter('tag'):

        # Extract the key and check it for problems
        key = child.get('k')
        if re.search(PROBLEMCHARS, key):
            # If there are problems, just skip the entire child element
            print 'skipped ' + key
            continue

        # Initialize a child dictionary with the already extracted parent id
        child_dict = {'id': parent_id}

        value = child.get('v')
        # Update the street name if possible to remove abbreviations
        if audit_streetnames.is_street_name(child):
            street = audit_streetnames.update_street_name(value, mapping)
            child_dict['value'] = street
        # Update the post code if possible
        elif audit_postcodes.is_postcode(child):
            postcode = audit_postcodes.update_postcodes(value)
            # Skip this entry if there is a difficult to fix postcode
            if postcode is None:
                continue
            child_dict['value'] = postcode
        # Check if it has a name, used for tiger checking
        elif audit_tiger.is_name(child):
            has_name = True
            child_dict['value'] = value
        # Check if it has a tiger street type
        elif audit_tiger.is_tiger_type(child):
            tiger_type = value
            has_tiger = True
        # Record the tiger name
        elif audit_tiger.is_tiger_name(child):
            tiger_name = value
        # No cleaning necessary on other data types
        else:
            child_dict['value'] = value

        # check if there is a colon in the key
        colon_loc = key.find(':')

        # if there is a colon, split the string
        if colon_loc != -1:
            # the part before the colon is the type
            child_dict['type'] = key[:colon_loc]
            # the part after the colon is the key
            child_dict['key'] = key[colon_loc + 1:]
        # if there is no colon
        else:
            # the type is regular
            child_dict['type'] = 'regular'
            # the key is the entire key
            child_dict['key'] = key

        # add the dictionary to the tags list
        tags.append(child_dict)

    # Check if the tiger name needs to be fixed
    if has_tiger is True and has_name is False:
        tags.append(audit_tiger.update_tiger(parent_id, tiger_name, tiger_type))

    return tags


def get_way_nodes(element):
    """
    Given a way element, returns a list of dictionaries containing the
    the way id, node id, and position of each node element from the way.
    """
    way_nodes = []
    parent_id = element.get('id') # extract the parent id

    # iterate through each node element (nd) in the way
    for position, child in enumerate(element.iter('nd')):
        # Extract the proper elements from the element
        child_dict = {'id': parent_id}
        child_dict['node_id'] = child.get('ref')
        child_dict['position'] = position

        # append it to the way node list
        way_nodes.append(child_dict)

    return way_nodes


def shape_element(element, node_attr_fields=NODE_FIELDS, way_attr_fields=WAY_FIELDS,
                  problem_chars=PROBLEMCHARS, default_tag_type='regular'):
    """Clean and shape node or way XML element to Python dict"""

    if element.tag == 'node':
        node_attribs = get_attribs(NODE_FIELDS, element)
        tags = get_tags(element)
        return {'node': node_attribs, 'node_tags': tags}
    elif element.tag == 'way':
        way_attribs = get_attribs(WAY_FIELDS, element)
        tags = get_tags(element)
        way_nodes = get_way_nodes(element)
        return {'way': way_attribs, 'way_nodes': way_nodes, 'way_tags': tags}

# Note that the code below is used for importing but was provided
# by the Udacity case study.
# I added comments as an exersise to make sure I understood the code
# ================================================== #
#               Helper Functions                     #
# ================================================== #
def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag"""

    context = ET.iterparse(osm_file, events=('start', 'end'))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


def validate_element(element, validator, schema=SCHEMA):
    """Raise ValidationError if element does not match schema"""
    if validator.validate(element, schema) is not True:
        field, errors = next(validator.errors.iteritems())
        message_string = "\nElement of type '{0}' has the following errors:\n{1}"
        error_string = pprint.pformat(errors)

        raise Exception(message_string.format(field, error_string))


class UnicodeDictWriter(csv.DictWriter, object):
    """Extend csv.DictWriter to handle Unicode input"""

    def writerow(self, row):
        # encodes the unicode if it is given
        super(UnicodeDictWriter, self).writerow({
            k: (v.encode('utf-8') if isinstance(v, unicode) else v) for k, v in row.iteritems()
        })

    def writerows(self, rows):
        # Write each row if given a list of rows
        for row in rows:
            self.writerow(row)


# ================================================== #
#               Main Function                        #
# ================================================== #
def process_map(file_in, validate):
    """Iteratively process each XML element and write to csv(s)"""

    # open each file with a codes to help with unicode writing
    with codecs.open(NODES_PATH, 'w') as nodes_file, \
            codecs.open(NODE_TAGS_PATH, 'w') as nodes_tags_file, \
            codecs.open(WAYS_PATH, 'w') as ways_file, \
            codecs.open(WAY_NODES_PATH, 'w') as way_nodes_file, \
            codecs.open(WAY_TAGS_PATH, 'w') as way_tags_file:

        # initialize the UnicodeDictWriter for each file
        nodes_writer = UnicodeDictWriter(nodes_file, NODE_FIELDS)
        node_tags_writer = UnicodeDictWriter(nodes_tags_file, NODE_TAGS_FIELDS)
        ways_writer = UnicodeDictWriter(ways_file, WAY_FIELDS)
        way_nodes_writer = UnicodeDictWriter(way_nodes_file, WAY_NODES_FIELDS)
        way_tags_writer = UnicodeDictWriter(way_tags_file, WAY_TAGS_FIELDS)

        # write all the headers
        nodes_writer.writeheader()
        node_tags_writer.writeheader()
        ways_writer.writeheader()
        way_nodes_writer.writeheader()
        way_tags_writer.writeheader()

        # initialize a validator
        validator = cerberus.Validator()

        # Iterate through the nodes and ways in the file
        for element in get_element(file_in, tags=('node', 'way')):
            # shape the element according to our defined schema
            el = shape_element(element)
            if el:
                # validate using cerberus if validate is true
                if validate is True:
                    validate_element(el, validator)

                # Write the extracted fields to the appropriate file
                if element.tag == 'node':
                    nodes_writer.writerow(el['node'])
                    node_tags_writer.writerows(el['node_tags'])
                elif element.tag == 'way':
                    ways_writer.writerow(el['way'])
                    way_nodes_writer.writerows(el['way_nodes'])
                    way_tags_writer.writerows(el['way_tags'])


if __name__ == '__main__':
    # Note: Validation is ~ 10X slower. For the project consider using a small
    # sample of the map when validating.
    process_map(OSM_PATH, validate=False)
