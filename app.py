import tkinter as tk
from tkinter import font

# ---------- COLORS ----------
BG_MAIN = "#faeddc"
BTN_SIDEBAR = "#efe2f5"
BTN_MAIN = "#b6ff38"
DETAIL_BG = "#ede0f0"
NAV_BG = "#0f1a2a"
TEXT_DARK = "#000000"
TEXT_LIGHT = "#ffffff"


# ----------
# WINDOW SETUP
# ----------
root = tk.Tk()
root.title("Recipe App UI")
root.geometry("1000x600")
root.configure(bg=BG_MAIN)

# Default Font
default_font = font.Font(family="Arial", size=14, weight="bold")


# ----------
# LEFT SIDEBAR (RECIPE BUTTONS)
# ----------
sidebar = tk.Frame(root, bg=BG_MAIN)
sidebar.place(x=30, y=30)

for i in range(1, 6):
    btn = tk.Button(
        sidebar,
        text=f"Recipe {i}",
        bg=BTN_SIDEBAR,
        fg=TEXT_DARK,
        width=18,
        height=2,
        font=default_font,
        relief="flat",
        bd=0,
    )
    btn.pack(pady=10)


# ----------
# MAIN DETAIL PANEL
# ----------
detail = tk.Frame(root, bg=DETAIL_BG, width=500, height=350)
detail.place(x=300, y=60)

lbl_title = tk.Label(detail, text="Recipe 1", font=("Arial", 18, "bold"), bg=DETAIL_BG)
lbl_title.place(x=20, y=20)

lbl_info = tk.Label(detail, text="Details about recipe here ...", font=("Arial", 14), bg=DETAIL_BG)
lbl_info.place(x=20, y=70)


# ----------
# RIGHT ACTION BUTTONS
# ----------
right_panel = tk.Frame(root, bg=BG_MAIN)
right_panel.place(x=800, y=100)

for txt in ["Upload", "Download", "Comment"]:
    tk.Button(
        right_panel,
        text=txt,
        font=default_font,
        bg=BTN_MAIN,
        fg=TEXT_DARK,
        width=12,
        height=2,
        relief="flat",
    ).pack(pady=25)


# ----------
# BOTTOM NAVIGATION BAR
# ----------
bottom_nav = tk.Frame(root, bg=NAV_BG, height=80, width=1000)
bottom_nav.place(x=0, y=520)

nav_items = ["Home", "Recipes", "Settings"]
positions = [150, 450, 780]

for label, x in zip(nav_items, positions):
    tk.Label(bottom_nav, text=label, fg=TEXT_LIGHT, bg=NAV_BG,
             font=("Arial", 20, "bold")).place(x=x, y=20)


root.mainloop()
import tkinter as tk
from tkinter import font

# ---------- COLORS ----------
BG_MAIN = "#faeddc"
BTN_SIDEBAR = "#efe2f5"
BTN_MAIN = "#b6ff38"
DETAIL_BG = "#ede0f0"
NAV_BG = "#0f1a2a"
TEXT_DARK = "#000000"
TEXT_LIGHT = "#ffffff"


# ----------
# WINDOW SETUP
# ----------
root = tk.Tk()
root.title("Recipe App UI")
root.geometry("1000x600")
root.configure(bg=BG_MAIN)

# Default Font
default_font = font.Font(family="Arial", size=14, weight="bold")


# ----------
# LEFT SIDEBAR (RECIPE BUTTONS)
# ----------
sidebar = tk.Frame(root, bg=BG_MAIN)
sidebar.place(x=30, y=30)

for i in range(1, 6):
    btn = tk.Button(
        sidebar,
        text=f"Recipe {i}",
        bg=BTN_SIDEBAR,
        fg=TEXT_DARK,
        width=18,
        height=2,
        font=default_font,
        relief="flat",
        bd=0,
    )
    btn.pack(pady=10)


# ----------
# MAIN DETAIL PANEL
# ----------
detail = tk.Frame(root, bg=DETAIL_BG, width=500, height=350)
detail.place(x=300, y=60)

lbl_title = tk.Label(detail, text="Recipe 1", font=("Arial", 18, "bold"), bg=DETAIL_BG)
lbl_title.place(x=20, y=20)

lbl_info = tk.Label(detail, text="Details about recipe here ...", font=("Arial", 14), bg=DETAIL_BG)
lbl_info.place(x=20, y=70)


# ----------
# RIGHT ACTION BUTTONS
# ----------
right_panel = tk.Frame(root, bg=BG_MAIN)
right_panel.place(x=800, y=100)

for txt in ["Upload", "Download", "Comment"]:
    tk.Button(
        right_panel,
        text=txt,
        font=default_font,
        bg=BTN_MAIN,
        fg=TEXT_DARK,
        width=12,
        height=2,
        relief="flat",
    ).pack(pady=25)


# ----------
# BOTTOM NAVIGATION BAR
# ----------
bottom_nav = tk.Frame(root, bg=NAV_BG, height=80, width=1000)
bottom_nav.place(x=0, y=520)

nav_items = ["Home", "Recipes", "Settings"]
positions = [150, 450, 780]

for label, x in zip(nav_items, positions):
    tk.Label(bottom_nav, text=label, fg=TEXT_LIGHT, bg=NAV_BG,
             font=("Arial", 20, "bold")).place(x=x, y=20)


root.mainloop()
import tkinter as tk
from tkinter import font

# ---------- COLORS ----------
BG_MAIN = "#faeddc"
BTN_SIDEBAR = "#efe2f5"
BTN_MAIN = "#b6ff38"
DETAIL_BG = "#ede0f0"
NAV_BG = "#0f1a2a"
TEXT_DARK = "#000000"
TEXT_LIGHT = "#ffffff"


# ----------
# WINDOW SETUP
# ----------
root = tk.Tk()
root.title("Recipe App UI")
root.geometry("1000x600")
root.configure(bg=BG_MAIN)

# Default Font
default_font = font.Font(family="Arial", size=14, weight="bold")


# ----------
# LEFT SIDEBAR (RECIPE BUTTONS)
# ----------
sidebar = tk.Frame(root, bg=BG_MAIN)
sidebar.place(x=30, y=30)

for i in range(1, 6):
    btn = tk.Button(
        sidebar,
        text=f"Recipe {i}",
        bg=BTN_SIDEBAR,
        fg=TEXT_DARK,
        width=18,
        height=2,
        font=default_font,
        relief="flat",
        bd=0,
    )
    btn.pack(pady=10)


# ----------
# MAIN DETAIL PANEL
# ----------
detail = tk.Frame(root, bg=DETAIL_BG, width=500, height=350)
detail.place(x=300, y=60)

lbl_title = tk.Label(detail, text="Recipe 1", font=("Arial", 18, "bold"), bg=DETAIL_BG)
lbl_title.place(x=20, y=20)

lbl_info = tk.Label(detail, text="Details about recipe here ...", font=("Arial", 14), bg=DETAIL_BG)
lbl_info.place(x=20, y=70)


# ----------
# RIGHT ACTION BUTTONS
# ----------
right_panel = tk.Frame(root, bg=BG_MAIN)
right_panel.place(x=800, y=100)

for txt in ["Upload", "Download", "Comment"]:
    tk.Button(
        right_panel,
        text=txt,
        font=default_font,
        bg=BTN_MAIN,
        fg=TEXT_DARK,
        width=12,
        height=2,
        relief="flat",
    ).pack(pady=25)


# ----------
# BOTTOM NAVIGATION BAR
# ----------
bottom_nav = tk.Frame(root, bg=NAV_BG, height=80, width=1000)
bottom_nav.place(x=0, y=520)

nav_items = ["Home", "Recipes", "Settings"]
positions = [150, 450, 780]

for label, x in zip(nav_items, positions):
    tk.Label(bottom_nav, text=label, fg=TEXT_LIGHT, bg=NAV_BG,
             font=("Arial", 20, "bold")).place(x=x, y=20)


root.mainloop()
