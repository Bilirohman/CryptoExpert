import re


def sanitize_input(text: str) -> str:
    """
    Membersihkan input teks dari karakter non-printable jika diperlukan..
    """
    if not text:
        return ""
    return text


def validate_key(key: str) -> tuple[bool, str]:
    """
    Memastikan kunci valid (tidak kosong).
    """
    if not key:
        return False, "Kunci tidak boleh kosong."
    if not key.isalpha() and not key.isalnum():
        return False, "Kunci sebaiknya berupa alphanumeric."
    return True, ""


def format_step_description(step_idx, total_steps, action, detail):
    """Helper untuk log visualisasi"""
    return f"Langkah {step_idx}/{total_steps}: {action} -> {detail}"
