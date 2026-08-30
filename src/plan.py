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
UI_FILE = BASE_DIR / "ui" / "Plan.ui"
DATABASE_FILE = BASE_DIR / "bac_planner.db"


# ============================================================
# MAIN WINDOW
# ============================================================

class PlanWindow:

    def __init__(self):

        # Load Qt Designer UI
        self.window = loadUi(str(UI_FILE))

        # Initialize database
        self.db = BacDatabase(str(DATABASE_FILE))

        # ----------------------------------------------------
        # English interface
        # ----------------------------------------------------

        self.window.setWindowTitle("Bac Planner")

        # Labels
        self.window.label_2.setText("Lesson:")
        self.window.label_3.setText("Status:")

        # Buttons
        self.window.af.setText("Refresh")

        # The Add button is no longer needed
        self.window.aj.hide()

        # ----------------------------------------------------
        # Table headers
        # ----------------------------------------------------

        self.window.t1.setHorizontalHeaderLabels([
            "Lesson",
            "Status"
        ])

        # ----------------------------------------------------
        # Status list
        # ----------------------------------------------------

        self.statuses = [
            "🔴 To Do",
            "🟡 In Progress",
            "🟢 Completed",
            "🔵 Review"
        ]

        self.window.cb2.clear()
        self.window.cb2.addItems(self.statuses)

        # ----------------------------------------------------
        # Load subjects
        # ----------------------------------------------------

        self.charger_matieres()

        # ----------------------------------------------------
        # Connections
        # ----------------------------------------------------

        self.window.af.clicked.connect(self.afficher)

        self.window.cb.currentIndexChanged.connect(
            self.afficher
        )

        # ----------------------------------------------------
        # Initial display
        # ----------------------------------------------------

        self.afficher()

    # ========================================================
    # LOAD SUBJECTS
    # ========================================================

    def charger_matieres(self):

        self.window.cb.clear()

        subjects = self.db.get_all_subjects()

        for subject_name, coefficient in subjects:

            self.window.cb.addItem(
                subject_name,
                coefficient
            )

    # ========================================================
    # DISPLAY LESSONS
    # ========================================================

    def afficher(self):

        subject = self.window.cb.currentText().strip()

        # Clear table
        self.window.t1.setRowCount(0)

        if not subject:
            return

        try:

            lessons = self.db.get_lessons_by_subject(
                subject
            )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Unable to load lessons.\n\n{error}"
            )

            return

        # ----------------------------------------------------
        # Fill table
        # ----------------------------------------------------

        for row_number, (lesson, status) in enumerate(lessons):

            self.window.t1.insertRow(row_number)

            self.window.t1.setItem(
                row_number,
                0,
                QTableWidgetItem(lesson)
            )

            self.window.t1.setItem(
                row_number,
                1,
                QTableWidgetItem(status)
            )

        # Resize columns
        self.window.t1.resizeColumnsToContents()

        # Give lesson column more space
        self.window.t1.setColumnWidth(
            0,
            max(
                self.window.t1.columnWidth(0),
                300
            )
        )

    # ========================================================
    # SHOW WINDOW
    # ========================================================

    def show(self):
        self.window.show()


# ============================================================
# APPLICATION
# ============================================================

def main():

    app = QApplication(sys.argv)

    window = PlanWindow()

    window.show()

    sys.exit(app.exec_())


# ============================================================
# START
# ============================================================

if __name__ == "__main__":
    main()