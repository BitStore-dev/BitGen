from ast import Global
import random, string, os, aiohttp, asyncio, requests, ab5
from requests.exceptions import Timeout
from discord_webhook import DiscordWebhook, DiscordEmbed

class color:
    VIOLET, CYAN, DARK_CYAN, BLUE, GREEN, YELLOW, RED, WHITE, BLACK, GRAY, MAGENTA, BOLD, DIM, NORMAL, UNDERLINED, STOP = '\033[95m', '\033[96m', '\033[36m', '\033[94m', '\033[92m', '\033[93m', '\033[91m', '\033[37m', '\033[30m','\033[38;2;88;88;88m', '\033[35m', '\033[1m', '\033[2m', '\033[22m', '\033[4m', '\033[0m'

def gen_code(lenght: int):
    return ''.join(random.choice(string.ascii_letters + string.digits) for i in range(lenght))

def scrape():
    f, scraped = open('proxies.txt', 'a+'), 0
    f.truncate(0)
    r, proxies = requests.get('https://api.proxyscrape.com/?request=displayproxies'), []
    for proxy in r.text.split('\n'):
        if proxy:
            proxy = 'https://{}'.format(proxy).strip()
            proxies.append(proxy)
    for p in proxies:
        scraped += 1
        f.write('{}\n'.format(p))
    f.close()
    return scraped

def readproxies():
    try:
        p = open('proxies.txt', encoding='UTF-8')
    except FileNotFoundError:
        p = open('proxies.txt', 'w+', encoding='UTF-8')
        raise SystemExit
    rproxy = p.read().split('\n')
    for i in rproxy:
        if i == '' or ' ':
            index = rproxy.index(i)
            del rproxy[index]
    p.close()
    return rproxy

def ask(question: str):
    return str(input('[ {0.MAGENTA}?{0.STOP} ] {0.GRAY}{1}:{0.STOP} '.format(color, question)))

rproxy = readproxies()

async def main():
    checker = boost = False
    os.system('cls' if os.name == 'nt' else 'clear')
    logo = ('''
      __________.__  __     ________                
      \______   \__|/  |_  /  _____/  ____   ____   
       |    |  _/  \   __\/   \  ____/ __ \ /    \  
       |    |   \  ||  |  \    \_\  \  ___/|   |  \ 
       |______  /__||__|   \______  /\___  >___|  /
              \/                  \/     \/     \/ 
          ''')
    print(ab5.hgratient(logo, [0, 223, 50], [0, 25, 222]))
    print('[ {0.YELLOW}>{0.STOP} ] {0.GRAY}Made with {0.RED}<3{0.STOP} {0.GRAY}by{0.STOP} DaniDuese ({0.DARK_CYAN}{0.UNDERLINED}https://github.com/DaniEnsi{0.STOP})\n'.format(color))
    try:
        global count
        count = int(ask('How much codes should be generated'))
    except ValueError:
        print('\n[ {0.RED}>{0.STOP} ] {0.GRAY}Please enter an integer{0.STOP} !\n'.format(color))
        return exit()
    boost = True if ask('Boost codes or Classic codes (boost/classic)').lower() == 'boost' else False
    if ask('Enable Webhook (yes/no)').lower() == 'yes':
        global webhookval
        global webhookurl
        webhookurl = ask('Webhook URL: ')
        webhook = DiscordWebhook(url=webhookurl, timeout=1.0)
        embed = DiscordEmbed(
            title='Webhook Initialized', description='If you can see this Message, the webhook is working!', color=0x00ff00)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/1009045524667715714/1031322268896350238/unknown.png')
        embed.set_footer(text='BitGen™ - Nitro Generator')
        embed.set_timestamp()
        webhook.add_embed(embed)
        try:
            response = webhook.execute()
            if ask('Did you get the message? (yes/no)').lower() == 'yes':
                webhookval = True
            else:
                print('[ {0.RED}>{0.STOP} ] {0.GRAY}Please retry{0.STOP} !\n'.format(color))
                return exit()
        except Timeout as err:
            print(f'Oops! Connection to Discord timed out: {err}')
            return exit()
    else:
        webhookval = False
    if ask('Enable Checker (yes/no)').lower() == 'yes':
        try:
            valid, invalid, checker = [], 0, True
            print('\n[ {0.BLUE}i{0.STOP} ] {1} {0.GRAY}scraped proxys.{0.STOP}'.format(color, scrape()))
        except:
            print('\n[ {0.RED}>{0.STOP} ] {0.GRAY}Check your internet connection !{0.STOP}\n'.format(color))
            input('Press enter to continue... ')
            return exit()
    else:
        valid = invalid = 'CHECKER NOT ENABLED'
        checker = False
    print('')
    while count > 0:
        if boost:
            code = gen_code(24)
        else:
            code = gen_code(16)
        if checker:
            count -= 1
            badge = '#'
            async with aiohttp.ClientSession() as session:
                async with session.get('https://discordapp.com/api/v9/entitlements/gift-codes/{}?with_application=false&with_subscription_plan=true'.format(code)) as response:
                    if response.status == 429:
                        try:
                            proxi = random.choice(rproxy)
                            index = rproxy.index(proxi)
                            del rproxy[index]
                        except IndexError:
                            print('\n[ {0.RED}>{0.STOP} ] {0.GRAY}There are no more proxies available !{0.STOP}\n'.format(color))
                            print('[ {0.YELLOW}>{0.STOP} ] Result:\n{0.RED}Invalid{0.STOP}: {1}\n{0.GREEN}Valid{0.STOP}: {2}\n{0.GREEN}Links{0.STOP}: {3}\n'.format(color, invalid, len(valid), ', '.join(valid)))
                            input('Press enter to continue... ')
                            return exit()
                        invalid += 1
                        badge = '{0.RED}-{0.STOP}'.format(color)
                    elif response.status == 404:
                        invalid += 1
                        badge = '{0.RED}-{0.STOP}'.format(color)
                    elif response.status == 200:
                        valid.append('https://discord.gift/{}'.format(code))
                        badge = '{0.GREEN}+{0.STOP}'.format(color)
                    print('[ {1} ] {0.DARK_CYAN}{0.UNDERLINED}https://discord.gift/{2}{0.STOP}'.format(color, badge, code))
        else:
            count -= 1
            print('[ {0.BLUE}~{0.STOP} ] {0.DARK_CYAN}{0.UNDERLINED}https://discord.gift/{1}{0.STOP}'.format(color, code))
    return [invalid, valid]


if __name__ == '__main__':
    gen = asyncio.get_event_loop().run_until_complete(main())
    invalid = gen[0]
    if gen[1] == []:
        valid = 0
    else:
        valid = gen[1]
    num = int(valid + invalid)
    if webhookval == True:
        webhook = DiscordWebhook(url=webhookurl, timeout=1.0)
        embed = DiscordEmbed(
            title='Nitro Codes Created', description='BitGen™ has created and checked ' + str(num) + ' Nitro Codes...', color=0x000000)
        embed.add_embed_field(name='Vaid Codes:', value=valid)
        embed.add_embed_field(name='Invalid Codes', value=invalid)
        embed.set_thumbnail(
            url='https://cdn.discordapp.com/attachments/1009045524667715714/1031322268896350238/unknown.png')
        embed.set_footer(text='BitGen™ - Nitro Generator')
        embed.set_timestamp()
        webhook.add_embed(embed)
        try:
            response = webhook.execute()
        except Timeout as err:
            print(f'Oops! Connection to Discord timed out: {err}')
            exit()
    else:
        pass
    
    print('\n[ {0.YELLOW}>{0.STOP} ] Result:\n{0.RED}Invalid{0.STOP}: {1[0]}\n{0.GREEN}Valid{0.STOP}: {2}\n{0.GREEN}Links{0.STOP}: {3}'.format(color, gen, gen[1], gen[1])) if gen[1] == 'CHECKER NOT ENABLED' else print('\n[ {0.YELLOW}>{0.STOP} ] Result:\n{0.RED}Invalid{0.STOP}: {1[0]}\n{0.GREEN}Valid{0.STOP}: {2}\n{0.GREEN}Links{0.STOP}: {3}'.format(color, gen, len(gen[1]), ', '.join(gen[1])))
    print('\n[ {0.MAGENTA}*{0.STOP} ] {0.GRAY}Thanks for using our nitro generator !{0.STOP}\n'.format(color))
    input('Press enter to continue... ')
    
    exit()
