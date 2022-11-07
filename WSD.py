import math
import string
import collections
import sys


# Determines the number of instances, ranges for each fold, and the different senses
def process_file(fileName):
    # The word instance
    word = fileName.removesuffix('.wsd')
    # Stores the possible senses for the target word in a list
    senses = []
    # The number of instances in the file
    instances = 0
    # The ranges for each fold stored in a list
    ranges = []
    # Opening the file
    with open(fileName, 'r') as inputFile:
        # Grabbing each line
        for line in inputFile:
            if line.startswith("<answer"):
                # Grabs the sense for each instance
                sense = line[line.find(word + '%') + len(word) + 1:line.find('"/>')]
                # Adds a sense to the senses list if it does not already exist
                if sense not in senses:
                    senses.append(sense)
                # Counts the number of instances
                instances += 1
    # Determines the fold ranges for all five folds
    splitNum = math.ceil(instances / 5)
    ranges.append(splitNum)
    ranges.append(splitNum)
    ranges.append(splitNum)
    ranges.append(splitNum)
    ranges.append(instances - (ranges[0] + ranges[1] + ranges[2] + ranges[3]))

    # Returns the word, the possible senses, and the ranges for all the folds
    return word, senses, ranges

def process_train(fileName, word, senses, ranges):


# Grabbing the file name from the terminal as an argument
arg = " "

if len(sys.argv) >= 2:
    arg = sys.argv[1]

# Process the input file
word, senses, ranges = process_file(arg)
process_train(arg, word, senses, ranges)
