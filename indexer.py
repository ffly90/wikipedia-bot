#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to produce Index in Order to make searching Wikipedia dump xml file faster.

The Script takes a Wikipedia dump file and iterates over the lines in the file without 
loading its content into the memory at once. It then takes some informations like title,
id, text and whether or not it is a redirection to another article and stores them into
a file.
The articles are stored in files of 1000 each in a special index folder.
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

def strip_tag(tag):
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

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    try:
        if len(tag) > 15:
            tag = tag.rsplit('}', 1)[1]
        return tag
    except:
        print("Tag stripping error with:", tag)
        exit(1)

def indexer(config):
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    progressCounter = 0
    fileIndex = 0
    articleCounter = 0
    indexFileFH = open(os.path.join(config['PATH_INDEX_FILES'], '.'.join([str(fileIndex), "yml"])), "w")
    with open(os.path.join(config['PATH_WIKI_XML'], config['FILENAME_INDEX']), "w") as indexFH:
        for event, elem in etree.iterparse(os.path.join(config['PATH_WIKI_XML'], config['FILENAME_WIKI']), events=('start', 'end')):
            tagName = strip_tag(elem.tag)
            if articleCounter == 1000:
                indexFileFH.close()
                fileIndex += 1
                indexFileFH = open(os.path.join(config['PATH_INDEX_FILES'], '.'.join([str(fileIndex), "yml"])), "w")
                articleCounter = 0
            if event == 'start' and tagName == 'page':
                inRevision = False
                notAnArticle = False
                redirect = None
                title = None
                ns = None
            elif event == 'start':
                if tagName == 'revision':
                    #Making sure to only obtain the articles id
                    inRevision = True
                elif tagName == 'title':
                    title = elem.text
                elif tagName == 'id' and not inRevision:
                    articleIndex = elem.text
                elif tagName == 'redirect':
                    redirect = elem.attrib['title']
                elif tagName == 'ns':
                    try:
                        ns = int(elem.text)
                        if ns != 0:
                            notAnArticle = True
                    except TypeError as err:
                        print(err)
                        notAnArticle = True
                elif tagName == 'text' and event == "start":
                    text = elem.text
            else:
                if tagName == 'page' and not notAnArticle:
                    indexData = {
                        title : {
                            'file': fileIndex,
                            'article': articleIndex,
                            'redirect': redirect
                        }
                    }
                    yaml.safe_dump(indexData, indexFH, allow_unicode=True)
                    if redirect is None:
                        articleData = {
                            articleIndex : text
                        }
                        yaml.safe_dump(articleData, indexFileFH, allow_unicode=True)
                        articleCounter +=1
                        progressCounter +=1
                        if progressCounter > 1 and (progressCounter % 100000) == 0:
                            print("{:,}".format(progressCounter))
                # Free Memory from Data
                elem.clear()

def main():
    """Example function with types documented in the docstring.

    `PEP 484`_ type annotations are supported. If attribute, parameter, and
    return types are annotated according to `PEP 484`_, they do not need to be
    included in the docstring:

    Args:
        param1 (int): The first parameter.
        param2 (str): The second parameter.

    Returns:
        bool: The return value. True for success, False otherwise.

    .. _PEP 484:
        https://www.python.org/dev/peps/pep-0484/

    """
    with open("config.yml","r") as configYaml:
        config = yaml.load(configYaml, Loader=yaml.SafeLoader)
    indexer(config)

if __name__ == "__main__":
   exit(main())

