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

## AI Usage Disclaimer
*This is a disclaimer to show how AI was used in this project. Please read this in its entirety to get a full understanding of the developer's stances. Any statements in this disclaimer are the developer's opinions only.*

Firstly, I want to say that I believe AI is, will always be, and should be used as a tool. However, I DO NOT believe in using AI to generate full "working" code, art of any kind (imagery/visuals, 3D models, music, etc.), or replace anything that can be done by a human. I believe in expanding my own skills by teaching myself as much as possible and trying to understand how things work rather than building something quickly. I've never appreciated working on something without knowing what's happening or how it works and I try to extend that into the work I produce. As AI has progressed, I've tested the waters with its capabilities across ChatGPT, Gemini, and now Claude. As of writing (8/4/26), Claude has been the one I've found to be the most helpful for my use cases. For transparency, I do not use or have a paid subscription to Claude. I believe that I don't need the extra capabilities that come with it or really know how it would benefit me and how I work. I also don't want the agent having write access to any files, project related or otherwise. After seeing multiple stories of AI agents panicking and deleting files or even entire codebases, I'd rather just not mess with it. 

These are the various ways I've used Claude in this project. Please note this may be expanded as progress is made:

- "Rubber Ducky"
   - If you're unaware, a common debugging technique in programming is to use an inanimate object, such as a rubber ducky, to talk through a problem using natural language in an attempt to solve a problem. Often, this makes mistakes jump out more since you're looking at the problem from the bigger picture. Similarly, I will often approach Claude with an issue I've encountered and talk through possible solutions.
   - Similar to the rubber ducky, I use Claude as a second pair of eyes to help catch small mistakes. I have given Claude read access to this repo and its branches through the official Github connector but at no point in this project's development has Claude had write access to the Github repo OR working project files on my personal devices, nor do I intend to give it write access. All code and logic has been designed and written by me. The only caveat(s) to this is if Claude suggests something that fits my idea, I'll explore it and choose to implement it from there.

- Internal documentation
   - Behind the scenes, I have an internal documentation system that helps me track progress and keep notes on whatever I want to write down. Basically a project journal. I do not intend on publishing it at this time, mainly because it's a tool to keep me on track and much of it is likely just rambling and incomplete thoughts. Part of this documentation includes a "State of the System (SotS)" document. This is an evolving document that gets overwritten at the end of each session with a summary of how the code works at that moment in time, what's broken, and what items are next to be worked on.
   - Because I have a tendency to leave this project hanging for long periods, this serves as a "single point of truth" so I can come back to the project and know what to work on next without reviewing the entire codebase each time. Along with this, I keep individually dated logs that serve as a session journal where I write down things I think of while working (anything that comes to mind really). At the start of a session, I create new chats in a Claude project dedicated to this project dated the same. When I've finished a session and committed code, I will paste the session notes into the chat and tell Claude to summarize the notes, newly committed code, and all the context of the chat into points fitting the SotS criteria I mentioned earlier. From there I will write up a new SotS for the next session. The new SotS also gets pasted into a new Claude chat to give Claude context and update its memory.

- Research and code examples
  - This project is being developed alongside me learning Python. If I come across something that I have questions about and I'm not finding solid answers on Google, I'll usually turn to Claude to talk it through and get some examples. Any example generated by Claude does not end up in the final result as it will often have incompatible logic or I modify it to fit what I'm doing.
  - This is not to say that I immediately turn to Claude for something that is clearly a quick Google search. I always do my best to research things thoroughly using Google first to see if there's anything that matches what I'm doing. This is common for quick reference like nuances in Python. 
 
As much as AI has fatigued just about every aspect of modern life, I do believe that it has a place if used properly. However, I will always believe that humans can produce results far better than any LLM will ever be able to. All it takes is some curiosity and the will to learn and create something awesome. For me, it boils down to this: I'd rather ship slop I wrote myself over 3 months and understand than AI slop generated in 3 seconds that I can't maintain. If you're like me and follow some IT/homelab subreddits, you've undoubtedly seen many projects that were created in a very short amount of time that try to solve a niche problem that (sometimes) another FOSS project or proprietary solution already covers. That's not my intention for this project. I intend to build something that will work while also having the ability to maintain it. If you've read all this and are still turned off to this project because of AI use, I totally understand. 

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
    * Much more
