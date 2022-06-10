
def take_screenshot(driver, file_name):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.save_screenshot(file_name)