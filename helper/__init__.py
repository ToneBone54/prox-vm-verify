# Package containing (as of writing) miscellaneous helper functions that I found helpful in testing

import datetime as dt
from zoneinfo import ZoneInfo
import json

# Function to convert Unix time epoch to human readable time. Specifically Chicago time since that's my timezone.
# I'm still on the fence on this one as to whether or not this is necessary.
# When I finally get around to writing logging functions, it might be of use. 
def convert_epoch(epoch):
    central = ZoneInfo('America/Chicago')
    time_convert = dt.datetime.fromtimestamp(epoch, tz=central)
    return time_convert

# Function to pretty up JSON responses. Pretty much only used in early testing and debugging
# until I realized that Proxmoxer responses are already in Python lists/dicts
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=2)
    print(text)

# Displays time in Central time. Used for timestamping outputs
def timestamp():
    format = "%Y-%m-%d %H:%M:%S"
    central = ZoneInfo('America/Chicago')
    now = dt.datetime.now(central)
    return now.strftime(format)