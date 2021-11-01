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

## Set up the schedule
### Crontab
(*Using Ubuntu for example config - please check your distro/DE for setting up cron if you don't already know*)

* Figure out your cron schedule (ex: *every 5 mintues* [`*/5 * * * *`](https://crontab.guru/#*/5_*_*_*_*))
* Open terminal - run `crontab -e` - mine opens in Nano 
* Add your schedule - `*/5 * * * * python3 /home/user/path/to/script/directory/main.py`
* `ctrl + X` to close, `Y` to save to buffer, `Return/Enter` to confirm save and close
* Now your python script will run automatically every 5 minutes.


### Windows Task Scheduler
* Start > `Task Scheduler` > Enter to open the Task scheduler
* Create Task > Give it a name and allow it to run whether user is logged on or not (configure for Windows 10)
* Triggers Tab > **Begin the Task**: At startup, **Repeat Task every**: 5 minutes, **for a duration of**: Indefenitely
* Actions Tab > **New...**, **Action**: Start a program, **Program/script**: /path/to/python.exe, **Add arguments**: `main.py`, **Start in**: /path/to/script
* Save - Now the script will 5 minutes

## Version History

* 0.3
    * Added new functions for scraping and posting game updates/patch notes
    * Added vairable for second webhook url if user wishes to send updates/patch notes to a different channel than server status messages
* 0.2
    * Added options for mentioning roles
    * Updated readme to include full instructions for setup of script, crontab, and Windows task scheduler

* 0.1
    * Initial Release


## Acknowledgments

Inspiration was taken from user @40Cakes (their initial repo has since been deleted)
