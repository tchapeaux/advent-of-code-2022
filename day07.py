from collections import namedtuple
from typing import Optional, List

import aoc

data: List[str] = aoc.getLinesForDay(7)
# data: List[str] = aoc.getLinesForDay(7, force_filepath="inputs/day07_example.txt")

# Define Data Structures

File = namedtuple("File", ["name", "size"])


class Folder(object):
    def __init__(self):
        self.name: str = ""
        self.files: List[File] = []
        self.folders: List[Folder] = []
        self.parent: Optional[Folder] = None

    def getSize(self) -> int:
        accSize: int = 0
        for file in self.files:
            accSize += file.size
        for folder in self.folders:
            accSize += folder.getSize()
        return accSize


# Initialize values for the parsing

root: Folder = Folder()
root.name = "/"

allFolders: List[Folder] = [root]

currentFolder: Folder = root

# Parse the data

# Skip first line (cd to the root)
data = data[1:]
for lineIdx, line in enumerate(data):
    if line == "$ ls":
        # We can skip the ls as we assume they are always performed
        pass

    elif line.startswith("dir "):
        # We can skip those lines as the folders will be explored later anyway
        pass

    elif line.startswith("$ cd"):
        if line == "$ cd ..":
            assert currentFolder.parent is not None
            currentFolder = currentFolder.parent
        else:
            newFolder: Folder = Folder()
            newFolder.name = line[len("$ cd ") :]
            newFolder.parent = currentFolder

            allFolders.append(newFolder)

            currentFolder.folders.append(newFolder)
            currentFolder = newFolder

    else:
        [fileSize, fileName] = line.split(" ")
        newFile = File(name=fileName, size=int(fileSize))
        currentFolder.files.append(newFile)

print("Parsed", len(data), "lines")
print("Found", len(allFolders), "folders")
print("For a total of", root.getSize(), "size")

# Part 1: find the sum of "small-ish" folders

smallFolders = [f for f in allFolders if f.getSize() <= 100000]
part1Sum = sum([f.getSize() for f in smallFolders])
print("Part 1", part1Sum)

# Part 2: find the smallest of "big-ish" folders

TOTAL_SIZE: int = 70000000
UPDATE_SIZE: int = 30000000

currentlyOccupiedSize: int = root.getSize()
currentlyUnusedSize: int = TOTAL_SIZE - currentlyOccupiedSize
minimalSizeToDelete: int = UPDATE_SIZE - currentlyUnusedSize

print("Looking for folder of more than", minimalSizeToDelete)

candidateFolders = [f for f in allFolders if f.getSize() >= minimalSizeToDelete]
# print("\n".join([f"{f.getSize()} {f.name}" for f in candidateFolders]))
part2Value = min([f.getSize() for f in candidateFolders])
print("Part 2", part2Value)

# one wrong answer for Part 2
# because I got confused between free and occupied space in the minimalSizeToDelete calculation
