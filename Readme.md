# Information Retrieval System

This is a simple information retrieval system.

## Requirements

1. Python 2.7
2. Noteworthy modules: nltk. 

# Usage

	$ python search.py

It will download the json database and build the index in the first run.

## General Searches

A search prompt will appear. The query string is a list of words that will be searched in all fields. Example:

    > light bulb

The IR will show a list of documents ordered according to relevance. The
list is paginated. Pressing Enter will show the next page (Pressing "q"
exits the query).

## Search specific fields

Field-specific searches are possible by using the field name
(title, merchant, description) followed by a colon. Example:

	> shirt merchant: lewis

The word "shirt" will be searched on all fields. "lewis"
and all words from there on will be searched only on merchant 
field.

To disable a previously set field name, use the keyword "all:"

	> merchant: lewis all: shirt

*Important*: At this stage, field-specific searches 
just increase the weight of the matches on the corresponding field. 
If a little more time is allowed, a better filter can be implemented
in the `weighWord` functions.

## Exit the program

To exit the program, enter a single character "q".

	> q

## Force download the database

To force the download of the database, run the retrieve_data module.

	$ python retrieve_data.py

This will also force the rebuild of the index the next time that
search.py is run.

## Rebuild the index

To rebuild the index, run the index module.

	$ python index.py 







