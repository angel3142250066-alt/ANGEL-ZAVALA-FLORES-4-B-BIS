import tkinter as tk
from tkinter import ttk
import os
from abc import ABC, abstractmethod


# ==============================
# ABSTRACT BASE CLASS
# ==============================
class SmartDevice(ABC):
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    def turn_on(self) -> str:
        pass


# ==============================
# SMART SPEAKER
# ==============================
class SmartSpeaker(SmartDevice):
    def __init__(self, name):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is playing Lofi music at volume 20%"


# ==============================
# SMART TV
# ==============================
class SmartTv(SmartDevice):
    def __init__(self, name):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON. Enjoy your TV shows!"


# ==============================
# SMART LIGHT
# ==============================
class SmartLight(SmartDevice):
    def __init__(self, name):
        super().__init__(name)

    def turn_on(self) -> str:
        return f"{self.name} is ON. Brighten up your space!"


# ==============================
# GUI APPLICATION
# ==============================
class SmartHomeApp(tk.Tk):
    def __init__(self):
        super().__init__()

        # Window settings
        self.title("Lab 6: Polymorphism with GUI")
        self.geometry("480x360")
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

        # Create radiobuttons
        for key in self.items:
            rb = ttk.Radiobutton(
                group_box,
                text=key,
                value=key,
                variable=self.selected_key
            )
            rb.pack(anchor="w", pady=3)

        # Action Button
        btn_action = tk.Button(
            self,
            text="Turn On Device",
            command=self._handle_action,
            bg="#2980b9",
            fg="white",
            font=("Arial", 15, "bold"),
            relief="raised",
            cursor="hand2",
            padx=12,
            pady=6
        )
        btn_action.pack(pady=15)

        # Output box
        self.lbl_output = tk.Label(
            self,
            text="Select an option above and click 'Turn On Device'.",
            font=("Arial", 10, "italic"),
            bg="#ecf0f1",
            fg="#34495e",
            relief="groove",
            height=3,
            wraplength=420,
            justify="center"
        )
        self.lbl_output.pack(fill="x", padx=20, pady=5)

    def _handle_action(self):
        # Get selected device
        chosen_key = self.selected_key.get()

        # Retrieve the object
        active_object = self.items[chosen_key]

        # Polymorphic execution
        result_message = active_object.turn_on()

        # Display result
        self.lbl_output.config(
            text=result_message,
            font=("Arial", 10, "normal")
        )


# ==============================
# LAUNCHER
# ==============================
if __name__ == "__main__":
    app = SmartHomeApp()
    app.mainloop()
