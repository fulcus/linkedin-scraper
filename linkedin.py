from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException


email_input = "francescofgonzales@gmail.com"
password_input = "gradiente"
company_input = "google"

driver = webdriver.Chrome()
driver.get('https://www.linkedin.com')


email_box = driver.find_element_by_id("session_key")
print("Enter email:")
#email_input = input()
email_box.send_keys(email_input)

password_box = driver.find_element_by_id("session_password")
print("Enter password:")
#password_input = input()
password_box.send_keys(password_input + Keys.ENTER)

print("Logged in")

print("Enter company name:")
#company_input = input()
driver.get('https://www.linkedin.com/search/results/companies/?keywords=' + company_input)

#click on first result
driver.find_element_by_css_selector('ul.reusable-search__entity-results-list li:first-child').click()

#click on about
about_selector = 'ul.org-page-navigation__items li:nth-child(2)'
try:
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, about_selector)))
    driver.find_element_by_css_selector('ul.org-page-navigation__items li:nth-child(2)').click()
except TimeoutException:
    print("Loading took too much time!")

#get description
try:
    myElem = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'section p:nth-child(2)')))
    description = driver.find_element_by_css_selector('section p:nth-child(2)').text
    print(description)
except TimeoutException:
    print("Loading took too much time!")

#get website
website_xpath = "//dt[text()='Website']/following-sibling::dd"
try:
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, website_xpath)))
    website = driver.find_element_by_xpath(website_xpath).text
    print(website)
except TimeoutException:
    print("Loading took too much time!")


#get nr employees
nr_emp_class = "org-about-company-module__company-size-definition-text"
try:
    myElem = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, nr_emp_class)))
    nr_emp = driver.find_element_by_class_name(nr_emp_class).text
    print(nr_emp)
except TimeoutException:
    print("Loading took too much time!")


#find headquarters
hq = driver.find_element_by_xpath("//dt[text()='Headquarters']/following-sibling::dd").text
print(hq)

driver.quit()
