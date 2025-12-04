import re


def sanitize_input(text: str) -> str:
    """
    Membersihkan input teks dari karakter non-printable jika diperlukan.
    """
    if not text:
        return ""
    return text


def validate_key(key: str, mode: str = "text") -> tuple[bool, str]:
    """
    Memastikan kunci valid sesuai mode.
    """
    if not key:
        return False, "Kunci tidak boleh kosong."

    if mode == "text":
        if not key.isalpha() and not key.isalnum():
            return False, "Kunci text harus berupa alphanumeric."

    elif mode == "numeric":
        if not re.match(r"^[\d\s,]+$", key):
            return False, "Kunci numerik hanya boleh berisi angka."

        # 2. Parse angka
        if re.search(r"[\s,]", key):
            numbers = [int(n) for n in re.findall(r"\d+", key)]
        else:
            numbers = [int(n) for n in re.findall(r"\d", key)]

        if not numbers:
            return False, "Tidak ditemukan angka pada kunci."

        num_cols = len(numbers)
        expected_set = set(range(1, num_cols + 1))
        current_set = set(numbers)

        if current_set != expected_set:
            return (
                False,
                f"Kunci Numerik harus berupa permutasi angka 1 sampai {num_cols}. (Tidak boleh ada angka yang hilang atau duplikat)",
            )

    return True, ""


def format_step_description(step_idx, total_steps, action, detail):
    """Helper untuk log visualisasi"""
    return f"Langkah {step_idx}/{total_steps}: {action} -> {detail}"
