import streamlit as st
from src.cipher import ColumnarTransposition
from src.visuals import render_grid
from src import components


def reset_visuals():
    st.session_state.step_index = 0
    st.session_state.anim_phase = "write"


def render(key_input: str, key_mode: str):
    col_input, col_output = st.columns([1, 1], gap="large")

    # --- KOLOM KIRI: INPUT ---
    with col_input:
        st.subheader("🔓 Input Ciphertext")
        cipher_in = st.text_area("Masukkan Ciphertext:", height=200)

        if st.button("Buka Pesan (Dekripsi)", type="primary", use_container_width=True):
            if not key_input:
                st.error("Key diperlukan!")
            else:
                try:
                    st.session_state.decrypt_result = (
                        ColumnarTransposition.decrypt_text(
                            cipher_in, key_input, key_mode
                        )
                    )
                    reset_visuals()
                    st.success("Dekripsi Berhasil!")
                except Exception as e:
                    st.error(f"Gagal: {e}")

    # --- KOLOM KANAN: OUTPUT ---
    with col_output:
        st.subheader("📝 Hasil Plaintext")

        res = st.session_state.decrypt_result
        if res:
            st.text_area(
                "Plaintext yang ditemukan:",
                value=res["plaintext"],
                height=120,
                disabled=True,
            )

            st.download_button(
                "💾 Download Plaintext (.txt)",
                data=res["plaintext"],
                file_name="decrypted.txt",
                mime="text/plain",
                use_container_width=True,
            )
        else:
            st.info("Waiting for Input...", icon="⏳")

    # --- BAGIAN VISUALISASI ---
    if st.session_state.decrypt_result:
        st.divider()
        st.header("🎬 Visualisasi Dekripsi")
        res = st.session_state.decrypt_result

        phase_selection = st.radio(
            "Pilih Fase:",
            ["1. Rekonstruksi Grid", "2. Pembacaan Plaintext"],
            horizontal=True,
            key="phase_dec",
        )

        new_phase = "write" if "1." in phase_selection else "read"
        if st.session_state.anim_phase != new_phase:
            st.session_state.anim_phase = new_phase

        if st.session_state.anim_phase == "write":
            steps = res["fill_steps"]
            action_label = "Merekonstruksi Grid"
            desc_fmt = "Mengisi **'{char}'** ke Kolom {col}, Baris {row}"
        else:
            steps = res["read_steps"]
            action_label = "Membaca Plaintext"
            desc_fmt = "Membaca **'{char}'** dari Baris {row}, Kolom {col}"

        components.render_navigation_controls(
            "dec", st.session_state.step_index, len(steps), "step_index"
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
