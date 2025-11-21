import unittest
import sys
import os

# Setup path agar bisa import dari src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.cipher import ColumnarTransposition


class TestColumnarTransposition(unittest.TestCase):

    def test_1_basic_round_trip(self):
        """Test dasar: Apakah enkripsi lalu dekripsi mengembalikan pesan asli?"""
        plaintext = "KRIPTOGRAFI"
        key = "ZEBRA"

        enc = ColumnarTransposition.encrypt_text(plaintext, key)
        dec = ColumnarTransposition.decrypt_text(enc["ciphertext"], key)

        # Bersihkan padding dan spasi untuk perbandingan
        res_plain = dec["plaintext"].replace("X", "")
        self.assertEqual(res_plain, plaintext)

    def test_2_known_answer_test(self):
        """
        KAT (Known Answer Test): Memastikan ciphertext SESUAI TEORI manual.
        Contoh:
        Plain: "DEFEND" (6 chars)
        Key:   "KEY" (Order: E(1), K(0), Y(2) -> Urutan baca kolom: 1, 0, 2)

        Grid (2 baris, 3 kolom):
        K E Y
        -----
        D E F
        E N D

        Baca Kolom 1 (E): E N
        Baca Kolom 0 (K): D E
        Baca Kolom 2 (Y): F D

        Expected Ciphertext: "ENDEFD"
        """
        plaintext = "DEFEND"
        key = "KEY"
        # matikan padding otomatis agar hasil prediksi akurat
        enc = ColumnarTransposition.encrypt_text(plaintext, key, padding_char="")

        expected_cipher = "ENDEFD"
        self.assertEqual(
            enc["ciphertext"],
            expected_cipher,
            "Ciphertext tidak sesuai perhitungan manual teori!",
        )

    def test_3_duplicate_key_letters_stable(self):
        """
        CRITICAL TEST: Menangani kunci dengan huruf kembar (Mode Stable).
        Key: "APPLE"
        Sorted: A, E, L, P(pertama), P(kedua)
        Logika Stable harus mempertahankan urutan kemunculan P.
        """
        key = "APPLE"
        # Index Asli: A(0), P(1), P(2), L(3), E(4)
        # Sorted Stable:
        # A (idx 0)
        # E (idx 4)
        # L (idx 3)
        # P (idx 1) -> P pertama muncul
        # P (idx 2) -> P kedua muncul
        # Expected Order: [0, 4, 3, 1, 2]

        order = ColumnarTransposition.get_key_order(key, "stable")
        self.assertEqual(
            order, [0, 4, 3, 1, 2], "Gagal menangani huruf kembar di mode Stable"
        )

    def test_4_duplicate_key_letters_numbered(self):
        """
        CRITICAL TEST: Menangani kunci dengan huruf kembar (Mode Numbered).
        Biasanya mode ini memberi nomor pada huruf kembar, misal P1, P2.
        Logikanya mirip stable, tapi implementasinya beda di cipher.py.
        """
        key = "LEVEL"
        # L(0), E(1), V(2), E(3), L(4)
        # Numbered logic: E1, E2, L1, L2, V1
        # E1 (idx 1)
        # E2 (idx 3)
        # L1 (idx 0)
        # L2 (idx 4)
        # V1 (idx 2)
        # Expected Order: [1, 3, 0, 4, 2]

        order = ColumnarTransposition.get_key_order(key, "numbered")
        self.assertEqual(
            order, [1, 3, 0, 4, 2], "Gagal menangani huruf kembar di mode Numbered"
        )

    def test_5_file_encryption_integrity(self):
        """Test integritas data biner (File)"""
        # Simulasi file 10 byte
        original_data = b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a"
        key = "TEST"

        # Encrypt
        encrypted_bytes = ColumnarTransposition.encrypt_bytes(original_data, key)

        # Decrypt
        decrypted_bytes = ColumnarTransposition.decrypt_bytes(encrypted_bytes, key)

        # Potong padding jika ada (decrypt_bytes mengembalikan full grid)
        # cek apakah 10 byte awal sama persis
        self.assertEqual(
            original_data, decrypted_bytes[:10], "Data file rusak setelah dekripsi!"
        )

    def test_6_empty_and_short_input(self):
        """Test input kosong atau lebih pendek dari kunci"""
        # Case Empty
        res = ColumnarTransposition.encrypt_text("", "KEY")
        self.assertEqual(res["ciphertext"], "")

        # Case Pendek (Plaintext < Key length)
        # Plain: "HI", Key: "XYZ" -> Grid 1 baris, padding 1 char (X)
        # H I X -> Baca urutan XYZ -> H I X
        res_short = ColumnarTransposition.encrypt_text("HI", "XYZ", padding_char="X")
        self.assertEqual(len(res_short["ciphertext"]), 3)


if __name__ == "__main__":
    unittest.main()
