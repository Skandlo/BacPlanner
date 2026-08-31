# Bac Planner

A simple desktop application designed to help Tunisian Bac Informatique students organize their revision, track lesson progress, and calculate their overall **moyenne**.

This project comes in **two versions**:

* 🟢 **Simple Version**: revision planner + status tracking + moyenne calculation.
* 🤖 **AI Version**: includes everything in the Simple Version plus an AI study assistant.

---

## 📦 Versions

### 🟢 Simple Version

The Simple Version is recommended if you want a lightweight and straightforward Bac planner.

It includes:

* 📚 Bac Informatique subjects
* 📖 Lesson list for each subject
* 📊 Lesson progress tracking
* ⚪ Not yet
* 🔴 Poor
* 🟡 Average
* 🟢 Good
* ⭐ Excellent
* 🔎 Status filtering
* 📈 Bac moyenne calculation
* 💾 SQLite database for saving your progress

You can find:

```text
status.py
```

This opens the **Status Overview** window, where you can filter your lessons by:

* Status
* Subject

The Simple Version **does not require any AI package or API key**.

---

# 🤖 AI Version

The AI Version contains all the features of the Simple Version, with an additional AI study assistant.

The AI assistant can help you:

* Analyze your revision progress
* Discuss your current lesson
* Give study advice
* Create an action plan
* Answer questions about your revision

### ⚠️ Additional requirements

For the AI version, you need the Google Generative AI packages used by the project.

Install them with:

```bash
pip install google-generativeai
pip install google-ai-generativelanguage
```

> The exact package names may change over time. If the project provides a `requirements.txt`, installing from that file is preferable.

---

# 💻 Installation

## 1. Install Python

Make sure Python is installed on your computer.

Python **3.10+** is recommended.

You can check your version with:

```bash
python --version
```

---

## 2. Recommended: Thonny

### ⭐ Strongly recommended for beginners

If you are not familiar with Python, I **strongly recommend using Thonny**.

Thonny is simple and makes it much easier to:

* Open the project
* Install packages
* Run Python files
* See errors
* Manage Python

After installing Thonny, open the Bac Planner project folder.

---

# 3. Install PyQt5

**PyQt5 is required for both versions.**

Open the Thonny package manager and install:

```text
PyQt5
```

Or use the terminal:

```bash
pip install PyQt5
```

Without PyQt5, the graphical interface will not work.

---

# 4. Run the Simple Version

Once PyQt5 is installed, open the Simple Version.

Run:

```text
main.py
```

or the main Python file provided with the Simple Version.

The application will automatically create/use:

```text
bac_planner.db
```

You don't need to manually create the database.

---

# 🔎 Checking Revision Status

The Simple Version includes a separate status window.

Open:

```text
status.py
```

This allows you to see and filter your revision progress.

You can filter by:

### Status

```text
All Statuses
⚪ Not yet
🔴 Poor
🟡 Average
🟢 Good
⭐ Excellent
```

### Subject

```text
All Subjects
Mathématiques
Algorithmes & Prog.
STI
Sciences Physiques
Français
Anglais
Philosophie
Arabe
```

This is useful when you want to quickly see things such as:

> "Show me everything I haven't studied yet."

or:

> "Show me all the lessons I marked as Poor."

---

# 🤖 Setting up the AI Version

If you want to use the AI version, you need a **Google Gemini API key**.

After installing the required packages, find:

```text
config.json
```

Open it with a text editor and put your Gemini API key in the appropriate field.

For example:

```json
{
    "api_key": "YOUR_GEMINI_API_KEY"
}
```

**Do not share your API key publicly.**

---

## 🔑 How to get a Gemini API key

If you don't know how to create one, search YouTube or Google for:

```text
Gemini AI API key tutorial
```

or:

```text
How to get Google Gemini API key
```

Follow a recent tutorial from Google or another reliable source.

Once you have the key, put it in `config.json`.

### 💡 Recommendation

If you are new to APIs, don't try to modify the AI code itself.

Simply:

1. Get your Gemini API key.
2. Open `config.json`.
3. Put your key in the required field.
4. Save the file.
5. Run the AI version.

---

# 📁 Project Structure

A typical project structure looks like:

```text
Bac-Planner/
│
├── database.py
├── config.json
│
├── bac_planner.db
│
├── main.py
├── status.py
│
├── ai_assistant.py
│
├── ui/
│   ├── Plan.ui
│   └── Status.ui
│
└── README.md
```

The exact files may differ slightly between versions.

---

# 🟢 Simple vs 🤖 AI

| Feature             | Simple |  AI |
| ------------------- | :----: | :-: |
| Bac subjects        |    ✅   |  ✅  |
| Lessons             |    ✅   |  ✅  |
| Revision status     |    ✅   |  ✅  |
| Status filtering    |    ✅   |  ✅  |
| Moyenne calculation |    ✅   |  ✅  |
| SQLite database     |    ✅   |  ✅  |
| AI assistant        |    ❌   |  ✅  |
| Gemini API key      |    ❌   |  ✅  |
| PyQt5               |    ✅   |  ✅  |

---

# ⚠️ Important

### Simple Version

You only need:

```bash
pip install PyQt5
```

### AI Version

You need:

```bash
pip install PyQt5
pip install google-generativeai
pip install google-ai-generativelanguage
```

You also need a valid Gemini API key configured in:

```text
config.json
```

---

# 🚀 Quick Start

### Want the easiest setup?

Use **Thonny**.

Then:

```text
1. Install Python
        ↓
2. Install Thonny
        ↓
3. Open Bac Planner
        ↓
4. Install PyQt5
        ↓
5. Run the Simple Version
```

### Want AI?

After the above:

```text
6. Install Google AI packages
        ↓
7. Get a Gemini API key
        ↓
8. Put the key in config.json
        ↓
9. Run the AI Version
```

---

## 📌 Security

Never upload your personal Gemini API key to GitHub.

If you are publishing this project publicly, **do not put your real API key inside `config.json` before pushing the project**.

Use an example configuration instead, such as:

```json
{
    "api_key": "YOUR_GEMINI_API_KEY"
}
```

Then each user can add their own key locally.
