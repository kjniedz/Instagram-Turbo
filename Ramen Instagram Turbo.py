import time
import os
import requests
from selenium import webdriver
import configparser
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
configfile = os.path.join(ROOT_PATH, "config.ini")
executable_path = os.path.join(ROOT_PATH, "chromedriver.exe")

url = "https://www.instagram.com/accounts/login/"
edit = "https://www.instagram.com/accounts/edit/"

config = configparser.ConfigParser(interpolation=None)
config.read(configfile)
secret = config["SETTINGS"]
target_username = str(secret["target_username"])
username = str(secret["username"])
password = str(secret["password"])
delay = int(secret["delay"])
small_delay = int(secret["small_delay"])

account = "https://www.instagram.com/"+target_username

print("Starting Session...")

chrome_options = ChromeOptions()

chrome_options.add_argument('--kiosk-printing')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--log-level=OFF')

chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(executable_path, chrome_options=chrome_options)
driver.get(edit)

time.sleep(delay)

driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
driver.find_element_by_xpath("//input[@name='password']").send_keys(password)

driver.find_element_by_xpath("(//div[contains(.,'Log In')])[7]").click()

time.sleep(delay)

print("Logged In!")

driver.find_element_by_xpath("//button[contains(.,'Not Now')]").click()
time.sleep(delay)
driver.find_element_by_xpath("//input[@aria-required='true']").click()

driver.find_element_by_xpath("//input[contains(@aria-required,'true')]").send_keys(Keys.CONTROL + "a")
driver.find_element_by_xpath("//input[contains(@aria-required,'true')]").send_keys(Keys.DELETE)
driver.find_element_by_xpath("//input[contains(@aria-required,'true')]").send_keys(target_username)

while True:

	time.sleep(small_delay)
	r = requests.get(account)

	if r.status_code == 200:
		pass
	elif r.status_code == 404:
		driver.find_element_by_xpath("//input[contains(@aria-required,'true')]").send_keys(Keys.CONTROL + "a")
		driver.find_element_by_xpath("//input[contains(@aria-required,'true')]").send_keys(Keys.DELETE * 15)
		driver.find_element_by_xpath("//input[contains(@aria-required,'true')]").send_keys(target_username)
		driver.find_element_by_xpath("//button[contains(.,'Submit')]").click()

		print("Claimed",target_username+"!")
	exit()