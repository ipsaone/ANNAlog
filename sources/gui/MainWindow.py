"""
Created by Louis Etienne
Edited by Gregoire Henry
"""

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QAction, QMenuBar, qApp, QFileDialog, QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QColor

from sources.constants import log_levels
from sources.core.LogManager import LogManager
from sources.gui.About import About


class MainWindow(QMainWindow):
    def __init__(self, filename=None, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.filename = filename
        self.log_manager = None

        self.init_ui()

    def init_ui(self):
        loadUi("sources/gui/ui_files/main_window.ui", self)

        self.open_action.triggered.connect(self.on_open_action)
        self.update_action.triggered.connect(self.load_file)
        self.quit_action.triggered.connect(qApp.quit)
        self.about_action.triggered.connect(self.on_about_action)
        self.request_id_entry.editingFinished.connect(self.on_request_id_changed)

        self.level_choice.addItem("All")
        
        for level in log_levels:
            self.level_choice.addItem(level.upper())

        self.level_choice.currentIndexChanged.connect(self.on_level_changed)

        if not self.filename:
            self.statusBar().showMessage("Open a file to beggin")
        else:
            self.load_file()

    def on_open_action(self):
        filename = QFileDialog.getOpenFileName(self, "Open file", "./", "Log files(*.log *.json)")

        if filename[0]:
            self.filename = filename[0]
            self.load_file()

    def load_file(self):
        self.log_manager = LogManager(self.filename)
        self.statusBar().showMessage("{} logs loaded".format(self.log_manager.count()))
        self.update_logs_table()

    def enable(self, state=True):
        self.level_choice.setEnabled(state)
        self.request_id_entry.setEnabled(state)

    def clear_logs_table(self):
        self.logs_table.setRowCount(0)
        self.logs_table.setColumnCount(0)
        self.enable(False)

    def update_logs_table(self, check_filter=False):
        local_log_manager = self.log_manager

        # Using a local log manager avoid to reload the log file each time the user
        # want all the logs.
        
        if check_filter:
            if self.level_choice.currentText() != "All":
                local_log_manager = local_log_manager.filter_level(self.level_choice.currentText().lower())
            
            if len(self.request_id_entry.text()) > 0:
                local_log_manager = local_log_manager.filter_request_id(self.request_id_entry.text())

        self.clear_logs_table()

        self.logs_table.setRowCount(local_log_manager.count())
        self.logs_table.setColumnCount(4)

        self.logs_table.setHorizontalHeaderLabels(["Id", "Date and time", "Level", "Message"])
        self.logs_table.setColumnWidth(1, 175)

        self.logs_table.itemSelectionChanged.connect(self.on_row_selected)
        self.logs_table.setColumnHidden(0, True)

        for i, log in enumerate(local_log_manager.logs.values()):
            color = QColor(255, 255, 255)

            if log.level == log_levels["info"]:
                color = QColor(143, 185, 168)
            elif log.level == log_levels["warning"]:
                color = QColor(252, 208, 186)
            elif log.level == log_levels["error"]:
                color = QColor(241, 130, 141)

            self.logs_table.setItem(i, 0, QTableWidgetItem(log.id))

            self.logs_table.setItem(i, 1, QTableWidgetItem(log.timestamp_str()))
            self.logs_table.item(i, 1).setBackground(color)

            self.logs_table.setItem(i, 2, QTableWidgetItem(log.level_str()))
            self.logs_table.item(i, 2).setBackground(color)

            self.logs_table.setItem(i, 3, QTableWidgetItem(log.message_str()))
            self.logs_table.item(i, 3).setBackground(color)

        self.logs_table.sortItems(1, Qt.DescendingOrder)
        self.enable()

    def on_row_selected(self):
        row_index = self.logs_table.currentRow()
        
        if row_index >= 0:
            log = self.log_manager.logs[self.logs_table.item(row_index, 0).text()]
            self.log_aside.setText(log.render())
        else:
            self.log_aside.setText("")

    def on_level_changed(self):
        self.update_logs_table(True)

    def on_about_action(self):
        about_dialog = About()
        about_dialog.exec_()
