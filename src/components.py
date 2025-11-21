import streamlit as st


def render_navigation_controls(
    key_prefix: str,
    current_step: int,
    total_steps: int,
    state_key_index: str = "step_index",
):
    """
    Komponen reusable untuk tombol navigasi (First, Prev, Next, Last).

    Args:
        key_prefix (str): Prefix unik untuk key widget Streamlit.
        current_step (int): Langkah saat ini.
        total_steps (int): Total langkah.
        state_key_index (str): Key di session_state yang menyimpan index langkah (default: 'step_index').
    """

    # Menggunakan 4 kolom simetris
    c1, c2, c3, c4 = st.columns(4)

    # Tombol Awal
    if c1.button("⏮️ Awal", key=f"{key_prefix}_start", disabled=(current_step == 0)):
        st.session_state[state_key_index] = 0
        st.rerun()

    # Tombol Mundur
    if c2.button("◀️ Mundur", key=f"{key_prefix}_prev", disabled=(current_step == 0)):
        st.session_state[state_key_index] = max(0, current_step - 1)
        st.rerun()

    # Tombol Maju
    if c3.button(
        "Maju ▶️", key=f"{key_prefix}_next", disabled=(current_step == total_steps)
    ):
        st.session_state[state_key_index] = min(total_steps, current_step + 1)
        st.rerun()

    # Tombol Akhir
    if c4.button(
        "⏭️ Akhir", key=f"{key_prefix}_end", disabled=(current_step == total_steps)
    ):
        st.session_state[state_key_index] = total_steps
        st.rerun()


def render_step_info(idx: int, total: int, action_label: str, description: str):
    """
    Merender kotak informasi langkah dengan styling yang konsisten.
    """
    st.markdown(
        f"""
        <div class="step-box">
            <span class="step-title">{action_label} - Langkah {idx}/{total}</span>
            <span style="font-family:monospace; font-size:1.1em;">{description}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )
