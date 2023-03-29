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
import time
from itertools import combinations

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
	driver.find_element_by_xpath("//a[@href='ShowData.aspx']").click();
	soup = BeautifulSoup(driver.page_source,'lxml')
	span =  soup.find('span',id="ContentPlaceHolder1_dlPdfs")
	length = 0
	for i in span.find_all('span'):
		for k in i.find_all('table',class_="table"):
			length = length+1
	print(length)		
		
	allthelists = [[] for x in range(int(length))]
	index = 0
	for i in span.find_all('span'):
		for k in i.find_all('table',class_="table"):
			for x in k.find_all('tr'):
					j=x.findChildren()[2]
					if j.name == 'td':
						allthelists[index].append(j.get_text())

			allthelists[index]=[z.encode('utf-8') for z in allthelists[index]]

			allthelists[index] = list(dict.fromkeys(allthelists[index]))

			
			index = index + 1

	for i in range(len(allthelists)):
		ana_dict = {}
		for n in allthelists[i]:
			key = ''.join(sorted(n))
			key = key.replace(" ", "")
			if not ana_dict.get(key):
				ana_dict[key]=n

		allthelists[i]=ana_dict.values()
		ana_dict.clear()	
		
	for i in range(len(allthelists)):
		allthelists[i] =[",".join(map(str, comb)) for comb in combinations(allthelists[i], 2)]
		
	for i in range(len(allthelists)):
		allthelists[i] = set(allthelists[i])

	counter = 0	
	f = open("AI_data_Modeling.txt", "w")
	
	for j in range(len(allthelists)):
		for i in range(len(allthelists)):
			if allthelists[j].issubset(allthelists[i]):
				counter =  counter + 1
		counter = counter -1
		if counter == 0:
			f.write(str(allthelists[j])+'no viable relationship found \n \n \n')
		else:
			f.write(str(allthelists[j])+' pair occurences in all pdfs is  '+str(counter)+ '\n \n \n')
		counter = 0
	
	f.close()	
			
	driver.close()
	

if __name__== "__main__":
	scrapeFromEagleTracess("http://eagletracess.com/LoginPage.aspx")
	
				
			

	
	


