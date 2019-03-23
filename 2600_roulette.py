from datetime import datetime,timedelta # For all the date processing
import calendar				# Just to get the first friday of a month
import argparse				# To get year/month argument from user
import re				# Because I don't know how to breath without it
import random				# To get that random meeting location
from roulettesubs import validate_arg, waybackmeetings, currentmeetings, location_parse, state_parse, all_location_parse, is_states

parser = argparse.ArgumentParser(description='2600 Roulette - Tour random 2600 meetings, together')
parser.add_argument('day', help='yyyymm of 2600 Meeting', default='none')
parser.add_argument('-s', help='United States only', action='store_true')
args = parser.parse_args()

today = datetime.today()
# Make sure the date provided isn't stupid and return datetime object of beginning of requested month
meeting = validate_arg(args.day,today)

# Get First Friday
c = calendar.Calendar(firstweekday=calendar.SUNDAY)
monthcal = c.monthdatescalendar(meeting.year,meeting.month)
first_friday = [day for week in monthcal for day in week if day.weekday() == calendar.FRIDAY and day.month == meeting.month][0]

# Get datetime object that is 90 days prior to the requested meeting
archive_date = first_friday - timedelta(days=100)

# Go fetch the archived 2600 meetings page from at least 90 days ago
old_meeting_list = waybackmeetings(archive_date)

# Pick a seed that is based on the Year-Month of the meeting
seed = '{:02d}{:d}'.format(first_friday.month,first_friday.year)
random.seed(int(seed))

# Parse out all of the meeting locations (city, location, state) and inform user how many were found
locations = location_parse(old_meeting_list)
city = random.choice(locations) # 'city' still in (city, location, state) format
if not args.s:
  ilocations = all_location_parse(old_meeting_list)
  icity = random.choice(ilocations) # 'city' still in (city, location, state) format
  print('...compiled a list of {} cities\n'.format(len(ilocations)))
  if not is_states(icity[2].lstrip()):
    city = icity
else:
  print('...compiled a list of {} cities\n'.format(len(locations)))


# See if the same city/location is listed in current/official 2600 site
new_meeting_list = currentmeetings()			# Go directly get current meeting page from 2600
regex = r'.+(' + re.escape(city[0]) + r':.+?)\n'		# Regex: anything(city: location)anything
if re.match(regex, new_meeting_list, re.MULTILINE|re.DOTALL):	# Is the city still listed
  matches = re.match(regex, new_meeting_list, re.MULTILINE|re.DOTALL)
  current_location = matches.group(1).split(':')[1]	# parse out just the city
  print('When: Friday {}-{}-{}'.format(first_friday.year,first_friday.month,first_friday.day))
  # If there were no venue changes (but the city is still the same
  if current_location.lower() == city[1].lower():
    print('State/Country: {}\nCity: {}\nLocation: {}'.format(city[2].split('\n')[-1],city[0],city[1]))
  else:
    # This city has a new/updated meeting location
    print('Meet at (updated) location of: {}: {} - {}'.format(city[2].split('\n')[-1],city[0],current_location))
else:
  # City no longer listed
  print("Meeting Location no longer listed, so it's up to you to to anyway:")
  print('State/Country: {}\nCity: {}\nLocation: {}'.format(city[2].split('\n')[-1],city[0],city[1]))
