# Sets up authentication to PVE and PBS so we can call the APIs using the Python API client Proxmoxer
# https://proxmoxer.github.io/docs/latest/
# Creds are ignored from Git

from proxmoxer import ProxmoxAPI
from creds import pve_token_value, pve_token_name, pbs_token_name, pbs_token_value


pve = ProxmoxAPI(
    "192.168.1.70", user="tbone@pve", token_name=pve_token_name, token_value=pve_token_value, verify_ssl=False
)

pbs = ProxmoxAPI(
    "192.168.1.30:8007", user="tbone@pbs", token_name=pbs_token_name, token_value=pbs_token_value, service="pbs", verify_ssl=False
)