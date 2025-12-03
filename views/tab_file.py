import streamlit as st
from src.cipher import ColumnarTransposition
from src.file_handler import FileHandler
from src.visuals import render_bytes_dynamic, render_output_hex_grid
from src import components


def reset_file_visuals():
    """Helper internal untuk reset state file"""
    st.session_state.file_step_index = 0
    st.session_state.file_anim_phase = "write"


def render(key_input: str):
    st.subheader("📁 Enkripsi/Dekripsi File")
    components.render_step_info(
        "-",
        "-",
        "Mode Pratinjau",
        "Visualisasi ini mendemonstrasikan bagaimana algoritma Columnar Transposition bekerja menggunakan sampel 50 byte awal data / header file.",
    )

    col_file, col_viz = st.columns([1, 1])

    # --- INPUT SECTION ---
    with col_file:
        uploaded_file = st.file_uploader("Upload File", type=None)
        action = st.radio("Aksi", ["Enkripsi", "Dekripsi"])
        process_btn = st.button("Proses File")

    # --- PROCESS LOGIC ---
    if uploaded_file and process_btn:
        if not key_input:
            st.error("Key wajib diisi!")
        else:
            # Membaca file menggunakan handler
            file_bytes = FileHandler.read_file(uploaded_file)
            sample_bytes = file_bytes[:50]

            if action == "Enkripsi":
                result_bytes = ColumnarTransposition.encrypt_bytes(
                    file_bytes, key_input
                )
                st.session_state.file_viz_data = ColumnarTransposition.get_byte_steps(
                    sample_bytes, key_input, "encrypt"
                )
                with col_viz:
                    st.success(f"Terenkripsi! ({len(result_bytes)} bytes)")
                    st.download_button(
                        f"Download enc_{uploaded_file.name}",
                        result_bytes,
                        file_name=f"enc_{uploaded_file.name}",
                    )
            else:
                try:
                    result_bytes = ColumnarTransposition.decrypt_bytes(
                        file_bytes, key_input
                    )
                    st.session_state.file_viz_data = (
                        ColumnarTransposition.get_byte_steps(
                            sample_bytes, key_input, "decrypt"
                        )
                    )
                    with col_viz:
                        st.success(f"Terdekripsi! ({len(result_bytes)} bytes)")
                        st.download_button(
                            f"Download dec_{uploaded_file.name}",
                            result_bytes,
                            file_name=f"dec_{uploaded_file.name}",
                        )
                except Exception as e:
                    st.error(f"Gagal mendekripsi: {str(e)}")

            reset_file_visuals()

    # --- VISUALIZATION SECTION ---
    if st.session_state.file_viz_data:
        st.divider()
        st.header("Simulasi Visualisasi Byte")
        viz = st.session_state.file_viz_data

        phase_selection = st.radio(
            "Fase:",
            ["1. Input (Write)", "2. Output (Read)"],
            horizontal=True,
            key="f_phase",
        )

        new_phase = "write" if phase_selection == "1. Input (Write)" else "read"
        if st.session_state.file_anim_phase != new_phase:
            st.session_state.file_anim_phase = new_phase

        # Setup Steps Data
        if st.session_state.file_anim_phase == "write":
            steps = viz["fill_steps"]
            action_label = "Menulis Byte"
            desc_fmt = "Menulis 0x{val} ke Baris {row}, Kolom {col}"
        else:
            steps = viz["read_steps"]
            action_label = "Membaca Byte"
            desc_fmt = "Mengambil 0x{val} dari Baris {row}, Kolom {col}"

        # Navigation Controls
        components.render_navigation_controls(
            "file", st.session_state.file_step_index, len(steps), "file_step_index"
        )

        curr_idx = st.session_state.file_step_index
        st.progress(curr_idx / len(steps) if len(steps) > 0 else 0)

        # Step Description Info
        active_cell = None
        desc_text = "Siap..."
        if 0 < curr_idx <= len(steps):
            s = steps[curr_idx - 1]
            active_cell = (s[0], s[1])
            hex_val = f"{s[2]:02X}" if isinstance(s[2], int) else "PAD"
            desc_text = desc_fmt.format(val=hex_val, row=s[0] + 1, col=s[1] + 1)

        components.render_step_info(curr_idx, len(steps), action_label, desc_text)

        # Render Grid Logic
        partial_grid = (
            [[None for _ in range(len(key_input))] for _ in range(len(viz["grid"]))]
            if st.session_state.file_anim_phase == "write"
            else viz["grid"]
        )

        if st.session_state.file_anim_phase == "write":
            for i in range(curr_idx):
                r, c, val = steps[i]
                partial_grid[r][c] = val

        render_bytes_dynamic(
            partial_grid,
            key_input,
            viz["order"],
            active_cell,
            st.session_state.file_anim_phase,
        )

        # Final Output Grid
        st.divider()
        final_output_bytes = [s[2] for s in viz["read_steps"] if isinstance(s[2], int)]
        render_output_hex_grid(
            final_output_bytes, len(key_input), title="Hasil Header (50 Byte)"
        )
