from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com')


def login(email, password):

    email_box = driver.find_element_by_id("session_key")
    email_box.send_keys(email)

    password_box = driver.find_element_by_id("session_password")
    password_box.send_keys(password + Keys.ENTER)

    print("Logged in")


class Company:

    name = "default"

    def __init__(self, company_name):
        self.name = company_name
        driver.get(
            'https://www.linkedin.com/search/results/companies/?keywords=' + company_name)

        # click on first result
        driver.find_element_by_css_selector(
            'ul.reusable-search__entity-results-list li:first-child').click()

        # click on about
        about_selector = 'ul.org-page-navigation__items li:nth-child(2)'
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, about_selector)))
            driver.find_element_by_css_selector(
                'ul.org-page-navigation__items li:nth-child(2)').click()
        except TimeoutException:
            print("Loading took too much time!")

    # get description
    def get_description(self):
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'section p:nth-child(2)')))
            description = driver.find_element_by_css_selector(
                'section p:nth-child(2)').text
            return description
        except TimeoutException:
            print("Loading took too much time!")

    # get website
    def get_website(self):
        website_xpath = "//dt[text()='Website']/following-sibling::dd"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, website_xpath)))
            website = driver.find_element_by_xpath(website_xpath).text
            return website
        except TimeoutException:
            print("Loading took too much time!")

    # get nr employees
    def get_nr_employees(self):
        nr_emp_class = "org-about-company-module__company-size-definition-text"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, nr_emp_class)))
            nr_emp = driver.find_element_by_class_name(nr_emp_class).text
            return nr_emp
        except TimeoutException:
            print("Loading took too much time!")

    # get headquarters
    def get_headquarters(self):
        hq_xpath = "//dt[text()='Headquarters']/following-sibling::dd"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, hq_xpath)))
            hq = driver.find_element_by_xpath(hq_xpath).text
            return hq
        except TimeoutException:
            print("Loading took too much time!")



login("francescofgonzales@gmail.com","gradiente")
google = Company("google")
print(google.get_description())
print(google.get_headquarters())
print(google.get_nr_employees())
print(google.get_website())

driver.quit()
