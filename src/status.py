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
        # Statuses
        # ----------------------------------------------------

        self.statuses = [
            "⚪ Not yet",
            "🔴 Poor",
            "🟡 Average",
            "🟢 Good",
            "⭐ Excellent"
        ]

        # ----------------------------------------------------
        # Configure table
        # ----------------------------------------------------

        self.configure_table()

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
    # CONFIGURE TABLE
    # ========================================================

    def configure_table(self):
        """
        Configures the table to display:

        Subject | Course | Status
        """

        self.window.table.setColumnCount(3)

        self.window.table.setHorizontalHeaderLabels([
            "Subject",
            "Course",
            "Status"
        ])

        # Prevent editing directly inside the table
        self.window.table.setEditTriggers(
            self.window.table.NoEditTriggers
        )

        # Select complete rows
        self.window.table.setSelectionBehavior(
            self.window.table.SelectRows
        )

        # Hide vertical row numbers
        self.window.table.verticalHeader().setVisible(False)

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

        try:

            subjects = self.db.get_all_subjects()

            for subject_name, coefficient in subjects:

                self.window.subjectFilter.addItem(
                    subject_name
                )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Unable to load subjects.\n\n{error}"
            )

    # ========================================================
    # FILTER CHANGED
    # ========================================================

    def filter_changed(self):

        self.afficher()

    # ========================================================
    # GET SELECTED STATUS
    # ========================================================

    def get_selected_status(self):
        """
        Returns the selected status.

        None means all statuses.
        """

        index = self.window.statusFilter.currentIndex()

        if index <= 0:
            return None

        return self.window.statusFilter.currentText()

    # ========================================================
    # GET SELECTED SUBJECT
    # ========================================================

    def get_selected_subject(self):
        """
        Returns the selected subject.

        None means all subjects.
        """

        index = self.window.subjectFilter.currentIndex()

        if index <= 0:
            return None

        return self.window.subjectFilter.currentText()

    # ========================================================
    # DISPLAY
    # ========================================================

    def afficher(self):

        # ----------------------------------------------------
        # Get filters
        # ----------------------------------------------------

        status = self.get_selected_status()
        subject = self.get_selected_subject()

        # ----------------------------------------------------
        # Get filtered courses
        # ----------------------------------------------------

        try:

            courses = self.db.get_lessons_by_status(
                status=status,
                subject=subject
            )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Unable to load courses.\n\n{error}"
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
        #
        # subject_name
        # lesson_title
        # status
        #
        # We display all three.
        # ----------------------------------------------------

        for row_number, (
            subject_name,
            lesson_title,
            lesson_status
        ) in enumerate(courses):

            self.window.table.insertRow(
                row_number
            )

            # ------------------------------------------------
            # Subject
            # ------------------------------------------------

            self.window.table.setItem(
                row_number,
                0,
                QTableWidgetItem(
                    subject_name
                )
            )

            # ------------------------------------------------
            # Course
            # ------------------------------------------------

            self.window.table.setItem(
                row_number,
                1,
                QTableWidgetItem(
                    lesson_title
                )
            )

            # ------------------------------------------------
            # Status
            # ------------------------------------------------

            self.window.table.setItem(
                row_number,
                2,
                QTableWidgetItem(
                    lesson_status
                )
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
                200
            )
        )

        # Course
        self.window.table.setColumnWidth(
            1,
            max(
                self.window.table.columnWidth(1),
                550
            )
        )

        # Status
        self.window.table.setColumnWidth(
            2,
            max(
                self.window.table.columnWidth(2),
                180
            )
        )

        # ----------------------------------------------------
        # Summary
        # ----------------------------------------------------

        self.window.summary.setText(
            f"Courses found: {len(courses)}"
        )

    # ========================================================
    # SHOW WINDOW
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