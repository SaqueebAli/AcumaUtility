import pytest
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support import expected_conditions as EC

driver = None
def pytest_addoption(parser):
    parser.addoption(
        "--browser", action="store", default="chrome"
    )
    parser.addoption(
        "--fpath", type=str, action="store", default="null"
    )
    parser.addoption(
        "--u", type=str, action="store", default="u"
    )
    parser.addoption(
        "--p", type=str, action="store", default="p"
    )
    parser.addoption(
        "--sdate", type=str, action="store", default="sdate"
    )
    parser.addoption(
        "--edate", type=str, action="store", default="edate"
    )

@pytest.fixture(scope="class")
def setup(request):
    global driver
    global filepath
    global pstartDate
    global pendDate
    browser = request.config.getoption("browser")
    filepath = request.config.getoption("--fpath")
    username = request.config.getoption("--u")
    password = request.config.getoption("--p")
    pstartDate = request.config.getoption("--sdate")
    pendDate = request.config.getoption("--edate")
    print(filepath , username, password)
    if browser == "chrome":
        driver = webdriver.Chrome(ChromeDriverManager().install())
    elif browser == "firefox":
        driver = webdriver.Firefox(GeckoDriverManager().install())
    elif browser == "edge":
        driver = webdriver.Edge(EdgeChromiumDriverManager().install())
    driver.maximize_window()
    driver.implicitly_wait(60)
    url=f"https://{username}:{password}@managedservice.acuma.co.uk/Applications/Timesheet.aspx"
    print(url)
    driver.get(url)
    request.cls.driver = driver
    request.cls.filepath = filepath
    request.cls.pstartDate = pstartDate
    request.cls.pendDate = pendDate
    yield
    driver.close()
