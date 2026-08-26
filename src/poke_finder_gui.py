import signal
import sys
import threading
from typing import Any
from typing import Mapping
from typing import MutableMapping
from typing import Optional

import tkinter as tk
from tkinter import ttk


class PokeFinderGUI(tk.Frame):
    default_config: Mapping[str, Any] = {
        "tid": 12345,
        "sid": 54321,
        "shiny_charm": True,
        "oval_charm": True,
        "compatibility_str": "The two seem to get along very well",
        "gender_ratio_str": "88% M / 12% F",
    }

    def __init__(self, master: tk.Tk):
        super().__init__(master)
        self.master = master
        self.previewing_thread: Optional[threading.Thread] = None
        self.previewing: bool = False
        self.config_json: MutableMapping[str, Any] = {}
        self.pack()
        self.create_widgets()
        signal.signal(signal.SIGINT, self.__signal_handler)

    def create_widgets(self) -> None:
        self.master.title("PokeFinderXs")

        # col 0
        ttk.Label(self, text="TID:").grid(column=0, row=0)
        ttk.Label(self, text="SID:").grid(column=0, row=1)
        ttk.Label(self, text="Shiny Charm:").grid(column=0, row=2)
        ttk.Label(self, text="Oval Charm:").grid(column=0, row=3)
        ttk.Label(self, text="Compatibility:").grid(column=0, row=4)
        ttk.Label(self, text="Gender Ratio:").grid(column=0, row=5)
        ttk.Label(self, text="Masuda:").grid(column=0, row=6)

        # col 1
        self.tid_input = ttk.Entry(self)
        self.tid_input.grid(column=1, row=0)
        self.sid_input = ttk.Entry(self)
        self.sid_input.grid(column=1, row=1)
        self.shiny_charm_input = ttk.Combobox(self, values=["No", "Yes"])
        self.shiny_charm_input.grid(column=1, row=2)
        self.oval_charm_input = ttk.Combobox(self, values=["No", "Yes"])
        self.oval_charm_input.grid(column=1, row=3)
        self.compatibility_input = ttk.Combobox(self, values=[
            "The two don't seem to like each other",
            "The two seem to get along",
            "The two seem to get along very well",
        ])
        self.compatibility_input.grid(column=1, row=4)
        self.gender_ratio_input = ttk.Combobox(self, values=[
            "50% M / 50% F",
            "25% M / 75% F",
            "75% M / 25% F",
            "88% M / 12% F",
        ])
        self.gender_ratio_input.grid(column=1, row=5)
        ttk.Label(self, text="Yes").grid(column=1, row=6)

        # col 2
        ttk.Label(self, text="Parent-1").grid(column=2, row=0)
        ttk.Label(self, text="Gender:").grid(column=2, row=1)
        ttk.Label(self, text="Item:").grid(column=2, row=2)
        ttk.Label(self, text="Parent-2:").grid(column=2, row=4)
        ttk.Label(self, text="Gender:").grid(column=2, row=5)
        ttk.Label(self, text="Item:").grid(column=2, row=6)

        # col 3
        ttk.Label(self, text="M / Ditto").grid(column=3, row=1)
        ttk.Label(self, text="None").grid(column=3, row=2)
        ttk.Label(self, text="F / Ditto").grid(column=3, row=5)
        ttk.Label(self, text="None").grid(column=3, row=6)

        # col 4
        ttk.Label(self, text="Camera:").grid(column=4, row=0)
        # TODO display

        # col 5
        self.camera_index = tk.Spinbox(self, from_=0, to=99, width=5)
        self.camera_index.grid(column=5, row=0)

        # col 6
        ttk.Label(self, text="X").grid(column=6, row=0)
        ttk.Label(self, text="Y").grid(column=6, row=1)
        ttk.Label(self, text="W").grid(column=6, row=2)
        ttk.Label(self, text="H").grid(column=6, row=3)
        ttk.Label(self, text="Threshold").grid(column=6, row=4)
        self.preview_button = ttk.Button(self, text="Preview", command=self.preview)
        self.preview_button.grid(column=6, row=5, columnspan=2)
        self.monitor_blinks_button = ttk.Button(self, text="Monitor Blinks", command=self.monitor_blinks)
        self.monitor_blinks_button.grid(column=6, row=6, columnspan=2)

        # col 7
        self.pos_x = tk.Spinbox(self, from_=0, to=99999, width=5)
        self.pos_x.grid(column=7, row=0)
        self.pos_y = tk.Spinbox(self, from_=0, to=99999, width=5)
        self.pos_y.grid(column=7, row=1)
        self.pos_w = tk.Spinbox(self, from_=0, to=99999, width=5)
        self.pos_w.grid(column=7, row=2)
        self.pos_h = tk.Spinbox(self, from_=0, to=99999, width=5)
        self.pos_h.grid(column=7, row=3)
        self.pos_th = tk.Spinbox(self, from_=0, to=1, width=5, increment=0.1)
        self.pos_th.grid(column=7, row=4)

        self.camera_index.delete(0, tk.END)
        self.camera_index.insert(0, "0")
        self.pos_x.delete(0, tk.END)
        self.pos_x.insert(0, "0")
        self.pos_y.delete(0, tk.END)
        self.pos_y.insert(0, "0")
        self.pos_w.delete(0, tk.END)
        self.pos_w.insert(0, "40")
        self.pos_h.delete(0, tk.END)
        self.pos_h.insert(0, "40")
        self.pos_th.delete(0, tk.END)
        self.pos_th.insert(0, "0.9")

        self.after_task()

    def monitor_blinks(self) -> None:
        pass

    def preview(self) -> None:
        if not self.previewing:
            self.preview_button["text"] = "Stop Preview"
            self.previewing = True
            self.previewing_thread = threading.Thread(target=self.previewing_work)
            self.previewing_thread.daemon = True
            self.previewing_thread.start()
        else:
            self.preview_button["text"] = "Preview"
            self.previewing = False

    def previewing_work(self) -> None:
        pass

    def after_task(self) -> None:
        self.config_json["camera"] = int(self.camera_index.get())
        self.config_json["view"] = [
            int(self.pos_x.get()),
            int(self.pos_y.get()),
            int(self.pos_w.get()),
            int(self.pos_h.get()),
        ]
        self.config_json["thresh"] = float(self.pos_th.get())
        self.after(100, self.after_task)

    @staticmethod
    def __signal_handler(*_: Any) -> None:
        sys.exit(0)


if __name__ == "__main__":
    root: tk.Tk = tk.Tk()
    app: PokeFinderGUI = PokeFinderGUI(master=root)
    app.mainloop()
