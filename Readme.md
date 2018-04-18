# Information Retrieval System

This is a simple information retrieval system.

## Requirements

1. Python 2.7
2. Noteworthy modules: nltk, future. 

# Usage

	$ python search.py

It will download the json database and build the index in the first run.

## General Searches

A search prompt will appear. The query string is a list of words that will be searched in all fields. Example:

    > led light bulb

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


# Implementation

## Version 0.1

1. Basic NLP (tokenization, lemmatization, stopwords).
2. Field-specific weighting scheme.
3. Positional weighting scheme.

## Version 0.2

Improvements of this version:
	
1. Better documentation
2. Better function naming
3. Function modularization (calcWeight)
4. Weight factor modified by word or lemma match
5. Save search to file for later inspection
6. Avoid some duplication in indexing
7. Display result weights for better debugging

## Future versions

1. Improve  "search by field". 
Currently, it is implemented via weight manipulation (i.e.
if the word is match in the desired field, the weight
is multiplied). This approach works well for only one field. But if we search
in two or more fields at the same time, the results may not be what should
be expected. It is probably better to implement it as a filter.
2. Index the
POS (Part-of-speech) tag of the word, along with the
position. Nouns in the title could be given a higher weight that
verbs when matched at search time. 
3. The output of the function `wheighWord` (docs dict) could hold
more  information that just the gained weight. Some more 
information could help "global" query evaluation. For instance,
proximity of the words matched (on the query and on the field).   
4. Spelling correction, etc.
5. More advanced corpus indexing.










 










