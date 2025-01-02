import tkinter as tk
from tkinter import filedialog
import csv
import myNotebook as nb
from threading import Timer

class NeutronRouter:
    def __init__(self):
        self.route = []

    def load_route(self, path):
        try:
            with open(path, 'r') as f:
                reader = csv.DictReader(f)
                self.route = [
                    (row['System Name'].strip('"'), row['Neutron Star'].strip('"').lower() == 'yes')
                    for row in reader
                ]
            print(f"NeutronRouter: Loaded {len(self.route)} systems.")
        except Exception as e:
            print(f"NeutronRouter: Failed to load CSV: {e}")

    def copy_next_system(self, current_system):
        try:
            for i, (system_name, _) in enumerate(self.route):
                if system_name == current_system:
                    if i + 1 < len(self.route):  # Check if there's a next system
                        next_system = self.route[i + 1][0]

                        # Use tkinter to handle clipboard operations
                        root = tk.Tk()
                        root.withdraw()  # Hide the main tkinter window
                        root.clipboard_clear()
                        root.clipboard_append(next_system)
                        root.update()  # Ensure clipboard is updated
                        root.destroy()

                        # Display overlay with the system name
                        self.show_overlay(f"Copied to clipboard: {next_system}")
                        print(f"NeutronRouter: Copied next system: {next_system}")
                        return
                    else:
                        print("NeutronRouter: No more systems to copy after the current one.")
                        return
            print(f"NeutronRouter: Current system {current_system} not found in route.")
        except Exception as e:
            print(f"NeutronRouter: Failed to copy next system: {e}")

    @staticmethod
    def show_overlay(message):
        try:
            overlay = tk.Tk()
            overlay.title("System Copied")
            overlay.geometry("300x100+50+50")  # Adjust size and position
            overlay.attributes("-topmost", True)  # Keep on top
            overlay.overrideredirect(True)  # Remove window decorations

            label = tk.Label(overlay, text=message, font=("Helvetica", 14))
            label.pack(expand=True, fill="both", padx=10, pady=10)

            def close_overlay():
                overlay.destroy()

            # Automatically close overlay after 5 seconds
            Timer(5.0, close_overlay).start()

            # Start the Tkinter loop for the overlay
            overlay.mainloop()
        except Exception as e:
            print(f"NeutronRouter: Failed to display overlay: {e}")

class NeutronRouterPlugin:
    router = NeutronRouter()

    @staticmethod
    def start(plugin_dir):
        print("NeutronRouter: Plugin initialized.")
        return "Neutron Router"

    @staticmethod
    def create_prefs(parent, cmdr, is_beta):
        try:
            frame = nb.Frame(parent)
            button = nb.Button(frame, text="Select Route CSV", command=NeutronRouterPlugin.load_route)
            button.grid(row=0, column=0, padx=10, pady=10)
            return frame
        except Exception as e:
            print(f"NeutronRouter: Failed to create preferences tab: {e}")
            return None

    @staticmethod
    def load_route():
        try:
            file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if file_path:
                NeutronRouterPlugin.router.load_route(file_path)
        except Exception as e:
            print(f"NeutronRouter: Error selecting route file: {e}")

    @staticmethod
    def process_journal_entry(cmdr, is_beta, system, station, entry, state):
        try:
            if not NeutronRouterPlugin.router.route:
                return
            
            if entry.get('event') == 'FSDJump':
                current_system = entry.get('StarSystem', '')
                print(f"NeutronRouter: Jumped to system {current_system}. Checking route...")
                NeutronRouterPlugin.router.copy_next_system(current_system)
        except Exception as e:
            print(f"NeutronRouter: Error processing journal entry: {e}")
