import customtkinter as ctk
import os
import subprocess
import update
from PIL import Image
from tkinter import filedialog, messagebox
import configparser

class LegendsLauncher(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color="white")
        self.title("Legends Launcher")
        self.geometry("800x600")
        self.resizable(False, False)

        self.config_path = os.path.join(os.getcwd(), "config.ini")
        self.brawl_iso_path = self.check_brawl_iso()

        # Add logo
        logo_path = os.path.join(os.getcwd(), "legends_logo.png")
        if os.path.exists(logo_path):
            logo_img = ctk.CTkImage(light_image=Image.open(logo_path), size=(256, 128))
            logo_label = ctk.CTkLabel(self, image=logo_img, text="", fg_color="transparent")
            logo_label.pack(pady=20)
        else:
            logo_label = ctk.CTkLabel(self, text="Logo not found")
            logo_label.pack(pady=20)

        # Launch Dolphin button
        self.launch_btn = ctk.CTkButton(self, text="Launch Legends", command=self.launch_dolphin, fg_color="black", width=300, height=50)
        self.launch_btn.pack(pady=10)

        # Update Dolphin button
        self.update_btn = ctk.CTkButton(self, text="Update Legends", command=self.update_dolphin, fg_color="black", width=300, height=50)
        self.update_btn.pack(pady=10)

        # Settings button
        self.settings_btn = ctk.CTkButton(self, text="Settings", command=self.open_settings, fg_color="black", width=300, height=50)
        self.settings_btn.pack(pady=10)

    def check_brawl_iso(self):
        config = configparser.ConfigParser()
        if os.path.exists(self.config_path):
            config.read(self.config_path)
            if "BRAWL" in config and "iso_path" in config["BRAWL"]:
                iso_path = config["BRAWL"]["iso_path"]
                if os.path.exists(iso_path):
                    return iso_path

        # Show popup before file dialog
        messagebox.showinfo("Select Brawl ISO", "Please select your Brawl ISO file to continue.")

        iso_path = filedialog.askopenfilename(
            title="Select your Brawl ISO",
            filetypes=[("ISO files", "*.iso")]
        )
        if not iso_path:
            messagebox.showerror("Error", "Brawl ISO is required to continue.")
            self.destroy()
            exit()

        config["BRAWL"] = {"iso_path": iso_path}
        with open(self.config_path, "w") as configfile:
            config.write(configfile)
        return iso_path

    def launch_dolphin(self):
        # Assume Dolphin.exe is in the same folder for now
        dolphin_path = os.path.join(os.getcwd(), "Dolphin.exe")
        if os.path.exists(dolphin_path):
            subprocess.Popen([dolphin_path])
        else:
            ctk.CTkMessagebox(title="Error", message="Dolphin.exe not found!")

    def update_dolphin(self):
        # Run update and show result
        try:
            update.download_latest_dolphin(os.getcwd())
            ctk.CTkMessagebox(title="Update", message="Legends updated successfully!")
        except Exception as e:
            ctk.CTkMessagebox(title="Update Failed", message=f"Update failed: {e}")

    def open_settings(self):
        from settings import BUILD_TYPE, SETTINGS
        # Make sure the settings window pops up in front
        settings_window = ctk.CTkToplevel(self)
        settings_window.title("Settings")
        settings_window.geometry("600x400")
        settings_window.configure(fg_color="white")
        settings_window.lift()  # Bring window to front
        settings_window.focus_force()  # Focus the window
        settings_window.grab_set()  # Make it modal

        # Build type selector
        ctk.CTkLabel(settings_window, text="Build Type:", text_color="black", bg_color="white").pack(pady=5)
        build_var = ctk.StringVar(value=BUILD_TYPE)
        build_menu = ctk.CTkOptionMenu(settings_window, variable=build_var, values=list(SETTINGS.keys()), fg_color="black", text_color="white")
        build_menu.pack(pady=5)

        # DOLPHIN_RELEASE_API field
        ctk.CTkLabel(settings_window, text="Dolphin Release API URL:", text_color="black", bg_color="white").pack(pady=5)
        api_var = ctk.StringVar(value=SETTINGS[BUILD_TYPE]["DOLPHIN_RELEASE_API"])
        api_entry = ctk.CTkEntry(settings_window, textvariable=api_var, width=400, fg_color="white", text_color="black")
        api_entry.pack(pady=5)

        def save_settings():
            selected_build = build_var.get()
            SETTINGS[selected_build]["DOLPHIN_RELEASE_API"] = api_var.get()
            ctk.CTkMessagebox(title="Settings", message="Settings updated! Restart app to apply build type.")

        save_btn = ctk.CTkButton(settings_window, text="Save", command=save_settings, fg_color="black", text_color="white")
        save_btn.pack(pady=20)

if __name__ == "__main__":
    app = LegendsLauncher()
    app.mainloop()