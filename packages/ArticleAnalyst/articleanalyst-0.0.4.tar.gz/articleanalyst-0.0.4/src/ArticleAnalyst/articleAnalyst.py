#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: 
@version: 1.0.0
@file: articleAnalyst.py
@time: 2023/2/15 10:59
"""
import json
import os
import math

import time

import numpy as np
import pandas as pd
import networkx as nx

from scipy.stats import fisher_exact
from statsmodels.stats.multitest import fdrcorrection

from .function.article import Article
from .function.downloader import Downloader
from .function.meshAnalyst import MeSHAnalyst
from .function.annotation import NERAnnotation


class AnnotationNodeManager(object):

    def __init__(self, **kwargs):
        self.nodeId = 0
        self.allNodeList = []
        self.refDict = {}
        equalInfo = kwargs.get("equalInfo", None)
        if equalInfo:
            index = 0
            for equalList in equalInfo:
                self.refDict[index] = equalList[0]
                for word in equalList:
                    self.refDict[word] = index
                index += 1

    def returnNode(self, annotation):
        for refNode in self.allNodeList:
            if self.equal(refNode, annotation):
                return refNode
        return False

    def check(self, annotationNode):
        # if annotationNode.text == "NBP":
        #     # print(annotationNode)
        #     pass
        recordNode = self.returnNode(annotationNode)
        if recordNode:
            if annotationNode.text not in recordNode.synon:
                recordNode.synon.append(annotationNode.text)
            recordNode.num += 1
            return True
        self.nodeId += 1
        self.allNodeList.append(annotationNode)
        return False

    def addNode(self, annotation):
        annotationNode = AnnotationNode(annotation, nodeId=self.nodeId)
        return self.check(annotationNode)

    @staticmethod
    def getIdentifier(node):
        if isinstance(node, NERAnnotation):
            text = node.getValue("text")
            id = node.getValue("id")
        elif isinstance(node, AnnotationNode):
            text = node.text
            id = node.id
        elif isinstance(node, str):
            text = node
            id = None
        else:
            raise TypeError("node shoube be NERAnnotation, AnnotationNode or string")
        return text, id

    def equal(self, node1, node2):
        text1, id1 = AnnotationNodeManager.getIdentifier(node1)
        text2, id2 = AnnotationNodeManager.getIdentifier(node2)
        try:
            if self.refDict[text1] == self.refDict[text2]:
                return True
        except KeyError:
            if (id1 and id2) and id1 == id2:
                return True
            return text1 == text2


class AnnotationNode(object):

    def __init__(self, annotation, nodeId):
        self.nodeId = nodeId
        self.id = annotation.getValue("id")
        self.text = annotation.getValue("text")
        self.obj = annotation.getValue("obj")
        self.synon = [self.text]
        self.num = 1

    def __repr__(self):
        return "AnnotationNode(nodeId: {}, text: {})".format(self.nodeId, self.text)

    def __str__(self):
        return "AnnotationNode(nodeId: {}, text: {})".format(self.nodeId, self.text)


class ArticleSet(object):

    def __init__(self, dataSource, **kwargs):
        if dataSource == "query":
            records = kwargs["records"]
            self.articles = self.__setArticles(dataSource=dataSource, records=records)
        elif dataSource == "file":
            filePath = kwargs["filePath"]
            with open(filePath, "r") as f:
                records = json.load(f)
            self.articles = self.__setArticles(dataSource=dataSource, records=records)
        elif dataSource == "self":
            articles = kwargs["articles"]
            self.articles = articles
        else:
            raise ValueError("Unexpect dataSource received: {}".format(dataSource))

        self.index = self.articles.index

    @staticmethod
    def __setArticles(dataSource, records):
        articleSeries = pd.Series(
            list(map(
                lambda record: Article(dataSource, record) if "PMID" in record else None, records
            ))
        )
        articleSeries.dropna(inplace=True)
        articleSeries.drop_duplicates(keep="first", inplace=True)
        articleSeries.index = articleSeries.apply(lambda article: article.PMID).tolist()
        return articleSeries

    def __update(self, newArticles):
        self.articles = newArticles
        self.index = self.articles.index

    def __len__(self):
        return len(self.articles)

    def __iter__(self):
        return self.articles.__iter__()

    def __contains__(self, item):
        if isinstance(item, Article):
            return item.\
                       PMID in self.index
        else:
            return item in self.index

    def __repr__(self):
        return "ArticleSet({})".format(len(self))

    def __str__(self):
        return "ArticleSet({})".format(len(self))

    def getArticle(self, pmid):
        if isinstance(pmid, str):
            return self.articles[pmid]
        else:
            raise ValueError("pmid should be a string")

    def getArticles(self, pmid):
        if isinstance(pmid, str):
            pmid = [pmid]
        elif isinstance(pmid, (pd.Series, pd.Index)):
            pmid = pmid.tolist()
        articles = self.articles[self.articles.index.isin(pmid)]
        if len(articles) == 0:
            print("There is not article found by: {}".format(pmid))
        return articles

    def queryArticles(self, attrList):
        if isinstance(attrList, str):
            attrList = [attrList]
        return pd.DataFrame(
            list(map(lambda article: article.getValue(attrList), self)),
            index=self.index
        )

    @classmethod
    def concat(cls, concatObjs, identifierList=None, colAdded="identifier"):
        if identifierList:
            assert len(identifierList) == len(concatObjs), \
                """The len of 'concatObjs' should be equal to 'identifierList'"""

            for concatObj, identifier in zip(concatObjs, identifierList):
                concatObj.articles.apply(lambda article: article.addValue(colAdded, identifier))

        newArticles = pd.concat(list(map(lambda concatObj: concatObj.articles, concatObjs)))
        return cls(dataSource="self", articles=newArticles)


class ArticleAnalyst(ArticleSet):
    dimensionDAGs = []
    downloader = None

    @classmethod
    def setDownloader(cls, email):
        cls.downloader = Downloader(email)

    def __init__(self, dataSource="query", **kwargs):
        if self.downloader is None and dataSource == "query":
            email = kwargs["email"]
            self.setDownloader(email)

        if "savePath" in kwargs:
            self.setSavePath(kwargs["savePath"])

        if dataSource == "query":
            query = kwargs["query"]
            kwargs["records"] = self.__download(query)
        super().__init__(dataSource=dataSource, **kwargs)

        if dataSource == "query" and kwargs.get("save", False):
            fileName = kwargs.get("fileName", query)
            self.save(savePath=os.path.join(self.saveDir, "{}.json".format(fileName)))
        self.MeSHAnalyst = None
        print("{} articles have been loaded successfully".format(len(self)))

        saveDir = kwargs.get("saveDir", os.path.join(os.getcwd(), "Output"))
        if not os.path.exists(saveDir):
            os.mkdir(saveDir)
        self.saveDir = saveDir

    @classmethod
    def setSavePath(cls, storeDir):
        if not os.path.exists(storeDir):
            print("Create dir: {}".format(storeDir))
            os.mkdir(storeDir)
        if not os.path.samefile(cls.saveDir, storeDir):
            print("Change save path to: {}".format(storeDir))
            cls.saveDir = storeDir

    def __update(self, newArticles):
        self.articles = newArticles
        self.index = self.articles.index

    def __download(self, query):
        print("Start download articles for query: {}".format(query))
        records, failedUrl = self.downloader.download(query)
        return records

    def save(self, savePath):
        jsonObject = list(map(lambda article: article.toJson(), self))
        with open(savePath, "w") as f:
            json.dump(jsonObject, f)

    def dropNa(self, subset, how="any", inplace=False):
        """
        drop articles without attr in attrNameList
        """
        if isinstance(subset, str):
            subset = [subset]

        selectDf = self.queryArticles(subset)
        selectIndex = selectDf.dropna(subset=subset, how=how, inplace=False).index
        newArticles = self.getArticles(selectIndex)
        if inplace:
            self.__update(newArticles)
        else:
            return ArticleAnalyst(dataSource="self", articles=newArticles)

    def search(self, how="any", inplace=False, include=True, **kwargs):
        """
        search article follows kwargs
        by default, it will drop articles without attr in attrNameList
        kwargs should follow: attrName=[(opt, v2), ......,(opt, v2)], indicating the value of attrName opt v2,
        options include ">=", "<=", "<", ">", "!=", "==", "in", "contains"
        :param include: if true, return target article, else drop target article
        :param how:
            'any': if any attrs value pass the comparison, drop this article
            'all': if all attrs value pass the comparison, drop this article
        :param inplace: if True, do operation inplace and return None.
        :return:
        """
        if how not in ["all", "any"]:
            raise ValueError("invalid how option: {}".format(how))

        subset = []
        for attrName in kwargs.keys():
            subset.append(attrName)
        selectDf = self.queryArticles(subset)
        selectDf.dropna(subset=subset, how="any", inplace=True)

        switchDict = {
            ">=": lambda colName, value: selectDf[colName] >= value,
            "<=": lambda colName, value: selectDf[colName] <= value,
            ">": lambda colName, value: selectDf[colName] > value,
            "<": lambda colName, value: selectDf[colName] < value,
            "!=": lambda colName, value: selectDf[colName] != value,
            "==": lambda colName, value: selectDf[colName] == value,
            "in": lambda colName, value: selectDf[colName].isin(value),
            "contains": lambda colName, value: selectDf[colName].apply(
                lambda colValue: value in colValue
            ),
            "get": lambda colName, key: selectDf[colName].apply(
                lambda colValue: colValue[key]
            ),
        }

        if how == "any":
            selectSeries = [False] * len(selectDf)
        else:
            selectSeries = [True] * len(selectDf)

        for attrName, expressions in kwargs.items():
            for expression in expressions:
                option, v1 = expression[0], expression[1]
                if option == "get":
                    getSeries = switchDict[option](attrName, v1)
                    attrName = "{}_{}".format(attrName, v1)
                    selectDf[attrName] = getSeries
                    continue
                if how == "any":
                    selectSeries = selectSeries | switchDict[option](attrName, v1)
                else:
                    selectSeries = selectSeries & switchDict[option](attrName, v1)

        selectSeries = selectSeries if include else ~selectSeries
        newArticles = self.getArticles(selectDf.loc[selectSeries].index)
        if inplace:
            self.__update(newArticles)
        else:
            return ArticleAnalyst(dataSource="self", articles=newArticles)

    def returnYearDistribution(self, attrList, dropNa=False, how="all"):
        if isinstance(attrList, str):
            attrList = [attrList]

        if "Year" not in attrList:
            attrList = ["Year"] + attrList

        if "PMID" not in attrList:
            attrList = ["PMID"] + attrList

        queryDf = self.queryArticles(attrList)
        queryDf.index = range(0, len(queryDf))
        if dropNa:
            queryDf.dropna(subset=attrList, how=how)

        again = True
        while again:
            again = False

            typeList = [None] * len(attrList)
            for attr in attrList:
                if len(queryDf[attr].dropna()) == 0:
                    raise ValueError("None article contains {}".format(attr))
                for attrValue in queryDf[attr].dropna():
                    typeList[attrList.index(attr)] = type(attrValue)

            checkList = []
            for attr, attrType in zip(attrList, typeList):
                if attrType == list:
                    queryDf = queryDf.explode(attr)
                    queryDf.index = range(0, len(queryDf))

                    again = True
                    checkList.append(attr)
                elif attrType == dict:
                    expandDf = queryDf[attr].dropna().apply(pd.Series)
                    expandDf.columns = list(map(lambda expandCol: "{}_{}".format(attr, expandCol), expandDf.columns))

                    concatCols = queryDf.columns.to_list()
                    concatCols.remove(attr)
                    queryDf = pd.concat([queryDf[concatCols], expandDf], axis=1)

                    again = True
                    checkList += expandDf.columns.to_list()
                else:
                    continue

            attrList = checkList

        return queryDf

    def getCit(self, saveAttr="cit", inArticles=False, simplified=True, email=None):
        """
        return the citation graph of article in articleSet, in which edge points to the article cited
        :param saveAttr: the attr to save cit information
        :param inArticles: if true, article not in articleSet will be dropped
        :param simplified: if true, article whose degree is equal to 0 will be dropped
        :param email: the email to connect with PubMed database
        :return:
        """
        if self.downloader is None:
            self.setDownloader(email=email)

        if not isinstance(saveAttr, str):
            raise TypeError("only str can be passed as saveAttr")

        queryDf = self.queryArticles(saveAttr)
        if queryDf["cit"].isna().sum() == 0:
            print("All article has get citation information.")
        else:
            # self.search()
            citResult, failedUrl = self.downloader.returnCit(ids=queryDf.index.tolist())

            self.articles.apply(
                lambda article: article.addValue("cit", citResult[article.PMID])
            )

        G = nx.DiGraph()
        G.add_nodes_from(self.index.to_list(), inArticles=True)
        self.articles.apply(lambda article: G.add_edges_from(
            list(map(lambda citArticle: (citArticle, article.PMID), article.__getattribute__(saveAttr)))
        ))

        if inArticles:
            removeNodes = set(G.nodes) - set(self.index)
            G.remove_nodes_from(removeNodes)

        if simplified:
            list(map(lambda node: G.remove_node(node) if G.degree(node) == 0 else False, list(G.nodes)))

        return G

    def __repr__(self):
        return "ArticleAnalyst({})".format(len(self))

    def __str__(self):
        return "ArticleAnalyst({})".format(len(self))

    def returnMeSHAnalyst(self, countThreshold=20, majorCountThreshold=5):
        import warnings
        warnings.warn(
            "returnMeSHAnalyst will be replaced with setMeSHAnalyst, and you can access the result by self.MeSHAnalyst"
        )
        MeSHDf = self.returnYearDistribution(["MHDict"])
        return MeSHAnalyst(MeSHDf, countThreshold, majorCountThreshold)

    def setMeSHAnalyst(self, MeSHDf=None, countThreshold=20, majorCountThreshold=5):
        if MeSHDf is None:
            MeSHDf = self.returnYearDistribution(["MHDict"])
        self.MeSHAnalyst = MeSHAnalyst(MeSHDf, countThreshold, majorCountThreshold)

    def returnMeSHYearCounts(self, meshTerm, major=True, **kwargs):
        """
            return the Year-Count Df for target MeSH term
        :param meshTerm: target MeSH term, a MeSH term name or a MeSHTerm object
        :param major: return articles whose major MeSH was tagged with target MeSH
        :param kwargs: any parameters used in MeSHAnalyst.returnIsInArticles
        :return: a count series
        """
        if not self.MeSHAnalyst:
            self.setMeSHAnalyst()
        meshAnalyst = self.MeSHAnalyst

        meshTerm = meshAnalyst.MeSHTermDAG.getTerm(meshTerm)
        # if (major and meshTerm not in meshAnalyst.majorMeSHs) or (not major and meshTerm not in meshAnalyst.MeSHs):
        #     return pd.Series([], name=meshTerm.name)
        articles = meshAnalyst.returnIsInArticles(meshTerm, major=major, **kwargs)
        years = [self.articles[article].Year for article in articles]
        yearCounts = pd.Series(years).value_counts()
        yearCounts.name = meshTerm.name
        return yearCounts

    def setDimensions(self, dimensions, returnDimensions=True):
        def returnAdjMatrix(dagObj):
            adjMatrix = pd.DataFrame(
                [],
                index=[term.name for term in dagObj.terms],
                columns=[term.name for term in dagObj.terms]
            )
            for term in dagObj.terms:
                adjMatrix.loc[term.name, [child.name for child in term.children]] = 1
                adjMatrix.loc[term.name, term.name] = 0

            adjMatrix = adjMatrix.fillna(0)
            return adjMatrix

        if not isinstance(dimensions, (list, pd.Series, set, tuple)):
            dimensions = [dimensions]

        self.dimensionDAGs = pd.Series()
        for dimensionDAG in dimensions:
            dimensionDAG = self.MeSHAnalyst.MeSHTermDAG.getSub(dimensionDAG)
            g = nx.from_pandas_adjacency(returnAdjMatrix(dimensionDAG), create_using=nx.DiGraph())

            root = dimensionDAG.root
            self.dimensionDAGs[root.name] = g

        if returnDimensions:
            return self.dimensionDAGs

    def projectArticles(self, dimensions, keyAdded, major=True, force=True):
        """
            project articles in an embedding with a series of subDAG graph
        :param dimensions: a collection of MeSHTern|MeSHTerm Name|MeSHDAG
        :param keyAdded: the key name to store subDAG information
        :param major: whether to use major MeSh
        :param force: if key existed in article, whether to replace, not works if store=True
        :return:
        """

        def returnEditGraph(g, rootName, terms):
            # def getGraph(node):
            #     if g.nodes[node]["is_sub"] is None:
            #         setGraph(node)
            #     return g.nodes[node]["is_sub"]
            #
            # def setGraph(node):
            #     if node in terms:
            #         g.nodes[node]["is_sub"] = True
            #     elif len(g.edges(node)) == 0:
            #         g.nodes[node]["is_sub"] = False
            #
            #     else:
            #         checkResult = False
            #         for edges in g.edges(node):
            #             checkResult = checkResult or getGraph(edges[1])
            #         g.nodes[node]["is_sub"] = checkResult
            #
            # nx.set_node_attributes(g, None, "is_sub")
            # setGraph(rootName)

            paths = list(nx.all_simple_paths(g, source=rootName, target=terms))
            allNodes = []
            for path in paths:
                allNodes += path
            # allNodes = [node for node in g.nodes if g.nodes[node]["is_sub"]]
            editGraph = nx.subgraph(g, list(set(allNodes)))
            return editGraph

        def projectArticle(article):
            if major:
                meshList = article.majorMHList
            else:
                meshList = article.MHList

            meshList = self.MeSHAnalyst.MeSHTermDAG.getTerms(meshList)
            rootList = list(dimensionDAGs.index)
            isinDf = self.MeSHAnalyst.MeSHTermDAG.returnIsInDf(ancestors=rootList, descendants=meshList)

            try:
                article.addValue("{}_dimension".format(keyAdded), [])
            except ValueError as e:
                if force:
                    article.modifyValue(
                        "{}_dimension".format(keyAdded),
                        []
                    )
                else:
                    raise ValueError(e)

            dimensionGraphs = {}
            for dag, rootName in zip(dimensionDAGs, dimensionDAGs.index):
                dimensionTerm = list(isinDf.columns[isinDf.loc[rootName]])

                editGraph = returnEditGraph(dag, rootName, dimensionTerm)
                storeDAG = nx.to_dict_of_lists(editGraph)
                dimensionGraphs[rootName] = storeDAG

            try:
                article.addValue("{}_dimension".format(keyAdded), dimensionGraphs)
            except ValueError as e:
                if force:
                    article.modifyValue(
                        "{}_dimension".format(keyAdded),
                        dimensionGraphs
                    )
                else:
                    raise ValueError(e)

            else:
                return dimensionGraphs

        if not self.MeSHAnalyst:
            self.setMeSHAnalyst()

        dimensionDAGs = self.setDimensions(dimensions, returnDimensions=True)
        dimensionSeries = self.articles.apply(lambda article: projectArticle(article))
        return dimensionSeries

    def returnEmbeddingDf(self, meshEmbeddingDf, major=True, useWeight=False, drop_duplicated=True):
        if not self.MeSHAnalyst:
            self.setMeSHAnalyst()
        meshAnalyst = self.MeSHAnalyst
        meshDf = meshAnalyst.majorMeSHDf if major else meshAnalyst.MeSHDf

        MHs = list(set(meshDf["MHDict_MeSH Name"].unique()) & set(meshEmbeddingDf.index))
        meshDf = meshDf.loc[meshDf["MHDict_MeSH Name"].isin(MHs)].copy()
        meshEmbeddingDf = meshEmbeddingDf.loc[MHs]

        # for big data, it may cause ValueError: Unstacked DataFrame is too big, causing int32 overflow
        try:
            weights = pd.crosstab(meshDf["PMID"], meshDf["MHDict_MeSH Name"])
        except ValueError:
            articleStep = 10000
            subArticles = np.array_split(self.articles.index, len(self) // articleStep)
            subMeSHDfs = [
                meshDf.loc[meshDf["PMID"].isin(articles)] for articles in subArticles
            ]
            weights = list(map(
                lambda subMeSHDf: pd.crosstab(subMeSHDf["PMID"], subMeSHDf["MHDict_MeSH Name"]), subMeSHDfs
            ))
            weights = pd.concat(weights)

        weights = weights.fillna(0)
        if not useWeight:
            weights = weights > 0
        weights = weights[MHs]

        embeddingDf = weights.values.dot(meshEmbeddingDf.values)
        embeddingDf = pd.DataFrame(embeddingDf, index=weights.index)
        embeddingDf = (embeddingDf.T / weights.sum(axis=1)).T
        if drop_duplicated:
            embeddingDf.drop_duplicates(keep="first", inplace=True)
        return embeddingDf

    def returnDistanceMatrix(self, reference, normalization=True):
        row = []
        for i, article in zip(range(0, len(self)), self.articles):
            col = []
            for j, other in zip(range(0, len(self)), self.articles):
                if i <= j:
                    col.append(article.returnArticleDistance(other, reference=reference))
                else:
                    col.append(row[j][i])
            row.append(col)

        distanceMatrix = np.array(row)
        if normalization:
            maxValue = distanceMatrix.max(axis=0).max(axis=0)
            minValue = distanceMatrix.min(axis=0).min(axis=0)
            distanceMatrix = (distanceMatrix - minValue) / (maxValue - minValue)

        return distanceMatrix.sum(axis=2)

    def returnMeSHsYearCounts(self, meshTerms, major=True, **kwargs):
        """
            return the Year-Count Df for target MeSH terms
        :param meshTerms: target MeSH terms
        :param major: return articles whose major MeSH was tagged with target MeSH
        :param kwargs: any parameters used in MeSHAnalyst.returnIsInArticles
        :return: a count dataframe with columns = MeSH Name, index = Year
        """
        if not self.MeSHAnalyst:
            self.setMeSHAnalyst()
        meshAnalyst = self.MeSHAnalyst

        assert len(meshTerms) == len(meshAnalyst.MeSHTermDAG.simplyTerms(meshTerms)[0]), """
            there is overlap between MeSHTerms: {}.
        """.format(meshTerms)

        yearCounts = pd.concat(
            [self.returnMeSHYearCounts(meshTerm, major=major, **kwargs) for meshTerm in meshTerms],
            axis=1
        )
        yearCounts = yearCounts.fillna(0)
        return yearCounts

    def enrichmentAnalysis(self, other, root, major=True, FCThreshold=2):

        def returnObservedDf(aaObj):
            if not aaObj.MeSHAnalyst:
                raise AttributeError("There is non MeSHAnalyst found, please run setMeshAnalyst firstly!")
            countDf = aaObj.MeSHAnalyst.majorMeSHCountDf if major else aaObj.MeSHAnalyst.MeSHCountDf
            countDf = countDf.loc[
                countDf["MeSH Name"].apply(
                    lambda termName:  aaObj.MeSHAnalyst.MeSHTermDAG.getTerm(termName).isDescendant(root)
                )
            ]
            observedDf = pd.DataFrame(
                countDf["count"].to_list(),
                index=countDf["MeSH Name"].to_list(), columns=["observed"]
            )
            observedDf["ratio"] = observedDf["observed"]/(observedDf["observed"].sum())
            return observedDf

        def returnControl(targetTerm, passedP, rootTerm, resultDict):
            isDescendantSum = sum([child.isDescendant(rootTerm) for child in targetTerm.children]) + 1
            averageP = passedP / isDescendantSum
            resultDict[targetTerm.name] = resultDict.get(targetTerm.name, 0) + averageP
            for child in targetTerm.children:
                if child.isDescendant(rootTerm):
                    resultDict = returnControl(child, averageP, rootTerm, resultDict)
            return resultDict

        meshTermDAG = MeSHAnalyst.MeSHTermDAG
        if isinstance(root, str):
            root = meshTermDAG.getTerm(root)
        subMeSHTermDAG = meshTermDAG.getSub(root)
        termNumber = len(subMeSHTermDAG.terms)

        targetDf = returnObservedDf(self)
        if isinstance(other, str) and other == "background":
            otherDf = pd.DataFrame.from_dict(returnControl(root, 1, root, {}), orient='index')
            otherDf.columns = ["P"]
            otherDf["observed"] = targetDf["observed"].sum() * otherDf["P"]
        elif isinstance(other, ArticleAnalyst):
            otherDf = returnObservedDf(other)

        mergeDf = pd.merge(
            left=targetDf, right=otherDf,
            left_on=targetDf.index, right_on=otherDf.index,
            how="outer", suffixes=("_target", "_other")
        )
        mergeDf.fillna(0, inplace=True)
        mergeDf.set_index("key_0", inplace=True)
        mergeDf.index.name = "MeSH Name"
        mergeDf = mergeDf.loc[(mergeDf["ratio_target"] > FCThreshold * mergeDf["ratio_other"])]
        upTermList = mergeDf.index.to_list()

        def calculatedP_fisher(targetTerm):
            relatedTerms = subMeSHTermDAG.terms.loc[
                subMeSHTermDAG.terms.apply(lambda term: term.isDescendant(targetTerm))
            ]
            relatedTermsList = relatedTerms.index.to_list()
            # fisher dataframe
            a = len(set(upTermList) & set(relatedTermsList))
            b = len(upTermList) - a
            c = len(relatedTermsList) - a
            d = termNumber - a - b - c
            fisher_exactArray = np.array([[a, b], [c, d]])
            odd, p = fisher_exact(fisher_exactArray, alternative="greater")
            return targetTerm.name, p, (set(upTermList) & set(relatedTermsList)), a, a / len(relatedTermsList)

        def returnEnrichmentResult(target, result=[]):
            if target.isDescendant(root):
                result.append(calculatedP_fisher(targetTerm=target))
                for child in target.children:
                    result = returnEnrichmentResult(child, result)
            return result

        resultDfData = returnEnrichmentResult(root, [])
        resultDf = pd.DataFrame(resultDfData, columns=["Term Name", "P", "Hit Term", "Hit Term Number", "Fraction"])
        resultDf.sort_values(by="P", inplace=True)
        resultDf.drop_duplicates(subset=["Term Name"], inplace=True)

        rejected, pvalue_corrected = fdrcorrection(resultDf["P"], is_sorted=True)
        resultDf["P"] = pvalue_corrected
        resultDf["-lgP"] = resultDf["P"].apply(lambda P: - math.log10(P))
        return resultDf, mergeDf

    def associationAnalysis(self, rowCategories, colCategories, major=True, minCount=5):
        """
        :param rowCategories: list of MeSH name or MeSH term
        :param colCategories: list of MeSH name or MeSH term
        :param major: return articles whose major MeSH was tagged with target MeSH
        :return:
        """
        if not self.MeSHAnalyst:
            self.setMeSHAnalyst()

        useDAG = True

        rowCategories = [
            rowCategory if isinstance(rowCategory, str) else rowCategory.name for rowCategory in rowCategories
        ]
        colCategories = [
            colCategory if isinstance(colCategory, str) else colCategory.name for colCategory in colCategories
        ]
        pDf = pd.DataFrame([], index=rowCategories, columns=colCategories, dtype="float")
        countDf = pd.DataFrame([], index=rowCategories, columns=colCategories, dtype="float")
        if major:
            MeSHDf = self.MeSHAnalyst.majorMeSHDf.drop_duplicates(subset=["PMID", "MHDict_MeSH Name"], keep="first")
        else:
            MeSHDf = self.MeSHAnalyst.MeSHDf.drop_duplicates(subset=["PMID", "MHDict_MeSH Name"], keep="first")

        isInDf = self.MeSHAnalyst.returnIsInDf(
            list(set(rowCategories + colCategories)), MeSHDf, useDAG
        )

        for rowCategory in rowCategories:
            # rowArticle = self.MeSHAnalyst.returnIsInArticles(rowCategory, major=major, useDAG=useDAG)
            rowArticle = isInDf[rowCategory]
            for colCategory in colCategories:
                # colArticle = self.MeSHAnalyst.returnIsInArticles(colCategory, major=major, useDAG=useDAG)
                colArticle = isInDf[colCategory]
                a = (rowArticle & colArticle).sum()
                b = rowArticle.sum() - a
                c = colArticle.sum() - a
                d = len(self) - (a + b + c)

                fisher_exactArray = np.array([[a, b], [c, d]])
                odd, p = fisher_exact(fisher_exactArray, alternative="greater")

                pDf.loc[rowCategory, colCategory] = p if a >= minCount else 1
                countDf.loc[rowCategory, colCategory] = a
        return pDf, countDf
