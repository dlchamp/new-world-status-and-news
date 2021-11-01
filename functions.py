import json
import requests
from bs4 import BeautifulSoup
from discord_webhook import DiscordWebhook, DiscordEmbed


class ServerStatus:
    def __init__(self):
        super().__init__()


    def webhook_embed(webhook_url,server,status,message,role):
        if status == "✅":
            status_color = "00cf00"
        elif status == "❌":
            status_color = "ff0000"
        else:
            status = "ffaa00"

        webhook = DiscordWebhook(url=webhook_url, rate_limit_retry=True)
        if role is None:
            embed = DiscordEmbed(title='Server Status',
                description=f'**{message}**', color=status_color)
        else:
            embed = DiscordEmbed(title='Server Status',
                description=f'{role}\n**{message}**', color=status_color)
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


    def get_old_status(cwd):
        with open(f'{cwd}status.json') as x:
            old_status = json.load(x)
        return old_status

    def update_json_status(new_status,cwd):
        with open(f'{cwd}status.json','w+') as f:
            json.dump(new_status, f, indent=2)


    def scrape_status_page(status_url,monitored_servers):
        r = requests.get(status_url)
        page = BeautifulSoup(r.content, 'html.parser')
        status_section = page.find('div',
            class_='ags-ServerStatus-content-responses')
        server_sections = status_section.find_all('div',
            class_='ags-ServerStatus-content-responses-response-server')

        new_status = {}

        for server in server_sections:
            server_name = server.find('div',
                class_='ags-ServerStatus-content-responses-response-server-name').text.strip()
            if server_name in monitored_servers:
                if server.find('div',
                    class_='ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--up'):
                    new_status[server_name] = '✅'
                if server.find('div',
                    class_='ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--down'):
                    new_status[server_name] = '❌'
                if server.find('div',
                    class_='ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--maintenance'):
                    new_status[server_name] = '🛠️'
                if server.find('div',
                    class_='ags-ServerStatus-content-responses-response-server-status ags-ServerStatus-content-responses-response-server-status--full'):
                    new_status[server_name] = '⚠️'
        return new_status


class GameNews:
    def __init__(self):
        super().__init__()


    def scrape_news_articles(news_url):
        r = requests.get(news_url)
        page = BeautifulSoup(r.content,'html.parser')
        articles_section = page.find('div',
            class_='ags-ContainerModule-container-slotModuleContainer js-blogContainer')
        articles = articles_section.find_all('div',
            class_='ags-SlotModule ags-SlotModule--blog ags-SlotModule--threePerRow')

        new_articles_dict = {}
        article_num = 0
        for article in articles:
            article_num += 1
            title = article.find('span',
                class_='ags-SlotModule-contentContainer-heading ags-SlotModule-contentContainer-heading ags-SlotModule-contentContainer-heading--blog').text.strip()
            desc = article.find('div',
                class_='ags-SlotModule-contentContainer-text ags-SlotModule-contentContainer-text--blog ags-SlotModule-contentContainer-text').text.strip()
            url = 'https://newworld.com/' + article.find('a')['href']
            img = 'https:' + article.find('img', class_='ags-SlotModule-imageContainer-image')['src']
            new_articles_dict[f'article_{article_num}'] = {
                    'title':title,'desc': desc,'url':url,'img': img}

        return new_articles_dict


    def get_old_articles(cwd):
        with open(f'{cwd}articles.json') as x:
            old_articles = json.load(x)
        return old_articles

    def update_articles(send_articles_dict,cwd):
        with open(f'{cwd}articles.json', 'w+') as f:
            json.dump(send_articles_dict,f,indent=2, ensure_ascii=False)


    def articles_webhook(news_webhook_url,send_articles_dict,role):
        for article in send_articles_dict:
            title = send_articles_dict[article]['title']
            desc = send_articles_dict[article]['desc']
            url = send_articles_dict[article]['url']
            img = send_articles_dict[article]['img']

            webhook = DiscordWebhook(url=news_webhook_url, rate_limit_retry=True)
            if role is None:
                embed = DiscordEmbed(title=f'Game Updates')
            else:
                embed = DiscordEmbed(title='Server Status',
                    description=f'{role}')
            embed.add_embed_field(name=title, value=f'{desc} -- [[More info...]]({url})')
            embed.set_image(url=img)
            webhook.add_embed(embed)
            response = webhook.execute()
