# New World Server Status (Discord Webhook)

A simple script that scrapes the server status from `https://www.newworld.com/en-us/support/server-status` and reports status changes via Discord webhook.

## Description

The script should be setup to run on a schedule, I run it every 5 minutes via a cron job, but it can be setup to run as often as you'd like in whichever scheduling method
is most convenient for you.
Once this data has been retrieved, it will compare it against existing last known statuses, stored as JSON.  If no existing statuses found, it will write the 
newest status for each server into JSON and send an initial status message to the Discord webhook URL configured.  If existing status are found, and the status has been updated, it will send a new status message for each changed 
server to the Discord webhook URL.

![Server Status Example](https://raw.githubusercontent.com/dlchamp/new-world-status/main/sample_images/server_status_example.JPG) ![Game Updates Example](https://raw.githubusercontent.com/dlchamp/new-world-status/main/sample_images/game_updates_news_example.JPG)

## Getting Started

### Dependencies

* [Python 3.9.7](https://www.python.org/downloads/release/python-397/)
* Cron, Windows task scheduler, or any other task scheduling methods you're most comfortable with
* See requirements.txt for full python dependencies

### Installing

* Install python (for Windows - Add Python to PATH or environment variables)
* Clone this repo, or download as zip, unpack 
* Navigate to the directory where you unpacked or stored the repo
* Open command prompt or terminal within that directory
* Install requirements `pip install -r requirements.txt`
*

### Configure the script

* Open main.py in your favorite text editor.
* Get your Discord webhook URL ([Webhook setup help and info](https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks))
* Add second URL if you wish to have updates/patch notes sent to a different channel, if not, leave `news_webhook_url` as is.
* Input the server's you wish to monitor in the `monitored_servers` list
* Input a role that you'd like to mention when new updates are sent to a channel - use `None` if you do not wish to setup a mention role.  (*ex: mention_role = '<@&78986543516879564'* or *mention_role = None*)
* Setup to run on a schedule via crontab or Windows task schedular, or whatever other means you find the most comfortable. 


## Version History

*1.3
    * Fixed an issue where the script was sending every article when one article changed
    * Instead of grabbing every single article, every time, script now just grabs the latest article
    * Fixed spelling issues in the embed message and fixed an issue where a mispelled variable wsa causing errors, breaking the script

* 1.2
    * Added new functions for scraping and posting game updates/patch notes
    * Added vairable for second webhook url if user wishes to send updates/patch notes to a different channel than server status messages
* 1.1
    * Added options for mentioning roles
    * Updated readme to include full instructions for setup of script, crontab, and Windows task scheduler

* 1.0
    * Initial Release


## Acknowledgments

Inspiration was taken from user @40Cakes (their initial repo has since been deleted)
