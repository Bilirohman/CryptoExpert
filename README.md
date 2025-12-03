# CryptoExpert: Columnar Transposition Cipher

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**CryptoExpert** adalah platform edukasi dan visualisasi kriptografi interaktif yang berfokus pada algoritma **Columnar Transposition Cipher**. Aplikasi ini dibangun menggunakan Python dan Streamlit, dirancang untuk membantu pengguna memahami mekanisme enkripsi dan dekripsi Columnar Transposition melalui visualisasi langkah-demi-langkah.

## Website CryptoExpert
https://cryptoexpert.streamlit.app/

## Anggota
| No. | Nama                      | NPM    |
| :-- | :------------------------ | :----- | 
| 1   | Gunawan Sabili Rohman     | 140810230018 | 
| 2   | Maritza Ratnamaya Nugroho | 140810230076 | 

## Fitur Utama

* **Enkripsi Teks**
    * Input teks fleksibel.
    * Opsi **Padding Otomatis** (karakter pengisi) untuk melengkapi blok matriks.
    * Dukungan mode kunci: *Stable* (urutan kemunculan) dan *Numbered* (A1, A2, dst).
* **Dekripsi Teks**
    * Mengembalikan *Ciphertext* menjadi *Plaintext* menggunakan kunci yang sama.
* **Pemrosesan File**
    * Melakukan enkripsi dan dekripsi pada input file.

## Tambahan
* **Visualisasi Step :**
    * Visualisasi dan animasi pembentukan matriks (Grid) untuk proses dekripsi dan enkripsi teks

## Teknologi yang Digunakan
Proyek ini dibangun di atas ekosistem Python dengan:

* **[Streamlit](https://streamlit.io/):** Framework utama untuk antarmuka pengguna (UI) web interaktif.
* **[Pandas](https://pandas.pydata.org/):** Manipulasi data untuk struktur matriks/tabel enkripsi.

## Struktur Proyek

Proyek ini menerapkan arsitektur modular untuk memisahkan *logic*, *view*, dan *style* agar kode mudah dipelihara (*maintainable*):

```text
CRYPTOGRAPHY/
├── assets/             # Aset statis dan styling
│   └── styles.py       # Konfigurasi CSS global
├── src/                # Backend
│   ├── cipher.py       # Implementasi algoritma Columnar Transposition
│   ├── components.py   # Komponen UI reusable
│   ├── file_handler.py # Utilitas pembacaan/penulisan file
│   ├── utils.py        # Fungsi bantuan umum
│   └── visuals.py      # Logika visualisasi grafis
├── views/              # Frontend
│   ├── tab_decrypt.py  # Halaman Dekripsi
│   ├── tab_encrypt.py  # Halaman Enkripsi
│   └── tab_file.py     # Halaman Proses File
├── test/               # Unit Testing
│   └── test_cipher.py  # Pengujian logika cipher
├── app.py              # Entry point aplikasi
├── requirements.txt    # Daftar dependensi
└── README.md           # Dokumentasi proyek
```

## Instalasi dan Penggunaan

### 1. Prasyarat
Python 3.9 atau versi yang lebih baru.

### 2. Kloning Repositori
```Bash
git clone https://github.com/Bilirohman/CryptoExpert.git
cd crypto-expert
```
### 3. Buat Virtual Environment (Disarankan)
```Bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```
### 4. Instal Dependensi 

```Bash
pip install -r requirements.txt
```

### 5. Jalankan Aplikasi
```Bash
streamlit run app.py
```
Aplikasi akan otomatis terbuka di browser default dengan alamat http://localhost:8501.

## Lisensi
Didistribusikan di bawah Lisensi MIT. Lihat file LICENSE untuk informasi lebih lanjut.
