# new-world-status# New World Server Status (Discord Webhook)

A simple script that scrapes the server status from `https://www.newworld.com/en-us/support/server-status` and reports status changes via Discord webhook.

## Description

The script should be setup to run on a schedule, I run it every 5 minutes via a cron job, but it can be setup to run as often as you'd like in whichever scheduling method
is most convenient for you.

The script looks at the `monitored_servers` list in `main.py` and scrapes the server name and status for each server name in that list from `https://www.newworld.com/en-us/support/server-status`.
Once this data has been retrieved, it will compare it against existing last known statuses, stored as JSON.  If no existing statuses found, it will write the 
newest status for each server into JSON and send an initial status message to the Discord webhook URL configured.  If existing status are found, and the status has been updated, it will send a new status message for each changed 
server to the Discord webhook URL.

## Getting Started

### Dependencies

* [Python 3.9.7](https://www.python.org/downloads/release/python-397/)
* Cron, Windows task scheduler, or any other task scheduling methods you're most comofortable with
* See requirements.txt for full python dependencies

### Installing

* Install python (for Windows - Add Python to PATH or environment variables)
* Clone this repo, or download as zip, unpack 
* Navigate to the directory where you unpacked or stored the repo
* Open command prompt or terminal within that directory
* Install requirements `pip install -r requirements.txt`

### Executing program

* Run `python main.py` or `python3 main.py` if you have multiple version of Python installed


## Version History

* 0.1
    * Initial Release


## Acknowledgments

Inspiration was taken from user @40Cakes (their initial repo has since been deleted)
