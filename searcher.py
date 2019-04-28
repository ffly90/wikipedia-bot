import os
import yaml

def binary_index_search(indexList, searchString):
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
            last = midpoint - 1
        else:
            first = midpoint + 1
    if not found:
        first, last = 0, len(indexList) - 1
        while first < last:
            pos = 0
            midpoint = (first + last) >> 1
            print(indexList[midpoint][0])
            if indexList[midpoint][0].startswith(searchString + " ") or indexList[midpoint][0].startswith(searchString + "-"):
                results.append(indexList[midpoint][0])
                found = True
            if searchString <= indexList[midpoint][0]:
                last = midpoint-1
            else:
                first = midpoint+1
    if found and results:
        return results, True
    elif found and (indexList[pos][3] != 'None'):
        print(indexList[pos][3])
        return binary_search(indexList, indexList[pos][3].lower()), "redirect"
    elif found:
        return indexList[pos], False
    else:
        return False


def get_text(config, fileNumber, articleIndex):
    open(os.path.join())


def main():
    indexList = []
    with open("/media/black/ssd/sorted_index.txt", 'r') as index:
        for line in index.readlines():
            indexList.append(line.rstrip('\n').split('|'))
    binary_search(indexList, 'atos')

#     return

# if __name__ == "__main__":
#    exit(main())
