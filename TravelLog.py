# collect user input for distance travelled, compute progress against goal

import json
import os
import sys
from datetime import date
# import smtplib
# import email.utils
# from email.mime.text import MIMEText


def load_data(datafile):
    """
    if database exists, return contents as json_data variable. if not, create new file with 'totalDistance' and
    'distanceTravelled' (set as empty list)
    :rtype : dict
    """
    if os.path.exists(datafile):
        with open(datafile, "r") as json_file:
            json_data = json.load(json_file)
    else:
        json_data = {'totalDistance': 1910, 'distanceTravelled': []}
        with open(datafile, "w") as json_file:
            json.dump(json_data, json_file)
    return json_data


def write_data(datafile, json_data):
    """
writes any changes to existingData variable to JSON data file
    :param datafile: path to JSON data file
    :param json_data: pass existingData variable to function
    """
    with open(datafile, "w") as json_file:
        json.dump(json_data, json_file)


def collect_new_data(datafile):
    """
    prompt, store, and write (using write_data function) new travel data based on user input
    """
    user_input = float(input('How far did you travel today? '))
    existingData['distanceTravelled'].append(user_input)
    write_data(datafile, existingData)  # write changes to file using write_date function
    return existingData


def gen_graph(file_path, data_string):
    """
    writes variable (preformatted as string) to .dat file, then calls termgraph against that file
    """
    with open(file_path, 'w+') as f:
        f.write(data_string)
    os.system('python files/termgraph.py {}'.format(file_path))


def section_divider(display_text):
    print(display_text)
    print('_'*70, '\n')


# call data reading functions, returns json_data dictionary
existingData = load_data('files/TravelData.json')

# test whether user wants to input new data: if no, skips to displaying existing stats
print('\n')

# if no daily data exists, jump straight to collection
if len(existingData['distanceTravelled']) == 0:
    collect_new_data('files/TravelData.json')

# otherwise, prompt user for new data collection
else:
    newDataPrompt = input('Welcome! Do you have new data to log? (Y/N): ')

    yes = set(['y', 'Y', 'yes', 'Yes'])

    if newDataPrompt in yes:
        collect_new_data('files/TravelData.json')

# calculate progress variables
totalDistance = existingData['totalDistance']
completedDistance = sum(existingData['distanceTravelled'])
remainingDistance = totalDistance - completedDistance

totalDays = len(existingData['distanceTravelled'])
averageDistance = completedDistance / totalDays

today = date.today()
end = date(2015, 11, 20)

remainingDays = str(end - today)
remainingDays = remainingDays[:3]

averageDays = int(remainingDistance / averageDistance)
overUnder = int(remainingDays) - averageDays

# print various stats for user
print('\n')
print('Your trip so far...', '\n')

# print(str(totalDays) + ' days in.')
# print(str(completedDistance) + ' km travelled.')

# generate graph of current distance against total
progress_graph = 'Total Distance    :, ' + str(totalDistance) + '\n' + 'Completed Distance:, ' + str(completedDistance)

section_divider('Total Trip Progress')

gen_graph('files/progressData.dat', progress_graph)
print(str(round(float(completedDistance)/float(totalDistance)*100, 2)) + '% complete.')
print(str(round(remainingDistance, 2)) + ' km remain.')
print('\n')

# generate graph comparing all daily distance totals
day = 1
daily_distance_graph = ''

for e in existingData['distanceTravelled']:
    if day < 10:
        daily_distance_graph = daily_distance_graph + 'Day 0{},'.format(day) + '{}'.format(e) + '\n'
    else:
        daily_distance_graph = daily_distance_graph + 'Day {},'.format(day) + '{}'.format(e) + '\n'
    day += 1

section_divider('Daily Distance Totals')

gen_graph('files/dailyData.dat', daily_distance_graph)

print(str(round(averageDistance, 1)) + ' km current daily average.')
print(str(remainingDays) + ' days before departure.')
print(str(averageDays) + ' days remain at current pace.')
if overUnder == 0:
    print('You are on schedule.')
elif overUnder == 1:
    print(str(overUnder) + ' days ahead of schedule.')
elif overUnder > 0:
    print(str(overUnder) + ' days ahead of schedule.')
elif overUnder == -1:
    print(str(-1 * overUnder) + ' day behind schedule.')
else:
    print(str(-1 * overUnder) + ' days behind schedule.')
print('\n')

# sys.exit(0)

# print('Sending email...', '\n')

# # Create the message
# # https://pymotw.com/2/smtplib/
# msg = MIMEText('Test')
# msg['To'] = email.utils.formataddr(('Chris Watkins', 'chris.watkins93@gmail.com'))
# msg['From'] = email.utils.formataddr(('Chris Watkins', 'chris.watkins93@gmail.com'))
# msg['Subject'] = 'Trip updates...'+'Day {}'.format(day)
#
# server = smtplib.SMTP('mail')
# server.set_debuglevel(True) # show communication with the server
# try:
#     server.sendmail('author@example.com', ['recipient@example.com'], msg.as_string())
# finally:
#     server.quit()
