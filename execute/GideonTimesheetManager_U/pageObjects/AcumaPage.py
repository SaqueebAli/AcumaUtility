from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium import webdriver
from utilities.BaseClass import BaseClass
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class AcumaPage(BaseClass):
    def __init__(self, driver):
        self.driver = driver

    add = (By.XPATH, "//*[@ value='Add']")
    save = (By.XPATH, "//*[@ value='Save']")
    save_Submit = (By.XPATH, "//*[@ value='Save & Submit']")
    comment = (By.XPATH, "//*[contains(@name,'Comments') and @type='text']")
    New = (By.XPATH, "//*[contains(text(),'New')]")
    NewTimeSheet = (By.XPATH, "//a[text()='New Timesheet']")

    @classmethod
    def XPATH_NameCONTAINS(cls, phrase):
        xpath = f"//*[contains(@name, '{phrase}')]"
        return (By.XPATH, xpath)

    def selectNewTimeSheet(self):
        newsheet = self.driver.find_element(*self.NewTimeSheet)
        self.driver.execute_script("arguments[0].click();", newsheet)

    def consultants(self, resource):
        sel = Select(self.driver.find_element(*self.XPATH_NameCONTAINS("consultant")))
        sel.select_by_visible_text(resource)

    def weekends(self, weekend):
        sel = Select(self.driver.find_element(*self.XPATH_NameCONTAINS("Weekend")))
        sel.select_by_visible_text(weekend)

    def managers(self, manager):
        sel = Select(self.driver.find_element(*self.XPATH_NameCONTAINS("manager")))
        sel.select_by_visible_text(manager)

    def managers1(self, manager1):
        sel = Select(self.driver.find_element(*self.XPATH_NameCONTAINS("manager1")))
        sel.select_by_visible_text(manager1)

    def managers2(self, manager2):
        sel = Select(self.driver.find_element(*self.XPATH_NameCONTAINS("manager2")))
        if len(manager2.strip(" ")) > 0:
            sel.select_by_visible_text(manager2)

    def customers(self, customer):
        sel = Select(self.driver.find_element(*self.XPATH_NameCONTAINS("customer")))
        for option in sel.options:
            if option.text.strip() == customer:
                sel.select_by_visible_text(option.text)
                break

    def projects(self, project):
        sel = Select(self.driver.find_element(*self.XPATH_NameCONTAINS("project")))
        for option in sel.options:
            if option.text.strip() == project:
                sel.select_by_visible_text(option.text)
                break

    def activities(self, activity):
        sel = Select(self.driver.find_element(*self.XPATH_NameCONTAINS("activity")))
        sel.select_by_visible_text(activity)

    def days(self, day):
        ele = self.driver.find_element(*self.XPATH_NameCONTAINS(day))
        return ele

    def addRow(self):
        return self.driver.find_element(*self.add)

    def saveAndSubmit(self):
        self.driver.find_element(*self.save_Submit).click()

    def text_comments(self):
        return self.driver.find_element(*self.comment)
