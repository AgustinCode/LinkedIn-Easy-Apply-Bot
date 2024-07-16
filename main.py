# -*- coding: utf-8 -*-

import tkinter as tk
from classes.gui import LinkedInBotApp

def main():
    root = tk.Tk()
    app = LinkedInBotApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()