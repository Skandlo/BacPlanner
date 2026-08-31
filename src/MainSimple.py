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

        self.window.setWindowTitle("Bac Planner")

        # ----------------------------------------------------
        # Labels
        # ----------------------------------------------------

        self.window.label_2.setText("Lesson:")
        self.window.label_3.setText("Status:")

        # ----------------------------------------------------
        # Buttons
        # ----------------------------------------------------

        self.window.af.setText("Refresh")

        # Update Status button
        self.window.updateStatusButton.setText(
            "Update Status"
        )

        # ----------------------------------------------------
        # Remove AI button if it exists
        # ----------------------------------------------------

        if hasattr(self.window, "aj"):
            self.window.aj.hide()

        if hasattr(self.window, "aiButton"):
            self.window.aiButton.hide()

        # ----------------------------------------------------
        # Table
        # ----------------------------------------------------

        self.window.t1.setColumnCount(2)

        self.window.t1.setHorizontalHeaderLabels([
            "Lesson",
            "Status"
        ])

        # ----------------------------------------------------
        # Status list
        # ----------------------------------------------------

        self.statuses = [
            "⚪ Not yet",
            "🔴 Poor",
            "🟡 Average",
            "🟢 Good",
            "⭐ Excellent"
        ]

        self.window.cb2.clear()

        self.window.cb2.addItems(
            self.statuses
        )

        # ----------------------------------------------------
        # Load subjects
        # ----------------------------------------------------

        self.charger_matieres()

        # ----------------------------------------------------
        # Connections
        # ----------------------------------------------------

        self.window.af.clicked.connect(
            self.afficher
        )

        self.window.cb.currentIndexChanged.connect(
            self.subject_changed
        )

        self.window.cr.currentIndexChanged.connect(
            self.cours_selectionne
        )

        self.window.updateStatusButton.clicked.connect(
            self.update_status
        )

        # ----------------------------------------------------
        # Initial display
        # ----------------------------------------------------

        self.charger_cours()
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
    # LOAD LESSONS
    # ========================================================

    def charger_cours(self):

        subject = self.window.cb.currentText().strip()

        self.window.cr.blockSignals(True)
        self.window.cr.clear()

        if not subject:

            self.window.cr.blockSignals(False)

            return

        try:

            lessons = self.db.get_lessons_by_subject(
                subject
            )

            for lesson, status in lessons:

                self.window.cr.addItem(
                    lesson,
                    status
                )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Unable to load lessons.\n\n{error}"
            )

        self.window.cr.blockSignals(False)

        self.cours_selectionne()

    # ========================================================
    # SUBJECT CHANGED
    # ========================================================

    def subject_changed(self):

        self.charger_cours()

        self.afficher()

    # ========================================================
    # LESSON SELECTED
    # ========================================================

    def cours_selectionne(self):

        index = self.window.cr.currentIndex()

        if index < 0:
            return

        status = self.window.cr.itemData(index)

        if not status:
            status = "⚪ Not yet"

        status_index = self.window.cb2.findText(
            status
        )

        if status_index >= 0:

            self.window.cb2.blockSignals(True)

            self.window.cb2.setCurrentIndex(
                status_index
            )

            self.window.cb2.blockSignals(False)

    # ========================================================
    # UPDATE STATUS
    # ========================================================

    def update_status(self):

        subject = self.window.cb.currentText().strip()

        lesson = self.window.cr.currentText().strip()

        status = self.window.cb2.currentText()

        # ----------------------------------------------------
        # Validate subject
        # ----------------------------------------------------

        if not subject:

            QMessageBox.warning(
                self.window,
                "Missing Subject",
                "Please select a subject."
            )

            return

        # ----------------------------------------------------
        # Validate lesson
        # ----------------------------------------------------

        if not lesson:

            QMessageBox.warning(
                self.window,
                "Missing Lesson",
                "Please select a lesson."
            )

            return

        # ----------------------------------------------------
        # Update database
        # ----------------------------------------------------

        try:

            self.db.update_lesson_status(
                subject,
                lesson,
                status
            )

        except sqlite3.Error as error:

            QMessageBox.critical(
                self.window,
                "Database Error",
                f"Unable to update status.\n\n{error}"
            )

            return

        # ----------------------------------------------------
        # Update lesson combo data
        # ----------------------------------------------------

        index = self.window.cr.currentIndex()

        if index >= 0:

            self.window.cr.setItemData(
                index,
                status
            )

        # ----------------------------------------------------
        # Refresh table
        # ----------------------------------------------------

        self.afficher()

        # ----------------------------------------------------
        # Confirmation
        # ----------------------------------------------------

        QMessageBox.information(
            self.window,
            "Status Updated",
            f"Status updated successfully!\n\n"
            f"Lesson: {lesson}\n"
            f"Status: {status}"
        )

    # ========================================================
    # DISPLAY LESSONS
    # ========================================================

    def afficher(self):

        subject = self.window.cb.currentText().strip()

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

        for row_number, (lesson, status) in enumerate(
            lessons
        ):

            self.window.t1.insertRow(
                row_number
            )

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

        # ----------------------------------------------------
        # Resize columns
        # ----------------------------------------------------

        self.window.t1.resizeColumnsToContents()

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