from prox_auth import pve, pbs, config
from time import sleep

def get_volid():
    # Get backup groups from PVE and PBS
    pve_groups = pve.nodes(node).storage(storage).content.get()
    pbs_groups = pbs.admin.datastore(datastore).groups.get()

    # Iterates through pve groups and compares their creation time to the last backup time reported by pbs
    # When it finds a match, it grabs the volume ID of the backup to use later.

    for b in pbs_groups:
        for v in pve_groups:
            if v['ctime'] == b['last-backup']:
                # print(f"{v['volid']} matches PBS backup {b['backup-id']}")
                ids.append({v['volid']})

    # print(f"All volids: {ids}")

config.read('./config.ini')

### MAIN

ids = []
node = config['PVE']['node']
storage = config['PVE']['backup_storage']
datastore = config['PBS']['datastore']

# Get most recent volume ids of all backups in chosen datastore
get_volid()

for i in ids:
    pve.nodes(node).qemu.create(vmid=500, archive=i, start=1)
    sleep(120)
