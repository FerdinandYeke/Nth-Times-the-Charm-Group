import tkinter as tk
from tkinter import font

#############################################
# DATABASE INTEGRATION POINTS (TO BE FILLED)
#############################################

# TODO DB: Fetch list of recipe names for sidebar
def db_get_recipe_list():
    # return ["Recipe 1", "Recipe 2", "Recipe 3", ...]
    return []  # placeholder

# TODO DB: Load full recipe details by name or ID
def db_get_recipe_details(recipe_name):
    # Query recipe description, ingredients, steps, etc
    return "No details available yet."  # placeholder

# TODO DB: Save new uploaded recipe to database
def db_upload_recipe(data):
    # data = {title, ingredients, text, image, etc}
    pass

# TODO DB: Download/export recipe data
def db_download_recipe(recipe_name):
    pass

# TODO DB: Store user comment in database
def db_add_comment(recipe_name, comment_text):
    pass


# Colors (same as before)
BG_MAIN = "#faeddc"
BTN_SIDEBAR = "#efe2f5"
BTN_MAIN = "#b6ff38"
DETAIL_BG = "#ede0f0"
NAV_BG = "#0f1a2a"
TEXT_DARK = "#000000"
TEXT_LIGHT = "#ffffff"


root = tk.Tk()
root.title("Recipe App UI")
root.geometry("1000x600")
root.configure(bg=BG_MAIN)

default_font = font.Font(family="Arial", size=14, weight="bold")


#############################################
# FUNCTION: When user clicks a recipe
#############################################
def open_recipe(name):
    # TODO DB: Pull recipe details when selected
    details = db_get_recipe_details(name)

    recipe_title_label.config(text=name)
    recipe_details_label.config(text=details)


#############################################
# PAGE: RECIPES
#############################################
recipes_page = tk.Frame(root, bg=BG_MAIN)

# Sidebar Recipe Buttons
sidebar = tk.Frame(recipes_page, bg=BG_MAIN)
sidebar.place(x=30, y=30)

recipe_list = db_get_recipe_list() or ["Recipe 1", "Recipe 2", "Recipe 3", "Recipe 4"]

for recipe in recipe_list:
    tk.Button(
        sidebar,
        text=recipe,
        bg=BTN_SIDEBAR,
        fg=TEXT_DARK,
        width=18, height=2,
        font=default_font,
        relief="flat",
        command=lambda r=recipe: open_recipe(r)   # UI -> DB connection
    ).pack(pady=10)

# Detail panel where DB data shows up
detail = tk.Frame(recipes_page, bg=DETAIL_BG, width=500, height=350)
detail.place(x=300, y=60)

recipe_title_label = tk.Label(detail, text="(Select a Recipe)", font=("Arial", 18, "bold"), bg=DETAIL_BG)
recipe_title_label.place(x=20, y=20)

recipe_details_label = tk.Label(detail, text="Recipe details will appear here...",
                                font=("Arial", 14), bg=DETAIL_BG, justify="left")
recipe_details_label.place(x=20, y=70)


#############################################
# ACTION BUTTONS (DB HOOK POINTS)
#############################################
right_panel = tk.Frame(recipes_page, bg=BG_MAIN)
right_panel.place(x=800, y=100)

tk.Button(right_panel, text="Upload", bg=BTN_MAIN, font=default_font,
          command=lambda: db_upload_recipe({"sample":"data"})).pack(pady=25)

tk.Button(right_panel, text="Download", bg=BTN_MAIN, font=default_font,
          command=lambda: db_download_recipe(recipe_title_label.cget("text"))).pack(pady=25)

tk.Button(right_panel, text="Comment", bg=BTN_MAIN, font=default_font,
          command=lambda: db_add_comment(recipe_title_label.cget("text"), "sample comment")).pack(pady=25)


#############################################
# PAGE NAVIGATION (Home - Recipes - Settings)
#############################################
home_page = tk.Frame(root, bg=BG_MAIN)
settings_page = tk.Frame(root, bg=BG_MAIN)

def show_page(page):
    for p in (home_page, recipes_page, settings_page):
        p.place_forget()
    page.place(x=0, y=0, relwidth=1, relheight=1)


bottom_nav = tk.Frame(root, bg=NAV_BG, height=80)
bottom_nav.pack(side="bottom", fill="x")

tk.Button(bottom_nav, text="Home", bg=NAV_BG, fg=TEXT_LIGHT, font=("Arial",18,"bold"),
          command=lambda: show_page(home_page)).place(x=150, y=20)

tk.Button(bottom_nav, text="Recipes", bg=NAV_BG, fg=TEXT_LIGHT, font=("Arial",18,"bold"),
          command=lambda: show_page(recipes_page)).place(x=450, y=20)

tk.Button(bottom_nav, text="Settings", bg=NAV_BG, fg=TEXT_LIGHT, font=("Arial",18,"bold"),
          command=lambda: show_page(settings_page)).place(x=780, y=20)

show_page(recipes_page)
root.mainloop()
