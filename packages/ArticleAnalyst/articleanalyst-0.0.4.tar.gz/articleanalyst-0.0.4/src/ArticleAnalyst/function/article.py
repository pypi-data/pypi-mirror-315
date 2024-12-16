#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: the behavior of article
@version: 1.0.0
@file: article.py
@time: 2023/2/21 10:29
"""
import re

import pandas as pd

from .document import Document


class Article(object):
    basicAttrs = ["PMID", "TI", "Journal", "DP"]

    def __init__(self, dataSource, record):
        for key, value in record.items():
            self.__setattr__(key, value)

        if dataSource == "query":
            self.__preprocess()

    def __repr__(self):
        return "Article({})".format(self.PMID)

    def __str__(self):
        return """PMID: {}\nYear: {}\nTitle: {}\nAbstract: {}......
        """.format(self.PMID,
                   self.Year if "Year" in self else None,
                   self.TI if "TI" in self else None,
                   self.AB[:100] if "AB" in self else None)

    def __eq__(self, other):
        return self.PMID == other.PMID

    def __hash__(self):
        return hash(self.PMID)

    def __contains__(self, item):
        return True if item in self.__dict__ else False

    def __preprocess(self):
        if "MH" in self:
            majorMHList = []
            MHList = []
            MHDict = []
            # if not isinstance(self.MH, list):
            #     self.MH = [self.MH]
            for MH in self.MH:
                majorMH = True if "*" in MH else False
                MH = re.sub("\*", "", MH)
                MeSHName = MH.split("/")[0]
                MH = {
                    "MeSH Name": MeSHName,
                    "Subheading": MH.split("/")[1:] if len(MH.split("/")) > 1 else None,
                    "Major MeSH": majorMH
                }

                MHDict.append(MH)

                if MeSHName not in MHList:
                    MHList.append(MeSHName)
                if majorMH and MeSHName not in majorMHList:
                    majorMHList.append(MeSHName)

            self.addValue("MHDict", MHDict)
            self.addValue("MHList", MHList)
            self.addValue("majorMHList", majorMHList)

        if "TA" in self or "JT" in self or "JID" in self:
            self.addValue("Journal", {
                "Journal": self.__dict__.get("JT", None),
                "Journal Abbrs": self.__dict__.get("TA", None),
                "Journal ID": self.__dict__.get("JID", None),
            })

            if "TA" in self:
                self.delValue("TA")

            if "JT" in self:
                self.delValue("JT")

            if "JID" in self:
                self.delValue("JID")

        if "DP" in self:
            DPValue = self.DP
            try:
                year = int(re.match("^([0-9]{4}).*", DPValue).group(1))
                self.addValue("Year", year)
            except AttributeError:
                raise AttributeError("Failed to convert DP to year for article {}: {}".format(self.PMID, self.DP))

    def addValue(self, attrName, attrValue):
        """
        add an attr named attrName as attrValue for a Article object,
        if attr exists, raise ValueError
        :param attrName:
        :param attrValue:
        :return: None
        """
        if attrName not in self:
            self.__setattr__(attrName, attrValue)
        else:
            raise ValueError("{} has existed already: {}.".format(attrName, self.__getattribute__(attrName)))

    def delValue(self, attrName):
        """
        del attrValue from attrName attr for Article object,
        if attrName in basic attrs, raise ValueError
        :param attrName:
        :param attrValue:
        :return: None
        """
        if attrName in self:
            if attrName in self.basicAttrs:
                raise ValueError("Can't del the basic attr: {}".format(attrName))
            self.__delattr__(attrName)
        else:
            print("Article({}) does not has attribute named {}.".format(self.PMID, attrName))

    def modifyValue(self, attrName, attrValue):
        """
        modify the value of attrName as attrV
        if attrName not exists, raise AttributeError
        if attrName in basic attrs, raise ValueError
        :param attrName:
        :param attrValue:
        :return: None
        """
        if attrName not in self:
            raise AttributeError("Article {} don't has the attribute named {}".format(self.PMID, attrName))
        if attrName in self.basicAttrs:
            raise ValueError("Can't modify basic attr: {}".format(attrName))
        self.__setattr__(attrName, attrValue)

    def getValue(self, attrName):
        """
        return attrValue from attrName
        """

        if isinstance(attrName, list):
            valueList = list(map(
                lambda trueAttrName: self.__getattribute__(trueAttrName) if trueAttrName in self else pd.NA, attrName
            ))
            return pd.Series(valueList, index=attrName)
        else:
            return self.__getattribute__(attrName)

    def queryValue(self, attrName, valueList=None):
        """
        for any value in valueList, if value in attrName, return True, else False;
        if valueList is none, return the value of attrName
        :param attrName:
        :param valueList:
        :return:
        """
        if not valueList:
            return self.__getattribute__(attrName)
        else:
            switchDict = {
                float: lambda value, attrValueFloat: value == attrValueFloat,
                int: lambda value, attrValueInt: value == attrValueInt,
                str: lambda value, attrValueStr: value.lower() in attrValueStr.lower(),
                list: lambda value, attrValueList: sum(
                    [switchDict[type(subAttrValue)](value, subAttrValue) for subAttrValue in attrValueList]),
                dict: lambda value, attrValueDict: sum(
                    [switchDict[type(attrValueDict[key])](value, attrValueDict[key]) if attrValueDict[key] else False
                     for key in attrValueDict])
                # object(Document)
            }

            attrValue = self.__getattribute__(attrName)
            for queryValue in valueList:
                if switchDict[type(attrValue)](queryValue, attrValue):
                    return True
            return False

    def setDocument(self, replace=True):
        if "TI" in self and "AB" in self:
            document = Document(identifier=None, training=False, title=self.TI, abstract=self.AB, PMID=self.PMID)
            try:
                self.addValue("document", document)
            except ValueError as e:
                if replace:
                    self.modifyValue("document", document)
                else:
                    raise ValueError(e)
        else:
            print("There is no title or abstract attribute for article: {}".format(self.PMID))
            self.addValue("document", None)

    def returnArticleDistance(self, other, reference, cacheKey="Cache"):
        """
        a method based edit graph to get the distance of two articles
        :param other: other article
        :param reference: key to store edit graph
        :return:
        """
        import networkx as nx
        assert isinstance(other, Article), """other should be Article type Object"""

        if "{}_dimension".format(reference) not in self or "{}_dimension".format(reference) not in other:
            raise AttributeError("no graph embedding information found in {}_dimension".format(reference))

        key = "{}_dimension".format(reference)
        assert self.getValue(key).keys() == other.getValue(key).keys(), """
            The dimension of {} and {} should be equal
        """.format(self, other)

        if self == other:
            return pd.Series([0] * len(self.getValue(key)), index=self.getValue(key).keys())
        distanceSeries = pd.Series([None] * len(self.getValue(key)), index=self.getValue(key).keys())
        for dimension in self.getValue(key):
            g1 = self.getValue("{}_dimension".format(reference))[dimension]
            g2 = other.getValue("{}_dimension".format(reference))[dimension]

            # if g1 == {} and g2 == {}:
            #     distanceSeries[dimension] = 0
            # elif g1 == {}:
            #     g2 = nx.from_dict_of_lists(g2, create_using=nx.DiGraph)
            #     distanceSeries[dimension] = len(g2.nodes) + len(g2.edges)
            # elif g2 == {}:
            #     g1 = nx.from_dict_of_lists(g1, create_using=nx.DiGraph)
            #     distanceSeries[dimension] = len(g1.nodes) + len(g1.edges)
            # else:
            #     # in nx, only the attributes of node and edge were used to judge same node or same edge
            #     # so an id using ID is necessary for graph edit distance
            #     g1 = nx.from_dict_of_lists(g1, create_using=nx.DiGraph)

            #     [g1.add_node(node, id=node) for node in g1.nodes]
            #     [g1.add_edge(edge[0], edge[1], id=edge) for edge in g1.edges]
            #     g2 = nx.from_dict_of_lists(g2, create_using=nx.DiGraph)
            #     [g2.add_node(node, id=node) for node in g2.nodes]
            #     [g2.add_edge(edge[0], edge[1], id=edge) for edge in g2.edges]
            #     distanceSeries[dimension] = nx.graph_edit_distance(g1, g2, roots=(dimension, dimension))

            # an alternative method is to calculate the sum of unique node and edge between tow graph
            # based on mesh characteristic
            g1 = nx.from_dict_of_lists(g1, create_using=nx.DiGraph)
            g2 = nx.from_dict_of_lists(g2, create_using=nx.DiGraph)
            distanceSeries[dimension] = (
                len(g1.nodes) + len(g1.edges)
                + len(g2.nodes) + len(g2.edges)
                - 2 * (
                        len(set(g1.nodes) & set(g2.nodes)) + len(set(g1.edges) & set(g2.edges))
                )
            )

        return distanceSeries

    def toJson(self):
        jsonObj = self.__dict__
        if "document" in jsonObj and isinstance(jsonObj["document", Document]):
            raise ValueError("Can't convert document to json, please save it in another file and del it")
        return jsonObj


if __name__ == '__main__':
    import json
    with open("../download/4712/Cell Atlas of Human.json") as f:
        obj = json.load(f)

    article = Article(dataSource="file", record=obj[24])
    article.setDocument()

    print(article)

    # add attr
    article.addValue("test", "Hello World")
    print(article.test)
    try:
        article.addValue("GR", "CN 001")
    except ValueError as e:
        print(e)

    # del attr
    article.delValue("test")
    try:
        print(article.test)
    except AttributeError as e:
        print(e)
    try:
        article.delValue("Journal")
    except ValueError as e:
        print(e)

    # modify attr
    GRValue = article.GR
    print(GRValue)
    article.modifyValue("GR", ["CN 001"])
    print(article.GR)
    article.modifyValue("GR", GRValue)
    try:
        article.modifyValue("Journal", "Nature")
    except ValueError as e:
        print(e)

    # query attr
    print(article.queryValue("MH"))
    print(article.queryValue("MH", ["Humans"]))
    print(article.queryValue("MH", ["It should be False"]))

    print("Article Class Test has been finished successfully.")

