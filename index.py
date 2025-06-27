import tkinter as tk
from tkinter import ttk
import subprocess

# Replace this with your detected output name
display_output = "eDP-1-1"

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

def reset_xrandr():
    cmd = f"xrandr --output {display_output} --gamma 1:1:1 --brightness 1"
    print(f"Resetting: {cmd}")
    subprocess.run(cmd, shell=True)

    # Reset slider values to defaults
    red_scale.set(1.0)
    green_scale.set(1.0)
    blue_scale.set(1.0)
    brightness_scale.set(1.0)

root = tk.Tk()
root.title("Xrandr Light Blue Tint Configurator")
root.geometry("700x800")  # Make the window larger

# Red Scale
tk.Label(root, text="Red Channel [0.1 - 1.5]", font=("Arial", 12)).pack(pady=5)
red_scale = tk.Scale(root, from_=0.1, to=1.5, orient="horizontal", resolution=0.01, length=300)
red_scale.set(0.8)
red_scale.pack(pady=5)

# Green Scale
tk.Label(root, text="Green Channel [0.1 - 1.5]", font=("Arial", 12)).pack(pady=5)
green_scale = tk.Scale(root, from_=0.1, to=1.5, orient="horizontal", resolution=0.01, length=300)
green_scale.set(0.9)
green_scale.pack(pady=5)

# Blue Scale
tk.Label(root, text="Blue Channel [0.1 - 1.5]", font=("Arial", 12)).pack(pady=5)
blue_scale = tk.Scale(root, from_=0.1, to=1.5, orient="horizontal", resolution=0.01, length=300)
blue_scale.set(1.2)
blue_scale.pack(pady=5)

# Brightness Scale
tk.Label(root, text="Brightness [0.1 - 1.5]", font=("Arial", 12)).pack(pady=5)
brightness_scale = tk.Scale(root, from_=0.1, to=1.5, orient="horizontal", resolution=0.01, length=300)
brightness_scale.set(1.0)
brightness_scale.pack(pady=5)

# Apply Button
apply_button = ttk.Button(root, text="Apply Blue Tint", command=apply_xrandr)
apply_button.pack(pady=15)

# Reset Button
reset_button = ttk.Button(root, text="Reset to Default", command=reset_xrandr)
reset_button.pack(pady=10)

root.mainloop()