import threading
import socket
import tkinter as tk
import time

TELLO_IP = '192.168.10.1'
TELLO_PORT = 8889
TELLO_ADDRESS = (TELLO_IP, TELLO_PORT)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', TELLO_PORT))

def send_command(command):
    try:
        sock.sendto(command.encode('utf-8'), TELLO_ADDRESS)
    except Exception as e:
        print(f"Error sending {command}: {e}")

def takeoff(): send_command('takeoff')
def land(): send_command('land')
def up(): send_command('up 20')
def down(): send_command('down 20')
def forward(): send_command('forward 20')
def back(): send_command('back 20')
def right(): send_command('right 20')
def left(): send_command('left 20')
def cw(): send_command('cw 90')
def ccw(): send_command('ccw 90')
def speed40(): send_command('speed 40')
def speed20(): send_command('speed 20')
def emergency(): send_command('emergency')

def udp_receiver():
    while True:
        try:
            data, _ = sock.recvfrom(1518)
            resp = data.decode('utf-8').strip()
            if resp.isdecimal():
                battery_text.set(f"Battery: {resp}%")
            elif resp.endswith('s'):
                time_text.set(f"Flight Time: {resp}s")
            else:
                status_text.set(f"Status: {resp}")
        except:
            pass

def ask():
    while True:
        send_command('battery?')
        time.sleep(5)
        send_command('time?')
        time.sleep(5)


def centering_main_window(event):
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    x = screen_width / 2 - window_width /2
    y = screen_height / 2 - window_height / 2
    root.geometry("+%d+%d" % (x, y))

root = tk.Tk()
root.geometry("600x600")
root.bind("<Visibility>", centering_main_window)
root.title('Tello Drone Controller')

send_command('command')
send_command('speed 20')

threading.Thread(target=ask, daemon=True).start()
threading.Thread(target=udp_receiver, daemon=True).start()

battery_text = tk.StringVar(value="Battery: ")
time_text = tk.StringVar(value="Flight Time: ")
status_text = tk.StringVar(value="Status: ")

tk.Label(root, textvariable=battery_text).pack()
tk.Label(root, textvariable=time_text).pack()
tk.Label(root, textvariable=status_text).pack()

tk.Button(root, text='Takeoff', command=takeoff, height=2).pack(fill='x')
tk.Button(root, text='Land', command=land, height=2).pack(fill='x')

direction_frame = tk.Frame(root)
direction_frame.pack(pady=10)

btn_size = {'width': 8, 'height': 3}

tk.Button(direction_frame, text='↑', command=forward, **btn_size).grid(row=0, column=1)
tk.Button(direction_frame, text='←', command=left, **btn_size).grid(row=1, column=0)
tk.Button(direction_frame, text='↓', command=back, **btn_size).grid(row=1, column=1)
tk.Button(direction_frame, text='→', command=right, **btn_size).grid(row=1, column=2)

tk.Button(direction_frame, text='Up', command=up, **btn_size).grid(row=0, column=3)
tk.Button(direction_frame, text='Down', command=down, **btn_size).grid(row=2, column=3)
tk.Button(direction_frame, text='CW', command=cw, **btn_size).grid(row=2, column=0)
tk.Button(direction_frame, text='CCW', command=ccw, **btn_size).grid(row=2, column=2)

tk.Button(root, text='Speed 40', command=speed40, height=2).pack(fill='x')
tk.Button(root, text='Speed 20', command=speed20, height=2).pack(fill='x')
# tk.Button(root, text='Emergency Stop', command=emergency, bg='red', height=3).pack(fill='x', pady=10)
tk.Button(root, text='Emergency Stop', command=emergency, highlightbackground='red', height=10).pack(fill='x', pady=10)
# tk.Button(root, text = "Emergency Stop", command = emergency, highlightbackground='red').place(x=0, y=300, width = 200, height = 100)

root.mainloop()
