#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        : document.py    
@Author      : shi4712
@Version     : 1.0  
@Create Time : 2022/3/15 14:23
@Modify Time : 2022/3/15 14:23
"""

import re

import pandas as pd
from nltk.tokenize import word_tokenize

from .annotation import Annotation, CDRAnnotation


class Word(object):
    def __init__(self, word, wordLabel, sentenceIndex, otherInfo=None):
        self.text = word
        self.wordLabel = wordLabel
        self.sentenceIndex = sentenceIndex
        self.otherInfo = otherInfo

    def lookUp(self):
        info = pd.Series([self.text, self.wordLabel, self.sentenceIndex], index=["text", "wordLabel", "sentenceIndex"])
        otherInfo = pd.Series(self.otherInfo, dtype="object")
        return pd.concat([info, otherInfo])

    # def toJson(self):
    #     return self.__dict__


class Document(object):
    sentencePattern = r"[\.!\?]\ [^a-z]"  # the re pattern to identify sentence split position

    def __init__(self, identifier, training, **kwargs):
        self.annotations = {}
        self.sentencesIndexDict = {}
        self.words = {}
        # self.sentTokenizer = self.returnSentTokenizer()
        # self.sentences = {}

        self.training = training
        self.identifier = identifier
        self.__create(**kwargs)
        self.splitAndLabel()

    def __create(self, **kwargs):
        if self.identifier == "CDR":
            self.createByCDR(**kwargs)
        else:
            try:
                self.__setattr__("title", kwargs["title"])
                self.__setattr__("abstract", kwargs["abstract"])
            except KeyError:
                raise ValueError("Miss parameter 'title' or 'abstract' to init document object with no identifier!")

            for attrName in ["title", "abstract"]:
                text = self.__getattribute__(attrName)
                sendIndexList = self.returnSentencePos(text)
                self.sentencesIndexDict[attrName] = sendIndexList

            self.__setattr__("id", kwargs["PMID"])

    def setAnnotations(self, annotationList, identifier):
        assert identifier in ["title", "abstract"], """identify should be 'title' or 'abstract'"""
        annotationList = sorted(annotationList, key=lambda annotation: annotation.getValue("start"), reverse=False)
        self.annotations[identifier] = annotationList

    def isSet(self):
        if "title" in self.annotations and "abstract" in self.annotations:
            return True
        return False

    def createByCDR(self, document):
        assert len(document.passages) == 2, "Error passages length {} for article {}".format(len(document.passages),
                                                                                             document.id)

        self.__setattr__("title", document.passages[0].text)
        self.__setattr__("abstract", document.passages[1].text)

        self.__setattr__("id", document.id)
        self.__setattr__("relations", [relation.infons for relation in document.relations])

        def createAnnotation(passage, multiLabelOption="max"):
            annotationList = []
            for annotation in passage.annotations:
                entityType = annotation.infons["type"]
                text = annotation.text
                MeSH = annotation.infons["MESH"]
                for loc in annotation.locations:
                    annotationList.append(
                        CDRAnnotation(text, loc.offset - passage.offset, loc.length, entityType, MeSH)
                    )
            annotationList = sorted(annotationList, key=lambda annotation: annotation.getValue("start"))
            if multiLabelOption == "max" and len(annotationList) > 0:  # 对于同一位置有多个 Annotation 的情况选择跨度最大的 Annotation
                newAnnotationList = [annotationList.pop(0)]
                while len(annotationList) > 0:
                    compareAnnotation = annotationList.pop(0)
                    assert compareAnnotation.getValue("start") >= newAnnotationList[
                        -1].getValue("start"), """The later annotation start should no less than the pre one"""
                    if compareAnnotation.getValue("start") > newAnnotationList[-1].getValue("end"):
                        newAnnotationList.append(compareAnnotation)
                    else:
                        if compareAnnotation.getValue("end") <= newAnnotationList[-1].getValue("end"):
                            continue
                        elif compareAnnotation.getValue("end") >= newAnnotationList[-1].getValue("end"):
                            newAnnotationList.pop()
                            newAnnotationList.append(compareAnnotation)
                        else:
                            raise ValueError(
                                "There are other compare situation for annotation(from {} to {}) with annotation(from {} to {}).".format(
                                    newAnnotationList[-1].getValue("start"), newAnnotationList[-1].getValue("end"),
                                    compareAnnotation.getValue("start"), compareAnnotation.getValue("end")
                                ))
                annotationList = newAnnotationList
            return annotationList

        if self.training:
            self.annotations["title"] = createAnnotation(document.passages[0])
            self.annotations["abstract"] = createAnnotation(document.passages[1])

        for attrName in ["title", "abstract"]:
            text = self.__getattribute__(attrName)
            sendIndexList = self.returnSentencePos(text)
            self.sentencesIndexDict[attrName] = sendIndexList

    def returnSentencePos(self, text):
        baseOffset = 0
        senEndIndexList = []

        while re.search(self.sentencePattern, text):
            senEnd = re.search(self.sentencePattern, text).span()[0]
            baseOffset += (senEnd + 2)
            senEndIndexList.append(baseOffset-2)
            text = text[senEnd+2:]
        senEndIndexList.append(baseOffset + len(text) - 1)
        return senEndIndexList

    @staticmethod
    def returnLabelWords(labelText, senIndex):
        annotationInfo = None
        if not isinstance(labelText, str):
            annotationInfo = labelText.returnOtherInfo()
            labelText = labelText.getValue("text")
        wordList = word_tokenize(labelText)

        if len(wordList) == 0:
            return []

        labelWords = [Word(wordList[0], "B" if annotationInfo else "O", senIndex, annotationInfo)]
        for word in wordList[1:]:
            labelWords.append(
                Word(word, "I" if annotationInfo else "O", senIndex, annotationInfo)
            )
        return labelWords

    def splitAndLabel(self):
        for attrName in self.sentencesIndexDict:
            text = self.__getattribute__(attrName)
            annotationList = self.annotations.get(attrName, []).copy()

            self.words[attrName] = []
            baseOffset = 0
            senEndIndexList = self.sentencesIndexDict[attrName]
            for senIndex in range(0, len(senEndIndexList)):
                while annotationList:
                    annotation = annotationList.pop(0)
                    if annotation.getValue("end") <= senEndIndexList[senIndex]:
                        self.words[attrName] += self.returnLabelWords(
                            text[baseOffset: annotation.getValue("start")],
                            senIndex
                        )
                        self.words[attrName] += self.returnLabelWords(
                            annotation,
                            senIndex
                        )
                        baseOffset = annotation.getValue("end") + 1
                    else:
                        annotationList = [annotation] + annotationList
                        break
                self.words[attrName] += self.returnLabelWords(
                    text[baseOffset: senEndIndexList[senIndex] + 1],
                    senIndex)
                baseOffset = senEndIndexList[senIndex] + 1

    def lookUp(self, keyAdded=None):
        if not keyAdded:
            keyAdded = "document_id"

        lookUpDfList = []
        for key in self.words.keys():
            words = self.words[key]
            lookUpInfo = list(map(lambda word: word.lookUp(), words))
            lookUpDf = pd.DataFrame(lookUpInfo)
        # for key in self.sentences.keys():
        #     sentences = self.sentences[key]
        #     lookUpInfo = list(map(lambda sentence: sentence.lookUp(), sentences))
        #     lookUpDf = pd.concat(lookUpInfo, sort=False)
            lookUpDf["identifier"] = key
            lookUpDfList.append(lookUpDf)

        lookUpDf = pd.concat(lookUpDfList, sort=False)
        lookUpDf[keyAdded] = self.id
        lookUpDf.index = range(0, len(lookUpDf))
        return lookUpDf

    def seekWordPairs(self, **kwargs):
        wordPairs = []
        for identifier in self.annotations:
            sentenceEndIndex = self.sentencesIndexDict[identifier]
            identifierAnnotations = self.annotations[identifier].copy()
            currentSentenceIndex = 0
            currentSentencePairs = []
            while identifierAnnotations:
                annotation = identifierAnnotations.pop(0)
                if not annotation.check(**kwargs):
                    continue
                if annotation.getValue("end") <= sentenceEndIndex[currentSentenceIndex]:
                    currentSentencePairs.append(annotation)
                else:
                    identifierAnnotations = [annotation] + identifierAnnotations
                    if currentSentencePairs:
                        wordPairs.append([identifier, currentSentenceIndex, currentSentencePairs])
                    currentSentenceIndex += 1
                    currentSentencePairs = []
            if currentSentencePairs:
                wordPairs.append([identifier, currentSentenceIndex, currentSentencePairs])
        return wordPairs

    # def toJson(self):
    #     jsonObj = self.__dict__


if __name__ == "__main__":
    # tested by article
    pass
    # import bioc
    #
    # filePath = "../testData/CDR_TrainingSet.BioC.xml"
    # reader = bioc.BioCXMLDocumentReader(filePath)
    # for document in reader:
    #     if document.id == "12464714":    # error report document
    #         print(document.id)
    #         break
    # testDocument = Document(identifier="CDR", training=True, document=document)
    # print(testDocument.lookUp()[:15])
    # print(testDocument.seekWordPairs())
