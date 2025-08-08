from prox_auth import pve, pbs
import datetime as dt
from zoneinfo import ZoneInfo

# Function to convert Unix time epoch to human readable time. Specifically Chicago time since that's my timezone.
def convert_epoch(epoch):
    central = ZoneInfo('America/Chicago')
    time_convert = dt.datetime.fromtimestamp(epoch, tz=central)
    return time_convert

group = pbs.admin.datastore("BoxOfMagic").groups.get()
snapshots = pbs.admin.datastore("BoxOfMagic").snapshots.get()

for grp in group:
    for snap in snapshots:
        if snap["backup-time"] == grp["last-backup"]:
            print(f"{snap["backup-id"]} match ({convert_epoch(grp['last-backup'])})")
        else:
            print("no match")
    