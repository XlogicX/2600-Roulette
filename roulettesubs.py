import re
from datetime import datetime,timedelta # For all the date processing
import http.client                      # To make WayBackMachine and 2600.com requests
import json                             # To gracefully parse json data from WayBack Machine api
import pprint

def validate_arg(date,today):
  if re.match(r'^\d{6}$', date): #Validation of 6 digits, ranges will be covered seperately for more granular error reporting
    year = int(date[:4])
    month = int(date[4:])
    if month > 12 or month < 1:
      print('Breh, what kind of month is {}'.format(month))
      quit()
    meeting = datetime(year, month, 1)
    deltadays = (meeting - today).days
    if deltadays > 90:
      print('This meeting date COULD be too far into the future, so results may not be accurate')
    if deltadays < 0:
      print('Picking a day in the past wouldn\'t make sense for this tool, so why pick one?')
      quit()
  else:
    print('Something was wrong with your date format (yyyymm), as in 202004 (April 2020).')
    quit()
  return(meeting)

def waybackmeetings(archive_meeting):
  """
  Get's an archived version of the 2600 meeting page. The arcived version is
  3 months back or older. This has to be done in two requests to archive.org.
  The first request is the query of which archived page is at least 3 months
  old. Once we have this page, we then can pull down that page and return its
  data.
  """
  # Get the time machined meeting page
  locations = http.client.HTTPConnection('archive.org')
  locations.request('GET', '/wayback/available?url=www.2600.com/meetings/mtg.html&timestamp={}{:02d}'.format(archive_meeting.year,archive_meeting.month))
  response = locations.getresponse()
  data = response.read().decode('utf-8')
  locations.close()
  locations_json = json.loads(data)

  locations = http.client.HTTPConnection('web.archive.org')
  newurl = re.sub(r'http://web.archive.org', '', locations_json['archived_snapshots']['closest']['url'], flags=re.IGNORECASE) 
  locations.request('GET', newurl)
  response = locations.getresponse()
  meeting_locations = response.read().decode('utf-8')
  locations.close()
  return meeting_locations

def currentmeetings():
  locations = http.client.HTTPSConnection('www.2600.com')
  locations.request('GET', '/meetings/mtg.html')
  response = locations.getresponse()
  meeting_locations = response.read().decode('utf-8')
  locations.close()
  return meeting_locations

def location_parse(webdata):
  cities = []
  with open('states.txt', 'rU') as states:
    [state_parse(webdata,state.rstrip(),cities) for state in states]
  return cities

def state_parse(data,state,cities):
  regex = r'.+' + re.escape(state) + r'\n(.+?)\n\n'
  if re.match(regex, data, re.MULTILINE|re.DOTALL):
     matches = re.match(regex, data, re.MULTILINE|re.DOTALL)
     places = matches.group(1)
     [cities.append([city.split(':')[0],city.split(':')[1],state]) for city in places.split('\n') if city != '']

def all_location_parse(webdata):
  cities = []
  #^([^:]+)\n([^:]+:[^:]+\n)+
  # Cut out just the location data part of the web page
  if re.match(r'.+pre>(.+?)<!--', webdata, re.MULTILINE|re.DOTALL):
    matches = re.match(r'.+pre>(.+?)<!--', webdata, re.MULTILINE|re.DOTALL)
    webdata = matches.group(1)
  else:
    print("Something was wrong/different about the wayback machine archived webdata")
    quit()
  
  # Parse Countries/States
  country = ''
  while re.match(r'^([^:]+?)\n([^:\n]+?:[^\n]+?\n)+', webdata, re.MULTILINE|re.DOTALL):
    matches = re.match(r'^([^:]+?)\n(([^:\n]+?:[^\n]+?\n)+)', webdata, re.MULTILINE|re.DOTALL)
    # Group 1 has Country/State, Group 2 has the city:location
    # Get each location (city, location, state)
    [cities.append([city.split(':')[0],city.split(':')[1],matches.group(1)]) for city in matches.group(2).split('\n') if city != '']

    # Remove Country/State before next iteration
    country = matches.group(1) + '\n' + matches.group(2)
    webdata = webdata.replace(country,'')
  return cities

def is_states(country):
  # Yes/No response
  with open('states.txt', 'r') as states:
    if any(country in state for state in states):
      return True
    else:
      return False
