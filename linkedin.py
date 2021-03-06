from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import xlrd
from xlutils.copy import copy
import traceback

WAIT_TIME = 5

NAME_COL = 0
DESCR_COL = 1
WEB_COL = 2
INDUSTRY_COL = 3
EMPL_COL = 4
EMPL_LINKEDIN_COL = 5
HQ_COL = 6
TYPE_COL = 7
FOUNDED_COL = 8
SPECIALTIES_COL = 9
LINKEDIN_COL = 10

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

    def __init__(self, company_name):
        self.name = company_name

        driver.get(
            'https://www.linkedin.com/search/results/companies/?keywords=' + company_name)

        # click on first result
        driver.find_element_by_css_selector(
            'ul li:first-child div.scale-down a').click()

        about_xpath = "//li[contains(@class, 'org-page-navigation__item')]/a[text()='About']"
        WebDriverWait(driver, WAIT_TIME).until(
            EC.presence_of_element_located((By.XPATH, about_xpath)))
        driver.find_element_by_xpath(about_xpath).click()

    def get_linkedin(self):
        return driver.current_url

    def get_description(self):
        descr_xpath = "//h4[text()='Overview']/following-sibling::p"
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, descr_xpath)))
            descr = driver.find_element_by_xpath(descr_xpath).text
            return descr
        except TimeoutException:
            print("Couldn't find " + self.name + " description")
            return None

    def get_website(self):
        website_xpath = "//dt[text()='Website']/following-sibling::dd"
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, website_xpath)))
            website = driver.find_element_by_xpath(website_xpath).text
            return website
        except TimeoutException:
            print("Couldn't find " + self.name + " website")
            return None

    def get_nr_employees(self):
        nr_emp_class = "org-about-company-module__company-size-definition-text"
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.CLASS_NAME, nr_emp_class)))
            nr_emp = driver.find_element_by_class_name(nr_emp_class).text
            nr_emp = nr_emp.replace(" employees", "")
            return nr_emp
        except TimeoutException:
            print("Couldn't find " + self.name + " nr employees")
            return None

    def get_headquarters(self):
        hq_xpath = "//dt[text()='Headquarters']/following-sibling::dd"
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, hq_xpath)))
            hq = driver.find_element_by_xpath(hq_xpath).text
            return hq
        except TimeoutException:
            print("Couldn't find " + self.name + " headquarters")
            return None

    def get_industry(self):
        industry_xpath = "//dt[text()='Industry']/following-sibling::dd"
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, industry_xpath)))
            industry = driver.find_element_by_xpath(industry_xpath).text
            return industry
        except TimeoutException:
            print("Couldn't find " + self.name + " industry")
            return None

    def get_employees_linkedin(self):
        linkedin_emp_class = "org-page-details__employees-on-linkedin-count"
        child_xpath = "//dd[contains(@class, 'org-page-details__employees-on-linkedin-count')]/span"
        
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.CLASS_NAME, linkedin_emp_class)))
            linkedin_emp = driver.find_element_by_class_name(
                linkedin_emp_class).text
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, child_xpath)))
            child = driver.find_element_by_xpath(child_xpath).text
            linkedin_emp = linkedin_emp.replace(" on LinkedIn", "")
            linkedin_emp = linkedin_emp.replace(child, "")
            return linkedin_emp
        except TimeoutException:
            print("Couldn't find " + self.name + " nr employees on linkedin")
            return None

    def get_type(self):
        type_xpath = "//dt[text()='Type']/following-sibling::dd"
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, type_xpath)))
            type = driver.find_element_by_xpath(type_xpath).text
            return type
        except TimeoutException:
            print("Couldn't find " + self.name + " company type")
            return None

    def get_foundation(self):
        founded_xpath = "//dt[text()='Founded']/following-sibling::dd"
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, founded_xpath)))
            founded = driver.find_element_by_xpath(founded_xpath).text
            return founded
        except TimeoutException:
            print("Couldn't find " + self.name + " foundation date")
            return None

    def get_specialties(self):
        specialties_xpath = "//dt[text()='Specialties']/following-sibling::dd"
        try:
            WebDriverWait(driver, WAIT_TIME).until(
                EC.presence_of_element_located((By.XPATH, specialties_xpath)))
            specialties = driver.find_element_by_xpath(specialties_xpath).text
            return specialties
        except TimeoutException:
            print("Couldn't find " + self.name + " specialties")
            return None

# login()
# company = Company("google")
# print(company.get_description())
# print(company.get_website())
# print(company.get_industry())
# print(company.get_nr_employees())
# print(company.get_employees_on_linkedin())
# print(company.get_headquarters())
# print(company.get_type())
# print(company.get_foundation())
# print(company.get_specialties())


# open excel
rb = xlrd.open_workbook("input.xlsx")
r_sheet = rb.sheet_by_index(0)  # read only copy to introspect the file
# a writable copy (I can't read values out of this, only write to it)
wb = copy(rb)
w_sheet = wb.get_sheet(0)  # the sheet to write to within the writable copy

# login linkedin
login()

#dictionary with key = row, value = company_name
not_found_companies = {}

# ROWS: 1 to 91 (excluded) in python (2 to 91 excel)
for row in range(1, 91):

    # get company name
    company_name = r_sheet.cell_value(row, NAME_COL)
    try:
        company = Company(company_name)
    except:
        print("Couldn't find " + company_name)
        not_found_companies[row] = company_name
        continue

    # write data to sheet
    try:
        w_sheet.write(row, DESCR_COL, company.get_description())
        w_sheet.write(row, WEB_COL, company.get_website())
        w_sheet.write(row, INDUSTRY_COL, company.get_industry())
        w_sheet.write(row, EMPL_COL, company.get_nr_employees())
        w_sheet.write(row, EMPL_LINKEDIN_COL, company.get_employees_linkedin())
        w_sheet.write(row, HQ_COL, company.get_headquarters())
        w_sheet.write(row, TYPE_COL, company.get_type())
        w_sheet.write(row, FOUNDED_COL, company.get_foundation())
        w_sheet.write(row, SPECIALTIES_COL, company.get_specialties())
        w_sheet.write(row, LINKEDIN_COL, company.get_linkedin())
    except:
        print("Error fetching company data")



for c_row, c_name in not_found_companies.items():
    cmd = input("You can type an alternative name for " + c_name + " or press s to skip, q to quit\n")
    if(cmd == 's'):
        continue
    elif(cmd == 'q'):
        break
    else:
        try:
            company = Company(cmd)
        except:
            print("Couldn't find " + cmd + " either. Skipping this one")
            continue

        try:
            w_sheet.write(c_row, DESCR_COL, company.get_description())
            w_sheet.write(c_row, WEB_COL, company.get_website())
            w_sheet.write(c_row, INDUSTRY_COL, company.get_industry())
            w_sheet.write(c_row, EMPL_COL, company.get_nr_employees())
            w_sheet.write(c_row, EMPL_LINKEDIN_COL, company.get_employees_linkedin())
            w_sheet.write(c_row, HQ_COL, company.get_headquarters())
            w_sheet.write(c_row, TYPE_COL, company.get_type())
            w_sheet.write(c_row, FOUNDED_COL, company.get_foundation())
            w_sheet.write(c_row, SPECIALTIES_COL, company.get_specialties())
            w_sheet.write(c_row, LINKEDIN_COL, company.get_linkedin())
        except:
            print("Error fetching company data")


wb.save('output.xlsx')

driver.quit()
