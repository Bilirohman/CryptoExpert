import streamlit as st
import assets.styles as styles
from views import tab_encrypt, tab_decrypt, tab_file

# --- Konfigurasi Halaman ---
st.set_page_config(
    page_title="CryptoExpert: Columnar Transposition",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- INJEKSI GLOBAL CSS ---
st.markdown(styles.get_global_css(), unsafe_allow_html=True)

# --- State Management Global ---
default_states = {
    "step_index": 0,
    "anim_phase": "write",
    "cipher_result": None,
    "decrypt_result": None,
    "file_viz_data": None,
    "file_step_index": 0,
    "file_anim_phase": "write",
}

for key, default_val in default_states.items():
    if key not in st.session_state:
        st.session_state[key] = default_val


def main():
    # --- Header ---
    st.markdown(
        '<h1 class="main-title">🔐 Columnar Transposition Cipher</h1>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-title">Platform Edukasi & Visualisasi Kriptografi</p>',
        unsafe_allow_html=True,
    )

    # --- Sidebar Configuration ---
    with st.sidebar:
        st.header("⚙️ Konfigurasi")
        mode = st.selectbox(
            "Pilih Operasi", ["Enkripsi Teks", "Dekripsi Teks", "Proses File"]
        )

        st.subheader("Parameter Kunci")
        key_input = st.text_input(
            "Masukkan Kunci (Key)", value="TEKNIK", help="Kunci pengacakan kolom"
        )
        key_mode = st.radio(
            "Mode Duplikat Kunci",
            ["stable", "numbered"],
            help="Stable: Sesuai urutan muncul. Numbered: A1, A2...",
        )

        # Logic Padding Hanya untuk Enkripsi Teks
        padding_char = "X"
        if mode == "Enkripsi Teks":
            if st.checkbox("Padding Otomatis", value=True):
                padding_char = st.text_input("Karakter Padding", value="X", max_chars=1)
            else:
                padding_char = ""

        st.info(
            "ℹ️ **Our Team**\n\nGunawan Sabili Rohman | 230018\nMaritza Ratnamaya Nugroho | 230076"
        )

    # --- Routing ke Views ---
    if mode == "Enkripsi Teks":
        tab_encrypt.render(key_input, padding_char, key_mode)
    elif mode == "Dekripsi Teks":
        tab_decrypt.render(key_input, key_mode)
    elif mode == "Proses File":
        tab_file.render(key_input)


if __name__ == "__main__":
    main()
