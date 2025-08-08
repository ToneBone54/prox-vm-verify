from prox_auth import pve, pbs
import json
from func import convert_epoch

volid = "PBS:backup/vm/113/2025-08-06T14:11:38Z"

# Unfinished. API command to create a vm out of the provided backup volid
pve.nodes("pve").qemu.create(vmid=301, archive=volid)