#!/usr/bin/env python3
"""
Simple Auto-Clicker Application
A tkinter-based GUI autoclicker for automating repetitive clicking tasks.
"""

import tkinter as tk
from tkinter import ttk
import pyautogui
import threading
import time


class AutoClicker:
    def __init__(self, root):
        self.root = root
        self.root.title("Auto Clicker")
        self.root.geometry("350x300")
        self.root.resizable(False, False)

        # Variables
        self.is_running = False
        self.click_thread = None

        # Create GUI
        self.create_widgets()

        # Bind keyboard shortcut (F8 to stop)
        self.root.bind('<F8>', lambda e: self.stop_clicking())

    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Title
        title_label = ttk.Label(main_frame, text="Auto Clicker",
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Click interval settings
        interval_frame = ttk.LabelFrame(main_frame, text="Click Interval", padding="10")
        interval_frame.grid(row=1, column=0, columnspan=2, pady=(0, 15), sticky=(tk.W, tk.E))

        ttk.Label(interval_frame, text="Hours:").grid(row=0, column=0, sticky=tk.W)
        self.hours_var = tk.StringVar(value="0")
        self.hours_spin = ttk.Spinbox(interval_frame, from_=0, to=23, width=10,
                                      textvariable=self.hours_var)
        self.hours_spin.grid(row=0, column=1, padx=5)

        ttk.Label(interval_frame, text="Minutes:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.minutes_var = tk.StringVar(value="0")
        self.minutes_spin = ttk.Spinbox(interval_frame, from_=0, to=59, width=10,
                                        textvariable=self.minutes_var)
        self.minutes_spin.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(interval_frame, text="Seconds:").grid(row=2, column=0, sticky=tk.W)
        self.seconds_var = tk.StringVar(value="1")
        self.seconds_spin = ttk.Spinbox(interval_frame, from_=0, to=59, width=10,
                                        textvariable=self.seconds_var)
        self.seconds_spin.grid(row=2, column=1, padx=5)

        ttk.Label(interval_frame, text="Milliseconds:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.milliseconds_var = tk.StringVar(value="0")
        self.milliseconds_spin = ttk.Spinbox(interval_frame, from_=0, to=999, width=10,
                                             textvariable=self.milliseconds_var)
        self.milliseconds_spin.grid(row=3, column=1, padx=5, pady=5)

        # Click type
        click_type_frame = ttk.LabelFrame(main_frame, text="Click Type", padding="10")
        click_type_frame.grid(row=2, column=0, columnspan=2, pady=(0, 15), sticky=(tk.W, tk.E))

        self.click_type_var = tk.StringVar(value="left")
        ttk.Radiobutton(click_type_frame, text="Left Click", variable=self.click_type_var,
                       value="left").grid(row=0, column=0, padx=5)
        ttk.Radiobutton(click_type_frame, text="Right Click", variable=self.click_type_var,
                       value="right").grid(row=0, column=1, padx=5)
        ttk.Radiobutton(click_type_frame, text="Double Click", variable=self.click_type_var,
                       value="double").grid(row=0, column=2, padx=5)

        # Control buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=3, column=0, columnspan=2, pady=(0, 10))

        self.start_button = ttk.Button(button_frame, text="Start (F8 to stop)",
                                       command=self.start_clicking, width=20)
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = ttk.Button(button_frame, text="Stop",
                                      command=self.stop_clicking, width=20,
                                      state=tk.DISABLED)
        self.stop_button.grid(row=1, column=0, padx=5, pady=5)

        # Status label
        self.status_label = ttk.Label(main_frame, text="Status: Stopped",
                                     font=('Arial', 10))
        self.status_label.grid(row=4, column=0, columnspan=2, pady=(10, 0))

    def get_interval(self):
        """Calculate total interval in seconds"""
        try:
            hours = int(self.hours_var.get())
            minutes = int(self.minutes_var.get())
            seconds = int(self.seconds_var.get())
            milliseconds = int(self.milliseconds_var.get())

            total_seconds = (hours * 3600 + minutes * 60 + seconds +
                           milliseconds / 1000.0)

            if total_seconds <= 0:
                return None
            return total_seconds
        except ValueError:
            return None

    def click_worker(self, interval, click_type):
        """Worker thread for clicking"""
        while self.is_running:
            try:
                if click_type == "left":
                    pyautogui.click()
                elif click_type == "right":
                    pyautogui.rightClick()
                elif click_type == "double":
                    pyautogui.doubleClick()

                time.sleep(interval)
            except Exception as e:
                print(f"Error during clicking: {e}")
                break

    def start_clicking(self):
        """Start the auto-clicking"""
        if self.is_running:
            return

        interval = self.get_interval()
        if interval is None:
            self.status_label.config(text="Status: Invalid interval!",
                                    foreground="red")
            return

        self.is_running = True
        click_type = self.click_type_var.get()

        # Start clicking thread
        self.click_thread = threading.Thread(target=self.click_worker,
                                            args=(interval, click_type),
                                            daemon=True)
        self.click_thread.start()

        # Update UI
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_label.config(text="Status: Running...", foreground="green")

        # Disable interval controls
        self.hours_spin.config(state=tk.DISABLED)
        self.minutes_spin.config(state=tk.DISABLED)
        self.seconds_spin.config(state=tk.DISABLED)
        self.milliseconds_spin.config(state=tk.DISABLED)

    def stop_clicking(self):
        """Stop the auto-clicking"""
        if not self.is_running:
            return

        self.is_running = False

        # Update UI
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.status_label.config(text="Status: Stopped", foreground="black")

        # Enable interval controls
        self.hours_spin.config(state=tk.NORMAL)
        self.minutes_spin.config(state=tk.NORMAL)
        self.seconds_spin.config(state=tk.NORMAL)
        self.milliseconds_spin.config(state=tk.NORMAL)


def main():
    root = tk.Tk()
    app = AutoClicker(root)
    root.mainloop()


if __name__ == "__main__":
    main()
