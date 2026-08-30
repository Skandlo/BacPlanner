# BacPlanner

A desktop study and revision planner designed for Tunisian Bac Informatique students.

## Description

BacPlanner is a Python-based desktop application that helps students organize their Bac Informatique revision in one place.

The application provides a structured database of subjects and lessons, allows students to track their revision status and academic progress, and features an integrated AI study assistant.

## Features

- 📚 Bac Informatique subjects and lessons
- 📝 Revision tracking and status filters
- ⚪ Not yet
- 🔴 Poor
- 🟡 Average
- 🟢 Good
- ⭐ Excellent
- 🤖 Integrated AI Study Assistant (Gemini-powered tutor speaking Tunisian Arabic)
- 💾 SQLite local database
- 🖥️ PyQt5 graphical interface & Qt Designer UI files
- 📊 Grade and progress features planned

## Technologies

- Python 3.x
- PyQt5
- SQLite3
- Google GenAI SDK (`google-genai`)
- Qt Designer

## Project Structure

```text
BacPlanner/
│
├── src/
│   ├── ai_assistant.py
│   ├── database.py
│   ├── main.py
│   ├── plan.py
│   └── status.py
│
├── ui/
│   ├── Plan.ui
│   └── Status.ui
│
├── .gitignore
├── LICENSE
└── README.md
