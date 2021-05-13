import math
import re
import os
import random

class Mail:
    """
    Data class that is used to parse the content that we get from file
    """
    def __init__(self, id, subjects):
        self.id = id
        self.subjects = subjects
        self.content = ""
        for item in subjects:
            self.content = self.content + " " + item
        self.words = []
        if self.content != "":
            contentCleaned = punctiationCleaner(self.content)
            contentTokens = contentCleaned.split(sep=" ")
            for word in contentTokens :
                if word != "" and word.lower() != "subject":
                    self.words.append(word.lower())


def readMails(isTest):
    """
    Reads the txt files.
    :return: the content of files as a list of data class objects
    """
    base = "training"
    if isTest:
        base = "test"

    spamMails = []
    legitimateMails = []
    entriesSpam = os.listdir(base + '/spam/')
    entriesLegitimate = os.listdir(base + '/legitimate/')
    for spamEntry in entriesSpam:
        with open(base + "/spam/" + spamEntry) as f:
            if spamEntry == ".DS_Store":
                continue
            lines = f.read().splitlines()
            spamMail = Mail(spamEntry, lines)
            spamMails.append(spamMail)


    for legitimateEntry in entriesLegitimate:
        with open(base + "/legitimate/" + legitimateEntry) as f:
            if legitimateEntry == ".DS_Store":
                continue
            lines = f.read().splitlines()
            legitimateMail = Mail(legitimateEntry, lines)
            legitimateMails.append(legitimateMail)

    return legitimateMails, spamMails

def punctiationCleaner(text):
    """
    Cleans the given text from new lines and punctiation
    :param text: the text that is going to be cleaned
    :return: the text cleaned from new line and punctiation
    """
    text = text.replace('\n', ' ')
    text = re.sub(r'[^\w\s]', ' ', text)
    return text

def createInvertedIndex(dataList):
    """
    Loops over articles and creates inverted index.
    :return: inverted index, vocabulary set and total word size in mails
    """
    invertedIndex = dict()
    vocabulary = set()
    totalToken = 0
    for i in range(0, len(dataList)):
        for word in dataList[i].words:
            totalToken = totalToken + 1
            vocabulary.add(word)
            if word != "" and word not in invertedIndex:
                invertedIndex[word] = []
                invertedIndex[word].append(dataList[i].id)
            elif word != "":
                invertedIndex[word].append(dataList[i].id)

    return invertedIndex, vocabulary, totalToken

def mutualInfo():
    """
    Loops over words of the legitimate mails.
    :return: mutual information dictionary
    """
    mutualInfoDict = dict()
    for word in legitimateDict.keys():
        countLegitimateDoc = len(set(legitimateDict[word])) #n10
        countSpamDoc = 0
        if word in spamDict:
            countSpamDoc = len(set(spamDict[word])) #n11

        nonSpamDocCount = 240 - countSpamDoc #n01
        nonLegitimateCount = 240 - countLegitimateDoc #n00
        if nonSpamDocCount == 0 and nonLegitimateCount == 0:
            nonSpamDocCount = 1
        one = (countSpamDoc / numberOfDocuments) * math.log2((numberOfDocuments * countSpamDoc) / ((countSpamDoc + countLegitimateDoc) * (countSpamDoc + nonSpamDocCount)) if (numberOfDocuments * countSpamDoc) / ((countSpamDoc + countLegitimateDoc) * (countSpamDoc + nonSpamDocCount)) != 0 else 1)
        two = (nonSpamDocCount / numberOfDocuments) * math.log2((numberOfDocuments * nonSpamDocCount) / ((nonSpamDocCount + nonLegitimateCount) * (countSpamDoc + nonSpamDocCount)) if (numberOfDocuments * nonSpamDocCount) / ((nonSpamDocCount + nonLegitimateCount) * (countSpamDoc + nonSpamDocCount)) != 0 else 1)
        three = (countLegitimateDoc / numberOfDocuments)* math.log2((numberOfDocuments * countLegitimateDoc) / ((countSpamDoc + countLegitimateDoc) * (countLegitimateDoc + nonLegitimateCount)) if (numberOfDocuments * countLegitimateDoc) / ((countSpamDoc + countLegitimateDoc) * (countLegitimateDoc + nonLegitimateCount)) != 0 else 1)
        four = (nonLegitimateCount/numberOfDocuments) * math.log2((numberOfDocuments*nonLegitimateCount)/((nonSpamDocCount + nonLegitimateCount) * (countLegitimateDoc + nonLegitimateCount)) if (numberOfDocuments*nonLegitimateCount)/((nonSpamDocCount + nonLegitimateCount)*(countLegitimateDoc + nonLegitimateCount)) != 0 else 1)

        mutualInfoDict[word] = one + two + three + four
    return mutualInfoDict

def checkIfMailSpam(mail):
    """
    Loops over words of the mail and calculates if the mail is spam or not
    :return: if the mail is spam or not
    """
    legitimateProb = 0
    spamProb = 0

    legitimateWordCount = 0
    spamWordCount = 0
    for word in mail.words:
        if word in legitimateDict:
            legitimateProb = legitimateProb + math.log2(legitimateProbabilityDic.get(word, 1))
            legitimateWordCount = legitimateWordCount + 1
        if word in spamDict:
            spamProb = spamProb + math.log2(spamProbabilityDic.get(word, 1))
            spamWordCount = spamWordCount + 1
    return spamProb/spamWordCount > legitimateProb/legitimateWordCount

def checkIfMailSpamAccordingMutualInfo(mail):
    """
    Loops over words of the mail and calculates if the mail is spam or not according to mutual informations
    :return: if the mail is spam or not
    """
    legitimateProb = 0
    spamProb = 0

    legitimateWordCount = 0
    spamWordCount = 0
    for word in mail.words:
        if word in firstKWords:
            if word in legitimateDict:
                legitimateProb = legitimateProb + math.log2(legitimateProbabilityDic.get(word, 1))
                legitimateWordCount = legitimateWordCount + 1
            if word in spamDict:
                spamProb = spamProb + math.log2(spamProbabilityDic.get(word, 1))
                spamWordCount = spamWordCount + 1
    if spamWordCount == 0:
        return False
    elif legitimateWordCount == 0:
        return True

    return spamProb/spamWordCount > legitimateProb/legitimateWordCount

def calculateLegitimateAndSpamProbabilityDicts():
    """
    Loops over words of the legitimate vocabulary set and spam vocabulary set and calculates word probability for each word
    :return: probability dictionaries of legitimate case and spam case
    """
    legitimateProbabilityDic = dict()
    spamProbabilityDic = dict()
    for word in legitimateVocabularySet:
        if not word in legitimateProbabilityDic.keys() and word in legitimateDict.keys():
            legitimateProbabilityDic[word] = (len(legitimateDict[word]) + 1) / (legitimateTotalToken + len(vocabularySet))
    for word in spamVocabularySet:
        if not word in spamProbabilityDic.keys() and word in spamDict.keys():
            spamProbabilityDic[word] = (len(spamDict[word]) + 1) / (spamTotalToken + len(vocabularySet))
    return legitimateProbabilityDic, spamProbabilityDic

def randomization_test():
    """
    This method calculates randomization test
    :return: result of the randomization test
    """
    statsCounter = 0
    r = 1000
    realStat = abs(macroAveragedRecall - mutualMacroAveragedRecall)
    for trial in range(0, r):
        newSpams = dict()
        newTopKSpams = dict()
        for key in testSpamMailDict.keys():
            if random.randint(1, 2) == 1:
                newSpams[key] = testSpamMailDict[key]
                newTopKSpams[key] = mutualtestSpamMailDict[key]
            else:
                newSpams[key] = mutualtestSpamMailDict[key]
                newTopKSpams[key] = testSpamMailDict[key]

        newLegitimates = dict()
        newTopKLegitimate = dict()
        for key in testLegitimateMailDict.keys():
            if random.randint(1, 2) == 1:
                newLegitimates[key] = testLegitimateMailDict[key]
                newTopKLegitimate[key] = mutualtestLegitimateMailDict[key]
            else:
                newLegitimates[key] = mutualtestLegitimateMailDict[key]
                newTopKLegitimate[key] = testLegitimateMailDict[key]

        pseudoStat = abs(calculateMacroValuesAndFScore(sum(newLegitimates.values()), sum(newSpams.values()),len(testLegitimateMailDict.keys()),len(testSpamMailDict.keys()))[2] - calculateMacroValuesAndFScore(sum(newTopKLegitimate.values()), sum(newTopKSpams.values()), len(testLegitimateMailDict.keys()), len(testSpamMailDict.keys()))[2])

        if pseudoStat >= realStat:
            statsCounter = statsCounter + 1
    resultRandomization = (statsCounter + 1) / (r + 1)
    return resultRandomization

def calculateResultsOfMails(testLegitimateMails, testSpamMails):
    """
    Takes legitimate and spam mails as parameter than calculates fp, tp ,fn ,tn counters
    :return: legitimate counter for legitimate mails, legitimate mail ids dictionary, spam counter for spam mails and spam mail ids dictionary
    """
    legcounter = 0
    testLegitimateMailDict = dict()
    for mail in testLegitimateMails:
        testLegitimateMailDict[mail.id] = 0
        if not checkIfMailSpam(mail):
            legcounter = legcounter + 1
            testLegitimateMailDict[mail.id] = 1
    spamcounter = 0
    testSpamMailDict = dict()
    for mail in testSpamMails:
        testSpamMailDict[mail.id] = 1
        if checkIfMailSpam(mail):
            testSpamMailDict[mail.id] = 0
            spamcounter = spamcounter + 1

    return legcounter, testLegitimateMailDict, spamcounter, testSpamMailDict

def calculateResultMutual(testLegitimateMails, testSpamMails):
    """
    Takes legitimate and spam mails as parameter than calculates fp, tp ,fn ,tn counters for mutual information scenario
    :return: legitimate counter for legitimate mails, legitimate mail ids dictionary, spam counter for spam mails and spam mail ids dictionary
    """
    mutuallegcounter = 0
    mutualtestLegitimateMailDict = dict()
    for mail in testLegitimateMails:
        mutualtestLegitimateMailDict[mail.id] = 0
        if not checkIfMailSpamAccordingMutualInfo(mail):
            mutualtestLegitimateMailDict[mail.id] = 1
            mutuallegcounter = mutuallegcounter + 1
    mutualspamcounter = 0
    mutualtestSpamMailDict = dict()
    for mail in testSpamMails:
        mutualtestSpamMailDict[mail.id] = 1
        if checkIfMailSpamAccordingMutualInfo(mail):
            mutualspamcounter = mutualspamcounter + 1
            mutualtestSpamMailDict[mail.id] = 0

    return mutuallegcounter, mutualtestLegitimateMailDict, mutualspamcounter, mutualtestSpamMailDict

def calculateMacroValuesAndFScore(legitimateCounter, spamCounter, legitimateFileCount, spamFileCount):
    """
    Takes legitimate mail counter, spam mail conter, legitimate mail size and spam mail size as parameter and calculates their macro
    avarage precision, recall and fscore values
    :return: macro avarage precision, macro avarage recall, f score
    """
    macroAveragedPrecision = (legitimateCounter / (legitimateCounter + spamFileCount - spamCounter) + spamCounter / (spamCounter + legitimateFileCount - legitimateCounter)) / 2
    macroAveragedRecall = (legitimateCounter / legitimateFileCount + spamCounter / spamFileCount) / 2
    fScore = (2 * macroAveragedPrecision * macroAveragedRecall) / (macroAveragedPrecision + macroAveragedRecall)

    return macroAveragedPrecision, macroAveragedRecall, fScore

[legitimateMails, spamMails] = readMails(False)

legitimateDict, legitimateVocabularySet, legitimateTotalToken = createInvertedIndex(legitimateMails)
spamDict, spamVocabularySet, spamTotalToken = createInvertedIndex(spamMails)
vocabularySet = legitimateVocabularySet.union(spamVocabularySet)
numberOfDocuments = len(legitimateMails) + len(spamMails)
legitimateProbabilityDic, spamProbabilityDic = calculateLegitimateAndSpamProbabilityDicts()
mutualInfoDict = mutualInfo()
mutualInfoDict = {k: v for k, v in sorted(mutualInfoDict.items(), key=lambda item: item[1], reverse=True)}
firstKWords = list(mutualInfoDict)[:100]
[testLegitimateMails, testSpamMails] = readMails(True)

legcounter, testLegitimateMailDict, spamcounter, testSpamMailDict = calculateResultsOfMails(testLegitimateMails, testSpamMails)
mutuallegcounter, mutualtestLegitimateMailDict, mutualspamcounter, mutualtestSpamMailDict = calculateResultMutual(testLegitimateMails, testSpamMails)


macroAveragedPrecision, macroAveragedRecall, fScore = calculateMacroValuesAndFScore(legcounter, spamcounter, len(testLegitimateMails), len(testSpamMails))
mutualMacroAveragedPrecision, mutualMacroAveragedRecall, mutualFScore = calculateMacroValuesAndFScore(mutuallegcounter, mutualspamcounter, len(testLegitimateMails), len(testSpamMails))
print("Vocabulary size = " + str(len(vocabularySet)))
print("Most Discriminating 100 Words = ")
print(firstKWords)
print("No feature case:")
print("Macro avg precision = " + str(macroAveragedPrecision))
print("Macro avg recall = " + str(macroAveragedRecall))
print("F score = " + str(fScore))

print("First k case:")
print("Macro avg precision = " + str(mutualMacroAveragedPrecision))
print("Macro avg recall = " + str(mutualMacroAveragedRecall))
print("F score = " + str(mutualFScore))
ert = randomization_test()
print("")
print("Randomization test = " + str(ert))