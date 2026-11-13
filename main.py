import os
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox
import src.scrapper as sc


class AppLauncher:

    def __init__(self, root):
        self.root = root
        self.root.title("Launcher analizatora")
        self.root.geometry("360x260")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.api_key = os.getenv("STEAM_API_KEY")

        self.visualizer_process = None

        title_label = tk.Label(
            root, text="Sterowanie", font=("Arial", 14, "bold")
        )
        title_label.pack(pady=15)

        # przycisk Scrapper
        self.btn_scraper = tk.Button(
            root,
            text="Uruchom Scrapper",
            command=self.run_scraper,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            width=24,
            height=2,
        )
        self.btn_scraper.pack(pady=5)

        # visualizer Włącz / Wyłącz
        self.btn_visualizer = tk.Button(
            root,
            text="Włącz Visualizer",
            command=self.toggle_visualizer,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            width=24,
            height=2,
        )
        self.btn_visualizer.pack(pady=5)


        self.status_label = tk.Label(
            root, text="Status: Gotowy", font=("Arial", 9), fg="gray"
        )
        self.status_label.pack(side=tk.BOTTOM, pady=10)


        if not self.api_key:
            self.status_label.config(
                text="brak zmiennej STEAM_API_KEY", fg="#e67e22"
            )

    def run_scraper(self):
        if not self.api_key:
            messagebox.showerror(
                "Błąd",
                "brak zmiennej STEAM_API_KEY"
            )
            return

        def target():
            try:
                self.status_label.config(
                    text="Status: Scrapper pobiera dane...", fg="#d35400"
                )
                self.btn_scraper.config(state=tk.DISABLED)

                sc.start(self.api_key)

                messagebox.showinfo(
                    "Sukces", "Scrapper zakończył pomyślnie działanie!"
                )
                self.status_label.config(
                    text="Status: Scrapper zakończył pracę", fg="#27ae60"
                )
            except Exception as e:
                messagebox.showerror(
                    "Błąd Scrappera", f"Wystąpił błąd podczas działania:\n{e}"
                )
                self.status_label.config(text="Status: Błąd scrappera", fg="#c0392b")
            finally:
                self.btn_scraper.config(state=tk.NORMAL)

        threading.Thread(target=target, daemon=True).start()

    def toggle_visualizer(self):

        if (
                self.visualizer_process is None
                or self.visualizer_process.poll() is not None
        ):
            try:
                self.status_label.config(
                    text="Status: Uruchamianie visualizera...", fg="#2980b9"
                )

                script_path = os.path.join("src", "visualizer.py")

                self.visualizer_process = subprocess.Popen(
                    ["streamlit", "run", script_path]
                )

                self.btn_visualizer.config(text="Wyłącz Visualizer", bg="#e74c3c")
                self.status_label.config(
                    text="Status: Visualizer działa w tle", fg="#27ae60"
                )
            except Exception as e:
                messagebox.showerror(
                    "Błąd", f"Nie udało się uruchomić visualizera:\n{e}"
                )
                self.status_label.config(text="Status: Błąd visualizera", fg="#c0392b")
        else:

            try:
                self.visualizer_process.terminate()
                self.visualizer_process = None
                self.btn_visualizer.config(text="Włącz Visualizer", bg="#2ecc71")
                self.status_label.config(
                    text="Status: Visualizer wyłączony", fg="gray"
                )
            except Exception as e:
                messagebox.showerror("Błąd", f"Nie udało się wyłączyć visualizera:\n{e}")

    def on_close(self):
        if self.visualizer_process and self.visualizer_process.poll() is None:
            self.visualizer_process.terminate()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AppLauncher(root)
    root.mainloop()