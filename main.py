import os
from functions import ServerStatus as func


'''
###CONFIG###
Get your webhook link by editing the channel you wish to send webhooks, click on "Integrations" > "Webhooks"
Click "New Webhook" > Give the webhook a name, and icon, then save.  Copy URL
Get Role mention ID - put `\ in front of @role before sending mention to channel (\@role)
'''
url = 'https://www.newworld.com/en-us/support/server-status' # Should never need to change
webhook_url = 'discord-webhook-url' # Paste your discord channel webhook URL here
monitored_servers = ['Valgrind','Emain Albach','Savoya'] # Add or remove which ever servers you wish to monitor
mention_role = 'role-mention-id' # Paste role ID here, if you do not wish to mention a role, replace 'role_id' with None (ex mention_role = None)

cwd = os.path.abspath(__file__).replace('main.py', '')  # Absolute path to script file - DO NOT EDIT
'''
Start server status checks and webhook sending
old_status = gets exisitng json file, returns empty dict if none exists
new_status = run web scrape function to get status for servers in monitored_servers

'''
old_status_dict = func.get_old_status(cwd)
new_status_dict = func.scrape_status_page(url,monitored_servers)

'''
Check if existing JSON is empty.  If not empty, check differece in old vs new status
diff_dict = looks for difference between old and new status, stores changed servers and new status
Return message that correlates the status change, then sends embedded webhook, and updates
json file for next run
'''
if bool(old_status_dict):
    diff_status_dict = func.compare_status(old_status_dict,new_status_dict)
    for server,diff_status in diff_status_dict.items():
        if diff_statuts == '✅':
            print(f'{server} status has been updated: ✅')
            if old_status_dict[server] == '❌':
                message = 'The following server is now online!'
                func.webhook_embed(webhook_url,server,diff_status, message,mention_role)
            elif old_status_dict[server] == '🛠️':
                message = 'The following server has completed maintenance and has come back online!'
                func.webhook_embed(webhook_url,server,diff_status, message,mention_role)
            elif old_status_dict[server] == '⚠️':
                message = 'The following server is no longer full and should have reduce or no wait time to log in!'
                func.webhook_embed(webhook_url,server,diff_status, message,mention_role)

        elif diff_statuts == '⚠️':
            print(f'{server} status has been updated: ⚠️')
            message = 'The following server is now full!  Login queues should be expected.'
            func.webhook_embed(webhook_url,server,diff_status, message,mention_role)
        elif diff_statuts == '❌':
            print(f'{server} status has been updated: ❌')
            message = 'The following server is now offline!'
            func.webhook_embed(webhook_url,server,diff_status, message,mention_role)
        elif diff_statuts == '🛠️':
            print(f'{server} status has been updated: 🛠️')
            message = 'The following server is undergoing maintenance. A new status message will be sent when it becomes available!'
            func.webhook_embed(webhook_url,server,diff_status, message,mention_role)
        func.update_json_status(diff_dict,cwd)

else:
    func.update_json_status(new_status_dict,cwd)
    for server,status in new_status_dict.items():
        if status == '✅':
            message = 'The following server is online!'
            func.webhook_embed(webhook_url,server,status, message,mention_role)
        elif status == '❌':
            message = 'The following server is offline!'
            func.webhook_embed(webhook_url,server,status, message,mention_role)
        elif status == '⚠️':
            message = 'The following server is currently full! Loging qeueus should be expected.'
            func.webhook_embed(webhook_url,server,status, message,mention_role)
        elif status == '🛠️':
            message = ' The following server is undergoing maintenance! A new message status will be sent once it\'s back online.'
            func.webhook_embed(webhook_url,server,status, message,mention_role)




