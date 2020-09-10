from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import xlrd
from xlutils.copy import copy

driver = webdriver.Chrome()


def login():
    driver.get('https://www.linkedin.com')

    email_box = driver.find_element_by_id("session_key")
    email = input('Enter your email\n')
    email_box.send_keys(email)

    password_box = driver.find_element_by_id("session_password")
    password = input('Enter your password\n')
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
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, about_selector)))
        driver.find_element_by_css_selector(
            'ul.org-page-navigation__items li:nth-child(2)').click()


    def get_description(self):
        try:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'section p:nth-child(2)')))
            description = driver.find_element_by_css_selector(
                'section p:nth-child(2)').text
            return description
        except TimeoutException:
            print("Loading took too much time!")
            return None

    def get_website(self):
        website_xpath = "//dt[text()='Website']/following-sibling::dd"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, website_xpath)))
            website = driver.find_element_by_xpath(website_xpath).text
            return website
        except TimeoutException:
            print("Loading took too much time!")
            return None

    def get_nr_employees(self):
        nr_emp_class = "org-about-company-module__company-size-definition-text"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, nr_emp_class)))
            nr_emp = driver.find_element_by_class_name(nr_emp_class).text
            nr_emp = nr_emp.replace(" employees", "")
            return nr_emp
        except TimeoutException:
            print("Loading took too much time!")
            return None

    def get_headquarters(self):
        hq_xpath = "//dt[text()='Headquarters']/following-sibling::dd"
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, hq_xpath)))
            hq = driver.find_element_by_xpath(hq_xpath).text
            return hq
        except TimeoutException:
            print("Loading took too much time!")
            return None


# open excel
rb = xlrd.open_workbook("companies.xlsx")
r_sheet = rb.sheet_by_index(0) # read only copy to introspect the file
wb = copy(rb) # a writable copy (I can't read values out of this, only write to it)
w_sheet = wb.get_sheet(0) # the sheet to write to within the writable copy

# login linkedin
login()

# ROWS: 3 to 92 (excluded) in python (4 to 92 excel)
for row in range(3, 92):

    # COLUMNS: 2 name, 3 website, 4 HQ, 5 state, 6 description, 7 employees, 8 others
    NAME_COL = 2
    WEB_COL = 3
    HQ_COL = 4
    HQ_COUNTRY_COL = 5
    DESCR_COL = 6
    EMPL_COL = 7

    # get company name
    company_name = r_sheet.cell_value(row, NAME_COL)
    try:
        company = Company(company_name)
    except: 
        print("Couldn't find company")
        continue

    # write data to sheet
    web = company.get_website()
    w_sheet.write(row, WEB_COL, web)

    hq = company.get_headquarters()
    w_sheet.write(row, HQ_COL, hq)

    descr = company.get_description()
    w_sheet.write(row, DESCR_COL, descr)

    empl = company.get_nr_employees()
    w_sheet.write(row, EMPL_COL, empl)

file_path = 'w_companies'
#wb.save(file_path + '.out' + os.path.splitext(file_path)[-1])
wb.save(file_path + '.xlsx')


driver.quit()
