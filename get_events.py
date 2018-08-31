from __future__ import print_function
from datetime import datetime, timedelta
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools

# If modifying these scopes, delete the file token.json.
SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
DAYS_DELTA = 1


def get_service():
    store = file.Storage('token.json')
    creds = store.get()
    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets('credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    return build('calendar', 'v3', http=creds.authorize(Http()), cache_discovery=False)


def get_events():
    service = get_service()

    # To get list of calendars and it's ids uncomment next code
    # calendars_result = service.calendarList().list().execute()
    # calendars = calendars_result.get('items', [])
    # for cal in calendars:
    #   print(cal['summary'], "id:", cal['id'])

    now = datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    end_date = (datetime.utcnow() + timedelta(days=DAYS_DELTA)).isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary',
                                          timeMin=now, timeMax=end_date,
                                          singleEvents=True,
                                          orderBy='startTime').execute()
    events = events_result.get('items')
    res = []
    for event in events:
        start = event['start'].get('dateTime')
        res.append((start, event['summary']))
    return res


if __name__ == '__main__':
    get_events()
