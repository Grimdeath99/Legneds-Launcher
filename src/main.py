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
        self.check_for_auto_update()

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
        import customtkinter as ctk
        config = configparser.ConfigParser()
        # First time build type selection
        if not os.path.exists(self.config_path):
            build_type = self.select_build_type()
            from settings import SETTINGS
            config["BUILD"] = {"type": build_type}
            with open(self.config_path, "w") as configfile:
                config.write(configfile)
            # Auto download after build type selection
            if build_type == "main":
                update.download_latest_dolphin(os.getcwd())
            else:
                update.download_latest_alpha(os.getcwd())
        else:
            config.read(self.config_path)
            if "BRAWL" in config and "iso_path" in config["BRAWL"]:
                iso_path = config["BRAWL"]["iso_path"]
                if os.path.exists(iso_path):
                    return iso_path

        # Use CTk for popup and file dialog
        popup = ctk.CTkToplevel(self)
        popup.title("Select Brawl ISO")
        popup.geometry("400x180")
        popup.configure(fg_color="white")
        popup.lift()
        popup.grab_set()
        ctk.CTkLabel(popup, text="Please select your Brawl ISO file to continue.", text_color="black", fg_color="white", wraplength=350).pack(pady=20)
        iso_var = ctk.StringVar()

        def select_iso():
            iso_path = filedialog.askopenfilename(
                title="Select your Brawl ISO",
                filetypes=[("ISO files", "*.iso")]
            )
            if iso_path:
                iso_var.set(iso_path)

        def confirm():
            iso_path = iso_var.get()
            if not iso_path or not os.path.exists(iso_path):
                ctk.CTkMessagebox(title="Error", message="Brawl ISO is required to continue.")
                return
            config["BRAWL"] = {"iso_path": iso_path}
            with open(self.config_path, "w") as configfile:
                config.write(configfile)
            popup.destroy()
            self.brawl_iso_path = iso_path

        select_btn = ctk.CTkButton(popup, text="Browse", command=select_iso, fg_color="black", text_color="white")
        select_btn.pack(pady=5)
        entry = ctk.CTkEntry(popup, textvariable=iso_var, width=320, fg_color="white", text_color="black")
        entry.pack(pady=5)
        confirm_btn = ctk.CTkButton(popup, text="OK", command=confirm, fg_color="black", text_color="white")
        confirm_btn.pack(pady=15)
        popup.wait_window()
        return getattr(self, 'brawl_iso_path', None)

    def select_build_type(self):
        import customtkinter as ctk
        build_type = None
        popup = ctk.CTkToplevel(self)
        popup.title("Choose Build Type")
        popup.geometry("400x200")
        popup.configure(fg_color="white")
        popup.lift()
        popup.grab_set()
        ctk.CTkLabel(popup, text="Select your preferred build type for Legends Launcher:", text_color="black", fg_color="white", wraplength=350).pack(pady=20)
        var = ctk.StringVar(value="main")
        def choose_and_close():
            nonlocal build_type
            build_type = var.get()
            popup.destroy()
        ctk.CTkRadioButton(popup, text="Main (Stable)", variable=var, value="main", fg_color="black", text_color="black").pack(pady=5)
        ctk.CTkRadioButton(popup, text="Alpha (Master branch)", variable=var, value="alpha", fg_color="black", text_color="black").pack(pady=5)
        ctk.CTkButton(popup, text="Continue", command=choose_and_close, fg_color="black", text_color="white").pack(pady=20)
        popup.wait_window()
        return build_type

    def launch_dolphin(self):
        # Assume Dolphin.exe is in the same folder for now
        dolphin_path = os.path.join(os.getcwd(), "Dolphin.exe")
        if os.path.exists(dolphin_path):
            subprocess.Popen([dolphin_path])
        else:
            ctk.CTkMessagebox(title="Error", message="Dolphin.exe not found!")

    def show_progress_bar(self, title="Downloading", message="Please wait..."):
        progress_popup = ctk.CTkToplevel(self)
        progress_popup.title(title)
        progress_popup.geometry("400x120")
        progress_popup.configure(fg_color="white")
        progress_popup.lift()
        progress_popup.grab_set()
        ctk.CTkLabel(progress_popup, text=message, text_color="black", fg_color="white").pack(pady=10)
        progress = ctk.CTkProgressBar(progress_popup, width=320, height=20, fg_color="white", progress_color="black")
        progress.pack(pady=10)
        progress.set(0)
        progress_popup.update()
        return progress_popup, progress

    def update_dolphin(self):
        # Run update and show result
        try:
            from settings import BUILD_TYPE
            import threading
            import sys
            def do_update():
                progress_popup, progress = self.show_progress_bar(title="Updating Legends", message="Downloading update...")
                def progress_callback(percent):
                    progress.set(percent)
                    progress_popup.update()
                if BUILD_TYPE == "main":
                    update.download_latest_dolphin(os.getcwd(), progress_callback=progress_callback)
                else:
                    update.download_latest_alpha(os.getcwd(), progress_callback=progress_callback)
                progress_popup.destroy()
                ctk.CTkMessagebox(title="Update", message="Legends updated! The launcher will now restart.")
                self.restart_launcher()
            threading.Thread(target=do_update).start()
        except Exception as e:
            ctk.CTkMessagebox(title="Update Failed", message=f"Update failed: {e}")

    def restart_launcher(self):
        import sys
        import subprocess
        python = sys.executable
        os.execl(python, python, *sys.argv)

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

        # Update source field
        ctk.CTkLabel(settings_window, text="Update Source:", text_color="black", bg_color="white").pack(pady=5)
        update_var = ctk.StringVar(value=SETTINGS[BUILD_TYPE]["UPDATE_SOURCE"])
        update_entry = ctk.CTkEntry(settings_window, textvariable=update_var, width=400, fg_color="white", text_color="black")
        update_entry.pack(pady=5)

        # Update mode selector
        ctk.CTkLabel(settings_window, text="Update Mode (auto/manual):", text_color="black", bg_color="white").pack(pady=5)
        update_mode_var = ctk.StringVar(value=SETTINGS[BUILD_TYPE].get("UPDATE_MODE", "auto"))
        update_mode_menu = ctk.CTkOptionMenu(settings_window, variable=update_mode_var, values=["auto", "manual"], fg_color="black", text_color="white")
        update_mode_menu.pack(pady=5)

        def save_settings():
            selected_build = build_var.get()
            SETTINGS[selected_build]["DOLPHIN_RELEASE_API"] = api_var.get()
            SETTINGS[selected_build]["UPDATE_SOURCE"] = update_var.get()
            SETTINGS[selected_build]["UPDATE_MODE"] = update_mode_var.get()
            ctk.CTkMessagebox(title="Settings", message="Settings updated! Restart app to apply build type.")

        save_btn = ctk.CTkButton(settings_window, text="Save", command=save_settings, fg_color="black", text_color="white")
        save_btn.pack(pady=20)

    def check_for_auto_update(self):
        import threading
        from settings import BUILD_TYPE, get_setting
        def do_auto_update():
            # Only check for update if UPDATE_MODE is 'auto'
            try:
                update_mode = get_setting("UPDATE_MODE")
            except Exception:
                update_mode = "auto"
            if update_mode != "auto":
                return
            current_version = self.get_current_version()
            latest = update.check_for_github_update(current_version)
            if latest:
                def on_choice(choice):
                    if choice == "Update Now":
                        self.update_dolphin()
                popup = ctk.CTkToplevel(self)
                popup.title("Update Available")
                popup.geometry("400x180")
                popup.configure(fg_color="white")
                popup.lift()
                popup.grab_set()
                ctk.CTkLabel(popup, text=f"A new update is available!\nCurrent: {current_version}\nLatest: {latest}", text_color="black", fg_color="white").pack(pady=20)
                def update_now():
                    popup.destroy()
                    on_choice("Update Now")
                def skip():
                    popup.destroy()
                ctk.CTkButton(popup, text="Update Now", command=update_now, fg_color="black", text_color="white").pack(pady=5)
                ctk.CTkButton(popup, text="Skip", command=skip, fg_color="black", text_color="white").pack(pady=5)
        threading.Thread(target=do_auto_update).start()

    def get_current_version(self):
        # Try to get version from settings or a VERSION file
        try:
            from settings import get_setting
            return get_setting("VERSION")
        except Exception:
            version_path = os.path.join(os.getcwd(), "VERSION")
            if os.path.exists(version_path):
                with open(version_path) as f:
                    return f.read().strip()
            return "Unknown"

if __name__ == "__main__":
    app = LegendsLauncher()
    app.mainloop()