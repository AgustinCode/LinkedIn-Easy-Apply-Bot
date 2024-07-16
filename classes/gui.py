import tkinter as tk
from tkinter import ttk, messagebox
from classes.LDscrapper import LinkedinDriver

class LinkedInBotApp:
    """
    A class to create a GUI application for LinkedIn Easy Apply Bot.
    """

    def __init__(self, root):
        """
        Initialize the LinkedInBotApp.

        Args:
            root (tk.Tk): The root window for the application.
        """
        self.root = root
        self.root.title("LinkedIn Easy Apply Bot")
        self.root.geometry('720x400')
        self.create_widgets()
        self.ldriver = None

    def create_widgets(self):
        """
        Create and arrange all widgets for the application GUI.
        """
        # Email
        tk.Label(self.root, text="Email:").grid(row=0, column=0, sticky="e")
        self.email_entry = tk.Entry(self.root)
        self.email_entry.grid(row=0, column=1, columnspan=2, sticky="we")

        # Password
        tk.Label(self.root, text="Password:").grid(row=1, column=0, sticky="e")
        self.password_entry = tk.Entry(self.root, show="*")
        self.password_entry.grid(row=1, column=1, columnspan=2, sticky="we")

        # Pages to scrape
        tk.Label(self.root, text="Pages to Scrape:").grid(row=2, column=0, sticky="e")
        self.pages_entry = tk.Entry(self.root)
        self.pages_entry.grid(row=2, column=1, columnspan=2, sticky="we")

        # Buttons
        run_button = tk.Button(self.root, text="Run Bot", command=self.run_bot)
        run_button.grid(row=3, column=1, sticky="we")

        apply_button = tk.Button(self.root, text="Apply", command=self.apply_jobs)
        apply_button.grid(row=3, column=0, sticky="we")

        button3 = tk.Button(self.root, text="Button 3")
        button3.grid(row=3, column=2, sticky="we")

        # Job listbox with scrollbar
        self.job_listbox = tk.Listbox(self.root, selectmode="multiple")
        self.job_listbox.grid(row=4, column=0, columnspan=3, sticky="nsew")

        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.job_listbox.yview)
        scrollbar.grid(row=4, column=3, sticky="ns")
        self.job_listbox.config(yscrollcommand=scrollbar.set)

        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def apply_jobs(self):
        """
        Handle the job application process for selected jobs.
        """
        if not self.ldriver:
            messagebox.showerror(message="Please run the bot first to collect jobs.", title="Error")
            return

        selected_indices = self.job_listbox.curselection()
        self.ldriver.listed_jobs = [self.ldriver.job_titles[i] for i in selected_indices]
        print("Selected jobs for application:")
        for job in self.ldriver.listed_jobs:
            print(job)
        messagebox.showinfo(message="Jobs selected for application.", title="Success")

    def run_bot(self):
        """
        Execute the LinkedIn bot to collect job listings.
        """
        email = self.email_entry.get()
        password = self.password_entry.get()
        pages = int(self.pages_entry.get())

        self.ldriver = LinkedinDriver(email, password)
        try:
            messagebox.showinfo(message="Collecting data.. Complete security checks", title="Process running.")
            self.ldriver.login()
            self.ldriver.search_easy_apply_jobs()
            self.ldriver.collect_jobs(pages=pages)
            
            self.job_listbox.delete(0, tk.END)  # Clear previous results
            for i, title in enumerate(self.ldriver.job_titles):
                self.job_listbox.insert(tk.END, f"Job {i+1}: {title}")
            messagebox.showinfo(message="Data collected. Select the jobs you want to apply", title="Success")
        except Exception as e:
            print(f"ERROR: {e}")
            messagebox.showerror(message=f"An error occurred: {e}", title="Error")
        finally:
            if self.ldriver:
                self.ldriver.close()