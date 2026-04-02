import os
import shutil
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox


def get_file_category(file_path):
    file_extension = file_path.suffix.lower()

    image_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg'}
    document_extensions = {
        '.pdf', '.doc', '.docx', '.txt', '.rtf', '.odt',
        '.xls', '.xlsx', '.csv', '.ods', '.ppt', '.pptx'
    }
    video_extensions = {'.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v'}
    audio_extensions = {'.mp3', '.wav', '.flac', '.aac', '.ogg', '.wma', '.m4a'}
    archive_extensions = {'.zip', '.rar', '.7z', '.tar', '.gz', '.bz2'}

    if file_extension in image_extensions:
        return "Images"
    elif file_extension in document_extensions:
        return "Documents"
    elif file_extension in video_extensions:
        return "Videos"
    elif file_extension in audio_extensions:
        return "Audio"
    elif file_extension in archive_extensions:
        return "Archives"
    else:
        return "Others"


# 🔥 CORE FUNCTION (COMMON FOR GUI + CLI)
def organize(folder_path):
    folder = Path(folder_path)

    categories = {
        "Images": [],
        "Documents": [],
        "Videos": [],
        "Audio": [],
        "Archives": [],
        "Others": []
    }

    moved_count = 0
    skipped_count = 0

    # 🔥 FIX: use rglob + full path store
    for file_path in folder.rglob("*"):
        if file_path.is_file():
            category = get_file_category(file_path)
            categories[category].append(file_path)

    # Move files
    for category, files in categories.items():
        if files:
            category_folder = folder / category
            category_folder.mkdir(exist_ok=True)

            for file_path in files:
                filename = file_path.name
                source_path = file_path
                dest_path = category_folder / filename

                try:
                    counter = 1
                    original_dest = dest_path
                    while dest_path.exists():
                        name, ext = original_dest.stem, original_dest.suffix
                        dest_path = category_folder / f"{name}_{counter}{ext}"
                        counter += 1

                    shutil.move(str(source_path), str(dest_path))
                    print(f"Moving: {filename} → {category}")

                    moved_count += 1

                except Exception as e:
                    print(f"Error moving {filename}: {str(e)}")
                    skipped_count += 1

    return moved_count, skipped_count, categories


# GUI FUNCTION
def organize_files():
    root = tk.Tk()
    root.withdraw()
    root.attributes('-topmost', True)

    folder_path = filedialog.askdirectory(title="Select Folder")

    root.destroy()

    if not folder_path:
        messagebox.showinfo("Cancelled", "No folder selected.")
        return

    moved, skipped, categories = organize(folder_path)

    summary = f"""
FILE ORGANIZATION COMPLETE!

📁 Folder: {folder_path}
✅ Files Moved: {moved}
⚠️ Files Skipped: {skipped}

"""

    for category, files in categories.items():
        if files:
            summary += f"📂 {category}: {len(files)} files\n"

    messagebox.showinfo("Done", summary)
    print(summary)


# CLI FUNCTION
def organize_files_cli(folder_path):
    moved, skipped, _ = organize(folder_path)

    print("\n=== ORGANIZATION COMPLETE ===")
    print(f"📁 Folder: {folder_path}")
    print(f"✅ Files Moved: {moved}")
    print(f"⚠️ Files Skipped: {skipped}")


# MAIN
def main():
    print("=== FILE ORGANIZER TOOL ===")
    print("1. GUI Mode")
    print("2. CLI Mode")

    choice = input("Choose (1/2): ").strip()

    if choice == "2":
        folder_path = input("Enter folder path: ").strip()

        if os.path.exists(folder_path):
            organize_files_cli(folder_path)
        else:
            print("❌ Invalid path!")
    else:
        organize_files()


if __name__ == "__main__":
    main()