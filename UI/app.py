import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
from predict import predict_note_and_authenticity

currency_names = {
    "10": "₹10 Note",
    "20": "₹20 Note",
    "50": "₹50 Note",
    "100": "₹100 Note",
    "200": "₹200 Note",
    "500": "₹500 Note",
    "2000": "₹2000 Note"
}

# ─────────────────────────────────────────
#  STATE
# ─────────────────────────────────────────
stats = {"total": 0, "real": 0, "fake": 0}
history = []

# ─────────────────────────────────────────
#  WINDOW
# ─────────────────────────────────────────
window = tk.Tk()
window.title("Smart Currency Detector")
window.geometry("720x780")
window.configure(bg="#F5F5F0")
window.resizable(True, True)

# ─────────────────────────────────────────
#  SCROLLABLE WRAPPER
# ─────────────────────────────────────────
main_canvas = tk.Canvas(window, bg="#F5F5F0", highlightthickness=0)
scrollbar = tk.Scrollbar(window, orient="vertical", command=main_canvas.yview)
main_canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

content_frame = tk.Frame(main_canvas, bg="#F5F5F0")
canvas_window = main_canvas.create_window((0, 0), window=content_frame, anchor="nw")

def on_frame_configure(event):
    main_canvas.configure(scrollregion=main_canvas.bbox("all"))

def on_canvas_configure(event):
    main_canvas.itemconfig(canvas_window, width=event.width)

content_frame.bind("<Configure>", on_frame_configure)
main_canvas.bind("<Configure>", on_canvas_configure)

# ── Mouse wheel / trackpad 2-finger scroll ──────────────────────────────────
def on_mousewheel(event):
    if event.delta:                              # Windows + macOS
        main_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
    elif event.num == 4:                         # Linux scroll up
        main_canvas.yview_scroll(-1, "units")
    elif event.num == 5:                         # Linux scroll down
        main_canvas.yview_scroll(1, "units")

window.bind_all("<MouseWheel>", on_mousewheel)   # Windows + macOS
window.bind_all("<Button-4>",   on_mousewheel)   # Linux
window.bind_all("<Button-5>",   on_mousewheel)   # Linux

# ─────────────────────────────────────────
#  FONTS
# ─────────────────────────────────────────
FONT_TITLE   = ("Helvetica Neue", 20, "bold")
FONT_SUB     = ("Helvetica Neue", 11)
FONT_LABEL   = ("Helvetica Neue", 12)
FONT_BOLD    = ("Helvetica Neue", 13, "bold")
FONT_SMALL   = ("Helvetica Neue", 10)
FONT_STAT    = ("Helvetica Neue", 26, "bold")
FONT_MONO    = ("Courier New", 11)

# ─────────────────────────────────────────
#  COLORS
# ─────────────────────────────────────────
BG          = "#F5F5F0"
CARD_BG     = "#FFFFFF"
BORDER      = "#E0DFD8"
TEXT_PRI    = "#1A1A1A"
TEXT_SEC    = "#6B6B6B"
TEXT_HINT   = "#A0A09A"
GREEN_BG    = "#EAF3DE"
GREEN_FG    = "#3B6D11"
RED_BG      = "#FCEBEB"
RED_FG      = "#A32D2D"
BLUE_BG     = "#E6F1FB"
BLUE_FG     = "#185FA5"
BTN_BG      = "#FFFFFF"
BTN_HOVER   = "#F0EFF8"

# ─────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────
def make_card(parent, pady=(0, 12)):
    frame = tk.Frame(parent, bg=CARD_BG, bd=0, highlightthickness=1,
                     highlightbackground=BORDER)
    frame.pack(fill="x", padx=24, pady=pady)
    return frame

def section_label(parent, text):
    tk.Label(parent, text=text.upper(), font=FONT_SMALL,
             bg=CARD_BG, fg=TEXT_HINT,
             anchor="w").pack(fill="x", padx=16, pady=(12, 4))

def divider(parent):
    tk.Frame(parent, bg=BORDER, height=1).pack(fill="x", padx=16)

# ─────────────────────────────────────────
#  HEADER
# ─────────────────────────────────────────
header_frame = tk.Frame(content_frame, bg=CARD_BG, bd=0,
                         highlightthickness=1, highlightbackground=BORDER)
header_frame.pack(fill="x", padx=24, pady=(20, 12))

header_inner = tk.Frame(header_frame, bg=CARD_BG)
header_inner.pack(fill="x", padx=16, pady=14)

logo_lbl = tk.Label(header_inner, text="₹", font=("Helvetica Neue", 28, "bold"),
                    bg="#EAF3DE", fg=GREEN_FG, width=2, relief="flat")
logo_lbl.pack(side="left", padx=(0, 14))

title_col = tk.Frame(header_inner, bg=CARD_BG)
title_col.pack(side="left", fill="both")

tk.Label(title_col, text="Smart Currency Detector",
         font=FONT_TITLE, bg=CARD_BG, fg=TEXT_PRI,
         anchor="w").pack(anchor="w")
tk.Label(title_col,
         text="AI-powered real vs. fake detection — because your eyes deserve a break",
         font=FONT_SUB, bg=CARD_BG, fg=TEXT_SEC,
         anchor="w").pack(anchor="w")

# ─────────────────────────────────────────
#  UPLOAD CARD
# ─────────────────────────────────────────
upload_card = make_card(content_frame, pady=(0, 12))

section_label(upload_card, "Upload note")
divider(upload_card)

drop_frame = tk.Frame(upload_card, bg="#FAFAF8", bd=0,
                       highlightthickness=1, highlightbackground=BORDER)
drop_frame.pack(fill="x", padx=16, pady=12)

image_label = tk.Label(drop_frame, bg="#FAFAF8",
                        text="No image selected yet.\nDrop your note here (even the crumpled one).",
                        font=FONT_SMALL, fg=TEXT_HINT,
                        pady=28)
image_label.pack(fill="x")

upload_btn = tk.Button(
    upload_card,
    text="  Upload Currency Image",
    font=FONT_BOLD,
    bg=BTN_BG, fg=TEXT_PRI,
    activebackground=BTN_HOVER,
    relief="flat",
    bd=0,
    highlightthickness=1,
    highlightbackground=BORDER,
    cursor="hand2",
    pady=9
)
upload_btn.pack(fill="x", padx=16, pady=(0, 14))

# ─────────────────────────────────────────
#  RESULT CARD
# ─────────────────────────────────────────
result_card = make_card(content_frame, pady=(0, 12))

section_label(result_card, "Detection result")
divider(result_card)

result_inner = tk.Frame(result_card, bg=CARD_BG)
result_inner.pack(fill="x", padx=16, pady=12)

result_thumb = tk.Label(result_inner, bg=BG,
                         text="₹?", font=("Helvetica Neue", 18, "bold"),
                         fg=TEXT_HINT, width=8, height=3,
                         relief="flat",
                         highlightthickness=1,
                         highlightbackground=BORDER)
result_thumb.pack(side="left", padx=(0, 16))

result_text_col = tk.Frame(result_inner, bg=CARD_BG)
result_text_col.pack(side="left", fill="both", expand=True)

result_denom = tk.Label(result_text_col,
                         text="Waiting for a note...",
                         font=FONT_BOLD, bg=CARD_BG, fg=TEXT_PRI,
                         anchor="w")
result_denom.pack(anchor="w")

result_conf = tk.Label(result_text_col,
                        text="Upload an image to begin",
                        font=FONT_SMALL, bg=CARD_BG, fg=TEXT_SEC,
                        anchor="w")
result_conf.pack(anchor="w", pady=(2, 6))

result_badge = tk.Label(result_text_col,
                         text="  Pending  ",
                         font=FONT_SMALL,
                         bg=BLUE_BG, fg=BLUE_FG,
                         padx=8, pady=3,
                         relief="flat")
result_badge.pack(anchor="w")

# ─────────────────────────────────────────
#  STATS CARD
# ─────────────────────────────────────────
stats_card = make_card(content_frame, pady=(0, 12))
section_label(stats_card, "Session stats")
divider(stats_card)

stats_row = tk.Frame(stats_card, bg=CARD_BG)
stats_row.pack(fill="x", padx=16, pady=12)

def make_stat_cell(parent, num_text, label_text, num_color=TEXT_PRI):
    cell = tk.Frame(parent, bg="#FAFAF8", bd=0,
                     highlightthickness=1, highlightbackground=BORDER)
    cell.pack(side="left", fill="both", expand=True, padx=(0, 8))
    num_var = tk.StringVar(value=num_text)
    tk.Label(cell, textvariable=num_var,
             font=FONT_STAT, bg="#FAFAF8",
             fg=num_color).pack(anchor="w", padx=12, pady=(10, 0))
    tk.Label(cell, text=label_text,
             font=FONT_SMALL, bg="#FAFAF8",
             fg=TEXT_SEC).pack(anchor="w", padx=12, pady=(0, 10))
    return num_var

stat_total = make_stat_cell(stats_row, "0", "Notes scanned")
stat_real  = make_stat_cell(stats_row, "0", "Genuine", GREEN_FG)
stat_fake  = make_stat_cell(stats_row, "0", "Suspicious", RED_FG)

# ─────────────────────────────────────────
#  HISTORY CARD
# ─────────────────────────────────────────
history_card = make_card(content_frame, pady=(0, 12))
section_label(history_card, "Recent scans")
divider(history_card)

history_inner = tk.Frame(history_card, bg=CARD_BG)
history_inner.pack(fill="x", padx=16, pady=10)

history_placeholder = tk.Label(history_inner,
                                 text="Nothing yet — the AI is patiently waiting.",
                                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_HINT)
history_placeholder.pack(anchor="w")

# ─────────────────────────────────────────
#  FOOTER
# ─────────────────────────────────────────
footer_frame = tk.Frame(content_frame, bg=BG)
footer_frame.pack(fill="x", padx=24, pady=(0, 24))

tk.Label(footer_frame, text="Powered by AI + Image Processing",
         font=FONT_SMALL, bg=BG, fg=TEXT_HINT,
         anchor="w").pack(side="left")

tk.Label(footer_frame, text="v1.0.0",
         font=FONT_SMALL, bg=BG, fg=TEXT_HINT,
         anchor="e").pack(side="right")

# ─────────────────────────────────────────
#  HISTORY CHIP UPDATER
# ─────────────────────────────────────────
def refresh_history():
    for w in history_inner.winfo_children():
        w.destroy()

    if not history:
        tk.Label(history_inner,
                 text="Nothing yet — the AI is patiently waiting.",
                 font=FONT_SMALL, bg=CARD_BG, fg=TEXT_HINT).pack(anchor="w")
        return

    row = tk.Frame(history_inner, bg=CARD_BG)
    row.pack(fill="x")
    for (denom, auth) in history[:6]:
        bg_c = GREEN_BG if auth == "real" else RED_BG
        fg_c = GREEN_FG if auth == "real" else RED_FG
        tk.Label(row, text=f"  {denom}  ",
                 font=FONT_SMALL,
                 bg=bg_c, fg=fg_c,
                 padx=6, pady=3,
                 relief="flat").pack(side="left", padx=(0, 6))

# ─────────────────────────────────────────
#  MAIN FUNCTION
# ─────────────────────────────────────────
def upload_image():
    file_path = filedialog.askopenfilename(
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if not file_path:
        return

    img = Image.open(file_path)
    img.thumbnail((380, 160))
    img_tk = ImageTk.PhotoImage(img)
    image_label.config(image=img_tk, text="", bg="#FAFAF8")
    image_label.image = img_tk

    denomination, authenticity = predict_note_and_authenticity(file_path)
    note = currency_names.get(str(denomination), f"₹{denomination} Note")
    auth_lower = authenticity.lower()

    result_thumb.config(text=f"₹{denomination}",
                         fg=GREEN_FG if auth_lower == "real" else RED_FG,
                         bg=GREEN_BG if auth_lower == "real" else RED_BG)
    result_denom.config(text=note)

    funny_conf_msg = (
        "The AI is very confident and slightly smug about this."
        if auth_lower == "real"
        else "Confidence: high. Suspicion: higher."
    )
    result_conf.config(text=funny_conf_msg)

    if auth_lower == "real":
        result_badge.config(
            text="  Genuine note — go spend it!  ",
            bg=GREEN_BG, fg=GREEN_FG
        )
    else:
        result_badge.config(
            text="  Looks suspicious — RBI incoming  ",
            bg=RED_BG, fg=RED_FG
        )

    stats["total"] += 1
    if auth_lower == "real":
        stats["real"] += 1
    else:
        stats["fake"] += 1

    stat_total.set(str(stats["total"]))
    stat_real.set(str(stats["real"]))
    stat_fake.set(str(stats["fake"]))

    history.insert(0, (note, auth_lower))
    refresh_history()

upload_btn.config(command=upload_image)

window.mainloop()