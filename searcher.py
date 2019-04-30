#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to search index file for matches with a given search word and returning .

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

import os
import yaml
import time

def binaryIndexSearch(indexList, searchString):
    first, last = 0, len(indexList) - 1
    found = False
    results = []
    while first < last and not found:
        pos = 0
        midpoint = (first + last) >> 1
        if indexList[midpoint][0] == searchString:
            pos = midpoint
            found = True
        elif searchString <= indexList[midpoint][0]:
            last = midpoint
        else:
            first = midpoint + 1
    if not found:
        first, last = 0, len(indexList) - 1
        while first < last:
            midpoint = (first + last) >> 1
            if searchString <= indexList[midpoint][0]:
                last = midpoint
            else:
                first = midpoint + 1
        resultIndex = 0
        while indexList[first + resultIndex][0].startswith(searchString) or indexList[first + resultIndex][0].startswith(searchString + "-"):
            results.append(indexList[first + resultIndex][0])
            resultIndex += 1
            found = True
    if found and results:
        return results, True
    elif found and (indexList[pos][3] != 'None'):
        return binaryIndexSearch(indexList, indexList[pos][3].lower())
    elif found:
        return indexList[pos], False
    else:
        return False, False

def getText(config, fileNumber, articleIndex):
    with open(os.path.join(config['PATH_INDEX_FILES'], ".".join([fileNumber, 'yml'])), 'r') as chunkFH:
        articlesDict = yaml.load(chunkFH, Loader=yaml.SafeLoader)
    return articlesDict[articleIndex]

def getInput(config, indexList):
    while True:
        inputValue = input("\tBitte geben Sie einen Suchbegriff ein.\n\tUm das Programm zu beenden geben geben Sie \"Programm beenden\" ein: ")
        start = time.time()
        inputValue = inputValue.strip().lower()
        if inputValue == "Programm beenden":
            break
        elif not inputValue:
            continue
        searchResult, multipleResults = binaryIndexSearch(indexList, inputValue)
        if not multipleResults and searchResult:
            print(getText(config, searchResult[1], searchResult[2]))
            end = time.time()
            print("Suchdauer: " + str(end - start))
        elif multipleResults:
            print("\n".join(["Wähle eines der folgenden Ergebnisse aus:"] + searchResult))
        elif not multipleResults and not searchResult:
            print("Zum übergebenen Suchbegriff wurde keine Definition gefunden. Bitte versuchen Sie es mit einem anderen Begriff erneut.")
    return


def main():
    with open("config.yml","r") as configYaml:
        # opens config file and stores the information to a variable
        config = yaml.load(configYaml, Loader=yaml.SafeLoader)
    indexList = []
    with open(os.path.join(config['PATH_WIKI_XML'], config['FILENAME_SORTED_INDEX']), 'r') as index:
        print("Lade index...")
        for line in index.readlines():
            indexList.append(line.rstrip('\n').split('|'))
    getInput(config, indexList)
    return

if __name__ == "__main__":
   exit(main())

