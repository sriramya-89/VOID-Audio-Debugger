import pyttsx3
import threading
import time
import subprocess
import tkinter as tk
from tkinter import ttk
import webbrowser
import re

class VOID_Complete_Sri:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("V.O.I.D - Real-Time Audio Debugger")
        self.root.geometry("750x850")
        self.root.configure(bg="#0d1117") 
        
        self.setup_voice_engine()
        self.build_ui()

    def setup_voice_engine(self):
        try:
            temp_engine = pyttsx3.init()
            self.all_voices = temp_engine.getProperty('voices')
            # Male/Female Mapping
            self.voice_map = {"Male Assistant": self.all_voices[0].id}
            if len(self.all_voices) > 1:
                self.voice_map["Female Assistant"] = self.all_voices[1].id
        except:
            self.voice_map = {"Default Assistant": None}

    def build_ui(self):
        tk.Label(self.root, text="V.O.I.D AUDIO DEBUGGER", font=("Segoe UI", 30, "bold"), fg="#58a6ff", bg="#0d1117").pack(pady=20)
        
        # Voice Selection
        tk.Label(self.root, text="CHOOSE YOUR ASSISTANT:", font=("Arial", 10, "bold"), fg="#c9d1d9", bg="#0d1117").pack(pady=(10, 0))
        self.voice_combo = ttk.Combobox(self.root, values=list(self.voice_map.keys()), state="readonly", width=30)
        self.voice_combo.current(0)
        self.voice_combo.pack(pady=10)

        # Command Input
        self.cmd_entry = tk.Entry(self.root, width=60, font=("Consolas", 12), bg="#010409", fg="#c9d1d9", insertbackground="white")
        self.cmd_entry.insert(0, "python test_code.py")
        self.cmd_entry.pack(pady=20)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0d1117")
        btn_frame.pack(pady=10)
        self.run_btn = tk.Button(btn_frame, text="RUN ANALYSIS", command=self.start_thread, bg="#238636", fg="white", font=("Arial", 11, "bold"), width=22, relief="flat")
        self.run_btn.pack(side=tk.LEFT, padx=10)
        self.ai_btn = tk.Button(btn_frame, text="AI FIX", command=self.open_ai, bg="#1f6feb", fg="white", font=("Arial", 11, "bold"), width=22, state="disabled", relief="flat")
        self.ai_btn.pack(side=tk.LEFT, padx=10)

        # Terminal Log
        self.log_box = tk.Text(self.root, height=18, width=85, bg="#010409", fg="#c9d1d9", font=("Consolas", 11), padx=15, pady=15)
        self.log_box.pack(pady=20, padx=20)
        self.log_box.tag_config("error", foreground="#f85149")
        self.log_box.tag_config("info", foreground="#58a6ff")

    def speak_task(self, phrase):
        engine = pyttsx3.init()
        engine.setProperty('rate', 145)
        selected_label = self.voice_combo.get()
        v_id = self.voice_map.get(selected_label)
        if v_id: engine.setProperty('voice', v_id)
        engine.say(phrase)
        engine.runAndWait()
        engine.stop()

    def start_thread(self):
        self.run_btn.config(state="disabled")
        threading.Thread(target=self.execute_logic, daemon=True).start()

    def execute_logic(self):
        cmd = self.cmd_entry.get()
        self.log_box.delete('1.0', tk.END)
        
        # Step 1: Start
        self.speak_task("System verification initiated. Monitoring execution progress.")

        # --- TIME TRACKING START ---
        start_time = time.time()
        
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stdout, stderr = proc.communicate()
        
        end_time = time.time()
        execution_duration = round(end_time - start_time, 2)
        # ---------------------------

        if stdout: 
            self.log_box.insert(tk.END, stdout)
            self.log_box.insert(tk.END, f"\n[INFO]: Execution took {execution_duration} seconds.\n", "info")

        if stderr:
            self.log_box.insert(tk.END, stderr, "error")
            self.ai_btn.config(state="normal")
            
            # Error Parsing
            error_line = ""
            lines = stderr.strip().split('\n')
            for line in lines:
                if "Error" in line or "Exception" in line:
                    error_line = line
            
            line_match = re.search(r'line (\d+)', stderr)
            line_num = line_match.group(1) if line_match else "unknown"

            # Sequential Voice Reporting
            self.speak_task("Alert. Execution failed due to a critical issue.")
            time.sleep(0.3)
            
            if "SyntaxError" in error_line:
                self.speak_task(f"A system syntax error has been caught. Specifically, {error_line}.")
            else:
                self.speak_task(f"A runtime exception has been caught. Specifically, {error_line}.")
            
            time.sleep(0.3)
            self.speak_task(f"The issue is located at line {line_num} of your source code.")
            time.sleep(0.3)
            self.speak_task(f"Total execution time before failure was {execution_duration} seconds.")
            self.speak_task("Would you like to fix this with AI tools?")
        else:
            self.log_box.insert(tk.END, f"\n>>> SUCCESS: Execution took {execution_duration} seconds.", "info")
            self.speak_task(f"System check complete. Process executed successfully in {execution_duration} seconds.")

        self.run_btn.config(state="normal")

    def open_ai(self):
        webbrowser.open("https://gemini.google.com")

if __name__ == "__main__":
    app = VOID_Complete_Sri()
    app.root.mainloop()