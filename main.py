from prox_auth import pve, pbs
import datetime as dt
import time
from zoneinfo import ZoneInfo
from func import timestamp, convert_epoch

# Function to monitor the restore task until it's done
def block_until_complete(prox_api, task_id, node_name):
    data = {"status": ""}
    while (data["status"] != "stopped"):
        data = prox_api.nodes(node_name).tasks(task_id).status.get()
        print(f"{timestamp()}: Job Status: {data['status']}")
        time.sleep(10)
    return data['exitstatus']

# Monitors the uptime of the VM (for now) and shuts it down after 60 secs
# This is where we could define some verification scripts
# After those, it shuts down and destroys the VM
def destroy_routine():
    destroy_params = {      # Parameters for the destroy command
        "destroy-unreferenced-disks": 1,
        "purge": 1
    }

    # Current status of the restored VM
    current_status = pve.nodes("pve").qemu("301").status.current.get()

    while current_status['uptime'] < 60:
        print(f"{timestamp()}: VM not ready yet")
        current_status = pve.nodes("pve").qemu("301").status.current.get()
        time.sleep(10)
    pve.nodes("pve").qemu("301").agent("shutdown").create()
    print(f"{timestamp()}: VM shutdown, executing destroy...")
    time.sleep(5)
    pve.nodes("pve").qemu("301").delete(**destroy_params)


### MAIN 

group = pbs.admin.datastore("BoxOfMagic").groups.get()
content = pve.nodes("pve").storage("PBS").content.get(content='backup')

# Compare the last backup time from the PBS groups endpoint to what PVE shows was the creation time of the backup

for e in group:
    for i in content:
        if convert_epoch(i['ctime']) == convert_epoch(e["last-backup"]):
            print(f"{i['volid']} found!")
            volid = i['volid']
            
            # Start the restore of the above volid to a new VM and starts it when complete
            pve.nodes("pve").qemu.create(vmid=301, archive=volid, start=1)
            
            # Queries all tasks for a restore job for VM 301
            running_tasks = pve.nodes("pve").tasks.get(vmid=301, typefilter="qmrestore", source="all")
            
            # Searches the running tasks for the upid of the active restore and stores it in a variable
            for i in running_tasks:
                if i['status'] == "RUNNING":
                    restore_upid = i['upid']
                    print(f"{timestamp()}: {i['upid']} is running.")
            restore_result = block_until_complete(pve, restore_upid, "pve")
            
            # Checks the restore result and begins the destroy routine if the status is OK
            if restore_result == "OK":
                destroy_routine()





            