# VM Verify: Automated Proxmox VM testing

Ever had a VM restore but fail to boot or critical services fail to start? We all know that we should test our backups but it can be tough to do manually. Inspired by the backup verification technology behind [Datto BCDR](https://www.datto.com/products/siris/features/) SIRIS devices and combined with the file-level verification already done by Proxmox Backup Server, VM Verify covers the gap and makes sure that you're taking good and functional backups. 

*At this time, this is a work in progress. The script in the main branch might not work as stated below. Currently, it's in a proof of concept phase. Follow the dev branch if you'd like to follow my progress. I have a full time job as well so much of this will take a while to implement.*

## How it's supposed to work

This program relies on the Proxmoxer API wrapper for Python to query PVE/PBS. After creating and/or supplying proper credentials in the script variables, it will query the PBS API to find the most recent backup. It then compares it to the data supplied by PVE to make sure that is the most recent backup. Then, it uses the PVE API to create a VM out of that backup archive. We can then use the guest agent inside the VM to run any verifications you'd like such as:

* Verifying uptime
* Verifying certain services start
* Running a custom script (Future)
* Log any results

Then, the script will shutdown and destroy the VM and send a log result to a log file. Finally, it will repeat for any other backups.

## Roadmap

* Full POC that runs through the entire basic process:
    * Pull backups
    * Create VM out of most recent one
    * Boot VM and verify uptime
    * Log results, shutdown, and destroy VM
    * Recurse for any other VMs
* Checking if backups are verified through PBS. If not, it runs verification on them first.
    * This is crucial to the process as we'd like to know if the filesystem has been checked before running VM verification.
* Logging
    * Log file
    * Syslog
    * Webhook
* Ability to use custom verification scripts
* Creating a web interface so users can customize the process to their liking including:
    * Setting the user credentials/API tokens that the program uses to authenticate to PVE and PBS
    * Customizing what the verification process checks for
        * Checking running services
        * Checking uptime
        * Using custom scripts
    * Much more