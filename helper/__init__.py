# Package containing (as of writing) miscellaneous helper functions that I found helpful in testing

import datetime as dt
from zoneinfo import ZoneInfo
import json

# Convert Unix time epoch to human readable time. 
# Certain API endpoints return times as Linux epochs in their responses. I used this early on to convert them to a readable format for testing,
# mainly to help me understand API responses.
# I'm still on the fence on this one as to whether or not this is necessary but I'm leaning on not. Mainly, because where these time values are being used and checked,
# it doesn't need to log it (yet), only compare it to another epoch.
def convert_epoch(epoch):
    central = ZoneInfo('America/Chicago')
    time_convert = dt.datetime.fromtimestamp(epoch, tz=central)
    return time_convert

# Function to pretty up Proxmoxer responses. Pretty much only used in early testing and debugging
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