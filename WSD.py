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


# Grab all the necessary counts from the training sections of the file per fold
def process_train(fileName, word, senses, ranges, startRange, endRange):
    # Counts of each sense
    sensesDict = collections.Counter()
    sensesDict[senses[0]] = 0
    sensesDict[senses[1]] = 0

    # Counts of each word given a sense
    senseOneWord = collections.Counter()
    senseTwoWord = collections.Counter()

    # Count of unique words given a sense (use len() function from senseOneWord and senseTwoWord dictionaries later on
    senseOneUniqueWords = 0
    senseTwoUniqueWords = 0

    # Default punctuation list from the string class, to remove punctuation from words
    punctuation_list = list(string.punctuation)

    # Counter for ranges
    counter = 0

    # Boolean to check if the line is the line with the sentence
    sentenceLine = False
    with open(fileName, 'r') as inputFile:
        # Grabbing each line
        for line in inputFile:
            # Ensures that the test set range is skipped when determining the counts
            if startRange <= counter < endRange:
                continue
            # Checks if the line begins with answer (since these lines have the sense of the word)
            if line.startswith("<answer"):
                # Grabs the sense for each instance
                sense = line[line.find(word + '%') + len(word) + 1:line.find('"/>')]
                # Adds sense to dictionary counter
                sensesDict[sense] += 1
            # Controls the boolean that determines if the line with the sentence is next
            if line.startswith("<context>"):
                sentenceLine = True
                continue
            # If the sentence line is encountered, we gather the word counts per sense
            if sentenceLine:
                counter += 1
                sentenceLine = False
                # Split line by space delimiter into an array
                eachLine = line.split()
                for item in eachLine:
                    # Remove punctuation from words
                    for element in punctuation_list:
                        item = item.replace(element, "")
                    # Lowercase all words
                    item = item.lower()
                    # Add the word to the proper dictionary, based on the current sense
                    if sense == senses[0]:
                        senseOneWord[item] += 1
                    if sense == senses[1]:
                        senseTwoWord[item] += 1

        # Remove instances of the word (<head>plant</head>)
        del senseOneWord['head' + word + 'head']
        del senseTwoWord['head' + word + 'head']

        # Count of unique words per sense to use for add one smoothing later on
        senseOneUniqueWords = len(senseOneWord)
        senseTwoUniqueWords = len(senseTwoWord)

    systemP = []
    return systemP


def naivebayes():
    hi = 5


# Grabbing the file name from the terminal as an argument
arg = " "

if len(sys.argv) >= 2:
    arg = sys.argv[1]

# Process the input file
wordMain, sensesMain, rangesMain = process_file(arg)
for fold in range(len(rangesMain)):
    startR = 0
    endR = 0
    if fold == 0:
        startR = 0
        endR = startR + rangesMain[fold]
    elif fold == 1:
        startR = rangesMain[0]
        endR = startR + rangesMain[fold]
    elif fold == 2:
        startR = rangesMain[0] + rangesMain[1]
        endR = startR + rangesMain[fold]
    elif fold == 3:
        startR = rangesMain[0] + rangesMain[1] + rangesMain[2]
        endR = startR + rangesMain[fold]
    elif fold == 4:
        startR = rangesMain[0] + rangesMain[1] + rangesMain[2] + rangesMain[3]
        endR = startR + rangesMain[fold]
    systemPrediction = process_train(arg, wordMain, sensesMain, rangesMain, startR, endR)
