# Ankit Anand
# aanand35@uic.edu
# I hereby attest that I have adhered to the rules for quizzes and projects as well as UIC’s Academic Integrity standards. Signed: Ankit Anand

from flask import Flask, render_template, request # importing flask modules
app = Flask(__name__)
from bs4 import BeautifulSoup # importing beautifulsoup
import urllib3
import json
import re


email_list = [] # Creating an empty list to store email output
def GetEmailAdress():
  """Function to extract email address"""
  http = urllib3.PoolManager()
  mscs_url = "https://mscs.uic.edu/people/faculty/" # Webpage url to extract emails
  requested = http.request('GET', mscs_url)
  B = BeautifulSoup(requested.data.decode('utf-8'), "html5lib")

  InfoField = B.find_all('span', attrs={'class': '_email'}) # Finding all inside span tag

  for info in InfoField:
    s = info.find_all('a') # Finding all inside a tag
    for i in s:

      email_output = i.text # Getting only text without tags
      email_list.append(email_output) # Appending it to an empty list

  return None


GetEmailAdress()

strip_list_email = [] # Creating a new empty list to store stripped value
for i in email_list:
  strip_element = i.strip() # Stripping every element
  strip_list_email.append(strip_element) # Appending it to the empty list created





emp_lst = [] # Creating an empty list to store name
def ScrapeName(art_url):
  """Function to extract Names"""
  http = urllib3.PoolManager()
  requested = http.request('GET', art_url)
  B = BeautifulSoup(requested.data.decode('utf-8'), "html5lib")
  InfoField = B.find('div', attrs={'class': '_colB'}) # Finding inside class _colB tag
  s = InfoField.find_all('h1') # Finding all inside h1 tag
  output = s[0].text # Getting only text without tags

  emp_lst.append(output) # Appending it to the empty list created


def ScrapeNameAutomate():
  """Scrapping name from every url"""
  http = urllib3.PoolManager()
  mscs_url = "https://mscs.uic.edu/people/faculty/" # Webpage url to extract names
  requested = http.request('GET', mscs_url)
  B = BeautifulSoup(requested.data.decode('utf-8'), "html5lib")
  InfoField = B.find_all('span', attrs={"class": "_name"})
  for info in InfoField:
    a_info = info.find_all('a')[0]
    art_url = a_info['href']
    ScrapeName(art_url)
  return None

ScrapeNameAutomate()

dict_for_json = dict(zip(strip_list_email, emp_lst)) # Creating dictionary from two lists by using zip function







list_teaching_schedule = []
final_list_teaching_schedule = []
final_list_teaching_schedule_2 = []

def GetTeachingSchedule(art_url):
  """Function to extract teaching schedules"""
  http = urllib3.PoolManager()
  requested = http.request('GET', art_url)
  B = BeautifulSoup(requested.data.decode('utf-8'), "html5lib")

  InfoField = B.find_all('div', attrs={'class': 'u-rich-text'})
 
 
  for info in InfoField:
    schedule = info.find_all("ul")
    for i in schedule:
     
      s = i.text
      spt = s.split()
      list_teaching_schedule.append(spt)
     
      for teaching_schedule in list_teaching_schedule:
        global lst
        lst = []
        for j in teaching_schedule:
          if re.match(
              r'[0-9]{2}\:[0-9]{2}\:[0-9]{2}\-[0-9]{2}\:[0-9]{2}\:[0-9]{2}',
              j): # Using regular expression to collect only timings
            lst.append(j)
        
  final_list_teaching_schedule_2.append(lst)  # Appending final value to the empty list created





def ScrapeTeachingScheduleAutomate():
  """Getting teaching schedule from every url"""
  http = urllib3.PoolManager()
  mscs_url = "https://mscs.uic.edu/people/faculty/"
  requested = http.request('GET', mscs_url)
  B = BeautifulSoup(requested.data.decode('utf-8'), "html5lib")
  InfoField = B.find_all('span', attrs={"class": "_name"})
  for info in InfoField:
    a_info = info.find_all('a')[0]
    art_url = a_info['href']
    GetTeachingSchedule(art_url)
  return None


ScrapeTeachingScheduleAutomate()

dict_for_teaching_schedule = dict(zip(emp_lst, final_list_teaching_schedule_2)) # Creating dictionary from two lists by using zip function

with open("dict_for_teaching_schedule", "w") as f_for_teaching_schedule:
  json.dump(dict_for_teaching_schedule, f_for_teaching_schedule, indent=1)

  
with open("name_and_email.json", "w") as f:
  json.dump(dict_for_json, f, indent=1)



@app.route('/')
def index(): # This is the main home page
    return render_template('index.html')

@app.route('/', methods = ['POST'])
def getvalue():
  email = request.form['email'] # Taking email input to find Name of the faculty
  time = request.form['time'] # Taking time input to check all the faculty teaching at that time
  with open("name_and_email.json") as file:
    json_load = json.load(file)
  emp_str = ""

  if len(email) <= 2: # Checking length of the input if it is less than or equat to 2
    inp_lst = list(email) # Converting it into a list
    inp_lst_0 = inp_lst[0] # Checking for value at index 0
    inp_lst_1 = inp_lst[1] # Checking for value at index 1
    for i in json_load: # looping through dictionary keys
      if inp_lst_0 == i[0] and inp_lst_1 == i[1]: # Checking dictionary to final all matching objects
        emp_str += i
        if emp_str in json_load.keys(): # Getting key value if it meets all requirements
          print_value = json_load[emp_str] # assigning variable for output

  else:
    if email in json_load.keys(): # if the length is more than 2 than getting the value of that key
      print_value = json_load[email]
  with open("dict_for_teaching_schedule", "r") as output_file:
    data = json.load(output_file)

  list_to_store_names = [] # Creating an empty list to store all the names of faculty teaching at that time
  for key, value in data.items():                             
    if value != []:
      for course_time in value:
        course_time = course_time.split('-')[0]
        if course_time == time:  
          print_key_value = key
          list_to_store_names.append(print_key_value)
  return render_template('pass.html', email = print_value, time = list_to_store_names) # Assigning values to be returned




@app.route('/about') # About page for website
def more():

  return render_template('about.html')

app.run(host='0.0.0.0', port=81)
