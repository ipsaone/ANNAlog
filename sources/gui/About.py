"""
Created by Louis Etienne
"""

from PyQt5.QtWidgets import QDialog, QLabel
from PyQt5.uic import loadUi


class About(QDialog):
    def __init__(self, *args, **kwargs):
        super(About, self).__init__(*args, **kwargs)
        self.init_ui()

    def init_ui(self):
        loadUi("sources/gui/ui_files/about.ui", self)