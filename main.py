from prox_auth import pve, pbs
from helper import jprint, convert_epoch

# Get backup groups from PVE and PBS
pve_groups = pve.nodes("pve").storage("PBS").content.get()
pbs_groups = pbs.admin.datastore("BoxOfMagic").groups.get()

# Iterates through pve groups and compares their creation time to the last backup time reported by pbs
# When it finds a match, it grabs the volume ID of the backup to use later.
for b in pbs_groups:
    for v in pve_groups:
        if v['ctime'] == b['last-backup']:
            print(f"{v['volid']} matches PBS backup {b['backup-id']}")