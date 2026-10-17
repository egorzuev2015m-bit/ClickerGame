import customtkinter as ctk
from functional import set_clicks, set_crit_100, parse_number

APP_SIZE = "420x280"
FONT = ("Montserrat ExtraBold", 13)

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Insane HackMenu")
app.geometry(APP_SIZE)

frame = ctk.CTkFrame(app)
frame.pack(pady=20, padx=20, fill="both", expand=True)

ctk.CTkLabel(frame, text="Clicks", font=FONT).pack(anchor="w", pady=(10, 0))

input_frame = ctk.CTkFrame(frame, fg_color="transparent")
input_frame.pack(fill="x", pady=8)

entry = ctk.CTkEntry(input_frame, placeholder_text="ex: 999999 or 1.5M")
entry.pack(side="left", fill="x", expand=True, padx=(0, 8))

status = ctk.StringVar(value="Ready")
status_label = ctk.CTkLabel(frame, textvariable=status, font=FONT, text_color="lightgreen")
status_label.pack(anchor="w", pady=(15, 0))


def confirm_clicks():
    try:
        raw_text = entry.get()
        value = parse_number(raw_text)
        if value < 0:
            status.set("⚠️ Must be ≥ 0")
            status_label.configure(text_color="yellow")
            return
        msg, color = set_clicks(value)
        status.set(msg)
        status_label.configure(text_color=color)
    except ValueError:
        status.set("⚠️ Invalid number format")
        status_label.configure(text_color="yellow")


def hack_crit():
    msg, color = set_crit_100()
    status.set(msg)
    status_label.configure(text_color=color)


ctk.CTkButton(input_frame, text="Confirm", font=FONT, command=confirm_clicks).pack(side="right")

ctk.CTkLabel(frame, text="Hacks", font=FONT).pack(anchor="w", pady=(15, 5))

ctk.CTkButton(frame, text="100% Crit", font=FONT,
              fg_color="darkred", hover_color="red",
              command=hack_crit).pack(fill="x", pady=5)

app.mainloop()