#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: the class for MeSH Analysis
@version: 1.0.0
@file: meshAnalyst.py
@time: 2023/2/21 8:59
"""
import pandas as pd
from bioDAG import MeSHDAG, MeSHTerm


class MeSHAnalyst(object):
    MeSHTermDAG = None

    defaultCategoryDict = {
        "Diseases Category": {
            "categoryList": ["Diseases Category"],
            "removeTermList": ["Disease Models, Animal"]
        },

        "Organ Category": {
            "categoryList": [
                "Cardiovascular System", "Digestive System", "Endocrine System", "Hemic and Immune Systems", "Integumentary System",
                "Musculoskeletal System", "Nervous System", "Respiratory System", "Stomatognathic System","Sense Organs", "Urogenital System",
            ]
        },
    }

    @classmethod
    def setMeSHDAG(cls, meshDAG=None):
        if meshDAG is None:
            cls.MeSHTermDAG = MeSHDAG.returnMeSHDAG()
        else:
            assert isinstance(meshDAG, MeSHDAG), """Error data type has been passed as meshDAG"""
            cls.MeSHTermDAG = meshDAG

    def __init__(self, MeSHDf, MeSHTermCountThreshold=20, majorMeSHTermCountThreshold=5):
        if self.MeSHTermDAG is None:
            print("Start to build MeSH Term DAG")
            self.setMeSHDAG()
            print("Done")

        # MeSH should be returned by ArticleAnalyst.returnYearDistribution("MHDict")
        # MeSH with columns(["MHDict_MeSH Name", "MHDict_Subheading", "MHDict_Major MeSH"])
        self.MeSHDf = MeSHDf
        # self.MeSHs = self.MeSHTermDAG.getTerms(self.MeSHDf["MHDict_MeSH Name"])
        self.MeSHCountDf = self.returnMeSHCountDf(self.MeSHDf, MeSHTermCountThreshold)

        self.majorMeSHDf = MeSHDf.loc[MeSHDf["MHDict_Major MeSH"].fillna(False)]
        # self.majorMeSHs = self.MeSHTermDAG.getTerms(self.majorMeSHDf["MHDict_MeSH Name"])
        self.majorMeSHCountDf = self.returnMeSHCountDf(self.majorMeSHDf, majorMeSHTermCountThreshold)

    # Mapping MeSH into MeSH DAG and get MeSH count dataframe
    @classmethod
    def __mappingMeSH(cls, targetMeSHTerm, resultSeries):
        # MeSHTerm is a series object passed by returnMeSHCountDf and concatMeSHCountDf

        if "depth_{}".format(targetMeSHTerm.depth) not in resultSeries.index:
            resultSeries["depth_{}".format(targetMeSHTerm.depth)] = [targetMeSHTerm.name]
        elif targetMeSHTerm.name not in resultSeries["depth_{}".format(targetMeSHTerm.depth)]:
            resultSeries["depth_{}".format(targetMeSHTerm.depth)] += [targetMeSHTerm.name]
        if targetMeSHTerm.parents:
            for parent in targetMeSHTerm.parents:
                resultSeries = cls.__mappingMeSH(parent, resultSeries)
        return resultSeries

    def returnMeSHCountDf(self, articleMeSHDf, countThreshold):
        """
            For each mesh, get the numbers of article with this mesh, and get the mapping data frame
        """
        articleMeSHDf_DropDuplicates = articleMeSHDf.drop_duplicates(subset=["MHDict_MeSH Name", "PMID"], keep="first")
        MeSHCountDf = pd.DataFrame(articleMeSHDf_DropDuplicates["MHDict_MeSH Name"].value_counts())
        MeSHCountDf.columns = ["count"]
        MeSHCountDf["MeSH Name"] = MeSHCountDf.index
        MeSHCountDf.index = range(0, len(MeSHCountDf))
        MeSHCountDf = MeSHCountDf[["MeSH Name", "count"]]

        MeSHCountDf = MeSHCountDf.loc[MeSHCountDf["count"] > countThreshold]
        MeSHCountDf = MeSHCountDf.T.apply(
            lambda meshCountSeries: self.__mappingMeSH(
                self.MeSHTermDAG.getTerm(meshCountSeries["MeSH Name"]),
                meshCountSeries
            )
        ).T
        sortedCol = sorted(
            MeSHCountDf.columns,
            key=lambda colName: int(colName.split("_")[1]) if "_" in colName else -1
        )
        MeSHCountDf = MeSHCountDf[sortedCol]
        return MeSHCountDf

    def returnMeSHDistributionDf(self, MeSHName, major=True, childDepth=-1, **kwargs):
        """
            For target MeSH, get the MeSH Count Distribution for a specially childDepth descendant MeSHes
            :param major: if use majorMeSHDf
            :param MeSHName: the name of target MeSH
            :param childDepth: the max child depth to return child term
        """

        if major:
            MeSHCountDf = self.majorMeSHCountDf
        else:
            MeSHCountDf = self.MeSHCountDf

        MeSH = self.MeSHTermDAG.getTerm(MeSHName)

        childTerms = MeSH.getTermsByChildDepth(childDepth=childDepth, **kwargs)
        dfTerms = MeSHCountDf["MeSH Name"].apply(lambda meshName: self.MeSHTermDAG.getTerm(meshName))
        selectSeries = dfTerms.apply(
            lambda dfTerm: sum(
                list(map(lambda term: term.isDescendant(dfTerm) and dfTerm.isDescendant(MeSH), childTerms))
            ) > 0
        )
        if selectSeries.sum() == 0:
            print("There is none descendant with depth {} MeSH found for: {}".format(childDepth, MeSH.name))
            return pd.DataFrame([[MeSH.name, 0]], columns=["MeSH Name", "count"])

        MeSHDistributionDf = MeSHCountDf.loc[selectSeries]
        MeSHDistributionDf.index = range(0, len(MeSHDistributionDf))
        return MeSHDistributionDf

    def returnTargetTermSetDict(self, categoryDict=None, major=True):
        def deepSearch(targetTerm):
            if targetTerm.name in resultTermsList and targetTerm.name not in reArrangeTermList:
                reArrangeTermList.append(targetTerm.name)
            if targetTerm.children:
                for child in targetTerm.children:
                    deepSearch(child)

        if major:
            MeSHCountDf = self.majorMeSHCountDf
        else:
            MeSHCountDf = self.MeSHCountDf

        if not categoryDict:
            categoryDict = self.defaultCategoryDict

        resultTermDict = {}
        index = MeSHCountDf["MeSH Name"]

        for interestingCategory in categoryDict:
            resultTermsList = []
            if "categoryList" in categoryDict[interestingCategory]:
                categoryList = categoryDict[interestingCategory]["categoryList"]
                for categoryTermName in categoryList:
                    categoryTerm = self.MeSHTermDAG.getTerm(categoryTermName)
                    resultTermsList += index[
                        index.apply(
                            lambda meshName: self.MeSHTermDAG.getTerm(meshName).isDescendant(categoryTerm)
                        )
                    ].to_list()

                resultTermsList = list(set(resultTermsList))

            if "removeTermList" in categoryDict[interestingCategory]:
                removeTermList = categoryDict[interestingCategory]["removeTermList"]
                for removeTermName in removeTermList:
                    try:
                        resultTermsList.remove(removeTermName)
                    except ValueError:
                        # print("{} not in resultTermsList for this MeSHCountDf.".format(removeTermName))
                        continue

            if "removeCategoryList" in categoryDict[interestingCategory]:
                newResultList = []
                removeCategoryList = categoryDict[interestingCategory]["removeCategoryList"]

                for term in resultTermsList:
                    removeCheck = list(map(
                            lambda ancestorTermName: self.MeSHTermDAG.getTerm(term).isDescendant(
                                self.MeSHTermDAG.getTerm(ancestorTermName)
                            ),
                            removeCategoryList
                    ))
                    if sum(removeCheck) == 0:
                        newResultList.append(term)
                resultTermsList = newResultList

            reArrangeTermList = []

            for categoryTermName in categoryList:
                categoryTerm = self.MeSHTermDAG.getTerm(categoryTermName)
                deepSearch(categoryTerm)

            if "addTermList" in categoryDict[interestingCategory]:
                reArrangeTermList += categoryDict[interestingCategory]["addTermList"]

            resultTermDict[interestingCategory] = reArrangeTermList

        return resultTermDict

    def returnIsInDf(self, MeSHNames, MeSHDf, useDAG=True):
        def selectArticle(articleSubDf, isInDf):
            isInSeries = isInDf.loc[MeSHNames, articleSubDf["MHDict_MeSH Name"]].sum(axis=1) >= 1
            return isInSeries

        if useDAG:
            isInDf = self.MeSHTermDAG.returnIsInDf(MeSHNames, MeSHDf["MHDict_MeSH Name"].unique())
        else:
            isInDf = pd.DataFrame(
                [[False] * len(MeSHDf["MHDict_MeSH Name"].unique())] * len(MeSHNames),
                index=MeSHNames, columns=MeSHDf["MHDict_MeSH Name"].unique(),
            )
            for MeSHName in MeSHNames:
                isInDf.loc[MeSHName, MeSHName] = True

        # reduce the dimension of MeSHSelectDf
        MeSHSelectDf = MeSHDf.loc[
            MeSHDf["MHDict_MeSH Name"].isin(isInDf.columns[isInDf.sum() > 0])
        ]
        selectSeries = MeSHSelectDf.groupby("PMID").apply(lambda articleSubDf: selectArticle(articleSubDf, isInDf))
        return selectSeries

    def returnIsInArticles(self, MeSHNames=[], how="any", major=True, useDAG=True):
        """
        return the articles with target MeSH
        :param MeSHNames: (list of) MeSH name or MeSH term
        :param how: if any, return articles with any MeSH in MeSHNames, if all, return articles with all
        :param major: return articles whose major MeSH was tagged with target MeSH
        :param useDAG: whether to use DAG structure to map MeSH
        :return:
        """
        assert how in ["any", "all"], """how should be one of ['any', 'all']"""

        if isinstance(MeSHNames, (str, MeSHTerm)):
            MeSHNames = [MeSHNames]
        MeSHNames = [MeSHName if isinstance(MeSHName, str) else MeSHName.name for MeSHName in MeSHNames]
        mappingDf = self.majorMeSHDf if major else self.MeSHDf
        MeSHSelectDf = mappingDf.drop_duplicates(subset=["PMID", "MHDict_MeSH Name"], keep="first")

        selectSeries = self.returnIsInDf(MeSHNames, MeSHSelectDf, useDAG).sum(axis=1)
        if how == "any":
            return selectSeries.loc[selectSeries > 0].index.to_list()
        else:
            return selectSeries.loc[selectSeries == len(MeSHNames)].index.to_list()

    def searchSubheadings(self, subheadings, major=True):
        if isinstance(subheadings, str):
            subheadings = [subheadings]

        def searchSubheading(subheading):
            resultDf = searchDf.loc[searchDf["MHDict_Subheading"] == subheading]
            articleNum = len(resultDf["PMID"].unique())
            resultDf = pd.DataFrame(resultDf["MHDict_MeSH Name"].value_counts())
            resultDf.columns = ["count"]
            resultDf["subheading"] = subheading
            resultDf["MeSH Name"] = resultDf.index
            resultDf = resultDf[["subheading", "MeSH Name", "count"]]
            return resultDf, articleNum

        searchDf = self.majorMeSHDf if major else self.MeSHDf
        searchResults = list(map(lambda subheading: searchSubheading(subheading), subheadings))
        return [
            pd.concat([searchResult[0] for searchResult in searchResults]),
            [searchResult[1] for searchResult in searchResults]
        ]

    @classmethod
    def concatMeSHCountDf(cls, meshCountDfList, weightList=None):
        if not weightList:
            weightList = [1] * len(meshCountDfList)

        assert len(meshCountDfList) == len(weightList), """The length of weightList should be equal to meshCountList"""

        indexSeries = []
        resultSeries = pd.Series([], name="count", dtype="float64")
        for index in range(0, len(meshCountDfList)):
            MeSHDf = meshCountDfList[index]
            MeSHDf.index = MeSHDf["MeSH Name"]

            weight = weightList[index]

            indexSeries = list(set(indexSeries) | set(MeSHDf.index))
            zeroSeries = pd.Series([0] * len(indexSeries), index=indexSeries)

            resultSeries = zeroSeries + resultSeries
            resultSeries.fillna(0, inplace=True)

            zeroSeries = zeroSeries + MeSHDf["count"] * weight
            zeroSeries.fillna(0, inplace=True)

            resultSeries += zeroSeries

        MeSHCountDf = pd.DataFrame(resultSeries, columns=["count"])
        MeSHCountDf["MeSH Name"] = MeSHCountDf.index
        MeSHCountDf.sort_values(by="count", ascending=False, inplace=True)
        MeSHCountDf.index = range(0, len(MeSHCountDf))

        MeSHCountDf = MeSHCountDf.T.apply(
            lambda meshCountSeries: cls.__mappingMeSH(
                cls.MeSHTermDAG.getTerm(meshCountSeries["MeSH Name"]),
                meshCountSeries
            )
        ).T
        sortedCol = sorted(
            MeSHCountDf.columns,
            key=lambda colName: int(colName.split("_")[1]) if "_" in colName else -1
        )
        MeSHCountDf = MeSHCountDf[sortedCol]
        return MeSHCountDf


if __name__ == '__main__':
    from ArticleAnalyst import ArticleAnalyst

    articleAnalyst = ArticleAnalyst(
        dataSource="file", filePath="../download/test/HCM.json"
    )

    meshAnalyst = articleAnalyst.returnMeSHAnalyst(countThreshold=100, majorCountThreshold=100)
    meshAnalyst.searchSubheadings("genetics")
    meshAnalyst.returnMeSHDistributionDf("Carrier Proteins")
    meshAnalyst.returnMeSHDistributionDf("Carrier Proteins", childDepth=1)

    meshAnalyst.returnIsInArticles("CD36 Antigens")
    print("?")


