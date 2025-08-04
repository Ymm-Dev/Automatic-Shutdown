import tkinter as tk
from tkinter import messagebox
import ctypes
import os

initial_time = 3600
time_left = initial_time
running = False
admin_pin = "Password123"
notified_90s = False

user32 = ctypes.windll.user32
screen_width = user32.GetSystemMetrics(0)
screen_height = user32.GetSystemMetrics(1)

def format_time(secs):
    mins = secs // 60
    secs = secs % 60
    return f"{mins:02}:{secs:02}"

def show_non_blocking_warning(msg):
    if hasattr(root, "warning_window") and root.warning_window.winfo_exists():
        return 

    warning = tk.Toplevel(root)
    root.warning_window = warning  

    warning.title("⚠️ System Warning")
    warning.configure(bg="#fff3cd")
    warning.resizable(False, False)
    warning.attributes("-topmost", True)

    container = tk.Frame(warning, bg="#856404", padx=2, pady=2)
    container.pack(expand=True, fill="both")

    content = tk.Frame(container, bg="#fff3cd")
    content.pack(expand=True, fill="both")

    w, h = 420, 200
    x = (screen_width // 2) - (w // 2)
    y = (screen_height // 2) - (h // 2)
    warning.geometry(f"{w}x{h}+{x}+{y}")

    tk.Label(content, text="⚠️", font=("Helvetica", 26), bg="#fff3cd", fg="#856404").pack(pady=(10, 0))
    tk.Label(content, text="Warning", font=("Helvetica", 16, "bold"), bg="#fff3cd", fg="#856404").pack(pady=(0, 5))
    tk.Label(
        content, text=msg, font=("Helvetica", 12),
        bg="#fff3cd", fg="#856404", wraplength=360, justify="center"
    ).pack(padx=20, pady=(0, 10))

    def close_warning():
        if warning.winfo_exists():
            warning.destroy()

    tk.Button(
        content, text="OK", command=close_warning,
        font=("Helvetica", 11, "bold"), bg="#ff914d", fg="white",
        activebackground="#e67e22", relief="flat", width=10, padx=5, pady=3
    ).pack(pady=(0, 15))

    warning.after(10000, close_warning)

def sleep_system():
    os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")

def countdown():
    global time_left, notified_90s
    try:
        if running and time_left > 0:
            time_left -= 1
            label.config(text=format_time(time_left))

            if time_left == 90 and not notified_90s:
                notified_90s = True
                show_non_blocking_warning("System will sleep in 90 seconds. Please save your work.")

            root.after(1000, countdown)
        elif running and time_left == 0:
            label.config(text="00:00")
            restart_btn.pack(pady=5)
            sleep_system()
    except Exception as e:
        print(f"Error in countdown: {e}")


def start():
    global running
    if not running:
        running = True
        countdown()

def pause():
    show_pin_prompt(action="pause")

def restart_timer():
    show_pin_prompt(action="restart")

def confirm_close():
    show_pin_prompt(action="close")

def show_pin_prompt(action=None):
    pin_window = tk.Toplevel(root)
    pin_window.title("Admin PIN")
    pin_window.configure(bg="#2b2b3d")
    pin_window.resizable(False, False)
    pin_window.grab_set()

    win_w = 300
    win_h = 160
    x = int((screen_width / 2) - (win_w / 2))
    y = int((screen_height / 2) - (win_h / 2))
    pin_window.geometry(f"{win_w}x{win_h}+{x}+{y}")

    tk.Label(pin_window, text="Enter Admin PIN", bg="#2b2b3d", fg="white", font=("Helvetica", 14, "bold")).pack(pady=(20, 10))

    pin_var = tk.StringVar()
    pin_entry = tk.Entry(pin_window, textvariable=pin_var, show='*', font=("Helvetica", 16), justify='center', bd=2, relief='solid')
    pin_entry.pack(pady=5)
    pin_entry.focus()

    def submit_pin():
        if pin_var.get() == admin_pin:
            global running, time_left, notified_90s
            if action == "pause":
                running = False
            elif action == "close":
                root.destroy()
            elif action == "restart":
                running = False
                time_left = initial_time
                notified_90s = False
                label.config(text=format_time(time_left))
                restart_btn.pack_forget()
            pin_window.destroy()
        else:
            messagebox.showerror("Incorrect PIN", "The PIN you entered is incorrect.")
            pin_entry.delete(0, tk.END)

    tk.Button(pin_window, text="Enter", command=submit_pin, bg="#4caf50", fg="white", font=("Helvetica", 12, "bold"), width=10).pack(pady=10)

    pin_window.bind("<Return>", lambda event: submit_pin())
    pin_window.bind("<Escape>", lambda event: pin_window.destroy())

root = tk.Tk()
root.title("Timer")
root.config(bg="#1e1e2f")
root.resizable(False, False)
root.protocol("WM_DELETE_WINDOW", confirm_close)

window_width = 320
window_height = 320
x = screen_width - window_width - 20
y = 20
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

label = tk.Label(root, text=format_time(time_left), font=("Helvetica", 48, "bold"), fg="#ff914d", bg="#1e1e2f")
label.pack(pady=30)

button_style = {
    "font": ("Helvetica", 14),
    "width": 10,
    "padx": 5,
    "pady": 5,
    "bd": 0,
    "activebackground": "#ff914d",
    "activeforeground": "#ffffff"
}

tk.Button(root, text="Start", command=start, bg="#2ecc71", fg="white", **button_style).pack(pady=5)
tk.Button(root, text="Pause", command=pause, bg="#e74c3c", fg="white", **button_style).pack()

restart_btn = tk.Button(root, text="Restart", command=restart_timer, bg="#3498db", fg="white", **button_style)
restart_btn.pack_forget()

root.mainloop()