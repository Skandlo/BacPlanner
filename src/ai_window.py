import sys
import sqlite3
from pathlib import Path

from PyQt5.uic import loadUi
from PyQt5.QtWidgets import (
    QApplication,
    QMessageBox,
    QMainWindow
)

from database import BacDatabase
from ai_assistant import BacAIAssistant


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
UI_FILE = BASE_DIR / "ui" / "AiWindow.ui"
DATABASE_FILE = BASE_DIR / "bac_planner.db"


# ============================================================
# AI WINDOW CLASS
# ============================================================

class AIWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        # Load UI
        self.window = loadUi(str(UI_FILE), self)

        # Initialize Database & AI
        self.db = BacDatabase(str(DATABASE_FILE))
        self.ai_coach = BacAIAssistant(api_key="YOUR_GEMINI_API_KEY")

        # Window configuration
        self.setWindowTitle("Bac Planner - AI Study Coach")

        # Connections
        self.window.generateButton.clicked.connect(self.get_ai_study_advice)

    def get_ai_study_advice(self):
        """Fetches student statistics from SQLite and asks the AI coach."""
        try:
            # 1. Fetch performance and pending tasks from database
            overall_moyenne = self.db.calculate_overall_moyenne()
            pending_lessons = self.db.get_lessons_by_status(status="⚪ Not Started")
            weak_subjects = [f"{lesson[0]}: {lesson[1]}" for lesson in pending_lessons[:5]]

            # 2. Status message
            self.window.aiOutputBox.setText("🤖 Analyzing your database records and building your personalized strategy...")
            QApplication.processEvents()

            # 3. Call Gemini AI
            advice = self.ai_coach.generate_study_advice(
                student_name="Mahjoub",
                weak_subjects=weak_subjects,
                overall_moyenne=overall_moyenne
            )

            # 4. Display result
            self.window.aiOutputBox.setText(advice)

        except Exception as e:
            QMessageBox.critical(
                self,
                "AI Error",
                f"Failed to generate AI advice:\n\n{e}"
            )

    def show(self):
        self.window.show()


# ============================================================
# MAIN (For testing this window independently)
# ============================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AIWindow()
    window.show()
    sys.exit(app.exec_())