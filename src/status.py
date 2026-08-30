import sys
import sqlite3
from pathlib import Path

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QTableWidgetItem
)

from database import BacDatabase


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

UI_FILE = BASE_DIR / "ui" / "Status.ui"
DATABASE_FILE = BASE_DIR / "bac_planner.db"


# ============================================================
# STATUS WINDOW
# ============================================================

class StatusWindow:

    def __init__(self):

        # ----------------------------------------------------
        # Load UI
        # ----------------------------------------------------

        self.window = loadUi(str(UI_FILE))

        # ----------------------------------------------------
        # Database
        # ----------------------------------------------------

        self.db = BacDatabase(str(DATABASE_FILE))

        # ----------------------------------------------------
        # Window
        # ----------------------------------------------------

        self.window.setWindowTitle(
            "Bac Planner - Status"
        )

        # ----------------------------------------------------
        # Statuses (Updated with "Not yet" and English list)
        # ----------------------------------------------------

        self.statuses = [
            "⚪ Not yet",
            "🔴 Poor",
            "🟡 Average",
            "🟢 Good",
            "⭐ Excellent"
        ]

        # ----------------------------------------------------
        # Load filters
        # ----------------------------------------------------

        self.load_status_filter()
        self.load_subject_filter()

        # ----------------------------------------------------
        # Connections
        # ----------------------------------------------------

        self.window.statusFilter.currentIndexChanged.connect(
            self.filter_changed
        )

        self.window.subjectFilter.currentIndexChanged.connect(
            self.filter_changed
        )

        # ----------------------------------------------------
        # Initial display
        # ----------------------------------------------------

        self.afficher()

    # ========================================================
    # LOAD STATUS FILTER
    # ========================================================

    def load_status_filter(self):

        self.window.statusFilter.clear()

        self.window.statusFilter.addItem(
            "All Statuses"
        )

        self.window.statusFilter.addItems(
            self.statuses
        )

    # ========================================================
    # LOAD SUBJECT FILTER
    # ========================================================

    def load_subject_filter(self):

        self.window.subjectFilter.clear()

        self.window.subjectFilter.addItem(
            "All Subjects"
        )

        subjects = self.db.get_all_subjects()

        for subject_name, coefficient in subjects:

            self.window.subjectFilter.addItem(
                subject_name
            )

    # ========================================================
    # FILTER CHANGED
    # ========================================================

    def filter_changed(self):

        self.afficher()

    # ========================================================
    # DISPLAY
    # ========================================================

    def afficher(self):

        # ----------------------------------------------------
        # Get selected status
        # ----------------------------------------------------

        status_index = (
            self.window.statusFilter.currentIndex()
        )

        if status_index <= 0:
            status = None
        else:
            status = self.window.statusFilter.currentText()

        # ----------------------------------------------------
        # Get selected subject
        # ----------------------------------------------------

        subject_index = (
            self.window.subjectFilter.currentIndex()
        )

        if subject_index <= 0:
            subject = None
        else:
            subject = self.window.subjectFilter.currentText()

        # ----------------------------------------------------
        # Get lessons from database
        # ----------------------------------------------------

        try:

            lessons = self.db.get_lessons_by_status(
                status=status,
                subject=subject
            )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Unable to load status.\n\n{error}"
            )

            return

        # ----------------------------------------------------
        # Clear table
        # ----------------------------------------------------

        self.window.table.setRowCount(0)

        # ----------------------------------------------------
        # Fill table
        # 
        # Database returns:
        # subject_name, lesson_title, status
        #
        # We ignore lesson_title because the UI
        # no longer displays it.
        # ----------------------------------------------------

        for row_number, (
            subject_name,
            lesson,
            lesson_status
        ) in enumerate(lessons):

            self.window.table.insertRow(
                row_number
            )

            # Subject
            self.window.table.setItem(
                row_number,
                0,
                QTableWidgetItem(subject_name)
            )

            # Status
            self.window.table.setItem(
                row_number,
                1,
                QTableWidgetItem(lesson_status)
            )

        # ----------------------------------------------------
        # Resize columns
        # ----------------------------------------------------

        self.window.table.resizeColumnsToContents()

        # Subject
        self.window.table.setColumnWidth(
            0,
            max(
                self.window.table.columnWidth(0),
                300
            )
        )

        # Status
        self.window.table.setColumnWidth(
            1,
            max(
                self.window.table.columnWidth(1),
                300
            )
        )

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        self.window.summary.setText(
            f"Lessons found: {len(lessons)}"
        )

    # ========================================================
    # SHOW
    # ========================================================

    def show(self):

        self.window.show()


# ============================================================
# MAIN
# ============================================================

def main():

    app = QApplication(sys.argv)

    window = StatusWindow()

    window.show()

    sys.exit(app.exec_())


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()