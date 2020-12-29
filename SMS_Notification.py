import urllib.request # url libraries
import json # import json libraries
import re # regex for cleaning entries

# creating dynamic time variable for yesterday
from datetime import datetime, timedelta # importing for date calculation
yesterday = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d') # yesterday's date

# reading in data
url = 'https://data.nsw.gov.au/data/api/3/action/datastore_search?resource_id=21304414-1ff1-4243-a5d2-f52778048b29&q=%22'+yesterday+'%22'
fileobj = urllib.request.urlopen(url)
dict_data = fileobj.read()
dict_data2 = json.loads(dict_data) # loading string returned from endpoint into dictionary

## Note: data is stored as nested dictionary e.g. {meta data{results}}

# print total cases
total_cases = dict_data2['result']['total']

# print local government areas as a list
lga_list = [] # initialise list
record_list = dict_data2['result']['records']
for dict_entry in record_list:
    if dict_entry['lga_name19'] != None:
        modified_entry = re.sub(r"\([^()]*\)", "", dict_entry['lga_name19'])
        lga_list.append(modified_entry + '(' + (dict_entry['postcode']) + ')')
    else:
        lga_list.append("Not Available")

# helper function to return string from list
def listtostring(input_list):
    final_string = ""
    final_string = '\n'.join([str(item) for item in input_list])
    return final_string

# sending out SMS to numbers
from twilio.rest import Client

# Twilio account details
account_sid = "" # Insert account id here 
auth_token = "" #Insert authentication token here 
numbers = ["+61"] # add numbers you want to send here
# karl, mum, alison, james, brandon, donald, hillman, daniel

client = Client(account_sid, auth_token)
message = client.api.account.messages.create(

    to=numbers,
    from_="+123456789",
    body="Welcome to Karl's COVID-19 SMS notification service - you are a beloved friend of Karl's and so he has provided you this service free of charge to keep you safe during these tough times. On the " + str(yesterday) +
         " there had been a total of " + str(total_cases) + " cases confirmed at these locations/post codes: \n\n"
        +
    
        listtostring(lga_list)
    
        +
        "\n\nData in this notification has been taken from the data.NSW web API (provided by NSW Health). \n\nThis script is running on a Raspberry Pi 4 Model B 24/7 - notifications will be sent out daily at 6pm AEST everyday regarding coronavirus cases in the previous day. \n\nStay Safe.")


    
    
    

