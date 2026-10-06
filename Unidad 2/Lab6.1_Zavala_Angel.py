import tkinter as tk
from tkinter import ttk
import os
from datetime import datetime
from abc import ABC, abstractmethod


class SmartDevice(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def turn_on(self) -> str:
        pass

    @abstractmethod
    def turn_off(self) -> str:
        pass


class SmartSpeaker(SmartDevice):
    def __init__(self, name):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is playing Lofi music at volume 20%"

    def turn_off(self) -> str:
        return f"{self.name} stopped the music. Silence restored."


class SmartTv(SmartDevice):
    def __init__(self, name):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON. Enjoy your TV shows!"

    def turn_off(self) -> str:
        return f"{self.name} is OFF. Screen went dark."


class SmartLight(SmartDevice):
    def __init__(self, name):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON. Brighten up your space!"

    def turn_off(self) -> str:
        return f"{self.name} is OFF. Lights out!"


class SmartFan(SmartDevice):
    def __init__(self, name):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON at speed 2. Cooling the room down!"

    def turn_off(self) -> str:
        return f"{self.name} is OFF. The blades are slowing down."

class SmartHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Lab 6: Polymorphism with GUI")
        self.geometry("520x640")
        self.resizable(False, False)

        # Application icon
        current_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(current_dir, "icon.png")

        if os.path.exists(icon_path):
            self.app_icon = tk.PhotoImage(file=icon_path)
            self.iconphoto(True, self.app_icon)
        else:
            print("The icon file doesn't exist:", icon_path)

        # Object registry
        self.items = {
            "TV": SmartTv("Roku Smart TV"),
            "Speaker": SmartSpeaker("Echo Dot 5"),
            "Light": SmartLight("Smart Light"),
            "Fan": SmartFan("Dyson Smart Fan"),
        }

        # Build interface
        self._build_interface()

    def _build_interface(self):
        # Header / Title Banner
        lbl_header = tk.Label(
            self,
            text="Smart Home Center",
            font=("Times New Roman", 28, "bold"),
            fg="#2c3e50"
        )
        lbl_header.pack(pady=12)

        # Selection Group
        group_box = tk.LabelFrame(
            self,
            text=" Select an Option ",
            font=("Arial", 14, "bold"),
            padx=15,
            pady=10
        )
        group_box.pack(fill="x", padx=20, pady=5)

        # Default selection
        first_key = list(self.items.keys())[0]
        self.selected_key = tk.StringVar(value=first_key)

        # Create radiobuttons (one per registered device)
        for key in self.items:
            rb = ttk.Radiobutton(
                group_box,
                text=key,
                value=key,
                variable=self.selected_key
            )
            rb.pack(anchor="w", pady=3)

        # Buttons frame (Turn On / Turn Off side by side)
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=12)

        btn_on = tk.Button(
            btn_frame,
            text="Turn On Device",
            command=self._handle_turn_on,
            bg="#2980b9",
            fg="white",
            font=("Arial", 13, "bold"),
            relief="raised",
            cursor="hand2",
            padx=12,
            pady=6
        )
        btn_on.pack(side="left", padx=8)

        btn_off = tk.Button(
            btn_frame,
            text="Turn Off Device",
            command=self._handle_turn_off,
            bg="#c0392b",
            fg="white",
            font=("Arial", 13, "bold"),
            relief="raised",
            cursor="hand2",
            padx=12,
            pady=6
        )
        btn_off.pack(side="left", padx=8)

        # Output box (latest message)
        self.lbl_output = tk.Label(
            self,
            text="Select an option above and click a button.",
            font=("Arial", 10, "italic"),
            bg="#ecf0f1",
            fg="#34495e",
            relief="groove",
            height=3,
            wraplength=460,
            justify="center"
        )
        self.lbl_output.pack(fill="x", padx=20, pady=5)

        # Activity Log
        log_box = tk.LabelFrame(
            self,
            text=" Activity Log ",
            font=("Arial", 12, "bold"),
            padx=8,
            pady=6
        )
        log_box.pack(fill="both", expand=True, padx=20, pady=(8, 5))

        log_inner = tk.Frame(log_box)
        log_inner.pack(fill="both", expand=True)

        scrollbar = ttk.Scrollbar(log_inner, orient="vertical")
        scrollbar.pack(side="right", fill="y")

        self.txt_log = tk.Text(
            log_inner,
            height=8,
            font=("Consolas", 9),
            wrap="word",
            state="disabled",
            bg="#fdfefe",
            yscrollcommand=scrollbar.set
        )
        self.txt_log.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.txt_log.yview)

        # Colors for each kind of log entry
        self.txt_log.tag_config("on", foreground="#1e8449")
        self.txt_log.tag_config("off", foreground="#c0392b")

        btn_clear = tk.Button(
            self,
            text="Clear Log",
            command=self._clear_log,
            font=("Arial", 9),
            cursor="hand2"
        )
        btn_clear.pack(pady=(0, 10))


    def _handle_turn_on(self):
        self._run_action("turn_on", "on")

    def _handle_turn_off(self):
        self._run_action("turn_off", "off")

    def _run_action(self, method_name: str, tag: str):
        # Get selected device object
        active_object = self.items[self.selected_key.get()]

        # Polymorphic execution: same call, different behavior per class
        result_message = getattr(active_object, method_name)()

        # Display result and record it
        self.lbl_output.config(text=result_message, font=("Arial", 10, "normal"))
        self._log(result_message, tag)

    def _log(self, message: str, tag: str):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.txt_log.config(state="normal")
        self.txt_log.insert("end", f"[{timestamp}] {message}\n", tag)
        self.txt_log.see("end")
        self.txt_log.config(state="disabled")

    def _clear_log(self):
        self.txt_log.config(state="normal")
        self.txt_log.delete("1.0", "end")
        self.txt_log.config(state="disabled")


if __name__ == "__main__":
    app = SmartHomeApp()
    app.mainloop()