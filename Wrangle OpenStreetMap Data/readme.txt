File overviews

Audit Files:

audit_general.py
  Used for printing some statistics about the chosen OSM file

audit_postcodes.py
  Used to inspect the postcodes in the OSM file, has the update postcodes
  function which can be used to update a postcode

audit_streetnames.py
  Used to inspect streetnames with inconsistent abbreviations, contains
  the update streetnames function to update given streetnames

audit_tiger.py
  Used to check for tiger GPS blocks that haven't yet been collated into
  a name. Contains the update_tiger function which creates a name given
  tiger elements

csv_convert.py
  Run this to create .csv files from a given xml file. Calls the update
  functions defined in the various audit scripts

schema.py
  Used in the csv convert for the Cerberus verification

reduce_file_size.py
  Provided by udacity, used to generate a smaller version of an XML file

data_wrangling_schema.sql
  Contains the schema used to build the SQL database. Read this file to create
  necessary tables

queries.sql
  Contains various queries that are also in the Jupyter notebook and pdf file
