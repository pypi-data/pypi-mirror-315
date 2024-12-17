from customtkinter import CTkToplevel, CTkButton, CTkLabel
from os import path
from winsound import MessageBeep, MB_ICONHAND, MB_OK
from pathlib import Path

class MessageContainer(object):
    def showError(title, message, **kwargs):
        MessageBeep(MB_ICONHAND)
        container = CTkToplevel()
        container.title(title)
        container.geometry("330x95")
        container.resizable(False, False)

        iconPath = Path(__file__).parent / "MessageBoxIcons/ErrorIcon.ico"
        container.after(250, lambda: container.iconbitmap(iconPath))
        container.attributes('-topmost', 'true')

        containerTitle = CTkLabel(container, text=message)
        containerTitle.place(relx=0.5, rely=0.28, anchor="center")

        containerButton = CTkButton(container, text="Weiter", cursor="hand2", command=lambda: container.destroy())
        containerButton.place(relx=0.5, rely=0.75, anchor="center")
        


    def showInfo(title, message, **kwargs):
        MessageBeep(MB_OK)
        container = CTkToplevel()
        container.title(title)
        container.geometry("330x95")
        container.resizable(False, False)

        iconPath = Path(__file__).parent / "MessageBoxIcons/InfoIcon.ico"
        container.after(250, lambda: container.iconbitmap(iconPath))
        container.attributes('-topmost', 'true')

        containerTitle = CTkLabel(container, text=message)
        containerTitle.place(relx=0.5, rely=0.28, anchor="center")

        containerButton = CTkButton(container, text="Weiter", cursor="hand2", command=lambda: container.destroy())
        containerButton.place(relx=0.5, rely=0.75, anchor="center")