from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import matplotlib.pyplot as plt
import os
import math

#help creating the csv file by original directory path
dir_path = os.path.dirname(os.path.realpath(__file__))

"""
Author: 		      LAW Willson King Tin (3035443342)
Application:	    Dream Dragon
Creation Date: 	  23/2/2018
Completion Date: 	31/3/2018
"""

what = raw_input("Do you need to create a new file?\n\"Y\" / \"N\"\n")

#store log file in comma separated file
#convert user input into upper case

# ========================================== 	NAMING COULD BE UPDATED 	==========================================
if(what.upper() == 'Y'):
	file = open(dir_path + '/bookingcom.csv', 'w')
	file.write("Test Date: " + datetime.now().strftime("%Y-%m-%d"))
	file.write("\r\n")
	file.write("Time: " + datetime.now().strftime("%H-%M-%S"))
	file.write("\r\n")		#switch to next line
else:
	file = open(dir_path + '/bookingcom.csv', 'a')

# ========================================== 	CONNECTION with selenium	==========================================

browser = webdriver.Firefox()
browser.get('http://www.booking.com')

#without in orginal
destination = raw_input("What is the destination?\n")

#"Tokyo"
browser.find_element_by_css_selector("#ss").send_keys(destination)

element = WebDriverWait(browser, 3).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "li.sb-autocomplete__item-with_photo:nth-child(1)")));
element.click()

#weekened use
time.sleep(8)
browser.find_element_by_css_selector(".c2-day-s-today > span:nth-child(1)").click()

#press search button
browser.find_element_by_css_selector(".sb-searchbox__button").click()

# ================== FINISH SEARCHING ==================

#wait until it finds the first page

okay = False

while(okay == False):

	time.sleep(8)
	#browser.implicitly_wait(100)

	try:
		print(browser.find_element_by_xpath("//*[contains(text(),'properties found')]").text)
		okay = True
	except:
		print('Cant find this location: ' + destination)
		print('Please try another region, if possible to check network connection!')

qty = (browser.find_element_by_xpath("//*[contains(text(),'properties found')]").text).split(": ")[1]
qty = qty.split(" ")[0]
print("There are " + str(qty) + " used for IF checking")
file.write(str(qty) + " Properties Found in " + destination)
file.write("\r\n")

time.sleep(8)
#browser.implicitly_wait(100)

# ==========================================		Web Crawling Part		==========================================
# search through page by page

x = 1					# for counting page
total = 0				# for counting total hotels

total_price = 0.0		# for calculation
visualize_list = []		# for drawing line chart, standard deviation

try:
	while(x < 100):
		#check condition of empty page or all unavailable
		find_any_hotel = False

		#storing every page's hotel
		pagecount = 0

		#wait 8 seconds
		time.sleep(8)
		#browser.implicitly_wait(8)

		#this is the scare price for each hotel
		for scare in browser.find_elements_by_css_selector("strong.price.scarcity_color > b"):

			temp_store = scare.text
			temp_store = temp_store.replace(',', '')

			total_price += int(temp_store.split(' ')[1])

			#print price
			print(scare.text)
			#file.write(record + ',' + price)
			#file.write(scare.text)

			
			temp_store = temp_store.split('HK$ ')[1]
			print("temp_store is actually:" + str(temp_store))
			visualize_list.append(int(temp_store))

			file.write(temp_store)
			file.write("\r\n")
			pagecount = pagecount+1
			find_any_hotel = True

		#this is the normal price of hotel
		for link in browser.find_elements_by_css_selector("strong.price.availprice.no_rack_rate > b"):
			"""
			temp_dos = link.text
			temp_dos = temp_dos.split('$ ')[1]
			price = int(temp_dos.replace(',', ''))

			#print price
			
			#file.write(record + ',' + temp_dos)
			"""
			temp_dos = link.text
			temp_dos = temp_dos.replace(',', '')

			total_price += int(temp_dos.split(' ')[1])

			print(link.text)
			
			temp_dos = temp_dos.split('HK$ ')[1]
			visualize_list.append(int(temp_dos))
			print("temp_dos is actually:" + str(temp_dos))
			file.write(temp_dos)
			file.write("\r\n")
			pagecount = pagecount+1
			find_any_hotel = True
		
		#next page behavior
		browser.find_element_by_css_selector(".paging-next").click()

		#when the page is still valid and without any return
		if(find_any_hotel):
			print("This page has " + str(pagecount))
			x = x + 1
		else:
			print("This page has no any hotel available")
			x = x + 1

		total = total + pagecount
		#switch to next page

		#if it exceed the provided number from booking.com, break the web-crawling part
		if(total > qty):
			print("exceeded, exit now")
			exit(0)
		
		#if find it find end page element, break the web-crawling part
		if(browser.find_element_by_css_selector("span.paging-end") == True):
			print("found paging-end")
			exit(0)

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

plt.plot(visualize_list, label="Booking.com")

plt.title("Booking.com Statistics")
plt.xlabel("#Priority of Hotel")
plt.ylabel("Price")

file.close()
browser.close()

plt.legend()
plt.show()
