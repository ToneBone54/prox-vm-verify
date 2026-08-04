from prox_auth import pve, pbs, config
from time import sleep
# from helper import get_volid

### FUNCTIONS

# Match each PBS backup group's most recent backup to its corresponding PVE volid by comparing timestamps
def get_volid():
    # Get backup groups from PVE and PBS
    pve_groups = pve.nodes(node).storage(storage).content.get()
    pbs_groups = pbs.admin.datastore(datastore).groups.get()

    # print(pve_groups)
    # print(pbs_groups)

    # Iterates through pve groups and compares their creation time to the last backup time reported by pbs
    # When it finds a match, it grabs the volume ID of the backup to use later.

    for b in pbs_groups:
        for v in pve_groups:
            if v['ctime'] == b['last-backup']:
                print(f"{v['volid']} matches PBS backup {b['backup-id']}")
                ids.append(v['volid'])


    print(f"All volids: {ids}")

# Queries active PVE qmrestore tasks and grabs the task ID of a restore with the test VMID
def restore_monitor():
    restore_upid = []
    # Collects all active restore tasks for the temp VM
    running_restore_tasks = pve.nodes(node).tasks.get(vmid=9999, typefilter="qmrestore", source="active")
    print(f"Found task: {running_restore_tasks}")
    if running_restore_tasks['status'] == 'RUNNING':
        restore_upid = running_restore_tasks['upid']
    
    return restore_upid

# Quick function to always return the latest VM status
def get_vm_status():
    return pve.nodes(node).qemu("9999").status("current").get()

# Logic to destroy the running test vm
def destroy_routine(prox, vmid):
    destroy_params = {      # Parameters for the destroy command
        "destroy-unreferenced-disks": 1,
        "purge": 1
    }

    vm_status = get_vm_status()
    
    if vm_status['status'] == 'running':
        print(f"Shutting down {vmid}...")
        prox.nodes(node).qemu(vmid).agent("shutdown").create()

    while vm_status['status'] != 'stopped':
        vm_status = get_vm_status()
        print(f"Current VM Status: {vm_status['status']}")
        sleep(5)

    print(f"Destroying VM {vmid}...")
    prox.nodes(node).qemu(vmid).delete(**destroy_params)

    print(f"VM {vmid} cleaned up!")


### MAIN

# Initial variables to use in the following code, including above functions.
ids = []
node = config['PVE']['node']
storage = config['PVE']['backup_storage']
datastore = config['PBS']['datastore']





# Get most recent volume ids of all backups in chosen datastore
get_volid()

# restore_id = restore_monitor()

for i in ids:
    print(f"Volume ID found: {i}")
    sleep(5) #Used in testing for console clarity
    print(f"Creating VM from volid {i}...")
    pve.nodes(node).qemu.create(vmid=9999, archive=i, start=1)

    # Print the task ID of the restore 
    # restore_id = restore_monitor()
    # print(f"Found restore ID: {restore_id}")

    # Arbitrary wait timer
    sleep(60)

    # Polls VM status to make sure it's running
    current_status = get_vm_status()
    print(f"Current status: {current_status['status']}")

    # Watch VM uptime and proceed after uptime is greater than 60 seconds
    while current_status['uptime'] < 60:
        print("VM not ready yet...")
        current_status = get_vm_status()
        sleep(5)

    print(f"VM verified!")

    destroy_routine(pve, "9999")

print("Verification complete!")