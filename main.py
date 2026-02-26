import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from datetime import datetime

# =========================
# GLOBAL VARIABLES
# =========================

loading_animation_id = None
loading_dots = 0

# =========================
# FUNCTIONS
# =========================

def start_loading_animation():
    """Start the loading animation with animated dots."""
    global loading_animation_id, loading_dots
    loading_dots = 0
    loading_label.config(text="Computing")
    loading_label.pack(pady=(0, 10))
    compute_btn.state(['disabled'])
    clear_btn.state(['disabled'])
    animate_loading()

def animate_loading():
    """Animate the loading dots."""
    global loading_animation_id, loading_dots
    dots = "." * (loading_dots % 4)
    loading_label.config(text=f"Computing{dots}")
    loading_dots += 1
    loading_animation_id = root.after(300, animate_loading)

def stop_loading_animation():
    """Stop the loading animation."""
    global loading_animation_id
    if loading_animation_id:
        root.after_cancel(loading_animation_id)
        loading_animation_id = None
    loading_label.pack_forget()
    compute_btn.state(['!disabled'])
    clear_btn.state(['!disabled'])

def compute_with_loading():
    """Wrapper to show loading animation before computing."""
    start_loading_animation()
    # Schedule the actual computation after a brief delay to show animation
    root.after(800, perform_computation)

def perform_computation():
    """Perform the actual computation after loading animation."""
    compute()
    stop_loading_animation()

def compute():
    trail_text.delete("1.0", tk.END)
    final_answer_var.set("")

    trail_output = "VALIDATION STATUS:\n"

    x0 = x0_entry.get().strip()
    tol = tol_entry.get().strip()
    max_iter = iter_entry.get().strip()

    # -------------------------
    # REQUIRED FIELD CHECK
    # -------------------------
    if not x0 or not tol or not max_iter:
        trail_output += "❌ Validation Failed: All fields are required.\n"
        trail_text.insert(tk.END, trail_output)
        return

    # -------------------------
    # TYPE CHECK
    # -------------------------
    try:
        x0 = float(x0)
    except ValueError:
        trail_output += "❌ Validation Failed: Initial Guess must be a number.\n"
        trail_text.insert(tk.END, trail_output)
        return

    try:
        tol = float(tol)
    except ValueError:
        trail_output += "❌ Validation Failed: Tolerance must be a decimal number.\n"
        trail_text.insert(tk.END, trail_output)
        return

    try:
        max_iter = int(max_iter)
    except ValueError:
        trail_output += "❌ Validation Failed: Max Iterations must be an integer.\n"
        trail_text.insert(tk.END, trail_output)
        return

    # -------------------------
    # RANGE CHECK
    # -------------------------
    if tol <= 0:
        trail_output += "❌ Validation Failed: Tolerance must be greater than 0.\n"
        trail_text.insert(tk.END, trail_output)
        return

    if max_iter <= 0 or max_iter > 1000:
        trail_output += "❌ Validation Failed: Max Iterations must be between 1 and 1000.\n"
        trail_text.insert(tk.END, trail_output)
        return

    # -------------------------
    # IF VALIDATION PASSES
    # -------------------------
    trail_output += "✅ Validation Passed\n\n"

    trail_output += f"""GIVEN:
Initial Guess (x0): {x0}
Tolerance: {tol}
Max Iterations: {max_iter}

METHOD:
Newton-Raphson Method (To be implemented Week 3)

STEPS:
Computation will be added next week.

FINAL ANSWER:
Not computed yet

VERIFICATION:
Pending implementation

SUMMARY:
Validation successful.
Timestamp: {datetime.now()}
"""

    trail_text.insert(tk.END, trail_output)


def clear():
    trail_text.delete("1.0", tk.END)
    final_answer_var.set("")
    x0_entry.delete(0, tk.END)
    tol_entry.delete(0, tk.END)
    iter_entry.delete(0, tk.END)


# =========================
# MAIN WINDOW
# =========================

root = tk.Tk()
root.title("Newton-Raphson Root Finder")
root.geometry("800x750")
root.configure(bg="#FFFFFF")
root.resizable(True, True)

# =========================
# STYLE CONFIGURATION
# =========================

style = ttk.Style()
style.theme_use('clam')

# Configure main background colors
style.configure(".", background="#FFFFFF", foreground="#000000")
style.configure("TFrame", background="#FFFFFF")
style.configure("TLabelframe", background="#FFFFFF", foreground="#000000")
style.configure("TLabelframe.Label", background="#FFFFFF", foreground="#000000", 
                font=("Segoe UI", 11, "bold"))

# Configure labels
style.configure("TLabel", background="#FFFFFF", foreground="#000000", 
                font=("Segoe UI", 10))
style.configure("Title.TLabel", background="#FFFFFF", foreground="#000000", 
                font=("Segoe UI", 14, "bold"))
style.configure("SectionTitle.TLabel", background="#FFFFFF", foreground="#000000", 
                font=("Segoe UI", 11, "bold"))
style.configure("InputLabel.TLabel", background="#FFFFFF", foreground="#000000", 
                font=("Segoe UI", 10, "bold"))
style.configure("Loading.TLabel", background="#FFFFFF", foreground="#555555", 
                font=("Segoe UI", 10, "italic"))

# Configure entries
style.configure("TEntry", fieldbackground="#FFFFFF", foreground="#000000", 
                font=("Segoe UI", 10))

# Configure buttons with hover effects
style.configure("Action.TButton",
                background="#F0F0F0",
                foreground="#000000",
                font=("Segoe UI", 10, "bold"),
                padding=(20, 10),
                borderwidth=1,
                relief="solid")
style.map("Action.TButton",
          background=[("active", "#E0E0E0"), ("disabled", "#F5F5F5")],
          foreground=[("disabled", "#AAAAAA")])

style.configure("Clear.TButton",
                background="#F0F0F0",
                foreground="#000000",
                font=("Segoe UI", 10),
                padding=(20, 10),
                borderwidth=1,
                relief="solid")
style.map("Clear.TButton",
          background=[("active", "#E0E0E0"), ("disabled", "#F5F5F5")],
          foreground=[("disabled", "#AAAAAA")])

# =========================
# MAIN CONTAINER
# =========================

main_container = ttk.Frame(root, padding=(30, 20, 30, 20))
main_container.pack(fill="both", expand=True)

# =========================
# HEADER / TITLE
# =========================

header_frame = ttk.Frame(main_container)
header_frame.pack(fill="x", pady=(0, 20))

title_label = ttk.Label(header_frame, text="Newton-Raphson Root Finder", 
                         style="Title.TLabel")
title_label.pack(anchor="center")

separator_top = ttk.Separator(main_container, orient="horizontal")
separator_top.pack(fill="x", pady=(0, 20))

# =========================
# INPUT SECTION
# =========================

input_section = ttk.LabelFrame(main_container, text="  Inputs  ", padding=(20, 15, 20, 15))
input_section.pack(fill="x", pady=(0, 15))

# Configure grid columns for alignment
input_section.columnconfigure(0, weight=0, minsize=150)
input_section.columnconfigure(1, weight=1)

# Initial Guess
ttk.Label(input_section, text="Initial Guess (x₀):", 
          style="InputLabel.TLabel").grid(row=0, column=0, sticky="w", padx=(5, 15), pady=8)
x0_entry = ttk.Entry(input_section, width=30, font=("Segoe UI", 10))
x0_entry.grid(row=0, column=1, sticky="w", padx=5, pady=8)

# Tolerance
ttk.Label(input_section, text="Tolerance:", 
          style="InputLabel.TLabel").grid(row=1, column=0, sticky="w", padx=(5, 15), pady=8)
tol_entry = ttk.Entry(input_section, width=30, font=("Segoe UI", 10))
tol_entry.grid(row=1, column=1, sticky="w", padx=5, pady=8)

# Max Iterations
ttk.Label(input_section, text="Max Iterations:", 
          style="InputLabel.TLabel").grid(row=2, column=0, sticky="w", padx=(5, 15), pady=8)
iter_entry = ttk.Entry(input_section, width=30, font=("Segoe UI", 10))
iter_entry.grid(row=2, column=1, sticky="w", padx=5, pady=8)

# =========================
# CONTROL BUTTONS SECTION
# =========================

button_section = ttk.Frame(main_container)
button_section.pack(fill="x", pady=(5, 15))

button_container = ttk.Frame(button_section)
button_container.pack(anchor="center")

compute_btn = ttk.Button(button_container, text="Compute", style="Action.TButton",
                          command=compute_with_loading)
compute_btn.pack(side="left", padx=(0, 15))

clear_btn = ttk.Button(button_container, text="Clear", style="Clear.TButton",
                        command=clear)
clear_btn.pack(side="left", padx=(15, 0))

# Loading indicator (hidden by default)
loading_label = ttk.Label(main_container, text="Computing...", style="Loading.TLabel")

# =========================
# FINAL ANSWER SECTION
# =========================

answer_section = ttk.LabelFrame(main_container, text="  Final Answer  ", padding=(20, 15, 20, 15))
answer_section.pack(fill="x", pady=(0, 15))

final_answer_var = tk.StringVar()
final_answer_var.set("—")

final_answer_display = ttk.Label(answer_section, textvariable=final_answer_var,
                                  font=("Segoe UI", 12), anchor="center")
final_answer_display.pack(fill="x", pady=5)

# =========================
# SOLUTION TRAIL SECTION
# =========================

trail_section = ttk.LabelFrame(main_container, text="  Solution Trail  ", padding=(15, 10, 15, 10))
trail_section.pack(fill="both", expand=True, pady=(0, 10))

# Create a frame to hold the text widget and scrollbar
trail_container = ttk.Frame(trail_section)
trail_container.pack(fill="both", expand=True)

# Create the scrolled text widget with custom styling
trail_text = scrolledtext.ScrolledText(
    trail_container,
    width=85,
    height=15,
    font=("Consolas", 10),
    bg="#FAFAFA",
    fg="#000000",
    insertbackground="#000000",
    selectbackground="#D0D0D0",
    selectforeground="#000000",
    relief="solid",
    borderwidth=1,
    padx=10,
    pady=10,
    wrap="word"
)
trail_text.pack(fill="both", expand=True, padx=5, pady=5)

# =========================
# FOOTER
# =========================

footer_frame = ttk.Frame(main_container)
footer_frame.pack(fill="x", pady=(10, 0))

footer_label = ttk.Label(footer_frame, text="Newton-Raphson Method — Numerical Analysis",
                          font=("Segoe UI", 9), foreground="#888888")
footer_label.pack(anchor="center")

# =========================
# RUN PROGRAM
# =========================

root.mainloop()