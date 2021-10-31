import os
import json
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed


class ServerStatus:
    def __init__(self):
        super().__init__()
        self.cwd = os.getcwd()


    def webhook_embed(webhook_url,server,status,message,role):
        if status == "✅":
            status_color = "00cf00"
        elif status == "❌":
            status_color = "ff0000"
        else:
            status = "ffaa00"

        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        if role is None:
            embed = DiscordEmbed(title='Server Status', description=f'**{message}**', color=status_color)
        else:
            embed = DiscordEmbed(title='Server Status', description=f'{role}\n**{message}**', color=status_color)
        embed.add_embed_field(name='Server', value=server)
        embed.add_embed_field(name='Status', value = status)
        webhook.add_embed(embed)
        response = webhook.execute()


    def compare_status(old_status,new_status):
        diff_dict = {}
        for key in new_status:
            if old_status[key] != new_status[key]:
                diff_dict[key] = new_status[key]
        return diff_dict


    def get_old_status():
        cwd = os.getcwd()
        with open(f'{cwd}/status.json') as x:
            old_status = json.load(x)
        return old_status

    def update_json_status(new_status):
        cwd = os.getcwd()
        with open(f'{cwd}/status.json','w+') as f:
            json.dump(new_status, f, indent=2)


    def scrape_status_page(url,monitored_servers):
        r = requests.get(url)
        page = BeautifulSoup(r.content, 'html.parser')
        status_section = page.find('div', class_='ags-ServerStatus-content-responses')
        server_sections = status_section.find_all('div', class_='ags-ServerStatus-content-responses-response-server')

        new_status = {}

        for server in server_sections:
            server_name = server.find('div', class_='ags-ServerStatus-content-responses-response-server-name').text.strip()
            if server_name in monitored_servers:
                if server.find('div',class_='ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--up'):
                    new_status[server_name] = '✅'
                if server.find('div',class_='ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--down'):
                    new_status[server_name] = '❌'
                if server.find('div',class_='ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--maintenance'):
                    new_status[server_name] = '🛠️'
                if server.find('div',class_='ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--full'):
                    new_status[server_name] = '⚠️'
        return new_status


