#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        : Annotation.py    
@Author      : shi4712
@Version     : 1.0  
@Create Time : 2022/3/15 14:22
@Modify Time : 2022/3/15 14:22
"""


class Annotation(object):
    def __init__(self, text, start, end):
        """
            start, end 定义了text start索引和 end索引
        """
        self._text = text
        self._start = start
        self._end = end
        self._length = end - start + 1

    def __contains__(self, item):
        if "_{}".format(item) in self.__dict__:
            return True
        return False

    def getValue(self, attrName):
        if attrName in self:
            return self.__getattribute__("_{}".format(attrName))
        else:
            raise AttributeError("{} has no attribute named : {}".format(self, attrName))

    def __str__(self):
        return "{}：({}, {})".format(self._text, self._start, self._end)

    def __repr__(self):
        return "Annotation<{}：({}, {})>".format(self._text, self._start, self._end)

    def check(self):
        return True

    def returnOtherInfo(self):
        return None


class CDRAnnotation(Annotation):
    def __init__(self, text, start, length, entityType, MeSH):
        super().__init__(text, start, start + length - 1)
        self._type = entityType
        self._MeSH = MeSH

    def __repr__(self):
        return "CDRAnnotation<{}：({}, {})>".format(self._text, self._start, self._end)

    def check(self):
        return True

    def returnOtherInfo(self):
        return {
            "type": self._type,
            "MeSH": self._MeSH
        }


class NERAnnotation(Annotation):
    def __init__(self, bern2Result, showDetail=False):
        text = bern2Result["mention"]
        start = bern2Result["span"]["begin"]
        end = bern2Result["span"]["end"]
        super().__init__(text, start, end)

        self._id = {}
        for idStr in bern2Result["id"]:
            if idStr != 'CUI-less':
                idTuple = idStr.split(":")
                # database, dataId = (idTuple[0], idTuple[1])
                # self._id[database] = dataId
                try:
                    database, dataId = (idTuple[0], idTuple[1])
                    self._id[database] = dataId
                except IndexError:
                    database, dataId = database, idStr  # ['NCBIGene:2629', '2630']
                    if showDetail:
                        print("Error to process : {}".format(bern2Result["id"]))
                        print("set {}: {}".format(database, dataId))

        self._obj = bern2Result["obj"]
        self._prob = bern2Result["prob"]
        self._is_neural_normalized = bern2Result["is_neural_normalized"]

    def __repr__(self):
        return "NERAnnotation<{}：({}, {})>".format(self._text, self._start, self._end)

    def check(self, objList=None, probThreshold=0):
        if not self._prob:
            return False
            # print("*****************")
            # print(self._text)
            # print(self.__dict__)
            # print("*****************")
        if self._prob and self._prob > probThreshold:
            if not objList:
                return True
            if objList and self._obj in objList:
                return True
        return False

    def returnOtherInfo(self):
        return {
            "id": self._id,
            "obj": self._obj,
            "prob": self._prob,
            "is_neural_normalized": self._is_neural_normalized,
        }


class BERNAnnotation(NERAnnotation):
    def __repr__(self):
        return "BNERAnnotation<{}：({}, {})>".format(self._text, self._start, self._end)


if __name__ == '__main__':
    annotationDict = {
        "start": 0,
        "end": 3,
        "length": 4,
        "MeSH": 0,
        "entityType": "test",
        "text": "test",
        "mention": "test",
        "span": {
            "begin": 0,
            "end": 3,
        },
        "obj": "test",
        "prob": 1.0,
        "is_neural_normalized": False,
        "id": ['CUI-less'],
    }
    annotation = Annotation(
        text=annotationDict["text"],
        start=annotationDict["start"],
        end=annotationDict["end"],
    )
    print(annotation)

    cdrAnnotation = CDRAnnotation(
        text=annotationDict["text"],
        start=annotationDict["start"],
        length=annotationDict["length"],
        entityType=annotationDict["entityType"],
        MeSH=annotationDict["MeSH"],
    )
    print(cdrAnnotation)

    bernAnnotation = BERNAnnotation(annotationDict)
    print(bernAnnotation.getValue("id"))
    print(bernAnnotation)
