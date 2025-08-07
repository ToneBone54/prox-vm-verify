from prox_auth import pve, pbs
import json
import datetime as dt
from zoneinfo import ZoneInfo


# Wrapper to make JSON more readable. May not be needed but nice to have
def jprint(obj):
    text = json.dumps(obj, sort_keys=True, indent=2)
    print(text)

# Function to convert Unix time epoch to human readable time. Specifically Chicago time since that's my timezone.
def convert_epoch(epoch):
    central = ZoneInfo('America/Chicago')
    time_convert = dt.datetime.fromtimestamp(epoch, tz=central)
    return time_convert

group = pbs.admin.datastore("BoxOfMagic").groups.get()
snapshots = pbs.admin.datastore("BoxOfMagic").snapshots.get()

for e in range(len(group)):
    for i in range(len(snapshots)):
        if snapshots[i]['backup-time'] == group[e]['last-backup']:
            print(f"{snapshots[i]["backup-id"]} matches last backup ({group[e]['last-backup']})")
    