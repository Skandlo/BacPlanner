import sys
import sqlite3
from pathlib import Path
from ai_assistant import BacAIAssistant

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QTableWidgetItem,
    QDialog,
    QVBoxLayout,
    QTextBrowser,
    QLineEdit,
    QPushButton
)

from database import BacDatabase


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
UI_FILE = BASE_DIR / "ui" / "Plan.ui"
DATABASE_FILE = BASE_DIR / "bac_planner.db"


# ============================================================
# AI CHAT DIALOG
# ============================================================

class AIChatDialog(QDialog):
    """
    Interactive chat dialog window allowing the user to converse 
    with the Gemini AI assistant using a clean, formatted HTML view.
    """

    def __init__(self, ai_assistant, subject, lesson, status, parent=None):
        super().__init__(parent)
        self.ai_assistant = ai_assistant
        self.subject = subject
        self.lesson = lesson
        self.status = status
        
        # Window configuration
        self.setWindowTitle(f"Bac Chat Assistant - {subject} 🤖")
        self.resize(650, 550)
        
        layout = QVBoxLayout(self)
        
        # Use QTextBrowser instead of QTextEdit for proper HTML/CSS rendering
        self.chat_history = QTextBrowser()
        self.chat_history.setOpenExternalLinks(True)
        # Apply clean CSS styling for readability, comfortable font size, and spacing
        self.chat_history.setStyleSheet("""
            QTextBrowser {
                background-color: #f8f9fa;
                color: #212529;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                font-size: 14px;
                line-height: 1.5;
                padding: 10px;
                border: 1px solid #ced4da;
                border-radius: 6px;
            }
        """)
        layout.addWidget(self.chat_history)
        
        # User input field for messaging
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Type your question here...")
        self.input_field.setStyleSheet("font-size: 14px; padding: 6px;")
        self.input_field.returnPressed.connect(self.send_msg)
        layout.addWidget(self.input_field)
        
        # Send message button
        self.send_btn = QPushButton("Send")
        self.send_btn.setStyleSheet("font-size: 14px; font-weight: bold; padding: 6px;")
        self.send_btn.clicked.connect(self.send_msg)
        layout.addWidget(self.send_btn)
        
        # Internal conversation HTML storage
        self.conversation_html = ""

        # Send a context-aware initial prompt including lesson and progress status
        initial_prompt = (
            f"I am preparing for the Tunisian Bac exam. "
            f"My current subject is {subject}. "
            f"I am looking at the lesson '{self.lesson}' and my current status/level is '{self.status}'. "
            f"Give me a strict diagnostic, analyze my current progress state for this specific lesson based on this level, "
            f"and provide a direct action plan to master it."
        )
        
        welcome_msg = self.ai_assistant.send_message(initial_prompt)
        self.append_message("AI", welcome_msg)

    def append_message(self, sender, text):
        """Appends formatted HTML messages to the conversation display."""
        formatted_text = text.replace("\n", "<br>")
        
        if sender == "You":
            self.conversation_html += f"""
                <div style='margin-bottom: 12px;'>
                    <b style='color: #0d6efd;'>You:</b> 
                    <span style='color: #333;'>{formatted_text}</span>
                </div>
            """
        else:
            self.conversation_html += f"""
                <div style='margin-bottom: 15px; background-color: #ffffff; padding: 10px; border-left: 4px solid #198754; border-radius: 4px;'>
                    <b style='color: #198754;'>AI Assistant:</b><br>
                    <div style='margin-top: 5px; color: #212529;'>{formatted_text}</div>
                </div>
            """
        
        self.chat_history.setHtml(self.conversation_html)
        self.chat_history.verticalScrollBar().setValue(
            self.chat_history.verticalScrollBar().maximum()
        )

    def send_msg(self):
        """
        Sends the user input message to the AI assistant and appends 
        both user and AI responses to the formatted chat window.
        """
        text = self.input_field.text().strip()
        if not text:
            return
        
        self.append_message("You", text)
        self.input_field.clear()
        
        response = self.ai_assistant.send_message(text)
        self.append_message("AI", response)


# ============================================================
# MAIN WINDOW
# ============================================================

class PlanWindow:

    def __init__(self):

        # Load Qt Designer UI
        self.window = loadUi(str(UI_FILE))

        # Initialize database
        self.db = BacDatabase(str(DATABASE_FILE))

        # Initialize AI Assistant
        self.ai_assistant = BacAIAssistant()

        # ----------------------------------------------------
        # Window
        # ----------------------------------------------------

        self.window.setWindowTitle("Bac Planner")

        # Labels
        self.window.label_2.setText("Lesson:")
        self.window.label_3.setText("Status:")

        # Buttons setup
        self.window.af.setText("Refresh")
        self.window.updateStatusButton.setText("Update Status")

        # Configure the single clean AI Assistant button
        self.window.aj.setText("🤖 Ask AI")
        self.window.aj.show()
        self.window.aj.clicked.connect(self.ask_ai_for_advice)

        if hasattr(self.window, "aiButton"):
            self.window.aiButton.hide()

        # ----------------------------------------------------
        # Table (Fixed: set column count to 2 so headers show properly)
        # ----------------------------------------------------

        self.window.t1.setColumnCount(2)
        self.window.t1.setHorizontalHeaderLabels([
            "Lesson",
            "Status"
        ])

        # ----------------------------------------------------
        # Status list in English with "Not yet" included
        # ----------------------------------------------------

        self.statuses = [
            "⚪ Not yet",
            "🔴 Poor",
            "🟡 Average",
            "🟢 Good",
            "⭐ Excellent"
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
        """Loads all available subjects from the database into the subject dropdown combo box."""
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
        """Loads lessons corresponding to the currently selected subject into the lesson dropdown."""
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
        """Handles events triggered when a different subject is chosen from the combo box."""
        self.charger_cours()
        self.afficher()

    # ========================================================
    # LESSON SELECTED
    # ========================================================

    def cours_selectionne(self):
        """Synchronizes the status dropdown selection with the currently selected lesson's saved progress state."""
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
        """Commits the newly selected progress status of a lesson to the database."""
        subject = self.window.cb.currentText().strip()

        lesson = self.window.cr.currentText().strip()

        status = self.window.cb2.currentText()

        if not subject:

            QMessageBox.warning(
                self.window,
                "Missing Subject",
                "Please select a subject."
            )

            return

        if not lesson:

            QMessageBox.warning(
                self.window,
                "Missing Lesson",
                "Please select a lesson."
            )

            return

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

        index = self.window.cr.currentIndex()

        if index >= 0:

            self.window.cr.setItemData(
                index,
                status
            )

        self.afficher()

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
        """Populates and structures the main overview table with all lesson statuses for the active subject."""
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

        self.window.t1.resizeColumnsToContents()

        self.window.t1.setColumnWidth(
            0,
            max(
                self.window.t1.columnWidth(0),
                300
            )
        )

    # ========================================================
    # AI STUDY ADVICE
    # ========================================================

    def ask_ai_for_advice(self):
        """Opens the interactive AI chat assistant dialog window passing the current subject, lesson, and status context."""
        subject = self.window.cb.currentText().strip()
        lesson = self.window.cr.currentText().strip()
        status = self.window.cb2.currentText().strip()

        if not subject:
            QMessageBox.warning(
                self.window,
                "Missing Subject",
                "Please select a subject first."
            )
            return

        if not lesson:
            lesson = "General Course"

        if not status:
            status = "⚪ Not yet"

        dialog = AIChatDialog(self.ai_assistant, subject, lesson, status, self.window)
        dialog.exec_()

    # ========================================================
    # SHOW WINDOW
    # ========================================================

    def show(self):
        """Displays the main application user interface window."""
        self.window.show()


# ============================================================
# APPLICATION
# ============================================================

def main():
    """Application entry point initializing the Qt Event Loop and main window."""
    app = QApplication(sys.argv)

    window = PlanWindow()

    window.show()

    sys.exit(app.exec_())


# ============================================================
# START
# ============================================================

if __name__ == "__main__":

    main()