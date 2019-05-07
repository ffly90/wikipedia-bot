#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to produce Index in Order to make searching Wikipedia dump xml file faster.

The Script takes a Wikipedia dump file and iterates over the lines in the file without 
loading its content into the memory at once. It then takes some information like title,
id, text and whether or not it is a redirection to another article and stores them into
a file.
The articles are stored in files of 100 each in a special index folder.
Also an entry to an index file is made containing title, filenumber, id and if present 
the title of the article it redirects to.

Example:
    The script can easily be executed from the commandline and only needs the
    config file to contain the necessary information::

        $ python indexer.py

.. Docstrings according to _PEP 484:
    https://www.python.org/dev/peps/pep-0484/

"""
from lxml import etree
import yaml
import os

def stripTag(tag):
    """
    Function to strip the tag provided by the xml parser.

    This function takes the tag the is returned by the xml parser and gets rid
    of the leading string the contains the URL of the revision of the wikipedia
    dump. Some tags to not contain the leading URL string, they are identified 
    by being shorter than the others. Those tags are returned without further
    manipulation:

    Args:
        tag (str): Contains the tag the is returned by the xml parser.

    Returns:
        str: returns stripped tag if successful. Closes Program if unexpected
        behavior occurs.
    
    TODO:
        * find better solution to find out if tag has meta information or not.
    """
    try:
        if len(tag) > 15:
            tag = tag.rsplit('}', 1)[1]
        return tag
    except IndexError as err:
        print(err, "Unexpected tag:", tag)
        exit(1)

def indexer(config):
    """
    Function to create article chunks and index file.

    This function opens a Wikipedia dump file and iterates over the tags of the xml.
    It then writes information the title, id, text and whether or not it is a 
    redirection to another article and stores them into a data chunk file.
    The articles are stored in chunk files of 100 articles each.
    Also an entry to an index file is made containing title, filenumber, id and if present 
    the title of the article it redirects to:

    Args:
        config (dict): Dictionary containing the information form the config file

    Returns:
        int: 0 if successful
    """
    progressCounter = 0
    fileIndex = 0
    articleCounter = 0

    # creates first data chunk file
    indexFileFH = open(os.path.join(config['PATH_INDEX_FILES'], '.'.join([str(fileIndex), "yml"])), "w")

    with open(os.path.join(config['PATH_WIKI_XML'], config['FILENAME_INDEX']), "w") as indexFH:
        # iterates over the wikipedia dump xml tag by tag
        for event, elem in etree.iterparse(os.path.join(config['PATH_WIKI_XML'], config['FILENAME_WIKI']), events=('start', 'end')):
            tagName = stripTag(elem.tag)
            # creates new data chunk file if the the 100 articles have been written to the actual file
            if articleCounter == 100:
                indexFileFH.close()
                fileIndex += 1
                indexFileFH = open(os.path.join(config['PATH_INDEX_FILES'], '.'.join([str(fileIndex), "yml"])), "w")
                articleCounter = 0
            # initializes all variables for each article
            if event == 'start' and tagName == 'page':
                inRevision = False
                notAnArticle = False
                redirect = None
                title = None
                ns = None
            elif event == 'start':
                if tagName == 'revision':
                    # Making sure to only obtain the id of article but not the revision id
                    inRevision = True
                elif tagName == 'title':
                    title = elem.text
                elif tagName == 'id' and not inRevision:
                    articleIndex = elem.text
                elif tagName == 'redirect':
                    redirect = elem.attrib['title']
                elif tagName == 'ns':
                    # the namespaces determine the page type. Only the namespace 0 contains article information
                    # the rest of the pages is going to be discarded. 
                    try:
                        ns = int(elem.text)
                        if ns != 0:
                            notAnArticle = True
                    except TypeError as err:
                        # sometimes the namespace is not specified. In this case the pages' inforation is not stored
                        print(err)
                        notAnArticle = True
                elif tagName == 'text' and event == "start":
                    text = elem.text
            else:
                if tagName == 'page' and not notAnArticle:
                    # if a page is parsed all the way through, the obtained data is stored.
                    if redirect and title.strip().lower() == redirect.strip().lower():
                        # ignore case insensitivity
                        continue
                    try:
                        indexData = "|".join([title.lower(), str(fileIndex), str(articleIndex), str(redirect)]) + "\n"
                    except AttributeError as err:
                        print(err)
                        continue
                    indexFH.write(indexData)
                    if redirect is None:
                        # if the page only contains a redirection it only needs to be stored in the index file
                        articleData = {
                            articleIndex : text
                        }
                        yaml.safe_dump(articleData, indexFileFH, allow_unicode=True)
                        articleCounter +=1
                        progressCounter +=1
                        if progressCounter > 1 and (progressCounter % 100000) == 0:
                            # prints progress for every 100000 successfully stored articles
                            print("{:,}".format(progressCounter))
                # Clears the memory of the xml element to prevent the parser to force the system into using swap
                elem.clear()
    # closes the last data chunk file
    indexFileFH.close()
    return

def sortIndex(config):
    """
    Function to sort the index file by title.

    This function sorts the index file by the title of the articles to make searching it
    easier. The result is written to the file specified in the config file:

    Args:
        config (dict): Dictionary containing the information form the config file

    Returns:
        int: 0 if successful
    """
    unsortedIndexFH = open(os.path.join(config['PATH_WIKI_XML'], config['FILENAME_INDEX']), 'r')
    unsortedIndex = unsortedIndexFH.readlines()
    sortedIndexFH = open(os.path.join(config['PATH_WIKI_XML'], config['FILENAME_SORTED_INDEX']), 'w')
    # splits every line once by the delimiter to access the title, then sorts them and stores the result
    for item in sorted(unsortedIndex, key=lambda line: line.split('|', 1)[0]):
        sortedIndexFH.write(item)
    unsortedIndexFH.close()
    sortedIndexFH.close()
    return

def main(configFilePath=".config/config_indexer.yml"):
    """
    Main Function.

    The main function opens the config file and calls the indexer and the sortIndex function:

    Returns:
        int: 0 if the script terminated successfully, 1 if an error occurred.
    """
    with open(configFilePath,"r") as configYaml:
        # opens config file and stores the information to a variable
        config = yaml.load(configYaml, Loader=yaml.SafeLoader)
    indexer(config)
    sortIndex(config)
    return 

if __name__ == "__main__":
   exit(main())
