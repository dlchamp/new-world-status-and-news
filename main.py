import os
from functions import ServerStatus as status_func
from functions import GameNews as news_func

'''
###########################  USER CONFIGURATION  ###########################
How to get your webhook url - https://support.discord.com/hc/en-us/articles/228383668-Intro-to-Webhooks
Paste your discord webhook channel URLs into the two variables below
If you wish for there to only be one channel for both server status and game news (patch notes),
make leave news_webhook_url = server_status_webhook_url
'''
server_status_webhook_url = 'discord-webhook-url'
news_webhook_url = server_status_webhook_url # Add second webhook url if you wish to send news messages to a different channel
'''
Set your list of 1 or more servers you wish to monitor
Assign a mention role, if you wish - Get your ID by typing \@role-you-wish-to-mention.  Copy the full ID (ex: <@&8997895432165879>)
and paste between the ''.  If you don't wish to have a role, just replace 'role-mention-id' with None (ex: mention_role = None)
'''
monitored_servers = ['Valgrind','Emain Albach','Savoya']
mention_role = '<@&1234567890112354'  # Mention role or use None (no quotes)

###################### END OF USER CONFIGURABLE AREA   ######################

status_url = 'https://www.newworld.com/en-us/support/server-status' # Should never need to change
news_url = 'https://www.newworld.com/en-us/news'  # Should never need to change.
cwd =  os.getcwd() # Absolute path to working dir - DO NOT EDIT

'''
Get old server status and compare with new status, update changes and send messages to discord webhook url
'''
old_status_dict = status_func.get_old_status(cwd)
new_status_dict = status_func.scrape_status_page(status_url,monitored_servers)

if bool(old_status_dict):
    diff_status_dict = status_func.compare_status(old_status_dict,new_status_dict)
    for server,diff_status in diff_status_dict.items():
        if diff_status == '✅':
            print(f'{server} status has been updated: ✅')
            if old_status_dict[server] == '❌':
                message = 'The following server is now online!'
                status_func.webhook_embed(server_status_webhook_url,server,diff_status, message,mention_role)
            elif old_status_dict[server] == '🛠️':
                message = 'The following server has completed maintenance and has come back online!'
                status_func.webhook_embed(server_status_webhook_url,server,diff_status, message,mention_role)
            elif old_status_dict[server] == '⚠️':
                message = 'The following server is no longer full and should have reduce or no wait time to log in!'
                status_func.webhook_embed(server_status_webhook_url,server,diff_status, message,mention_role)

        elif diff_status == '⚠️':
            print(f'{server} status has been updated: ⚠️')
            message = 'The following server is now full!  Login queues should be expected.'
            status_func.webhook_embed(server_status_webhook_url,server,diff_status, message,mention_role)
        elif diff_status == '❌':
            print(f'{server} status has been updated: ❌')
            message = 'The following server is now offline!'
            status_func.webhook_embed(server_status_webhook_url,server,diff_status, message,mention_role)
        elif diff_status == '🛠️':
            print(f'{server} status has been updated: 🛠️')
            message = 'The following server is undergoing maintenance. A new status message will be sent when it becomes available!'
            status_func.webhook_embed(server_status_webhook_url,server,diff_status, message,mention_role)
        status_func.update_json_status(diff_dict,cwd)

else:
    status_func.update_json_status(new_status_dict,cwd)
    for server,status in new_status_dict.items():
        if status == '✅':
            message = 'The following server is online!'
            status_func.webhook_embed(server_status_webhook_url,server,status, message,mention_role)
        elif status == '❌':
            message = 'The following server is offline!'
            status_func.webhook_embed(server_status_webhook_url,server,status, message,mention_role)
        elif status == '⚠️':
            message = 'The following server is currently full! Loging qeueus should be expected.'
            status_func.webhook_embed(server_status_webhook_url,server,status, message,mention_role)
        elif status == '🛠️':
            message = ' The following server is undergoing maintenance! A new message status will be sent once it\'s back online.'
            status_func.webhook_embed(server_status_webhook_url,server,status, message,mention_role)


'''
Scrape articles, compare new articles with old articles, if articles updated, send new articles to discord webhook url
'''
new_articles_dict = news_func.scrape_news_articles(news_url)
old_articles_dict = news_func.get_old_articles(cwd)
send_articles_dict = {}

if bool(old_articles_dict):
    for article in new_articles_dict:
        if new_articles_dict[article]['title'] == old_articles_dict[article]['title']:
            pass
        else:
            send_articles_dict[article] = {
                            'title':new_articles_dict[article]['title'],
                            'desc':new_articles_dict[article]['desc'],
                            'url':new_articles_dict[article]['url'],
                            'img':new_articles_dict[article]['img']
                            }

            print('New article found -- Sending to Discord...')
    news_func.articles_webhook(news_webhook_url,send_articles_dict,mention_role)
    news_func.update_articles(new_articles_dict,cwd)
else:
    print('New article(s) found -- Updating articles.json...')
    news_func.update_articles(new_articles_dict,cwd)


