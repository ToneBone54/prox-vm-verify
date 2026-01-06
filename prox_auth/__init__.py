# Package used to initiate authentication for both services
# USAGE
# - Sets up authentication parameters for both PVE and PBS
# - Initializes API token backends for both services

import configparser
import requests # Needed for proxmoxer
from proxmoxer import ProxmoxAPI

config = configparser.ConfigParser()
config.read('./prox_auth/my_config.ini')

# Authentication info
# PVE
pve_user = config['PVE']['user']
pve_token_name = config['PVE']['pve_token_name']
pve_token_value = config['PVE']['pve_token_value']
pve_ip = config['PVE']['ip']
pve_ssl = config['PVE'].getboolean('verify_ssl')

# PBS
pbs_user = config['PBS']['user']
pbs_token_name = config['PBS']['pbs_token_name']
pbs_token_value = config['PBS']['pbs_token_value']
pbs_service = config['PBS']['service']
pbs_ip = config['PBS']['ip']
pbs_ssl = config['PBS'].getboolean('verify_ssl')


# These variables become the backend used to access the APIs

pve = ProxmoxAPI(
    pve_ip, user=pve_user, token_name=pve_token_name, token_value=pve_token_value, verify_ssl=pve_ssl
)
pbs = ProxmoxAPI(
    pbs_ip, user=pbs_user, token_name=pbs_token_name, token_value=pbs_token_value, service=pbs_service, verify_ssl=pbs_ssl
)

# Prints all above information, mainly so I know the config is being pulled correctly. Mostly for debugging.
if __name__ == "__main__":
    print(f"PVE token info: {pve_ip}, {pve_user}, {pve_token_name}, {pve_token_value}, Verify SSL?: {pve_ssl}")
    print(f"PBS token info: {pbs_ip}, {pbs_user}, {pbs_token_name}, {pbs_token_value}, {pbs_service}, Verify SSL?: {pbs_ssl}")