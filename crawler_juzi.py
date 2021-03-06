from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
import json
import requests
import re
import time


def print_to_file(filename, string):
	with open(filename, 'a') as f:
		f.write(string + '\n')


def wait_to_load(driver, locator):
	try:
		WebDriverWait(driver, 20).until(
			EC.presence_of_element_located(locator)
		)
		return 1
	except:
		print(locator)
		print('Fail to load!')
		return 0

def main():

	# Webdriver Setting
	# dcap = dict(DesiredCapabilities.PHANTOMJS)
	# headers = {'Referer':'https://aminer.org/', 'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
	# for key, value in headers.items():
	# 	dcap['phantomjs.page.customHeaders.{}'.format(key)] = value
	# dcap['phantomjs.page.settings.userAgent'] = \
	# 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4'
	# dcap['phantomjs.page.settings.loadImages'] = False
	
	# service_args = ['--proxy=205.189.37.79:53281', '--proxy-type=none']
	driver = webdriver.Firefox()
	# driver = webdriver.PhantomJS(desired_capabilities=dcap)

	# When using phantomjs, need to maximize the window
	driver.maximize_window()

	# Check IP
	# check_url = "http://www.whatismyip.org"
	# driver.get(check_url)
	# locator = (By.XPATH, "/html/body/div[2]/span")
	# wait_to_load(driver, locator)
	# IP = driver.find_element(By.XPATH, "/html/body/div[2]/span")
	# print(IP.text)

	start_url = "http://radar.itjuzi.com/company"
	driver.get(start_url)

	# Allow time to manually apply filters
	time.sleep(70)

	name_result = []
	has_next = True
	page_num = 0

	while(has_next):
		
		# Scroll to Bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		locator = (By.XPATH, "//*[@id='searchList']")
		wait_to_load(driver, locator)
		company_lists = driver.find_element(By.ID, "searchList")
		company_lists = company_lists.find_elements(By.XPATH, "//a[@data-container='body']")

		for company_box in company_lists:
			# print(company_box.text)
			name_result.append(company_box.text)

		# Get Next Page
		try:
			next_page = driver.find_element(By.XPATH, "//li[@class='next']/a")
			action_chains = ActionChains(driver)
			action_chains.click(next_page).perform()
			time.sleep(5)
		except:
			has_next = False

		page_num = page_num + 1

		if page_num % 10 == 0:
			print('Success Collect ' + str(page_num) + " pages!")


	print_to_file('result_success.json', json.dumps(name_result))
	for result in name_result:
		print_to_file('result_success.txt', result)


if __name__ == '__main__':
	main()


