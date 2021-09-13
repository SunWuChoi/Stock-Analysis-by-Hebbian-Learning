'''
Hebbian Learning implenmented on 5884 stocks and 2164 ETFs
Goal is to find the relationship between any two stock or ETF

DUE DATE: 2020.12.08

VERSION: 1.0
'''

import pandas
import random
from pathlib import Path

pandas.set_option('display.max_rows', 500)
pandas.set_option('display.max_columns', 500)
pandas.set_option('display.width', 1000)


def readStocksData(code):
    filePath = Path("archive_8month/stocks/" + code + ".csv")
    if filePath.is_file():
        dataset = pandas.read_csv(filePath)
    else:
        print("Code '", code, "' do not exist")
        return None

    return dataset


def readETFData(code):
    filePath = Path("archive_8month/etfs/" + code + ".csv")
    if filePath.is_file():
        dataset = pandas.read_csv(filePath)
    else:
        print("Code '", code, "' do not exist")
        return None

    return dataset


def printNameFromSymbol(df, code):
    stockName = df[df['Symbol'] == code]['Security Name']

    if len(stockName) is not 0:
        print(stockName.item())
    else:
        print("Code '", code, "' do not exist")


def stockRelationshipFinder(companyCode1, companyCode2):
    data1 = readStocksData(companyCode1)
    data2 = readStocksData(companyCode2)

    if data1 is None or data2 is None:
        return None

    if len(data1) >= len(data2):
        companyOld = data1
        companyOldDate = data1['Date']
        companyOldOpen = data1['Open']
        companyOldClose = data1['Close']

        companyNew = data2
        companyNewDate = data2['Date']
        companyNewOpen = data2['Open']
        companyNewClose = data2['Close']
    else:
        companyOld = data2
        companyOldDate = data2['Date']
        companyOldOpen = data2['Open']
        companyOldClose = data2['Close']

        companyNew = data1
        companyNewDate = data1['Date']
        companyNewOpen = data1['Open']
        companyNewClose = data1['Close']

    # company1 is the older company with larger rows data
    # company2 is the rather newer company with less data

    length = len(companyNew)

    compareLength = 0
    score = 0

    # index 1 is the large index that starts in the middle
    indexOld = len(companyOld) - len(companyNew)

    for indexNew in range(length):
        if companyOldDate[indexOld] == companyNewDate[indexNew]:
            if companyOldDate[indexOld] == "2020-02-20":
                return compareLength, score
            if companyNewOpen[indexNew] != 0 and companyOldOpen[indexOld] != 0:
                diffNew = (companyNewOpen[indexNew] - companyNewClose[indexNew]) / companyNewOpen[indexNew]
                diffOld = (companyOldOpen[indexOld] - companyOldClose[indexOld]) / companyOldOpen[indexOld]

                abs1 = abs(diffOld)
                abs2 = abs(diffNew)

                if abs1 >= abs2:
                    abs1 = abs2
                else:
                    abs2 = abs1

                if diffNew * diffOld >= 0:
                    score += abs1 * abs2
                else:
                    score -= abs1 * abs2

                #score += diffNew * diffOld
                #score += (diffOld + diffNew) / (abs(diffOld - diffNew) + 1) / 2

                # if diffNew > 0 and diffOld > 0:
                #     score += 1
                # elif diffNew < 0 and diffOld < 0:
                #     score += 1
                # elif diffNew > 0 and diffOld < 0:
                #     score -= 1
                # elif diffNew < 0 and diffOld > 0:
                #     score -= 1
                # elif diffNew == 0 and diffOld == 0:
                #     score += 1

            compareLength += 1
            indexOld += 1
        else:
            indexOld += 1

    return compareLength, score


def printStockHistory(code):
    data = readStocksData(code)
    print(data)


def printETFHistory(code):
    data = readETFData(code)
    print(data)


def compareWithList(code, stocksCodeList):
    maxRelationship = 0
    maxRelationshipLength = 0
    maxRelationshipCompany = None
    index = stocksCodeList[stocksCodeList == code].index[0]
    print(index, code)
    dataFrame = pandas.DataFrame(columns=["Source", "Target", "Symbol", "Compare Length", "Score", "Relationship"])

    for stock in stocksCodeList:
        relationship = stockRelationshipFinder(code, stock)

        if stock == code:
            relationship = 0, 0
        if relationship is not None:

            # print("Comparing", stockCodeList[0], stock)
            # print("Compare Length:", relationship[0], "Score:", relationship[1])

            if relationship[0] > 250:
                # print("relationship:", relationship[1] / relationship[0])
                target = stocksCodeList[stocksCodeList == stock].index[0]
                addTemp = pandas.DataFrame(
                    [[index, target, relationship[1] / relationship[0], stock, relationship[0], relationship[1]]],
                    columns=["Source", "Target", "Relationship", "Symbol", "Compare Length", "Score"])
                dataFrame = dataFrame.append(addTemp)

            # else:
            # print("Comparing", stockCodeList[0], stock)
            # print("Compare Length:", relationship[0], "Score:", relationship[1])
            # print("relationship:", 0)

        # else:
        # print("None happened")
    name = code + ".csv"
    dataFrame.to_csv(name, index=False)


if __name__ == '__main__':
    baseDataFrame = pandas.read_csv("archive_8month/symbols_valid_meta.csv")

    stocksData = baseDataFrame[baseDataFrame['ETF'] == 'N']
    stocksData = stocksData[~stocksData['Security Name'].str.contains("ETN")]
    stocksData = stocksData[~stocksData['Security Name'].str.contains("ETF")]
    stocksData = stocksData[~stocksData['Security Name'].str.contains("Growth")]
    ETFsData = baseDataFrame[baseDataFrame['ETF'] == 'Y']

    stocksCodeList = stocksData['Symbol'].reset_index(drop=True)
    ETFCodeList = ETFsData['Symbol']

    stocksData.to_csv('stocksData.csv', index=False)
    stocksCodeList.to_csv('stocksCodeList.csv', index=False)


    compareWithList('TSLA', stocksCodeList)

    # practice = pandas.DataFrame(columns=["Symbol", "Compare Length", "Score", "Relationship"])
    # adding = pandas.DataFrame([['TSLA', 123, 123, 0.3]], columns=["Symbol", "Compare Length", "Score", "Relationship"])
    # practice = practice.append(adding)
    # adding.to_csv('adding.csv', index=False)
    # practice.to_csv('practice.csv',index=False)
