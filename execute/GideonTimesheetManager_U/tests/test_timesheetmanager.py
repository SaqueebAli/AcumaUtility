from datetime import datetime
import json
import configparser
import os
from utilities.logger import logs

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from time import sleep
from selenium import webdriver
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.support.wait import WebDriverWait

from pageObjects.AcumaPage import AcumaPage

from utilities.BaseClass import BaseClass
from utilities.ExcelDataFetcher import dataFetcher
from utilities.Utility import take_screenshot


class TestTimesheetManager(BaseClass):
    config = configparser.ConfigParser()
    config.read('../propertyFile/properties.ini')
    p = config["Efforts"]["P"]
    b = config["Efforts"]["B"]
    a = config["Efforts"]["A"]
    s = config["Efforts"]["S"]
    if os.path.exists("../../../logs"):
        pass
    else:
        os.mkdir("../../../logs")
    if os.path.exists("../../../Screenshots"):
        pass
    else:
        os.mkdir("../../../Screenshots")

    def present(self, tsp, customer, project, activity, Weekend, Week, updatedTime):
        absent = {}
        holiday = {}
        sickLeave = {}
        tsp.customers(customer)
        tsp.projects(project)
        tsp.activities(activity)
        tsp.weekends(Week)
        x = 1
        for day in Weekend:
            if Weekend[day] == "A":
                absent[day] = Weekend[day]
                continue
            elif Weekend[day] == "B":
                holiday[day] = Weekend[day]
                continue
            elif Weekend[day] == "S":
                sickLeave[day] = Weekend[day]
                continue
            elif Weekend[day] == "P":
                tsp.days(day).send_keys(str(updatedTime))
                x = 0
            else:
                continue
        if len(absent) != 5 and x != 1:
            tsp.text_comments().clear()
            tsp.text_comments().send_keys("Worked on assigned project")
            tsp.addRow().click()
        return absent, holiday, sickLeave

    def absence(self, tsp, customer, project, activity, absent, Week, updatedtime):
        tsp.customers(customer)
        tsp.projects(project)
        tsp.activities(activity)
        tsp.weekends(Week)
        for day in absent:
            tsp.days(day).send_keys(str(updatedtime))
        tsp.text_comments().clear()
        tsp.text_comments().send_keys("On casual Leave")
        tsp.addRow().click()

    def sickleave(self, tsp, customer, project, activity, sickLeave, Week, updatedtime):
        tsp.customers(customer)
        tsp.projects(project)
        tsp.activities(activity)
        tsp.weekends(Week)
        for day in sickLeave:
            tsp.days(day).send_keys(str(updatedtime))
        tsp.text_comments().clear()
        tsp.text_comments().send_keys("On Sick Leave")
        tsp.addRow().click()

    def clear_Weekdays(self, tsp):
        weekdays = ["mon", "tue", "wed", "thu", "fri"]
        for weekday in weekdays:
            tsp.days(weekday).clear()

    def holiday(self, tsp, customer, project, activity, holidays, Week):
        tsp.customers(customer)
        tsp.projects(project)
        tsp.activities(activity)
        tsp.weekends(Week)
        for day in holidays:
            tsp.days(day).send_keys(self.b)
        tsp.text_comments().clear()
        tsp.text_comments().send_keys("Bank holiday in India")
        tsp.addRow().click()

    def test_one(self):
        os.chdir("../../../logs")
        filename = os.path.join(os.getcwd(), datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".log")
        logger = logs(filename)
        try:
            datas = dataFetcher(self.filepath, self.pstartDate, self.pendDate)
            os.chdir("../Screenshots/")
            for data in datas:
                for Weekend in datas[data]["Dates"]:
                    tsp = AcumaPage(self.driver)
                    tsp.selectNewTimeSheet()
                    projects = datas[data]["project"].split(',')
                    updatedtime = float(self.p) / len(projects)
                    tsp.consultants(data)
                    tsp.managers(datas[data]["manager"])
                    tsp.managers1(datas[data]["manager1"])
                    tsp.managers2(datas[data]["manager2"])
                    self.clear_Weekdays(tsp)
                    for proj in projects:
                        absenteeism, holidays, sickLeave = self.present(tsp, datas[data]["customer"], proj,
                                                                        "Chargeable",
                                                                        datas[data]["Dates"][Weekend], Weekend,
                                                                        updatedtime)
                        if any(absenteeism):
                            self.clear_Weekdays(tsp)
                            self.absence(tsp, datas[data]["customer"], proj, "Non-Charge", absenteeism, Weekend,
                                         updatedtime)
                        if any(sickLeave):
                            self.clear_Weekdays(tsp)
                            self.sickleave(tsp, datas[data]["customer"], proj, "Non-Charge", sickLeave, Weekend,
                                           updatedtime)
                    if any(holidays):
                        self.clear_Weekdays(tsp)
                        self.holiday(tsp, "Acuma Solutions Ltd", "N2 Absence", "Ann-Hol", holidays, Weekend)
                    now = datetime.now()

                    timestamp = now.strftime("%d-%m-%Y-%H-%M-%S")
                    file_Name = data + "_" + Weekend + "_" + timestamp + ".png"

                    tsp.saveAndSubmit()
                    try:
                        WebDriverWait(self.driver, 60).until(EC.alert_is_present())
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except:
                        pass

                    try:
                        WebDriverWait(self.driver, 60).until(EC.alert_is_present())
                        alert = self.driver.switch_to.alert
                        alert.accept()
                    except:
                        pass

                    self.driver.find_element(By.XPATH, "//*[text()='Timesheet saved and submitted successfully.']")
                    take_screenshot(self.driver, file_Name)
                    logger.log(data + " " + Weekend + " :" + " passed")
        except Exception as exp:
            logger.log(data + " " + Weekend + " :" + " failed")
