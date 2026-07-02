import customtkinter as ctk
import threading
import subprocess
import sys
import os
from datetime import datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AutopilotGUI(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("🚀 AI KDP Autopilot V4")
        self.geometry("800x650")
        self.resizable(False, False)
        self._build_ui()

    def _build_ui(self):
        ctk.CTkLabel(self, text="🚀 AI KDP Autopilot V4",
            font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(20,5))
        ctk.CTkLabel(self, text="Automated Coloring Book Generator",
            font=ctk.CTkFont(size=13), text_color="gray").pack(pady=(0,20))

        frame = ctk.CTkFrame(self)
        frame.pack(padx=30, pady=5, fill="x")

        ctk.CTkLabel(frame, text="📚 Book Niche",
            font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=0, padx=15, pady=(15,5), sticky="w")
        self.niche_entry = ctk.CTkEntry(frame,
            placeholder_text="e.g. jungle animals, dinosaurs...", width=400, height=38)
        self.niche_entry.grid(row=1, column=0, padx=15, pady=(0,15), sticky="w")

        ctk.CTkLabel(frame, text="🎄 Season",
            font=ctk.CTkFont(size=13, weight="bold")).grid(row=0, column=1, padx=15, pady=(15,5), sticky="w")
        self.season_var = ctk.StringVar(value="skip")
        ctk.CTkOptionMenu(frame,
            values=["skip","christmas","halloween","easter","summer","winter"],
            variable=self.season_var, width=180, height=38).grid(row=1, column=1, padx=15, pady=(0,15), sticky="w")

        ctk.CTkLabel(frame, text="📄 Pages",
            font=ctk.CTkFont(size=13, weight="bold")).grid(row=2, column=0, padx=15, pady=(5,5), sticky="w")
        self.pages_slider = ctk.CTkSlider(frame, from_=20, to=80,
            number_of_steps=6, width=400, command=self._update_pages)
        self.pages_slider.set(40)
        self.pages_slider.grid(row=3, column=0, padx=15, pady=(0,5), sticky="w")
        self.pages_label = ctk.CTkLabel(frame, text="40 pages",
            font=ctk.CTkFont(size=12), text_color="gray")
        self.pages_label.grid(row=4, column=0, padx=15, pady=(0,15), sticky="w")

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(padx=30, pady=10, fill="x")

        self.generate_btn = ctk.CTkButton(btn_frame, text="⚡ Generate Book",
            font=ctk.CTkFont(size=14, weight="bold"), height=45, width=220,
            command=self._start)
        self.generate_btn.pack(side="left", padx=(0,10))

        ctk.CTkButton(btn_frame, text="📁 Open Output",
            height=45, width=160, fg_color="gray30", hover_color="gray40",
            command=self._open_output).pack(side="left", padx=(0,10))

        ctk.CTkButton(btn_frame, text="🗑️ Clear Log",
            height=45, width=130, fg_color="gray30", hover_color="gray40",
            command=self._clear_log).pack(side="left")

        self.progress_bar = ctk.CTkProgressBar(self, width=740)
        self.progress_bar.pack(padx=30, pady=(10,5))
        self.progress_bar.set(0)

        self.status_label = ctk.CTkLabel(self, text="Ready...",
            font=ctk.CTkFont(size=12), text_color="gray")
        self.status_label.pack(pady=(0,5))

        ctk.CTkLabel(self, text="📋 Live Log",
            font=ctk.CTkFont(size=13, weight="bold")).pack(padx=30, anchor="w")
        self.log_box = ctk.CTkTextbox(self, width=740, height=220,
            font=ctk.CTkFont(family="Courier", size=12))
        self.log_box.pack(padx=30, pady=(5,20))

        self._log("🚀 AI KDP Autopilot V4 Ready!")

    def _update_pages(self, value):
        self.pages_label.configure(text=f"{int(value)} pages")

    def _log(self, msg):
        t = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert("end", f"[{t}] {msg}\n")
        self.log_box.see("end")

    def _clear_log(self):
        self.log_box.delete("1.0", "end")

    def _open_output(self):
        subprocess.run(["open", os.path.join(os.getcwd(), "output")])

    def _start(self):
        niche = self.niche_entry.get().strip()
        if not niche:
            self._log("❌ Niche daalo!")
            return
        self.generate_btn.configure(state="disabled", text="⏳ Generating...")
        self.progress_bar.set(0)
        threading.Thread(target=self._run, args=(niche,), daemon=True).start()

    def _run(self, niche):
        season = self.season_var.get()
        try:
            self.after(0, self._log, f"🚀 Starting: {niche}")
            self.after(0, self.status_label.configure, {"text": "Running..."})

            process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True, bufsize=1
            )
            process.stdin.write(f"{niche}\n{season}\n")
            process.stdin.flush()