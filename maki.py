# -*- coding: UTF-8 -*-
# encoding=utf8

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import matplotlib.pyplot as plt
import os
import math

import sys

reload(sys)
sys.setdefaultencoding('utf8')

#help creating the csv file by original directory path
dir_path = os.path.dirname(os.path.realpath(__file__))

"""
Author: 			    LAW Willson King Tin (3035443342)
Application:		  Maki
Creation Date: 		21/2/2018
Completion Date: 	30/3/2018
"""

what = raw_input("Do you need to create a new file?\n\"Y\" / \"N\"\n")

#store log file in comma separated file
#convert user input into upper case

# ========================================== 	NAMING COULD BE UPDATED 	==========================================

if(what.upper() == 'Y'):
	file = open(dir_path + '/expedia.csv', 'w')
	file.write("Test Date: " + datetime.now().strftime("%Y-%m-%d"))
	file.write("\r\n")
	file.write("Time: " + datetime.now().strftime("%H-%M-%S"))
	file.write("\r\n")		#switch to next line
else:
	file = open(dir_path + '/expedia.csv', 'a')

# ========================================== 	CONNECTION with selenium	==========================================


browserChild2 = webdriver.Firefox()

browserChild2.get('http://www.expedia.com.hk/')

destination = raw_input("What is the destination?\n")

#click hotel tab
browserChild2.find_element_by_css_selector("#tab-hotel-tab-hp").click()

#input the destination
browserChild2.find_element_by_css_selector("#hotel-destination-hp-hotel").send_keys(destination)

# wait booking.com 

#click search button
browserChild2.find_element_by_css_selector("div.cols-nested:nth-child(13) > label:nth-child(1) > button:nth-child(1)").click()

# ================== FINISH SEARCHING ==================

#wait 8 second
time.sleep(8)

#until the first title pops up and show the records of total available hotels
WebDriverWait(browserChild2,10).until(EC.presence_of_element_located((By.ID, "hotelResultTitle")))

#show the result to console
print(browserChild2.find_element_by_class_name("section-header-main").text)

qty = (browserChild2.find_element_by_class_name("section-header-main").text).split("：")[1]
qty = qty.split(' ')[0]
print("There are " + str(qty) + " used for IF checking")
file.write(str(qty) + " Properties Found in " + destination)
file.write("\r\n")

time.sleep(8)

# ==========================================		Web Crawling Part		==========================================
# search through page by page

#initialize the counter function
count = 0			# for counting hotels
total = 0
total_price = 0.0	# for calculation
valid = 0			# for counting hotels
x = 1

visualize_list = []		# for drawing line chart, standard deviation

try:
	while(x < 100):

		find_any_hotel = False
		page_count = 0

		time.sleep(8)

		for link in browserChild2.find_elements_by_css_selector("span.actualPrice"):
			#count += 1
			if(str(link.text) != '' and str(link.text) != ' '):
									#print(link.text)
				linker = (link.text).split()
				linker = linker[0].split('HK$')[1]
									#print(linker)
				linker = linker.replace(',', '')
				money = int(linker.decode('utf-8'))
									#abc.append(money)
									#print(abc)
				count += 1
				find_any_hotel = True
				page_count = page_count + 1
				visualize_list.append(int(money))
				print(int(money))
				total_price += int(money)
				file.write(str(money))
				file.write("\r\n")

		for each in browserChild2.find_elements_by_css_selector("a.actualPrice.over-link.price-breakdown-tooltip-link.tabAccess.fakeLink"):
			eacher = (each.text).split()
			if(str(eacher) != '' and str(eacher) != ' '):
				price1_str = str(eacher[-1].split("HK$")[1])
				price1_str = price1_str.replace(',', '')

				#print(price1_str)
									#abc.append(price1_str)
									#print(abc)
				count += 1
				find_any_hotel = True
				page_count = page_count + 1
				visualize_list.append(int(price1_str))
				print(int(price1_str))
				total_price += int(price1_str)
				file.write(str(price1_str))
				file.write("\r\n")

		if(find_any_hotel == True):
			print("This page has " + str(page_count))
			x = x + 1
		else:
			print("This page has no result")
			x = x + 1

		total = total + page_count

		if(int(total) > int(qty)):
			print("exceeded, exit now")
			exit(0)

		try:
			if(browserChild2.find_element_by_css_selector("button.pagination-next").is_disabled() == True):
				print("found paging-end")
				exit(0)
		except:
			print("The crawler will be continued")

		time.sleep(8)

		browserChild2.find_element_by_css_selector("button.pagination-next").click()
except:
	print("The crawler can't capture anymore")

print("==================SUMMARY==================")
file.write('\r\n\r\n==================SUMMARY==================')
file.write("\r\n")
print("We have searched " + str(x) + " pages for you!")
file.write("Pages:," + str(x) + ",\r\n")
print("Through Crawler, there are " + str(total) + " hotels available in " + destination.upper())
file.write("Actual Avaliability:," + str(total) + ",\r\n")

if(int(total) < int(qty)):
	print("Compared with first page, it is \'" + str((float(total)/float(qty))*100) + "%\' on the market!")
	file.write("Percentage of it claims:," + str((float(total)/float(qty))*100) +"%" )
	file.write("\r\n")
else:
	print("Compared with first page, it is 100\%  on the market")
	file.write("Percentage of it claims:,'100%'")
	file.write("\r\n")

avgg = float(total_price/total)
print("Average Price: $" + str(avgg) )
file.write("Average Price:$," + str(avgg) + "\r\n")

# ==========================================		Visualize the Statistics	==========================================

print("Data List")
print(visualize_list)

# ==========================================		Standard Deviation (ALL) 	==========================================

variance = 0.0
for v in visualize_list:
	variance += math.pow((v - avgg), 2)

variance /= (total-1)
variance = math.sqrt(float(variance))
print("Standard Deviation: " + str(variance))
file.write("Standard Deviation:," + str(variance) + "\r\n")

# ==========================================	Standard Deviation (First 50)	==========================================
f_varience = 0.0
for vr in visualize_list[:50]:
	f_varience += math.pow((vr - avgg), 2)

f_varience /= (50-1)
f_varience = math.sqrt(float(f_varience))
print("Standard Deviation of first 50: " + str(f_varience))
file.write("First 50 Standard Deviation:," + str(f_varience))

plt.plot(visualize_list, label="Expedia")

plt.title("Expedia.com Statistics")
plt.xlabel("#Priority of Hotel")
plt.ylabel("Price")

file.close()
browserChild2.close()

plt.legend()
plt.show()
