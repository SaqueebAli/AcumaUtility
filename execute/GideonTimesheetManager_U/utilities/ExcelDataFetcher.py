import pandas as pd
import configparser
import datetime
import ast
import os
import json


def dataFetcher(path, pstartDate, pendDate):
    config = configparser.ConfigParser()
    filepath= rf'{path}'
    print(filepath)
    startDate=pstartDate
    endDate=pendDate

    try:
        xls = pd.ExcelFile(filepath)
        data = pd.read_excel(xls, "Annual Leave Tracker_Data", index_col=None, header=None, usecols=None, na_values=None, keep_default_na=False)
        config.read('../propertyFile/properties.ini')
        # startDate = config['DATE']['startDate']
        weekEnd = startDate
        # endDate = config['DATE']['endDate']
        date = datetime.datetime.strptime(startDate, "%d-%m-%Y") - datetime.timedelta(days=5)
        dt = date
        attendance = {}
        df = pd.DataFrame(data)
        rows = len(df.index)
        resources = []
        for row in range(6, len(df.index)):
            print(df.iat[row, 2])
            if df.iat[row, 2] != "":
                resources.append(df.iat[row, 2])
            else:
                break
        for res in resources:
            for row in range(6, len(df.index)):
                if df.iat[row, 2] == res:
                    rowCounter = row
                    attendance[res] = {}
                    eDate = datetime.datetime.strptime(endDate, "%d-%m-%Y")
                    attendance[res]["Dates"] = {}
                    while True:
                        attendance[res]["Dates"][weekEnd] = {}
                        for j in range(1, 6):
                            for column in df.columns[8:len(df.columns) - 1:]:
                                if df.iat[4, column] == date:
                                    attendance[res]["Dates"][weekEnd][str.lower(date.strftime("%a"))] = df.iat[rowCounter, column]
                                    date = date + datetime.timedelta(days=1)
                                    break
                        date = date + datetime.timedelta(days=2)
                        weekEnd = (date + datetime.timedelta(days=5)).strftime("%d-%m-%Y")
                        if eDate < date:
                            break
            i = 0
            Fields = ["Manager", "Manager1", "Manager2", "Project", "Customer"]
            for column in df.columns[0:len(df.columns) - 1:]:
                if df.iat[5, column] == Fields[i]:
                    attendance[res][str.lower(Fields[i])] = df.iat[rowCounter, column]
                    i = i + 1
                if i == 5:
                    break
            weekEnd = startDate
            date = dt
        print(attendance)
        return attendance
    except Exception as e:
        print(e)
        print("File Not Found: No file present to read data in file Folder")
