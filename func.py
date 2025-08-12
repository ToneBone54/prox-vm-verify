# General place for common testing functions

import datetime as dt
from zoneinfo import ZoneInfo
import json

# Function to convert Unix time epoch to human readable time. Specifically Chicago time since that's my timezone.
def convert_epoch(epoch):
    central = ZoneInfo('America/Chicago')
    time_convert = dt.datetime.fromtimestamp(epoch, tz=central)
    return time_convert

# Function to pretty up JSON responses
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=2)
    print(text)
# Displays time in Central time. Used for timestamping outputs
def timestamp():
    format = "%Y-%m-%d %H:%M:%S"
    central = ZoneInfo('America/Chicago')
    now = dt.datetime.now(central)
    return now.strftime(format)