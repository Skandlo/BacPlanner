import sqlite3


class BacDatabase:
    def __init__(self, db_name="bac_planner.db"):
        self.db_name = db_name
        self.initialize_tables()
        self.populate_bac_info_subjects()
        self.populate_bac_info_lessons()

    def initialize_tables(self):
        """Creates the necessary database tables if they do not exist."""
        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

            # Table 1: Stores core subjects and their official coefficients
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS subjects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_name TEXT UNIQUE,
                    coefficient REAL
                )
            """)

            # Table 2: Stores student grades for calculating the overall average
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS student_grades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_name TEXT UNIQUE,
                    controle_grade REAL DEFAULT 0.0,
                    synthese_grade REAL DEFAULT 0.0,
                    practical_grade REAL DEFAULT -1.0
                )
            """)

            # Table 3: Stores the revision checklists for every chapter
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS revision_tracker (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    subject_name TEXT,
                    lesson_title TEXT,
                    status TEXT DEFAULT '🔴 To Do'
                )
            """)

            connection.commit()

    def populate_bac_info_subjects(self):
        """Inserts the Bac Informatique subjects and their coefficients."""

        bac_info_subjects = [
            ("Mathématiques", 3.0),
            ("Algorithmes & Prog.", 3.0),
            ("STI", 3.0),
            ("Sciences Physiques", 2.0),
            ("Français", 1.0),
            ("Anglais", 1.0),
            ("Philosophie", 1.0),
            ("Arabe", 1.0),
            ("Sport", 1.0)
        ]

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

            for name, coef in bac_info_subjects:
                cursor.execute("""
                    INSERT OR IGNORE INTO subjects
                    (subject_name, coefficient)
                    VALUES (?, ?)
                """, (name, coef))

            connection.commit()

    def populate_bac_info_lessons(self):
        """Populates the lesson chapters for Bac Informatique."""

        lessons_data = [

            # ============================================================
            # MATHEMATICS
            # ============================================================

            ("Mathématiques", "T1 - 1. Nombres complexes"),
            ("Mathématiques", "T1 - 2. Suites réelles"),
            ("Mathématiques", "T1 - 3. Limites de fonctions + Continuité"),
            ("Mathématiques", "T1 - 4. Dérivation"),
            ("Mathématiques", "T1 - 5. Arithmétique"),
            ("Mathématiques", "T1 - 6. Primitive"),

            ("Mathématiques", "T2 - 1. Etude de fonctions"),
            ("Mathématiques", "T2 - 2. systèmes d'équation linéaires"),
            ("Mathématiques", "T2 - 3. Fonctions logarithmes"),
            ("Mathématiques", "T2 - 4. Fonctions exponentielles"),

            ("Mathématiques", "T3 - 1. Statistiques"),
            ("Mathématiques", "T3 - 2. Probabilités Conditionnelles"),
            ("Mathématiques", "T3 - 3. Variables aléatoires"),
            ("Mathématiques", "T3 - 4. Calcul intégral"),

            # ============================================================
            # SCIENCES PHYSIQUES
            # ============================================================

            ("Sciences Physiques", "Phys - T1 - 1. LE CONDENSATEUR"),
            ("Sciences Physiques", "Phys - T1 - 2. LE DIPOLE RC"),
            ("Sciences Physiques", "Phys - T1 - 3. LA BOBINE"),
            ("Sciences Physiques", "Phys - T1 - 4. LE DIPOLE RL"),
            (
                "Sciences Physiques",
                "Phys - T1 - 5. CIRCUIT RLC SERIE : LES OSCILLATIONS LIBRES AMORTIES"
            ),
            (
                "Sciences Physiques",
                "Phys - T1 - 6. CIRCUIT LC SERIE : LES OSCILLATIONS LIBRES NON AMORTIES"
            ),
            ("Sciences Physiques", "Phys - T1 - 7. ENTRETIEN DES OSCILLATIONS"),

            ("Sciences Physiques", "Phys - T2 - 1. LES OSCILLATIONS ELECTRIQUES FORCEES"),
            ("Sciences Physiques", "Phys - T2 - 2. LES FILTRES"),
            (
                "Sciences Physiques",
                "Phys - T2 - 3. PRODUCTION DE SIGNAUX PERIODIQUES NON SINUSOÏDAUX"
            ),
            ("Sciences Physiques", "Phys - T2 - 4. CONVERSION DES SIGNAUX"),

            ("Sciences Physiques", "Phys - T3 - 1. INTERACTION ONDE-MATIERE"),
            ("Sciences Physiques", "Phys - T3 - 2. ONDES MECANIQUES PROGRESSIVES"),
            ("Sciences Physiques", "Phys - T3 - 3. TRANSMISSION D'UN SIGNAL"),

            ("Sciences Physiques", "Chimie - Rappel - 1. PHENOMENE D'OXYDOREDUCTION"),
            ("Sciences Physiques", "Chimie - Rappel - 2. LES HYDROCARBURES ALIPHATIQUES"),
            ("Sciences Physiques", "Chimie - T1 - 1. MESURE D'UNE QUANTITE DE LA MATIERE"),
            (
                "Sciences Physiques",
                "Chimie - T2 - 1. PILE ELECTROCHIMIQUE - PILE DANIELL"
            ),
            ("Sciences Physiques", "Chimie - T2 - 2. L' ELECTROLYSE"),
            ("Sciences Physiques", "Chimie - T3 - 1. LES ALCOOLS"),

            # ============================================================
            # ALGORITHMES & PROGRAMMATION
            # ============================================================

            (
                "Algorithmes & Prog.",
                "4ème - 1. Les fichiers texte et binaire"
            ),
            (
                "Algorithmes & Prog.",
                "4ème - 2. Les algorithmes de tri"
            ),
            (
                "Algorithmes & Prog.",
                "4ème - 3. La récursivité"
            ),
            (
                "Algorithmes & Prog.",
                "4ème - 4. Les algorithmes récurrents"
            ),
            (
                "Algorithmes & Prog.",
                "4ème - 5. Les algorithmes arithmétiques"
            ),
            (
                "Algorithmes & Prog.",
                "4ème - 6. Les algorithmes d'approximation et d'optimisation"
            ),
            (
                "Algorithmes & Prog.",
                "4ème - 7. Les interfaces Graphiques (Qt-Designer)"
            ),
            (
                "Algorithmes & Prog.",
                "Rappel - 8. Le vecteur d'enregistrements"
            ),
            (
                "Algorithmes & Prog.",
                "Rappel - 9. La matrice"
            ),
            (
                "Algorithmes & Prog.",
                "Rappel - 10. Les algorithmes de recherche"
            ),
            (
                "Algorithmes & Prog.",
                "Rappel - 11. Les types de données en python"
            ),

            # ============================================================
            # STI
            # ============================================================

            ("STI", "1. Présentation du programme"),
            ("STI", "2. Développement web"),
            ("STI", "3. Gestion de données (new)"),
            ("STI", "4. Annexe HTML, CSS, JS, SQL"),

            # ============================================================
            # ARABE
            # ============================================================

            (
                "Arabe",
                "التقديم: تقديم عام لبرنامج العربية للبكالوريا شعب علمية"
            ),
            (
                "Arabe",
                "المحور الأول: في التفكير العلمي (جديد)"
            ),
            (
                "Arabe",
                "المحور الثاني: في الفن والأدب"
            ),
            (
                "Arabe",
                "المحور الثالث: في حوار الحضارات"
            ),
            (
                "Arabe",
                "المحور الرابع: في الفكر والفن"
            ),


            # ============================================================
            # PHILOSOPHIE
            # ============================================================

            (
                "Philosophie",
                "T1 - المحور الأول: الإنية والغيرية (جديد)"
            ),
            (
                "Philosophie",
                "T1 - المحور الثاني: الخصوصية والكونية (جديد)"
            ),
            (
                "Philosophie",
                "T2 - المحور الثالث: العلم بين الحقيقة والنمذجة (جديد)"
            ),
            (
                "Philosophie",
                "T2 - المحور الرابع: الدولة: السيادة والمواطنة (جديد)"
            ),
            (
                "Philosophie",
                "T3 - المحور الخامس: الأخلاق: الخير والسعادة (جديد)"
            ),

            # ============================================================
            # ENGLISH
            # ============================================================

            ("Anglais", "General - Grammar rules"),
            (
                "Anglais",
                "T1 - Unit One: Art Shows and Holidaying (NEW)"
            ),
            (
                "Anglais",
                "T1 - Unit Two: Education Matters (NEW)"
            ),
            (
                "Anglais",
                "T2 - Unit Three: Creative, Inventive Minds (NEW)"
            ),
            (
                "Anglais",
                "T3 - Unit Four: Life Issues (NEW)"
            ),


            # ============================================================
            # FRENCH
            # ============================================================

            (
                "Français",
                "T1 - Module n°1: Souvenirs et nostalgie"
            ),
            (
                "Français",
                "T1 - Module d'apprentissage n°2: Histoires d'amour NV"
            ),
            (
                "Français",
                "T2 - Module d'apprentissage n°3: Liberté, j'écris ton nom... (nouveau)"
            ),
            (
                "Français",
                "T3 - Module d'apprentissage n°4: Guerre et paix (nouveau)"
            ),
            (
                "Français",
                "T3 - Module d'apprentissage n°5: L'homme et la science (nouveau)"
            )
        ]

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

            # Only populate if the table is empty
            cursor.execute("SELECT COUNT(*) FROM revision_tracker")

            if cursor.fetchone()[0] == 0:
                cursor.executemany("""
                    INSERT INTO revision_tracker
                    (subject_name, lesson_title)
                    VALUES (?, ?)
                """, lessons_data)

                connection.commit()

    def update_student_grade(
        self,
        subject_name,
        controle,
        synthese,
        practical=-1.0
    ):
        """Saves or updates a student's grade entries in SQLite."""

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO student_grades
                (
                    subject_name,
                    controle_grade,
                    synthese_grade,
                    practical_grade
                )
                VALUES (?, ?, ?, ?)

                ON CONFLICT(subject_name) DO UPDATE SET
                    controle_grade = excluded.controle_grade,
                    synthese_grade = excluded.synthese_grade,
                    practical_grade = excluded.practical_grade
            """, (
                subject_name,
                controle,
                synthese,
                practical
            ))

            connection.commit()

    def calculate_overall_moyenne(self):
        """Calculates the overall Bac Informatique average."""

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

            # Fetch subjects, coefficients, and student grades.
            # LEFT JOIN ensures subjects without grades are still included.
            cursor.execute("""
                SELECT
                    s.subject_name,
                    s.coefficient,
                    g.controle_grade,
                    g.synthese_grade,
                    g.practical_grade
                FROM subjects s
                LEFT JOIN student_grades g
                    ON s.subject_name = g.subject_name
            """)

            rows = cursor.fetchall()

        total_weighted_points = 0.0
        total_coefficients = 0.0

        for name, coef, ctrl, synth, prac in rows:

            # Fallback values if grades have not been entered
            ctrl = ctrl if ctrl is not None else 0.0
            synth = synth if synth is not None else 0.0
            prac = prac if prac is not None else -1.0

            # Technical subjects
            if name in ["Algorithmes & Prog.", "STI"]:

                # Formula:
                # (Contrôle + Practical + 2 × Synthèse) / 4

                prac_val = prac if prac >= 0 else 0.0

                subject_grade = (
                    ctrl
                    + prac_val
                    + (2 * synth)
                ) / 4.0

            else:

                # Regular subjects:
                # (Contrôle + 2 × Synthèse) / 3

                subject_grade = (
                    ctrl
                    + (2 * synth)
                ) / 3.0

            total_weighted_points += subject_grade * coef
            total_coefficients += coef

        if total_coefficients > 0:
            return round(
                total_weighted_points / total_coefficients,
                2
            )

        return 0.0

    def get_all_subjects(self):
        """Fetches all subjects and coefficients."""

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT subject_name, coefficient
                FROM subjects
                ORDER BY id
            """)

            return cursor.fetchall()

    def get_lessons_by_subject(self, subject_name):
        """Fetches all lessons and their current progress status."""

        with sqlite3.connect(self.db_name) as connection:
            cursor = connection.cursor()

            cursor.execute("""
                SELECT lesson_title, status
                FROM revision_tracker
                WHERE subject_name = ?
                ORDER BY id
            """, (subject_name,))

            return cursor.fetchall()
def update_lesson_status(self, subject_name, lesson_title, status):
    """Updates the status of a specific lesson."""

    with sqlite3.connect(self.db_name) as connection:
        cursor = connection.cursor()

        cursor.execute("""
            UPDATE revision_tracker
            SET status = ?
            WHERE subject_name = ?
            AND lesson_title = ?
        """, (
            status,
            subject_name,
            lesson_title
        ))

        connection.commit()

# ============================================================
# TEST / EXAMPLE USAGE
# ============================================================

if __name__ == "__main__":

    db = BacDatabase()

    print("Database initialized successfully.")

    print("\nSubjects:")
    for subject, coefficient in db.get_all_subjects():
        print(f"- {subject}: coefficient {coefficient}")

    print("\nCurrent overall moyenne:")
    print(db.calculate_overall_moyenne())

    print("\nExample Mathématiques lessons:")
    lessons = db.get_lessons_by_subject("Mathématiques")

    for lesson, status in lessons:
        print(f"{status} {lesson}")