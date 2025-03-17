import shutil
import re
from datetime import datetime
from pathlib import Path

DOWNLOADS_DIR = Path.home() / "Downloads"

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"],
    "Documents": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".md"],
    "Videos": [".mp4", ".mkv", ".flv", ".avi", ".mov", ".wmv"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executables": [".exe", ".msi", ".dmg", ".sh", ".bat"],
    "Audio": [".mp3", ".wav", ".flac", ".aac", ".ogg"],
    "Code": [".py", ".java", ".c", ".cpp", ".js", ".html", ".css", ".php", ".rb", ".swift"]
}

DATE_FOLDER_PATTERN = re.compile(r"^\d{4}-\d{2}$")


def get_category(file_extension):
    """Return the category name based on file extension."""
    for category, extensions in FILE_CATEGORIES.items():
        if file_extension.lower() in extensions:
            return category
    return "Others"


def move_item(item):
    """Move a file or folder into the correct date-based subdirectory."""
    try:
        month_folder = datetime.fromtimestamp(item.stat().st_mtime).strftime("%Y-%m")
        dest_folder = DOWNLOADS_DIR / month_folder

        if item.is_file():
            category = get_category(item.suffix)
            category_folder = dest_folder / category
            category_folder.mkdir(parents=True, exist_ok=True)

            shutil.move(str(item), str(category_folder / item.name))
            print(f"Moved File: {item.name} → {category_folder}")

        elif item.is_dir() and not DATE_FOLDER_PATTERN.match(item.name):
            dest_folder.mkdir(parents=True, exist_ok=True)
            shutil.move(str(item), str(dest_folder / item.name))
            print(f"Moved Folder: {item.name} → {dest_folder}")

    except Exception as e:
        print(f"Error moving {item.name}: {e}")


def organize_downloads():
    """Organize files and folders in the downloads directory by month."""
    if not DOWNLOADS_DIR.exists():
        print(f"Error: {DOWNLOADS_DIR} does not exist.")
        return

    for item in DOWNLOADS_DIR.iterdir():
        if item.name not in ["System Volume Information", "desktop.ini"]:
            move_item(item)


if __name__ == "__main__":
    organize_downloads()
