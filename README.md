# 🔐 CryptoExpert: Columnar Transposition Cipher

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-1.30.0-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)

**CryptoExpert** adalah platform edukasi dan visualisasi kriptografi interaktif yang berfokus pada algoritma **Columnar Transposition Cipher**. Aplikasi ini dibangun menggunakan Python dan Streamlit, dirancang untuk membantu pengguna memahami mekanisme enkripsi dan dekripsi klasik melalui visualisasi langkah-demi-langkah.

## Our Team
| No. | Nama               | NPM    |
| :-- | :------------------------ | :----- | 
| 1   | Gunawan Sabili Rohman     | 140810230018 | 
| 2   | Maritza Ratnamaya Nugroho | 140810230076 | 

## 📋 Fitur Utama

Aplikasi ini menawarkan fitur komprehensif untuk kebutuhan pembelajaran dan pemrosesan data sederhana:

* **Enkripsi Teks Interaktif:**
    * Input teks fleksibel.
    * Visualisasi pembentukan matriks (Grid).
    * Opsi **Padding Otomatis** (karakter pengisi) untuk melengkapi blok matriks.
    * Dukungan mode kunci: *Stable* (urutan kemunculan) dan *Numbered* (A1, A2, dst).
* **Dekripsi Teks:**
    * Mengembalikan *Ciphertext* menjadi *Plaintext* menggunakan kunci yang sama.
    * Logika rekonstruksi kolom yang presisi.
* **Pemrosesan File:**
    * Kemampuan untuk melakukan enkripsi/dekripsi pada file teks (melalui modul `tab_file`).
* **Visualisasi & Animasi:**
    * Antarmuka modern dan responsif.
    * Penjelasan visual bagaimana kunci mempengaruhi pengacakan kolom.

## 🛠️ Teknologi yang Digunakan

Proyek ini dibangun di atas ekosistem Python yang kuat:

* **[Streamlit](https://streamlit.io/):** Framework utama untuk antarmuka pengguna (UI) web yang interaktif.
* **[Pandas](https://pandas.pydata.org/):** Manipulasi data untuk struktur matriks/tabel enkripsi.
* **[Plotly](https://plotly.com/):** (Opsional/Dependensi) Untuk visualisasi data tingkat lanjut jika diperlukan.

## 📂 Struktur Proyek

Proyek ini menerapkan arsitektur modular untuk memisahkan *logic*, *view*, dan *style* agar kode mudah dipelihara (*maintainable*):

```text
CRYPTOGRAPHY/
├── assets/             # Aset statis dan styling
│   └── styles.py       # Konfigurasi CSS global
├── src/                # Core Logic (Backend)
│   ├── cipher.py       # Implementasi algoritma Columnar Transposition
│   ├── components.py   # Komponen UI reusable
│   ├── file_handler.py # Utilitas pembacaan/penulisan file
│   ├── utils.py        # Fungsi bantuan umum
│   └── visuals.py      # Logika visualisasi grafis
├── views/              # UI Pages (Frontend)
│   ├── tab_decrypt.py  # Halaman Dekripsi
│   ├── tab_encrypt.py  # Halaman Enkripsi
│   └── tab_file.py     # Halaman Proses File
├── test/               # Unit Testing
│   └── test_cipher.py  # Pengujian logika cipher
├── app.py              # Entry point aplikasi
├── requirements.txt    # Daftar dependensi
└── README.md           # Dokumentasi proyek
```

## 🚀 Instalasi dan Penggunaan
Ikuti langkah-langkah berikut untuk menjalankan aplikasi di lingkungan lokal Anda:

### 1. Prasyarat
Pastikan Anda telah menginstal Python 3.9 atau versi yang lebih baru.

### 2. Kloning Repositori
```Bash
git clone https://github.com/Bilirohman/cryptography.git
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
Aplikasi akan otomatis terbuka di browser default Anda pada alamat http://localhost:8501.

## 📄 Lisensi
Didistribusikan di bawah Lisensi MIT. Lihat file LICENSE untuk informasi lebih lanjut.