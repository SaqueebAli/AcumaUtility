import pytest

from selenium.webdriver.support.select import Select


@pytest.mark.usefixtures("setup")
class BaseClass():

    def selectOptionByText(self, locator, text):
        sel = Select(locator)
        sel.select_by_visible_text(text)
