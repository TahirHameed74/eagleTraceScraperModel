from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import requests
import re
import os
from operator import itemgetter 
import json
import time


def scrapeFromEagleTracess(url):
	chrome_options = Options()  
	chrome_options.add_argument("--headless") 
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get(url)
	username = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtEmail")
	username.clear()
	username.send_keys("JC")
	password = driver.find_element_by_name("ctl00$ContentPlaceHolder1$txtPassword")
	password.clear()
	password.send_keys("Contender123")
	time.sleep(5)
	driver.find_element_by_name("ctl00$ContentPlaceHolder1$btnLogin").click()
	time.sleep(5)
	wait = WebDriverWait(driver, 20)
	driver.find_element_by_xpath("//a[@href='SuppliersReoprt.aspx']").click();
	soup = BeautifulSoup(driver.page_source,'lxml')
	table =  soup.find('table',class_="table")
	suppliersInfo = []
	try:
		for i in table.find_all('td'):
			suppliersInfo.append(i.get_text())
	except Exception as e:
		i = None

	suppliersInfo=[x.encode('utf-8') for x in suppliersInfo]
	driver.close()
	return suppliersInfo


def scrapeFromHipaaSpace(phoneNumbers, name):
	chrome_options = Options()  
	chrome_options.add_argument("--headless") 
	driver = webdriver.Chrome(chrome_options=chrome_options)
	driver.get("https://www.hipaaspace.com/medical_web_services/test.drive.restful.web.services?Type=NPI")
	search = driver.find_element_by_name("ctl00$ContentPlaceHolder1$QueryTextbox")
	search.clear()
	search.send_keys(phoneNumbers)
	driver.find_element_by_name("ctl00$ContentPlaceHolder1$SubmitQuery").click();
	soup = BeautifulSoup(driver.page_source,'lxml')
	data =  soup.find('div',class_="ui-tabs-panel").pre.text
	print(data)
	with open(name+'.json', 'w') as json_file:
    		#json.dump(data, json_file,ensure_ascii=False, indent=4)
    		json_file.write(data)

	driver.close()

if __name__== "__main__":
  suppliersInfo = scrapeFromEagleTracess("http://eagletracess.com/LoginPage.aspx")
  supplierName = suppliersInfo[::2]
  supplierPhone = suppliersInfo[1::2]
  for (i,j) in zip(supplierPhone,supplierName):
  		scrapeFromHipaaSpace(i,j)

















