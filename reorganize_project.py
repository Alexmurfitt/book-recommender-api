# reorganize_project.py

import os
import shutil

# --- Configuración ---
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SRC_DIR = os.path.join(BASE_DIR, "book_recommender_api")
APP_DIR = os.path.join(SRC_DIR, "app")
TESTS_DIR = os.path.join(SRC_DIR, "tests")
SCRIPTS_DIR = os.path.join(SRC_DIR, "scripts")

# Archivos que deben estar en app/
APP_FILES = [
    "main.py", "database.py", "models.py", "personality.py", "profile.py",
    "quiz.py", "recommender.py", "books_controller.py", "explain.py",
    "user_controller.py", "__init__.py", "app.py"
]

# Archivos de utilidad que deben ir en scripts/
SCRIPT_FILES = [
    "check_fields.py", "clean_books_fields.py", "run_recommender_test.py", "informe.md"
]

# Archivo de test esperado
EXPECTED_TEST = "test_books_cleanup.py"

# --- Funciones útiles ---

def ensure_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def move_file_if_exists(src_folder, filename, dest_folder):
    src_path = os.path.join(src_folder, filename)
    dest_path = os.path.join(dest_folder, filename)
    if os.path.exists(src_path):
        shutil.move(src_path, dest_path)
        print(f"✅ Movido: {filename} → {os.path.relpath(dest_folder, BASE_DIR)}")
    else:
        return False
    return True

def clean_redundant_dirs():
    duplicate_dir = os.path.join(SRC_DIR, "book_recommender_api")
    if os.path.isdir(duplicate_dir):
        shutil.rmtree(duplicate_dir)
        print(f"🗑️  Carpeta duplicada eliminada: {duplicate_dir}")

def update_pytest_ini():
    ini_path = os.path.join(BASE_DIR, "pytest.ini")
    if not os.path.exists(ini_path):
        return
    with open(ini_path, "r") as f:
        lines = f.readlines()

    updated = False
    with open(ini_path, "w") as f:
        for line in lines:
            if line.strip().startswith("testpaths"):
                f.write("testpaths = book_recommender_api/tests\n")
                updated = True
            else:
                f.write(line)
        if not updated:
            f.write("testpaths = book_recommender_api/tests\n")

    print("🛠️  pytest.ini actualizado correctamente.")

# --- Ejecución principal ---

if __name__ == "__main__":
    print("🔧 Reorganizando estructura del proyecto...")

    ensure_directory(APP_DIR)
    ensure_directory(TESTS_DIR)
    ensure_directory(SCRIPTS_DIR)

    # Mover archivos a app/
    print("\n📁 Archivos en app/:")
    for file in APP_FILES:
        move_file_if_exists(SRC_DIR, file, APP_DIR)

    # Mover scripts auxiliares a scripts/
    print("\n📁 Archivos utilitarios en scripts/:")
    for file in SCRIPT_FILES:
        move_file_if_exists(SRC_DIR, file, SCRIPTS_DIR)

    # Mover test si existe
    print("\n🧪 Archivos de test:")
    if not move_file_if_exists(SRC_DIR, EXPECTED_TEST, TESTS_DIR):
        print(f"⚠️  No encontrado: {EXPECTED_TEST}")

    # Eliminar duplicados si existen
    clean_redundant_dirs()

    # Actualizar pytest.ini
    update_pytest_ini()

    print("\n✅ Reorganización completa.")
