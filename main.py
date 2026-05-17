import customtkinter as ctk 
from tkinter import messagebox
from threading import Thread
from database import get_tasks, add_task, get_notes, add_note
from analytics import *
from timer import *
from theme import *
import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.geometry("1600x900")
app.title("NeuroDesk AI")
app.configure(fg_color=BACKGROUND)
              
#sidebar
sidebar = ctk.CTkFrame(app, width=260, fg_color="#0B1627")
sidebar.pack(side="left", fill="y")

logo = ctk.CTkLabel(
    sidebar, text="NEURODESK", font=("Orbitron", 28, "bold"), text_color=PRIMARY
)
logo.pack(pady=40)

#main area
main = ctk.CTkFrame(app, fg_color=BACKGROUND)
main.pack( fill="both", expand=True)

#top bar
header = ctk.CTkFrame(main, height=80, fg_color="#08101C")
header.pack(fill="x", padx=20, pady=20)

current_time = ctk.CTkLabel(header, text="", font=("Poppins", 18), text_color=TEXT)
current_time.pack(side="right", padx=20)

def update_clock():
    now = datetime.datetime.now().strftime("%A | %d %B %Y | %I:%M:%S:")
    current_time.configure(text=now)
    app.after(1000, update_clock)
update_clock()


#dashboard grid
content = ctk.CTkFrame(main, fg_color=BACKGROUND)
content.pack(fill="both", expand=True, padx=20, pady=10)

#cpu card
cpu_card = ctk.CTkFrame(content, corner_radius=25, fg_color=CARD)
cpu_card.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

cpu_title = ctk.CTkLabel(cpu_card, text="CPU USAGE", font=("Poppins", 22, "bold"), text_color=PRIMARY)
cpu_title.pack(pady=(20))

cpu_value = ctk.CTkLabel(cpu_card, text="0%", font=("Orbitron", 40, "bold"), text_color=SUCCESS)
cpu_value.pack(pady=(20))

#ram card
ram_card = ctk.CTkFrame(content, corner_radius=25, fg_color=CARD)
ram_card.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

ram_title = ctk.CTkLabel(ram_card, text="RAM USAGE", font=("Poppins", 22, "bold"), text_color=SECONDARY)
ram_title.pack(pady=(20))

ram_value = ctk.CTkLabel(ram_card, text="0%", font=("Orbitron", 40, "bold"), text_color=WARNING)
ram_value.pack(pady=(20))


#task manager 

task_card = ctk.CTkFrame(content, corner_radius=25, fg_color=CARD)
task_card.grid(row=1, column=0,  padx=15, pady=15, sticky="nsew")

ctk.CTkLabel(task_card, text="Smart Tasks", font=("Poppins", 24, "bold"), text_color=PRIMARY).pack(pady=(15))

task_input = ctk.CTkEntry(task_card, placeholder_text="Enter a task...", width=300, height=45, corner_radius=15)
task_input.pack(pady=(10))

task_box = ctk.CTkTextbox(task_card, width=500, height=250)
task_box.pack(pady=(15))

def refresh_tasks():
    task_box.delete("1.0", "end")
    tasks = get_tasks()
    for task in tasks:
        status = "✅" if task[2] == "Completed" else "⏳"
        task_box.insert("end", f"{status} {task[1]}\n")

        def add_new_task():
            text = task_input.get()
            if text:
                add_task(text)
                task_input.delete(0, "end")
                refresh_tasks()
            else:
                messagebox.showwarning("Input Error", "Please enter a task.")
                add_btn = ctk.CTkButton(task_card, text="Add Task", command=add_new_task, height=45, corner_radius=15, fg_color=PRIMARY, text_color="black")
                add_btn.pack(pady=(10))

                refresh_tasks()

                #notes panel
notes_card = ctk.CTkFrame(content, corner_radius=25, fg_color=CARD)
notes_card.grid(row=1, column=1, padx=15, pady=15, sticky="nsew")

ctk.CTkLabel(notes_card, text="AI Notes", font=("Poppins", 24, "bold"), text_color=SECONDARY).pack(pady=(15))
notes_input = ctk.CTkEntry(notes_card, placeholder_text="Enter a note...", width=450, height=150, corner_radius=15)
notes_input.pack(pady=(10))

notes_view = ctk.CTkTextbox(notes_card, width=450, height=150)
notes_view.pack(pady=(10))

def refresh_notes():
    notes_view.delete("1.0", "end")
    for note in get_notes():
        notes_view.insert("end", f"📝 {note[1]}\n")

        refresh_notes()

        def save_note():
            text = notes_input.get("1.0", "end")
            if text.strip():
                add_note(text)
                notes_input.delete("1.0", "end")
                refresh_notes()
            else:
                messagebox.showwarning("Input Error", "Please enter a note.")
                save_btn = ctk.CTkButton(notes_card, text="Save Note", command=save_note, height=45, corner_radius=15, fg_color=SECONDARY, text_color="black")
                save_btn.pack(pady=(10))

#pomodoro timer
timer_card = ctk.CTkFrame(content, corner_radius=25, fg_color=CARD)
timer_card.grid(row=2, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")

ctk.CTkLabel(timer_card, text="Focus Mode", font=("Orbitron", 24, "bold"), text_color=SUCCESS).pack(pady=(20))
timer_label = ctk.CTkLabel(timer_card, text="25:00", font=("Orbitron", 60, "bold"), text_color=TEXT)
timer_label.pack(pady=(10))

def update_timer_display(text):
    timer_label.configure(text=text)

def run_pomodoro():
      Thread(target=start_timer, args=(1500, update_timer_display),daemon=True).start()
start_btn = ctk.CTkButton(timer_card, text="Start Focus Session", command=run_pomodoro, height=50, width=300, corner_radius=20, fg_color=SUCCESS, text_color="black")
start_btn.pack(pady=(20))

#live update

def update_stats():
    cpu = get_cpu()
    ram = get_ram()

    cpu_value.configure(text=f"{cpu}%")
    ram_value.configure(text=f"{ram}%")

    app.after(5000, update_stats)
update_stats()


#responsive layout
content.grid_rowconfigure(0, weight=1)
content.grid_rowconfigure(1, weight=1)
content.grid_rowconfigure(2, weight=1)
content.grid_columnconfigure(0, weight=1)
content.grid_columnconfigure(1, weight=1)
app.mainloop()