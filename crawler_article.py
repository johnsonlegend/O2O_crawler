from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import ProxyType
from urllib.parse import unquote
import json
import requests
import re
import time
import pdfkit


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
		print_to_file('page_source.html', driver.page_source)
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
	# driver = webdriver.PhantomJS()

	# When using phantomjs, need to maximize the window
	driver.maximize_window()

	# Check IP
	# check_url = "http://www.whatismyip.org"
	# driver.get(check_url)
	# locator = (By.XPATH, "/html/body/div[2]/span")
	# wait_to_load(driver, locator)
	# IP = driver.find_element(By.XPATH, "/html/body/div[2]/span")
	# print(IP.text)

	with open('result_failed.json') as f:
		failed_list = json.load(f)
	with open('result_success.json') as f:
		success_list = json.load(f)

	# Choose to collect success_list or failed_list
	crawl_list = success_list

	for company in crawl_list:
		
		# Take first 5 as a trial
		if (crawl_list.index(company)) >= 3:
			break

		start_url = "http://www.google.com"
		driver.get(start_url)

		# Locate Search Box
		# PhantomJS
		# xpath = "//input[@class='lst']"
		# Firefox
		xpath = "//input[@id='lst-ib']"
		locator = (By.XPATH, xpath)
		wait_to_load(driver, locator)
		search_box = driver.find_element(By.XPATH, xpath)

		# Search
		search_box.clear()
		search_box.send_keys(company + " O2O article")
		search_box.send_keys(Keys.ENTER)

		# Get url result
		locator = (By.XPATH, "//h3[@class='r']")
		wait_to_load(driver, locator)
		href_list = driver.find_elements(By.XPATH, "//h3[@class='r']/a")
		href_list = [href.get_attribute("href") for href in href_list[:5]]
		href_list = [unquote(href) for href in href_list]

		print(href_list)

		for i in range(len(href_list)):
			# HTML format download
			# file_name = company + '_' + str(i) + '.html'
			# driver.get(href_list[i])
			# with open(file_name, 'a', encoding='utf8') as f:
			# 	f.write(driver.page_source)

			# Todo: Use pdfkit for pdf format download
			file_name = company + '_' + str(i) + '.pdf'
			# open(file_name, 'a').close()
			# try:
			# 	pdfkit.from_url(href_list[i], file_name)
			# except:
			# 	continue

if __name__ == '__main__':
	main()

