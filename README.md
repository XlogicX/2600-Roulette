# 2600-Roulette
Tour random 2600 meetings, together<br>
![alt tag](https://github.com/XlogicX/2600-Roulette/blob/master/roulette.png)

# Usage
Give this script a YYYYMM date and it will give you a 2600 meeting location to go to for that month. You can use the -s option if you want the choices limited to the United States Only.

Though it's a random 2600 meeting location, if a friend (or enemy) of yours runs this same script on a different computer, they will get the same suggested meeting location (because fixed seed).

# Frozen in Time
The meeting list is based on a cached version of the official 2600 meeting page, thanks to the WayBack Machine and their useful API. The cached version is about at least 3 months (100 days actually) before the meeting date requested. This 100 day window helps lock things in for the time frame, so everyone can prepare (flights, crash pads) and not have to worry about the meeting location changing becuase the official meetings listed by 2600 changed within that time (as in, one city being added or removed chnages the city pool and completely changes the random pick, even when the city it was going to pick was still there).

# Edge Cases
However, If the venue changes (in the same city) within that time, this script will know, and merely suggest the updated location with the same city. If the city is removed completely within the 3 month window... Just go anyway, assuming the venue didn't burn in a flood. And the script will warn you of this situation.

Pick a meeting month more than 3 months in the future at your own risk; the 3 month archive window may not help you. However, the meeting location will still be valid for everyone so long as 2600 doesn't change any meeting locations in that whole time.

Picking a meeting in the past is bad, and you should feel bad for trying it.

# Two Versions (States Vs. International)
Even though I originally created the script as US centric, the script intentionally defaults to an international version. This still mostly works well for those of us in the states, as the majority of the 2600 meeting locations are in the states anyway. A location outside of the US will occur maybe a couple to a few times a year. However, if the 'spin of the wheel' lands on a far away country and you'd rather have a city in the states, you can use the -s argument to pick a city in the US. What happens when you use the -s option on a month that the international version would have picked a US city anyway? They are using a different pool of cities that would surely affect the random result right? You would expect the international version to pick a different US city than the -s option one would.

The script handles the above situation and makes sure that if the international version picks a US location (which is common), that it will line up with the same city as the users always using the -s option.

# Maintenance and Code change
Python is one of my least frequently used langauges (for now), so things may not be perfect as of now and I will attempt to maintain the code. However, I will do it very conservatively, as to not disrupt the random functionality (to keep in consistent for everyone using it). For this reason, I still made a best effort to write reasonable code and attempt to address all of the edge-cases I could think of ahead of time.
