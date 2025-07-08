import tkinter as tk
from tkinter import ttk
import subprocess
import os

def get_first_connected_display():
    try:
        output = subprocess.check_output("xrandr --query", shell=True, text=True)
        for line in output.splitlines():
            if " connected" in line:
                return line.split()[0]
    except subprocess.CalledProcessError as e:
        print(f"Failed to get display info: {e}")
    return "eDP-1"  # default fallback

display_output = get_first_connected_display()
bash_script_path = os.path.expanduser("~/.local/bin/set_brightness.sh")
autostart_path = os.path.expanduser("~/.config/autostart/set-brightness.desktop")

def write_bash_script(r, g, b, brightness):
    os.makedirs(os.path.dirname(bash_script_path), exist_ok=True)
    with open(bash_script_path, "w") as f:
        f.write(f"""#!/bin/bash
sleep 5
xrandr --output {display_output} --gamma {r}:{g}:{b} --brightness {brightness}
""")
    os.chmod(bash_script_path, 0o755)
    print(f"Saved script to {bash_script_path}")

def write_autostart_entry():
    os.makedirs(os.path.dirname(autostart_path), exist_ok=True)
    with open(autostart_path, "w") as f:
        f.write(f"""[Desktop Entry]
Type=Application
Exec={bash_script_path}
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name=Set Brightness
""")
    print(f"Autostart entry created at {autostart_path}")

def apply_xrandr():
    r = red_scale.get()
    g = green_scale.get()
    b = blue_scale.get()
    brightness = brightness_scale.get()

    cmd = f"xrandr --output {display_output} --gamma {r}:{g}:{b} --brightness {brightness}"
    print(f"Running: {cmd}")

    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run xrandr: {e}")

    write_bash_script(r, g, b, brightness)
    write_autostart_entry()

def reset_xrandr():
    cmd = f"xrandr --output {display_output} --gamma 1:1:1 --brightness 1"
    print(f"Resetting: {cmd}")
    subprocess.run(cmd, shell=True)

    red_scale.set(1.0)
    green_scale.set(1.0)
    blue_scale.set(1.0)
    brightness_scale.set(1.0)

root = tk.Tk()
root.title("Xrandr Light Blue Tint Configurator")
root.geometry("700x800")

tk.Label(root, text=f"Detected Display: {display_output}", font=("Arial", 12, "bold")).pack(pady=5)

tk.Label(root, text="Red Channel [0.1 - 1.5]", font=("Arial", 12)).pack(pady=5)
red_scale = tk.Scale(root, from_=0.1, to=1.5, orient="horizontal", resolution=0.01, length=300)
red_scale.set(1.0)
red_scale.pack(pady=5)

tk.Label(root, text="Green Channel [0.1 - 1.5]", font=("Arial", 12)).pack(pady=5)
green_scale = tk.Scale(root, from_=0.1, to=1.5, orient="horizontal", resolution=0.01, length=300)
green_scale.set(1.0)
green_scale.pack(pady=5)

tk.Label(root, text="Blue Channel [0.1 - 1.5]", font=("Arial", 12)).pack(pady=5)
blue_scale = tk.Scale(root, from_=0.1, to=1.5, orient="horizontal", resolution=0.01, length=300)
blue_scale.set(1.0)
blue_scale.pack(pady=5)

tk.Label(root, text="Brightness [0.1 - 1.5]", font=("Arial", 12)).pack(pady=5)
brightness_scale = tk.Scale(root, from_=0.1, to=1.5, orient="horizontal", resolution=0.01, length=300)
brightness_scale.set(1.0)
brightness_scale.pack(pady=5)

apply_button = ttk.Button(root, text="Apply & Save to Startup", command=apply_xrandr)
apply_button.pack(pady=15)

reset_button = ttk.Button(root, text="Reset to Default", command=reset_xrandr)
reset_button.pack(pady=10)

root.mainloop()
