import streamlit as st
from src.cipher import ColumnarTransposition
from src.visuals import render_grid
from src import utils
from src import components


def reset_visuals():
    st.session_state.step_index = 0
    st.session_state.anim_phase = "write"


def render(key_input: str, padding_char: str, key_mode: str):
    col_input, col_output = st.columns([1, 1], gap="large")

    # --- KOLOM KIRI: INPUT ---
    with col_input:
        st.subheader("Input Plaintext")
        plaintext = st.text_area(
            "Masukkan pesan yang akan dienkripsi:",
            height=200,  
            value="KRIPTOGRAFI SERU DAN MENYENANGKAN",
        )

        if st.button("Enkripsi Sekarang", type="primary", use_container_width=True):
            valid, msg = utils.validate_key(key_input)
            if not valid:
                st.error(msg)
            else:
                st.session_state.cipher_result = ColumnarTransposition.encrypt_text(
                    plaintext, key_input, padding_char, key_mode
                )
                reset_visuals()
                st.success("Enkripsi Berhasil!")

    # --- KOLOM KANAN: OUTPUT ---
    with col_output:
        st.subheader("Hasil Ciphertext")

        res = st.session_state.cipher_result
        if res:
            st.code(res["ciphertext"], language="text")

            st.caption(
                f"Original: {len(plaintext)} chars | Padded: {len(res['padded_text'])} chars"
            )

            st.download_button(
                label="Simpan Ciphertext (.txt)",
                data=res["ciphertext"],
                file_name="ciphertext.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.info("Waiting for Input...", icon="⏳")

    # --- BAGIAN VISUALISASI ---
    if st.session_state.cipher_result:
        st.divider()
        st.header("Visualisasi Enkripsi")
        res = st.session_state.cipher_result

        phase_selection = st.radio(
            "Pilih Fase:",
            ["1. Pembuatan Grid (Input)", "2. Pembacaan Kolom (Output)"],
            horizontal=True,
            key="phase_enc",
        )

        new_phase = "write" if "1." in phase_selection else "read"
        if st.session_state.anim_phase != new_phase:
            st.session_state.anim_phase = new_phase

        # Penentuan step data
        if st.session_state.anim_phase == "write":
            steps = res["fill_steps"]
            action_label = "Menulis ke Grid"
            desc_fmt = "Mengisi karakter **'{char}'** ke Baris {row}, Kolom {col}"
        else:
            steps = res["read_steps"]
            action_label = "Membaca dari Grid"
            desc_fmt = "Mengambil karakter **'{char}'** dari Baris {row}, Kolom {col}"

        # Navigasi
        components.render_navigation_controls(
            "enc", st.session_state.step_index, len(steps), "step_index"
        )

        current_idx = st.session_state.step_index
        st.progress(current_idx / len(steps) if len(steps) > 0 else 0)

        active_cell = None
        desc_text = "Siap memulai..."
        if 0 < current_idx <= len(steps):
            s = steps[current_idx - 1]
            active_cell = (s[0], s[1])
            desc_text = desc_fmt.format(char=s[2], row=s[0] + 1, col=s[1] + 1)

        components.render_step_info(current_idx, len(steps), action_label, desc_text)

        # Render Grid
        partial_grid = (
            [["" for _ in range(len(key_input))] for _ in range(len(res["grid"]))]
            if st.session_state.anim_phase == "write"
            else res["grid"]
        )
    
        if st.session_state.anim_phase == "write":
            for i in range(current_idx):
                r, c, ch = steps[i]
                partial_grid[r][c] = ch

        render_grid(
            partial_grid,
            key_input,
            res["order"],
            active_cell,
            st.session_state.anim_phase,
        )

        # Tampilkan buffer hasil sementara
        accumulated = "".join([s[2] for s in steps[:current_idx]])
        st.text_area("Buffer Hasil:", value=accumulated, height=70, disabled=True)
