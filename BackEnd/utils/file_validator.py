import os

ALLOWED_TYPES = ["pdf", "txt", "docx"]
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB


def validate_file(file):
    filename = file.filename

    extension = filename.split(".")[-1]

    if extension not in ALLOWED_TYPES:
        return False, "File type not allowed"

    return True, "File valid"