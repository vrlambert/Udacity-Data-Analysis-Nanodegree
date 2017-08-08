import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

filename = "small_sample.osm"
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def count_tags(filename):
    """
    Function takes in an osm file and returns a dictionary of the counts of
    each type of tag in the file.
    """
    tags = {}
    # Iterate through the tags
    for event, element in ET.iterparse(filename):
        tag = element.tag

        # Increment the count if it's in the tag, add it otherwise
        if tag in tags:
            tags[tag] += 1
        else:
            tags[tag] = 1
    return tags

def key_type(element, keys):
    """
    Function takes in an element and checks each of the tags to see if it is
    all lowercase, lowercase with a colon, contains a problem character,
    or some other type.
    """
    # Only check if the element is a tag element
    if element.tag == "tag":
        # Extract the key from the element
        k = element.get('k')

        # Check if the key is all lower case
        if re.search(lower, k):
            keys['lower'] += 1

        # Check if the key is all lower case and contains a colon
        elif re.search(lower_colon, k):
            keys['lower_colon'] += 1

        # Check if the key has problem characters
        elif re.search(problemchars, k):
            keys['problemchars'] += 1

        # Otherwise, mark it other
        else:
            keys['other'] += 1

    return keys

def process_tags(filename):
    """
    Calls the key_type function on each element, searching for problem
    characters and other types of tags
    """
    # Initialize a dictionary to count the types
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}

    # Iterate through elements in the file
    for _, element in ET.iterparse(filename):
        # check the key of the element
        keys = key_type(element, keys)

    return keys

def process_users(filename):
    """
    Takes in an osm filename and returns a set of the users
    """
    # Iterate through the users and add each uid to a set
    users = set()
    for _, element in ET.iterparse(filename):
        # Important to use uid instead of user because it is unique
        uid = element.get('uid')
        if uid:
            users.add(uid)

    return users

def main():
    print 'Count element types:'
    pprint.pprint(count_tags(filename))

    print '\nCheck for tag problem characters:'
    pprint.pprint(process_tags(filename))

    print '\nNumber of unique users:'
    print len(process_users(filename))

if __name__ == '__main__':
    main()
