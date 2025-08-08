## Proof of Concept that we can access a list of backups and check them against PVE and PBS to make sure we have the right one

from prox_auth import pve, pbs
import datetime as dt
from zoneinfo import ZoneInfo
from func import convert_epoch

group = pbs.admin.datastore("BoxOfMagic").groups.get()
content = pve.nodes("pve").storage("PBS").content.get(content='backup')

# Compare the last backup time from the PBS groups endpoint to what PVE shows was the creation time of the backup
for e in group:
    for i in content:
        if convert_epoch(i['ctime']) == convert_epoch(e["last-backup"]):
            print("match")
        else:
            print("no match")
