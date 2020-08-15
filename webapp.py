from flask import Flask
from app import create_app
from tkinter import Tk

app = create_app()

if __name__ == "__main__":
    app.run()
