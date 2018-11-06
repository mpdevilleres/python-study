"""
This Application is to monitor attendance for events
"""
import datetime
import uuid
import json
import os
import csv
import sys


# HELPER FUNCTION
def generate_event_no():
    return uuid.uuid4().hex


def save_config(event):
    event['date'] = f'{event["date"]:%y%m%d %H:%M}'
    with open('config.json', 'w') as outfile:
        json.dump(event, outfile)


def update_config(event):
    event_registrants = event['registrants']
    while True:
        event_registrant = input("Enter Registrant or type q to stop: ")
        if event_registrant.lower() == 'q':
            break
        event_registrants.append([event_registrant, f'{len(event_registrants)+1:03}'])
    event['registrants'] = event_registrants

    return event


def get_config():
    if not os.path.isfile('config.json'):
        return None
    with open('config.json') as infile:
        data = json.loads(infile.read())
        data['date'] = datetime.datetime.strptime(data['date'], '%y%m%d %H:%M')
    return data


def setup_event():
    event_date = input("Event Date and Time: ")
    event_location = input("Location: ")

    event_registrants = []
    # [name, registration_no]
    while True:
        event_registrant = input("Enter Registrant or type q to stop: ")
        if event_registrant.lower() == 'q':
            break
        event_registrants.append([event_registrant, f'{len(event_registrants)+1:03}'])

    event = {
        'date': datetime.datetime.strptime(event_date, '%y%m%d %H:%M'),  # Date and Time
        'location': event_location,  # Emirates
        'registrants': event_registrants,  # person
        'event_no': generate_event_no(),  # Autogenerated Int
    }

    return event


def sign_in():
    try:

        attendance = int(input("Please enter your registration no: "))
        attendance = f'{attendance:03}'

        # f'{len(event_registrants)+1:03}'
        # [(name, num),(name, num)]
        # STRATEGY 1
        # registration_nos = []
        # for registrant in event['registrants']:
        #    registration_nos.append(registrant[1])

        # STRATEGY 2
        registration_nos = [i[1] for i in event['registrants']]

        if attendance in registration_nos:
            # check csv if exist append
            # check csv if not exist create
            print("Registered")
            is_exist = os.path.isfile('attendance.csv')
            with open('attendance.csv', 'a') as outfile:
                w = csv.DictWriter(outfile, ['time', 'registration_no'], lineterminator='\n')

                if not is_exist:
                    w.writeheader()

                w.writerow({
                    'registration_no': attendance,
                    'time': f'{datetime.datetime.now():%H:%M}'
                })

        else:
            print("Not Registered")
    except KeyboardInterrupt:
        sys.exit()


# -----------------------------------------
# SETUP EVENT
# -----------------------------------------
# STEP 1
event = get_config()

if event:
    is_update = input("Do you want to append registrants (y/N): ")
    if is_update.lower() == 'y':
        event = update_config(event)
        save_config(event)

if event is None:
    event = setup_event()
    save_config(event)

# STEP 2
while True:
    sign_in()
