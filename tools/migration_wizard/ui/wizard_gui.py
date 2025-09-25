import tkinter as tk
from tkinter import ttk, messagebox

def on_detect():
    messagebox.showinfo("Detect", "Detecting existing licenses... (demo)")

def on_generate():
    messagebox.showinfo("Generate", "Generated offline request. (demo)")

def on_activate_apply():
    messagebox.showinfo("Activate", "Applied activation ticket. (demo)")

def on_validate():
    messagebox.showinfo("Validate", "Validated license locally. (demo)")

def main():
    root = tk.Tk()
    root.title("LicenseHub Migration Wizard (Demo)")
    root.geometry("480x320")

    frm = ttk.Frame(root, padding=12)
    frm.pack(fill=tk.BOTH, expand=True)

    ttk.Label(frm, text="Migration Wizard (Demo)", font=("Segoe UI", 14, "bold")).pack(pady=6)
    ttk.Button(frm, text="Detect", command=on_detect).pack(fill=tk.X, pady=4)
    ttk.Button(frm, text="Generate Request", command=on_generate).pack(fill=tk.X, pady=4)
    ttk.Button(frm, text="Activate & Apply", command=on_activate_apply).pack(fill=tk.X, pady=4)
    ttk.Button(frm, text="Validate Ticket", command=on_validate).pack(fill=tk.X, pady=4)

    root.mainloop()

if __name__ == "__main__":
    main()
