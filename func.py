# General place for functions

import datetime as dt
from zoneinfo import ZoneInfo
import json

# Function to convert Unix time epoch to human readable time. Specifically Chicago time since that's my timezone.
def convert_epoch(epoch):
    central = ZoneInfo('America/Chicago')
    time_convert = dt.datetime.fromtimestamp(epoch, tz=central)
    return time_convert

def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=2)
    print(text)