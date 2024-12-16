#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Shi4712
@description: class and functions to download articles from PubMed
@version: 1.0.0
@file: downloader.py
@time: 2023/2/15 9:35
"""
import http
import time
import urllib

from Bio import Entrez, Medline


class Downloader(object):
    rangeLevel = ["None", "Century", "Decade", "Year", "Month", "TenDay"]
    maxTry = 5

    def __init__(self, pubmed_email):
        Entrez.email = pubmed_email
        self.failedRequest = []

    def download(self, query, **kwargs):
        self.failedRequest = []
        records = self.returnBatchRecords(query, **kwargs)
        return records, self.failedRequest

    # def download_failedRequest(self, query, failedRequest):
    def __eSearch(self, query, tryTime=0, **kwargs):
        try:
            handle = Entrez.esearch(
                term=query, db='pubmed', datetype="edat", usehistory='y', **kwargs
            )
            time.sleep(0.5)
        except urllib.error.HTTPError:
            if tryTime > self.maxTry:
                kwargs["query"] = query
                self.failedRequest.append(kwargs)
                return False
            else:
                time.sleep(0.5)
                return self.__eSearch(query, tryTime=tryTime+1, **kwargs)
        results = Entrez.read(handle)
        handle.close()
        return results

    def __eFetch(self, results, tryTime=0, **kwargs):
        webenv = results['WebEnv']
        query_key = results['QueryKey']

        try:
            handle = Entrez.efetch(
                db='pubmed', rettype='medline', retmode='text',
                webenv=webenv, query_key=query_key,
                **kwargs
            )
            time.sleep(1)
        except urllib.error.HTTPError:
            if tryTime > self.maxTry:
                kwargs["results"] = results
                self.failedRequest.append(kwargs)
                return [{}]
            else:
                time.sleep(1)
                return self.__eFetch(results, tryTime=tryTime+1, **kwargs)
        try:
            return list(Medline.parse(handle))
        except (http.client.IncompleteRead, urllib.error.HTTPError):
            time.sleep(1)
            return self.__eFetch(results, tryTime=tryTime+1, **kwargs)

    def __eLink(self, ids, db, LinkName, tryTime=0, **kwargs):
        try:
            handle = Entrez.elink(
                dbfrom="pubmed", db=db, LinkName=LinkName, id=ids
            )
            time.sleep(1)
        except urllib.error.HTTPError:
            if tryTime > self.maxTry:
                kwargs["ids"] = ids
                kwargs["LinkName"] = LinkName
                kwargs["db"] = LinkName
                self.failedRequest.append(kwargs)
                return [{}]
            else:
                time.sleep(1)
                return self.__eLink(ids, db, LinkName, tryTime=tryTime+1, **kwargs)

        results = Entrez.read(handle)
        handle.close()
        return results


    @staticmethod
    def __returnDateParameters(currentStart, currentEnd, end, step, modify, year="1900", month="01", day="01"):
        dateParameters = []
        while currentStart < end:
            if modify == "year":
                addDateParameters = [
                    "{}/{}/{}".format(currentStart, month, day), "{}/{}/{}".format(currentEnd, month, day)
                ]
            elif modify == "month":
                addDateParameters = [
                    "{}/{}/{}".format(year, currentStart, day), "{}/{}/{}".format(year, currentEnd, day)
                ]
            else:
                addDateParameters = [
                    "{}/{}/{}".format(year, month, currentStart), "{}/{}/{}".format(year, month, currentEnd)
                ]

            dateParameters.append(addDateParameters)
            currentStart = currentEnd
            currentEnd += step
        return dateParameters

    def returnBatchRecords(self, query, start=None, end=None, level=0):
        if not end:
            end = time.strftime("%Y/%m/%d")
        if not start:
            start = "1900/01/01"

        dateParameters = []
        if Downloader.rangeLevel[level] == "None":
            dateParameters.append([start, end])
        elif Downloader.rangeLevel[level] in ["Century", "Decade", "Year"]:
            end = int(end.split("/")[0])
            currentStart = int(start.split("/")[0])
            switchDict = {
                "Century": 100,
                "Decade": 10,
                "Year": 1
            }
            step = switchDict[Downloader.rangeLevel[level]]
            currentEnd = (int(currentStart / step) + 1) * step
            dateParameters = self.__returnDateParameters(
                currentStart=currentStart, currentEnd=currentEnd,
                end=end, step=step, modify="year",
                month="01", day="01"
            )
        elif Downloader.rangeLevel[level] == "Month":
            end = 12
            currentStart = 1
            currentEnd = 2
            step = 1
            dateParameters = self.__returnDateParameters(
                currentStart=currentStart, currentEnd=currentEnd,
                end=end, step=step, modify="month",
                year=start.split("/")[0], day="01"
            )
            dateParameters.append(
                [
                    "{}/{}/{}".format(start.split("/")[0], 12, "01"),
                    "{}/{}/{}".format(int(start.split("/")[0]) + 1, 1, "01")
                ]
            )
        elif Downloader.rangeLevel[level] == "TenDay":
            end = 20
            currentStart = 1
            currentEnd = 11
            step = 10
            dateParameters = self.__returnDateParameters(
                currentStart=currentStart, currentEnd=currentEnd,
                end=end, step=step, modify="day",
                year=start.split("/")[0], month=start.split("/")[1],
            )
            if int(start.split("/")[1]) == 12:
                dateParameters.append(
                    [
                        "{}/{}/{}".format(start.split("/")[0], start.split("/")[1], "21"),
                        "{}/{}/{}".format(int(start.split("/")[0])+1, 1, "01")
                    ]
                )
            else:
                dateParameters.append(
                    [
                        "{}/{}/{}".format(start.split("/")[0], start.split("/")[1], "21"),
                        "{}/{}/{}".format(start.split("/")[0], int(start.split("/")[1])+1, "01")
                    ]
                )
        else:
            raise ValueError("Unexpect level received: {}".format(Downloader.rangeLevel[level]))

        records = []
        for dateParameter in dateParameters:
            results = self.__eSearch(query, level, mindate=dateParameter[0], maxdate=dateParameter[1])
            if not results:
                continue
            count = int(results['Count'])
            if level == 0:
                print("There are total {} articles queried.".format(count, query))
            if count > 10000:
                records += self.returnBatchRecords(query, start=dateParameter[0], end=dateParameter[1], level=level+1)
            else:
                records += self.__eFetch(results, retmax=count)

        return records

    def returnCit(self, ids, batchSize=1000):
        self.failedRequest = []

        db = "pubmed"
        LinkName = "pubmed_pubmed_citedin"

        citResult = {}
        start = 0
        while start < len(ids):
            subIDs = ids[start: start+batchSize]
            start += batchSize
            results = self.__eLink(subIDs, db=db, LinkName=LinkName)
            for result in results:
                articleCited = result["IdList"][0]
                try:
                    article = [link["Id"] for link in result["LinkSetDb"][0]["Link"]]
                except IndexError:
                    if len(result["LinkSetDb"]) == 0:
                        article = []
                    else:
                        print(result["LinkSetDb"])
                citResult[articleCited] = article
        return citResult, self.failedRequest
