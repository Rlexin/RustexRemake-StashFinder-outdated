from flask import Flask, render_template, jsonify
import pyMeow as pm
import time
import keyboard
import os, random, string, ctypes, pyautogui, requests, io, sys, subprocess, hashlib, logging, psutil
import ctypes.wintypes as wintypes
from ctypes import windll
from ctypes import c_int
from ctypes import c_uint
from ctypes import c_ulong
from ctypes import POINTER
from ctypes import byref
from base64 import decodebytes
from threading import Thread
import socket
import fade


if getattr(sys, 'frozen', False):
    template_folder = os.path.join(sys._MEIPASS, 'templates')
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__)

def rw(length):
   letters = string.ascii_lowercase + string.ascii_uppercase
   return ''.join(random.choice(letters) for i in range(length))

os.system(f'title {rw(42)}')
os.system('mode 105,30')
os.system('cls')


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False 

if is_admin() == False:
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
    os._exit(1)



loading  = """
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠠⠀⡐⢠⡠⡔⡁⣠⣤⣰⣤⣠⣀⣀⠀⠀⠀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢀⢄⠄⠶⢞⡷⠼⡫⣼⣷⣮⣽⣛⣵⣿⣼⣯⣿⣟⡦⣆⢄⡀⢀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⢈⢄⢢⢣⣐⠵⠵⢧⢹⡽⢘⢿⠻⣾⣻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣽⣿⣗⣢⣠⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠠⡂⠌⡨⠣⣲⣊⡿⣯⣾⣟⡞⣾⢷⢿⣿⣿⣿⣿⣿⣽⣿⣽⣾⣿⣮⣿⠾⢞⣽⢾⡤⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠸⠨⢪⢂⠨⢀⢏⡑⢽⢆⣵⣿⣷⣿⣿⣿⣿⣿⣷⣿⡻⣿⣿⣿⣿⡓⢽⣿⣿⣽⣷⣿⡯⣳⣄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠐⢓⢕⠍⡰⣙⡰⣶⢱⢽⣿⢽⡜⠞⣽⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⡚⡟⣮⣿⣿⣷⣿⣯⣗⣯⡧⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠤⠅⡡⠉⠎⢔⠾⢣⢏⠭⢾⣶⣯⢽⣿⣣⣯⣿⣻⣿⣿⣾⢻⣿⡻⣍⣳⣿⣿⣿⣿⣿⣶⡿⣿⣿⢿⣶⣴⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⠀⠀⠀⠙⠄⡐⠣⢝⣓⢈⠬⠑⢁⠾⣿⣭⡎⣿⣿⣿⣿⣿⣿⣽⢿⢽⢱⣯⡿⣿⣿⣿⣿⣟⣿⣽⢿⣺⣿⡻⣧⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠀⠀⢀⢠⣼⣛⠔⢀⢊⡜⠀⠀⠀⠀⠈⠉⠽⢿⣿⠿⢻⡝⡽⢗⣍⡊⣲⣺⣿⣿⣷⣯⣯⣿⣿⣿⣿⢟⣣⡽⣸⠂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡀⠀⠔⠈⢹⣿⣷⢧⣔⢿⡔⠀⠀⠀⠀⠀⠀⠀⢁⢮⣠⠧⣻⣷⣷⡓⣒⣾⣾⣽⣯⣿⣿⡿⣻⣿⣫⣿⢿⢫⢲⠣⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠐⠀⢠⠁⠀⠈⣿⣿⣛⢿⠞⡗⠃⡄⠀⠀⠀⠀⠀⣖⣿⣅⣎⡽⣽⡾⣼⣿⣿⣿⣿⣾⡿⣿⣾⣻⣿⣿⢶⣫⣟⣝⠕⠄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢠⠡⢠⠈⠀⠀⠀⠹⣿⢼⣬⣇⢥⠩⠦⡀⠀⠀⠀⣬⣿⣿⡇⡰⠥⢚⡵⠹⣫⣷⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⢶⢳⣺⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡁⡢⡁⠠⠀⠀⠀⠀⠙⡘⡟⠡⡈⢊⣑⢶⠶⡶⣟⣿⣿⠿⡀⠢⢑⢳⡉⡢⠳⣙⡯⣝⢟⡿⢟⡿⣿⢿⣻⣯⣔⢥⢈⠑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢒⡔⠰⣀⠄⡄⠀⢰⡃⢤⢖⠠⡲⠦⢧⢩⢛⡅⣿⣿⣿⣼⣰⣥⢅⣬⢠⠁⠬⠒⣾⣵⣾⣾⣮⣿⣶⣿⡚⡱⠩⢂⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠃⡦⢠⠂⣢⣶⢦⣏⠬⢩⠉⠐⠈⠐⠙⠨⠸⡪⠽⢟⡻⠹⠨⠾⠦⠺⡴⠴⢛⢿⢟⡹⠻⢿⢻⣓⡩⢑⠨⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡰⣨⣚⣕⣹⠆⣻⣯⣥⣿⣣⡷⠈⢠⢐⢐⠠⠂⢊⡐⣙⢈⠀⠀⠀⠀⠀⢀⡴⢒⠁⠀⠀⣈⣶⡧⣱⢠⢔⡹⡑⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠰⡨⡆⣴⡇⣵⢆⣿⣿⣽⣿⣿⡇⣾⢴⡥⣖⠀⠔⠈⡼⣗⡾⢆⣀⣀⢤⣴⡞⠅⠀⢦⠼⠰⣕⣵⣮⣈⣮⠼⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣡⢴⠠⡂⠈⡈⢁⡳⢸⡽⣯⣽⡯⢿⣾⡿⠏⠀⠀⢨⡟⣴⣿⣫⣷⣿⣿⡟⣮⠒⠀⠀⣠⣾⡽⡭⡻⠡⠂⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡂⡸⢐⠀⠺⢇⢏⢇⢾⠀⣵⢠⢶⢱⠴⠀⠀⠀⢀⣼⢵⣺⣵⡿⣻⣿⢓⠊⠁⠀⠀⢀⠼⡽⠂⠂⠡⠐⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢁⢀⢄⠃⢹⠀⢛⠆⢺⠂⡷⠷⠸⠇⠀⡀⣴⣻⣾⣿⣿⢷⣿⢼⡯⠁⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢆⠼⢠⠂⢔⠰⣒⠶⢾⢶⣲⣾⣿⣾⣻⣾⣿⣽⣽⣵⣿⢗⣿⢞⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡨⢱⢖⣽⣾⣶⢲⢻⢯⣻⣣⢿⢽⢯⡿⣻⣿⣿⣿⣿⣿⣷⡷⣻⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠊⠪⠪⠿⡷⠷⣵⢙⣧⣝⡼⢋⠺⢾⡹⢕⠿⠻⠋⠙⠁⠛⠑⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
            ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠐⠛⠉⠚⠛⠑⠑⠘⠋⠉⠓⠀⠉⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
                                                ʟᴏᴀᴅɪɴɢ..."""
loading = fade.purplepink(loading)
print(loading)


# ----------------------------------
STASH_BASE = 0x5C8000000
STASH_REGION = 0xB6895140
# ----------------------------------




MessageBox = ctypes.windll.user32.MessageBoxW
class util():
    def errorLog(text):
        with open('ErrorLogs.txt', 'a') as f:
            f.write(text + "\n")


    def getlink(ip):
        z = f"http://{ip}:5000"
        return f"{z}{" " * (47-len(z))}"

    def get_local_ip():
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            s.connect(('10.255.255.255', 1))
            ip = s.getsockname()[0]
        except Exception:
            ip = '127.0.0.1'
        finally:
            s.close()
        return ip

    def psC(command):
        startupinfo = subprocess.STARTUPINFO()
        startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
        startupinfo.wShowWindow = subprocess.SW_HIDE
        
        return subprocess.check_output(
            ['powershell', '-Command', command],
            startupinfo=startupinfo,
            stderr=subprocess.DEVNULL,
            creationflags=subprocess.CREATE_NO_WINDOW
        ).decode().strip()

    def async_message_box(title: str, text: str):
            Thread(
                target=ctypes.windll.user32.MessageBoxW,
                args=(0, text, title, 0)
            ).start()

    def BSOD():
        nullptr = POINTER(c_int)()
        windll.ntdll.RtlAdjustPrivilege(
            c_uint(19),
            c_uint(1),
            c_uint(0),
            byref(c_int())
        )
        windll.ntdll.NtRaiseHardError(
            c_ulong(0xC000007B),
            c_ulong(0),
            nullptr,
            nullptr,
            c_uint(6),
            byref(c_uint())
        )


def get_player_coords():
    try:
        player_x = pm.r_float64(rr,
            pm.pointer_chain_64(rr,
                GAME_MODULE + 0x007F9080, 
                [0x0, 0x2A0, 0x4A8, 0x430, 0x340, 0x340, 0x70]
            )
        )

        player_y = pm.r_float64(rr,
            pm.pointer_chain_64(rr,
                GAME_MODULE + 0x007F9080, 
                [0x0, 0x2A0, 0x4A8, 0x430, 0x340, 0x340, 0x78]
            )
        )


        player_z = pm.r_float64(rr,
            pm.pointer_chain_64(rr,
                GAME_MODULE + 0x007F9080,
                [0x0, 0x2A0, 0x4A8, 0x430, 0x340, 0x340, 0x80]
            )
        )
        return player_x, player_y, player_z
    except Exception as e:
        util.errorLog(f'Ошибка получения координат ------ \n{e} ')
        return None, None
    




def scan_stashes():
    try:

        byte_buffer = pm.r_bytes(rr, STASH_BASE, STASH_REGION)
        results = pm.aob_scan_bytes("9F DD 00 F8 01 01 00 00", byte_buffer, False) 

        player_x, player_y, player_z = get_player_coords()
        if None in (player_x, player_z):
            return []

        found_stashes = []
        seen_coords = set()
        round_precision = 3
        # print(results)
        for addr in results:
            try:
                x = pm.r_float64(rr, STASH_BASE + addr + 184)
                y = pm.r_float64(rr, STASH_BASE + addr + 192)
                z = pm.r_float64(rr, STASH_BASE + addr + 200)

                if 50 < y < 140: # иногда были какие то баганные стеши на высоте 255 блоков или 0 хз
                    x_rounded = round(x, round_precision)
                    z_rounded = round(z, round_precision)
                    y_rounded = round(y, 1)

                    if (x_rounded, y_rounded, z_rounded) in seen_coords:
                        continue

                    distance = ((player_x - x)**2 + (player_z - z)**2)**0.5
                    
                    if abs(player_x - x) + abs(player_z - z) < 400:
                        found_stashes.append({
                            "x": x,
                            "y": y,
                            "z": z,
                            "distance": distance
                        })
                        seen_coords.add((x_rounded, y_rounded, z_rounded))
            except Exception as e:
                util.errorLog(f'Ошибка чтения стеша ----- \n{e}')
                continue
        found_stashes.sort(key=lambda x: x["distance"])
        return found_stashes

    except Exception as e:
        util.errorLog(f'Ошибка скана ------- \n{e}')
        return []


@app.route("/")
def index():
    return render_template("index.html", 
                         current=[0.0, 0.0, 0.0], 
                         stashes=[])

@app.route("/scan", methods=["POST"])
def handle_scan():
    try:
        stashes = scan_stashes()

        current_x, curent_y, current_z = get_player_coords()
        return jsonify({
            "current": [current_x, curent_y, current_z],
            "stashes": stashes
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/current_coords")
def get_current_coords():
    try:
        player_x, player_y,player_z = get_player_coords()
        return jsonify({
            "x": player_x,
            "y": player_y,
            "z": player_z
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


hidden = False
def hide_console():
    global hidden
    if ctypes.windll.kernel32.GetConsoleWindow():
        if not hidden:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 0)
            hidden = True
        else:
            ctypes.windll.user32.ShowWindow(ctypes.windll.kernel32.GetConsoleWindow(), 1)
            hidden = False




keyboard.add_hotkey('insert', hide_console)


log = logging.getLogger('werkzeug')
log.disabled = True


cli = sys.modules['flask.cli']
cli.show_server_banner = lambda *x: None


localIP = util.get_local_ip()


main_menu = f"""
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡀⠠⠀⡐⢠⡠⡔⡁⣠⣤⣰⣤⣠⣀⣀⠀⠀⠀⡀⠀⠀⠀⠀⠀
    ┌─┐┌┬┐┌─┐┌─┐┬ ┬  ┌─┐┬┌┐┌┌┬┐┌─┐┬─┐   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢀⢄⠄⠶⢞⡷⠼⡫⣼⣷⣮⣽⣛⣵⣿⣼⣯⣿⣟⡦⣆⢄⡀⢀⠀⠀⠀⠀
    └─┐ │ ├─┤└─┐├─┤  ├┤ ││││ ││├┤ ├┬┘   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠄⠠⡂⠌⡨⠣⣲⣊⡿⣯⣾⣟⡞⣾⢷⢿⣿⣿⣿⣿⣿⣽⣿⣽⣾⣿⣮⣿⠾⢞⣽⢾⡤⡄⠀⠀⠀⠀⠀
    └─┘ ┴ ┴ ┴└─┘┴ ┴  └  ┴┘└┘─┴┘└─┘┴└─   ⠀v1.3⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠸⠨⢪⢂⠨⢀⢏⡑⢽⢆⣵⣿⣷⣿⣿⣿⣿⣿⣷⣿⡻⣿⣿⣿⣿⡓⢽⣿⣿⣽⣷⣿⡯⣳⣄⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠐⢓⢕⠍⡰⣙⡰⣶⢱⢽⣿⢽⡜⠞⣽⣿⣯⣿⣿⣿⣿⣿⣿⣿⣿⣿⡚⡟⣮⣿⣿⣷⣿⣯⣗⣯⡧⡄⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠠⠤⠅⡡⠉⠎⢔⠾⢣⢏⠭⢾⣶⣯⢽⣿⣣⣯⣿⣻⣿⣿⣾⢻⣿⡻⣍⣳⣿⣿⣿⣿⣿⣶⡿⣿⣿⢿⣶⣴⡄⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡀⠀⠀⠀⠙⠄⡐⠣⢝⣓⢈⠬⠑⢁⠾⣿⣭⡎⣿⣿⣿⣿⣿⣿⣽⢿⢽⢱⣯⡿⣿⣿⣿⣿⣟⣿⣽⢿⣺⣿⡻⣧⡀
    ᴄᴏɴɴᴇᴄᴛ: {util.getlink(localIP)}⡀⠀⠀⢀⢠⣼⣛⠔⢀⢊⡜⠀⠀⠀⠀⠈⠉⠽⢿⣿⠿⢻⡝⡽⢗⣍⡊⣲⣺⣿⣿⣷⣯⣯⣿⣿⣿⣿⢟⣣⡽⣸⠂⠀
    ʟᴏᴄᴀʟ ᴄᴏɴɴᴇᴄᴛ: 127.0.0.1:5000       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⡀⠀⠔⠈⢹⣿⣷⢧⣔⢿⡔⠀⠀⠀⠀⠀⠀⠀⢁⢮⣠⠧⣻⣷⣷⡓⣒⣾⣾⣽⣯⣿⣿⡿⣻⣿⣫⣿⢿⢫⢲⠣⠁
    ʜɪᴅᴇ/sʜᴏᴡ ᴄᴏɴsᴏʟᴇ                   ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⠐⠀⢠⠁⠀⠈⣿⣿⣛⢿⠞⡗⠃⡄⠀⠀⠀⠀⠀⣖⣿⣅⣎⡽⣽⡾⣼⣿⣿⣿⣿⣾⡿⣿⣾⣻⣿⣿⢶⣫⣟⣝⠕⠄⠀
        [ɪɴsᴇʀᴛ]                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⢠⠡⢠⠈⠀⠀⠀⠹⣿⢼⣬⣇⢥⠩⠦⡀⠀⠀⠀⣬⣿⣿⡇⡰⠥⢚⡵⠹⣫⣷⣿⣿⣿⣿⣿⣿⣿⣿⣟⣻⢶⢳⣺⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⡁⡢⡁⠠⠀⠀⠀⠀⠙⡘⡟⠡⡈⢊⣑⢶⠶⡶⣟⣿⣿⠿⡀⠢⢑⢳⡉⡢⠳⣙⡯⣝⢟⡿⢟⡿⣿⢿⣻⣯⣔⢥⢈⠑⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠘⢒⡔⠰⣀⠄⡄⠀⢰⡃⢤⢖⠠⡲⠦⢧⢩⢛⡅⣿⣿⣿⣼⣰⣥⢅⣬⢠⠁⠬⠒⣾⣵⣾⣾⣮⣿⣶⣿⡚⡱⠩⢂⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⠃⡦⢠⠂⣢⣶⢦⣏⠬⢩⠉⠐⠈⠐⠙⠨⠸⡪⠽⢟⡻⠹⠨⠾⠦⠺⡴⠴⢛⢿⢟⡹⠻⢿⢻⣓⡩⢑⠨⠀⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡰⣨⣚⣕⣹⠆⣻⣯⣥⣿⣣⡷⠈⢠⢐⢐⠠⠂⢊⡐⣙⢈⠀⠀⠀⠀⠀⢀⡴⢒⠁⠀⠀⣈⣶⡧⣱⢠⢔⡹⡑⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠐⠰⡨⡆⣴⡇⣵⢆⣿⣿⣽⣿⣿⡇⣾⢴⡥⣖⠀⠔⠈⡼⣗⡾⢆⣀⣀⢤⣴⡞⠅⠀⢦⠼⠰⣕⣵⣮⣈⣮⠼⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⣡⢴⠠⡂⠈⡈⢁⡳⢸⡽⣯⣽⡯⢿⣾⡿⠏⠀⠀⢨⡟⣴⣿⣫⣷⣿⣿⡟⣮⠒⠀⠀⣠⣾⡽⡭⡻⠡⠂⠁⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡂⡸⢐⠀⠺⢇⢏⢇⢾⠀⣵⢠⢶⢱⠴⠀⠀⠀⢀⣼⢵⣺⣵⡿⣻⣿⢓⠊⠁⠀⠀⢀⠼⡽⠂⠂⠡⠐⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠠⢁⢀⢄⠃⢹⠀⢛⠆⢺⠂⡷⠷⠸⠇⠀⡀⣴⣻⣾⣿⣿⢷⣿⢼⡯⠁⠀⠀⠀⠀⠀⠀⠀⠀⠁⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢰⢆⠼⢠⠂⢔⠰⣒⠶⢾⢶⣲⣾⣿⣾⣻⣾⣿⣽⣽⣵⣿⢗⣿⢞⠁ ʀʟᴇxɪɴ ❤️
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⡨⢱⢖⣽⣾⣶⢲⢻⢯⣻⣣⢿⢽⢯⡿⣻⣿⣿⣿⣿⣿⣷⡷⣻⠁
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠊⠪⠪⠿⡷⠷⣵⢙⣧⣝⡼⢋⠺⢾⡹⢕⠿⠻⠋⠙⠁⠛⠑⠁⠀⠀⠀
                                        ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠁⠐⠛⠉⠚⠛⠑⠑⠘⠋⠉⠓⠀⠉⠁⠀⠀"""

main_menu = fade.purplepink(main_menu)


try:
    rr = pm.open_process('javaw.exe')
    GAME_MODULE = pm.get_module(rr, 'jvm.dll')['base']
except:
    util.async_message_box(title='Error', text="Open RustexRemake")
    time.sleep(3)
    os._exit(1)

if __name__ == "__main__":
    os.system('cls')
    print(main_menu)
    app.run(host='0.0.0.0', port=5000, debug=False)