# This script is mainly going to be used to test different scenarios of the main program interacting with the restored VM

from prox_auth import pve
from proxmoxer import ResourceException
import time
import json

node_name = "pve"
vmid = "113"

# Checks in with the VM to make sure we can communicate with the VM
# The default response if the agent is up is null/blank which is really dumb.
# Theoretically, the only two responses to this query should be the default or the ResourceException
# which is why the else breaks the loop. Some hyper security nerd will probably "uM aCkSuAlLy" this.
def agent_ping():
    unlock = 0
    while unlock == 0:
        try:
            pve.nodes(node_name).qemu(vmid).agent("ping").create()
        except ResourceException:
            print("Waiting 30 seconds for agent to respond... (5 for testing)")
            time.sleep(5)
        else:
            unlock = 1
    print("Agent responded")

# Prints "Hello World" to the VM shell (assuming it's Linux) as a test of the exec capabilities
def agent_hello():
    time.sleep(1)
    result_pid = pve.nodes(node_name).qemu(vmid).agent("exec").create(command=["/bin/bash", "-c", "echo Hello World"])
    ping_status = pve.nodes(node_name).qemu(vmid).agent("exec-status").get(pid=result_pid['pid'])
    print(ping_status['out-data'])

def ssh_check():
    time.sleep(1)
    result_pid = pve.nodes(node_name).qemu(vmid).agent("exec").create(command=["/bin/bash", "-c", "systemctl status ssh"])
    ssh_status = pve.nodes(node_name).qemu(vmid).agent("exec-status").get(pid=result_pid['pid'])
    print(json.dumps(ssh_status, indent=2))
agent_ping()
ssh_check()