"""
Created by Louis Etienne
"""

import sys
from PyQt5.QtWidgets import QApplication

from sources.gui.MainWindow import MainWindow


app = QApplication(sys.argv)

main = MainWindow()
main.show()

app.exec_()
