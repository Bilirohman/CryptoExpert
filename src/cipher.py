import math
import re


class ColumnarTransposition:
    """
    Implementasi Columnar Transposition Cipher.
    """

    @staticmethod
    def _parse_numeric_key(key_str: str) -> list[int]:
        """
        Helper untuk memparsing string kunci.
        Mendukung format spasi "4 1 3 2" maupun format sambung "4132".
        """
        # Cek apakah ada pemisah (spasi atau koma)
        if re.search(r"[\s,]", key_str):
            numbers = re.findall(r"\d+", key_str)
        else:
            numbers = list(re.findall(r"\d", key_str))

        return [int(n) for n in numbers]

    @staticmethod
    def get_key_metadata(key: str, mode: str = "text") -> dict:
        """
        Menentukan urutan kolom (order) dan jumlah kolom berdasarkan mode.
        """
        key_map = []

        if mode == "numeric":
            # Mode Numeric (Permutation): Key "4 1 3 2"

            numeric_keys = ColumnarTransposition._parse_numeric_key(key)
            if not numeric_keys:
                return {"order": [], "num_cols": 0, "clean_key_display": []}

            num_cols = len(numeric_keys)
            expected_set = set(range(1, num_cols + 1))
            if set(numeric_keys) != expected_set:
                return {"order": [], "num_cols": 0, "clean_key_display": []}

            order = [k - 1 for k in numeric_keys]
            clean_key_display = [str(i) for i in range(1, num_cols + 1)]

            return {
                "order": order,
                "num_cols": num_cols,
                "clean_key_display": clean_key_display,
            }

        else:
            num_cols = len(key)
            for i, char in enumerate(key):
                key_map.append(
                    {"orig_index": i, "sort_val": char.upper(), "display": char}
                )
            key_map.sort(key=lambda x: x["sort_val"])

            return {
                "order": [item["orig_index"] for item in key_map],
                "num_cols": num_cols,
                "clean_key_display": list(key),
            }

    @staticmethod
    def encrypt_text(
        plaintext: str, key: str, padding_char: str = "X", key_mode: str = "text"
    ) -> dict:
        metadata = ColumnarTransposition.get_key_metadata(key, key_mode)
        order = metadata["order"]
        num_cols = metadata["num_cols"]

        if num_cols == 0:
            return None

        num_rows = math.ceil(len(plaintext) / num_cols)

        padded_text = plaintext
        total_chars = num_rows * num_cols
        missing = total_chars - len(plaintext)
        if missing > 0:
            padded_text += padding_char * missing

        grid = [["" for _ in range(num_cols)] for _ in range(num_rows)]
        fill_steps = []

        char_idx = 0
        for r in range(num_rows):
            for c in range(num_cols):
                if char_idx < len(padded_text):
                    char = padded_text[char_idx]
                    grid[r][c] = char
                    fill_steps.append((r, c, char))
                    char_idx += 1

        ciphertext = ""
        read_steps = []

        for col_idx in order:
            for row_idx in range(num_rows):
                char = grid[row_idx][col_idx]
                ciphertext += char
                read_steps.append((row_idx, col_idx, char))

        return {
            "ciphertext": ciphertext,
            "grid": grid,
            "order": order,
            "fill_steps": fill_steps,
            "read_steps": read_steps,
            "padded_text": padded_text,
            "display_key": metadata["clean_key_display"],
        }

    @staticmethod
    def decrypt_text(ciphertext: str, key: str, key_mode: str = "text") -> dict:
        metadata = ColumnarTransposition.get_key_metadata(key, key_mode)
        order = metadata["order"]
        num_cols = metadata["num_cols"]

        if num_cols == 0:
            return None

        num_rows = math.ceil(len(ciphertext) / num_cols)

        grid = [["" for _ in range(num_cols)] for _ in range(num_rows)]
        fill_steps = []
        current_char_idx = 0

        for col_idx in order:
            for row_idx in range(num_rows):
                if current_char_idx < len(ciphertext):
                    char = ciphertext[current_char_idx]
                    grid[row_idx][col_idx] = char
                    fill_steps.append((row_idx, col_idx, char))
                    current_char_idx += 1

        plaintext = ""
        read_steps = []
        for r in range(num_rows):
            for c in range(num_cols):
                char = grid[r][c]
                plaintext += char
                read_steps.append((r, c, char))

        return {
            "plaintext": plaintext.rstrip(),
            "raw_plaintext": plaintext,
            "grid": grid,
            "order": order,
            "fill_steps": fill_steps,
            "read_steps": read_steps,
            "display_key": metadata["clean_key_display"],
        }

    @staticmethod
    def encrypt_bytes(data: bytes, key: str, key_mode: str = "text") -> bytes:
        if not data:
            return b""
        metadata = ColumnarTransposition.get_key_metadata(key, key_mode)
        order, num_cols = metadata["order"], metadata["num_cols"]
        if num_cols == 0:
            return b""

        len_data = len(data)
        num_rows = math.ceil(len_data / num_cols)
        total_len = num_rows * num_cols
        result = bytearray(total_len)

        dest_idx = 0
        for col_idx in order:
            for row_idx in range(num_rows):
                src_idx = (row_idx * num_cols) + col_idx
                if src_idx < len_data:
                    result[dest_idx] = data[src_idx]
                else:
                    result[dest_idx] = 0
                dest_idx += 1
        return bytes(result)

    @staticmethod
    def decrypt_bytes(data: bytes, key: str, key_mode: str = "text") -> bytes:
        if not data:
            return b""
        metadata = ColumnarTransposition.get_key_metadata(key, key_mode)
        order, num_cols = metadata["order"], metadata["num_cols"]
        if num_cols == 0:
            return b""

        len_data = len(data)
        num_rows = math.ceil(len_data / num_cols)
        result = bytearray(len_data)

        src_idx = 0
        for col_idx in order:
            for row_idx in range(num_rows):
                if src_idx < len_data:
                    dest_idx = (row_idx * num_cols) + col_idx
                    if dest_idx < len_data:
                        result[dest_idx] = data[src_idx]
                    src_idx += 1
        return bytes(result)

    @staticmethod
    def get_byte_steps(
        data_sample: bytes, key: str, mode="encrypt", key_mode="text"
    ) -> dict:
        byte_list = list(data_sample)
        metadata = ColumnarTransposition.get_key_metadata(key, key_mode)
        order, num_cols = metadata["order"], metadata["num_cols"]
        if num_cols == 0:
            return {}

        num_rows = math.ceil(len(byte_list) / num_cols)
        total_len = num_rows * num_cols
        padded_data = byte_list + [None] * (total_len - len(byte_list))

        grid = [[None for _ in range(num_cols)] for _ in range(num_rows)]
        fill_steps = []
        read_steps = []

        if mode == "encrypt":
            idx = 0
            for r in range(num_rows):
                for c in range(num_cols):
                    val = padded_data[idx] if idx < len(padded_data) else 0
                    grid[r][c] = val
                    fill_steps.append((r, c, val))
                    idx += 1
            for col_idx in order:
                for row_idx in range(num_rows):
                    val = grid[row_idx][col_idx]
                    read_steps.append((row_idx, col_idx, val))
        else:
            idx = 0
            for col_idx in order:
                for row_idx in range(num_rows):
                    val = padded_data[idx] if idx < len(padded_data) else 0
                    grid[row_idx][col_idx] = val
                    fill_steps.append((row_idx, col_idx, val))
                    idx += 1
            for r in range(num_rows):
                for c in range(num_cols):
                    val = grid[r][c]
                    read_steps.append((r, c, val))

        return {
            "grid": grid,
            "fill_steps": fill_steps,
            "read_steps": read_steps,
            "order": order,
            "display_key": metadata["clean_key_display"],
        }
