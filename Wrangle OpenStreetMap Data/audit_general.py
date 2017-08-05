import xml.etree.cElementTree as ET
import pprint
import re
from collections import defaultdict

filename = "rhode-island-latest.osm"
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def count_tags(filename):
    tags = {}
    for event, element in ET.iterparse(filename):
        tag = element.tag
        if tag in tags:
            tags[tag] += 1
        else:
            tags[tag] = 1
    return tags

def key_type(element, keys):

    if element.tag == "tag":
        k = element.get('k')
        if re.search(lower, k):
            keys['lower'] += 1
        elif re.search(lower_colon, k):
            keys['lower_colon'] += 1
        elif re.search(problemchars, k):
            keys['problemchars'] += 1
        else:
            keys['other'] += 1

    return keys

def process_tags(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

def process_users(filename):
    users = set()
    for _, element in ET.iterparse(filename):
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
