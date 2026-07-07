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
        self.geometry("850x700")
        self.resizable(False, False)

        self.build_ui()

    # ----------------------------------
    # UI
    # ----------------------------------

    def build_ui(self):

        title = ctk.CTkLabel(
            self,
            text="🚀 AI KDP Autopilot V4",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Automated Coloring Book Generator",
            text_color="gray"
        )
        subtitle.pack(pady=(0, 20))

        frame = ctk.CTkFrame(self)
        frame.pack(fill="x", padx=25)

        # -----------------------
        # Niche
        # -----------------------

        ctk.CTkLabel(
            frame,
            text="📚 Book Niche"
        ).grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")

        self.niche_entry = ctk.CTkEntry(
            frame,
            width=380,
            height=38,
            placeholder_text="jungle animals"
        )

        self.niche_entry.grid(
            row=1,
            column=0,
            padx=15,
            pady=(0, 15)
        )

        # -----------------------
        # Season
        # -----------------------

        ctk.CTkLabel(
            frame,
            text="🎄 Season"
        ).grid(row=0, column=1, padx=15, pady=(15, 5), sticky="w")

        self.season = ctk.StringVar(value="skip")

        self.season_menu = ctk.CTkOptionMenu(
            frame,
            variable=self.season,
            values=[
                "skip",
                "christmas",
                "halloween",
                "easter",
                "summer",
                "winter"
            ],
            width=170
        )

        self.season_menu.grid(
            row=1,
            column=1,
            padx=15,
            pady=(0, 15)
        )

        # -----------------------
        # Pages
        # -----------------------

        ctk.CTkLabel(
            frame,
            text="📄 Pages"
        ).grid(row=2, column=0, padx=15, sticky="w")

        self.page_slider = ctk.CTkSlider(
            frame,
            from_=20,
            to=80,
            number_of_steps=6,
            width=380,
            command=self.update_pages
        )

        self.page_slider.set(40)

        self.page_slider.grid(
            row=3,
            column=0,
            padx=15,
            pady=(5, 5)
        )

        self.page_label = ctk.CTkLabel(
            frame,
            text="40 pages",
            text_color="gray"
        )

        self.page_label.grid(
            row=4,
            column=0,
            padx=15,
            pady=(0, 15),
            sticky="w"
        )

        # -----------------------
        # Buttons
        # -----------------------

        button_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        button_frame.pack(
            fill="x",
            padx=25,
            pady=15
        )

        self.generate_btn = ctk.CTkButton(
            button_frame,
            text="⚡ Generate Book",
            width=220,
            height=45,
            command=self.start_generation
        )

        self.generate_btn.pack(side="left")

        self.output_btn = ctk.CTkButton(
            button_frame,
            text="📁 Open Output",
            width=160,
            height=45,
            command=self.open_output
        )

        self.output_btn.pack(side="left", padx=10)

        self.clear_btn = ctk.CTkButton(
            button_frame,
            text="🗑 Clear Log",
            width=140,
            height=45,
            command=self.clear_log
        )

        self.clear_btn.pack(side="left")

        # -----------------------
        # Progress
        # -----------------------

        self.progress = ctk.CTkProgressBar(
            self,
            width=780
        )

        self.progress.pack(
            padx=25,
            pady=(5, 5)
        )

        self.progress.set(0)

        self.status = ctk.CTkLabel(
            self,
            text="Ready..."
        )

        self.status.pack()

        # -----------------------
        # Log
        # -----------------------

        ctk.CTkLabel(
            self,
            text="📋 Live Log"
        ).pack(
            anchor="w",
            padx=25,
            pady=(15, 5)
        )

        self.log_box = ctk.CTkTextbox(
            self,
            width=790,
            height=250
        )

        self.log_box.pack(
            padx=25,
            pady=(0, 20)
        )

        self.log("🚀 GUI Ready")

    # ----------------------------------

    def update_pages(self, value):
        self.page_label.configure(
            text=f"{int(value)} pages"
        )

    # ----------------------------------

    def log(self, message):
        now = datetime.now().strftime("%H:%M:%S")
        self.log_box.insert(
            "end",
            f"[{now}] {message}\n"
        )
        self.log_box.see("end")

    # ----------------------------------

    def clear_log(self):
        self.log_box.delete("1.0", "end")

    # ----------------------------------

    def open_output(self):

        path = os.path.join(
            os.getcwd(),
            "output"
        )

        subprocess.run(["open", path])

    # ----------------------------------

    def start_generation(self):

        niche = self.niche_entry.get().strip()

        if niche == "":
            self.log("❌ Please enter a niche.")
            return

        self.generate_btn.configure(
            state="disabled",
            text="Generating..."
        )

        self.progress.set(0)

        threading.Thread(
            target=self.run_pipeline,
            args=(niche,),
            daemon=True
        ).start()
            # ----------------------------------
    # Run Pipeline
    # ----------------------------------

    def run_pipeline(self, niche):

        season = self.season.get()

        try:

            self.after(
                0,
                lambda: self.status.configure(
                    text="Running..."
                )
            )

            self.after(
                0,
                lambda: self.log(
                    f"🚀 Starting: {niche}"
                )
            )

            process = subprocess.Popen(
                [sys.executable, "main.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1
            )

            process.stdin.write(f"{niche}\n")
            process.stdin.write(f"{season}\n")
            process.stdin.write("2\n")
            process.stdin.flush()
            process.stdin.close()

            total_steps = 10
            current_step = 0

            while True:

                line = process.stdout.readline()

                if not line:
                    break

                line = line.rstrip()

                self.after(
                    0,
                    lambda m=line: self.log(m)
                )

                if line.startswith("[") and "/10]" in line:

                    current_step += 1

                    progress = current_step / total_steps

                    self.after(
                        0,
                        lambda p=progress: self.progress.set(p)
                    )

                    self.after(
                        0,
                        lambda s=current_step:
                        self.status.configure(
                            text=f"Step {s}/{total_steps}"
                        )
                    )

            process.wait()

            if process.returncode == 0:

                self.after(
                    0,
                    lambda: self.progress.set(1)
                )

                self.after(
                    0,
                    lambda: self.status.configure(
                        text="✅ Complete"
                    )
                )

                self.after(
                    0,
                    lambda: self.log(
                        "🎉 Book generated successfully."
                    )
                )

            else:

                self.after(
                    0,
                    lambda: self.status.configure(
                        text="❌ Failed"
                    )
                )

                self.after(
                    0,
                    lambda: self.log(
                        "❌ Pipeline failed."
                    )
                )

        except Exception as e:

            self.after(
                0,
                lambda: self.log(
                    f"❌ {e}"
                )
            )

        finally:

            self.after(
                0,
                lambda: self.generate_btn.configure(
                    state="normal",
                    text="⚡ Generate Book"
                )
            )