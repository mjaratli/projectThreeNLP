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
    # Boolean to check if the line is the line with the sentence
    sentenceLine = False
    # All the sentences in the file
    sentences = []
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
                    # Controls the boolean that determines if the line with the sentence is next
            if line.startswith("<context>"):
                sentenceLine = True
                continue
            # If the sentence line is encountered, we gather the word counts per sense
            if sentenceLine:
                sentenceLine = False
                sentences.append(line)

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
    return word, senses, ranges, sentences


# Grab all the necessary counts from the training sections of the file per fold
def process_train(fileName, word, senses, ranges, startRange, endRange, sentences):
    # Counts of each sense
    sensesDict = collections.Counter()
    sensesDict[senses[0]] = 0
    sensesDict[senses[1]] = 0

    # Counts of each word given a sense
    senseOneWord = collections.Counter()
    senseTwoWord = collections.Counter()

    # Count of unique words given a sense (use len() function from senseOneWord and senseTwoWord dictionaries later on
    sensesUniqueDict = collections.Counter()

    # Default punctuation list from the string class, to remove punctuation from words
    punctuation_list = list(string.punctuation)

    # Counter to determine which line we are currently on
    counter = -1

    with open(fileName, 'r') as inputFile:
        # Grabbing each line
        for line in inputFile:
            # Checks if the line begins with answer (since these lines have the sense of the word)
            if line.startswith("<answer"):
                # Each time answer is encountered it is a new instance, so we add to counter here
                counter += 1
                if startRange <= counter < endRange:
                    continue
                # Grabs the sense for each instance
                sense = line[line.find(word + '%') + len(word) + 1:line.find('"/>')]
                # Adds sense to dictionary counter
                sensesDict[sense] += 1
                # Grabs the line from the sentences array based on counter
                # Also splits line by space delimiter into an array
                eachLine = sentences[counter].split()
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
        sensesUniqueDict[senses[0]] = len(senseOneWord)
        sensesUniqueDict[senses[1]] = len(senseTwoWord)

    return sensesDict, senseOneWord, senseTwoWord, sensesUniqueDict


def naivebayes(sensesDict, sensesOneWord, sensesTwoWord, sensesUniqueDict):
    hi = 5


# Grabbing the file name from the terminal as an argument
arg = " "

if len(sys.argv) >= 2:
    arg = sys.argv[1]

# Process the input file
wordMain, sensesMain, rangesM, sentenceList = process_file(arg)
for foldm in range(len(rangesM)):
    startRm = 0
    endRm = 0
    if foldm == 0:
        startRm = 0
        endRm = startRm + rangesM[foldm]
    elif foldm == 1:
        startRm = rangesM[0]
        endRm = startRm + rangesM[foldm]
    elif foldm == 2:
        startRm = rangesM[0] + rangesM[1]
        endRm = startRm + rangesM[foldm]
    elif foldm == 3:
        startRm = rangesM[0] + rangesM[1] + rangesM[2]
        endRm = startRm + rangesM[foldm]
    elif foldm == 4:
        startRm = rangesM[0] + rangesM[1] + rangesM[2] + rangesM[3]
        endRm = startRm + rangesM[foldm]
    sensesDictM, sensesOneWordM, sensesTwoWordM, sensesUniqueDictM = \
        process_train(arg, wordMain, sensesMain, rangesM, startRm, endRm, sentenceList)

