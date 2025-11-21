import math


class ColumnarTransposition:
    """
    Implementasi Columnar Transposition Cipher.
    """

    @staticmethod
    def get_key_order(key: str, mode: str = "stable") -> list[int]:
        key_map = []
        if mode == "numbered":
            counts = {}
            for i, char in enumerate(key):
                char = char.upper()
                if char not in counts:
                    counts[char] = 0
                counts[char] += 1
                key_map.append(
                    {"char": char, "orig_index": i, "sort_val": f"{char}{counts[char]}"}
                )
            key_map.sort(key=lambda x: x["sort_val"])
        else:
            for i, char in enumerate(key):
                key_map.append({"char": char, "orig_index": i})
            key_map.sort(key=lambda x: x["char"].upper())

        return [item["orig_index"] for item in key_map]

    @staticmethod
    def encrypt_text(
        plaintext: str, key: str, padding_char: str = "X", key_mode: str = "stable"
    ) -> dict:
        order = ColumnarTransposition.get_key_order(key, key_mode)
        num_cols = len(key)
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
        }

    @staticmethod
    def decrypt_text(ciphertext: str, key: str, key_mode: str = "stable") -> dict:
        order = ColumnarTransposition.get_key_order(key, key_mode)
        num_cols = len(key)
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
        }

    # --- OPTIMIZED BYTE HANDLING (PENTING) ---

    @staticmethod
    def encrypt_bytes(data: bytes, key: str) -> bytes:
        """
        Enkripsi file menggunakan kalkulasi indeks matematis (1D Array).
        Jauh lebih cepat dan hemat memori daripada membuat Grid 2D.
        """
        if not data:
            return b""

        order = ColumnarTransposition.get_key_order(key)
        num_cols = len(key)
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
    def decrypt_bytes(data: bytes, key: str) -> bytes:
        """
        Dekripsi file menggunakan kalkulasi indeks matematis.
        """
        if not data:
            return b""

        order = ColumnarTransposition.get_key_order(key)
        num_cols = len(key)
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
    def get_byte_steps(data_sample: bytes, key: str, mode="encrypt") -> dict:
        """
        Visualisasi tetap menggunakan logika Grid lambat karena datanya kecil (50 bytes).
        """
        byte_list = list(data_sample)
        num_cols = len(key)
        num_rows = math.ceil(len(byte_list) / num_cols)
        order = ColumnarTransposition.get_key_order(key)

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
        }
