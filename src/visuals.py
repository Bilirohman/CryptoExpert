import streamlit as st
import math
import html

def render_grid(grid, key, order, active_cell=None, action_type="read"):
    """Merender grid TEKS."""

    html_table = '<table class="crypto-table">'

    # Header & Order
    safe_key = [html.escape(k) for k in key]

    html_table += (
        "<tr>"
        + "".join([f'<th class="header-cell">{char}</th>' for char in safe_key])
        + "</tr>"
    )
    display_order = [""] * len(key)
    for rank, original_idx in enumerate(order):
        display_order[original_idx] = rank + 1
    html_table += (
        "<tr>"
        + "".join([f'<td class="order-cell">{r}</td>' for r in display_order])
        + "</tr>"
    )

    # Data Rows
    for r_idx, row in enumerate(grid):
        html_table += "<tr>"
        for c_idx, char in enumerate(row):
            safe_char = html.escape(str(char)) if char != "" else "&nbsp;"

            cell_content = safe_char
            is_active = active_cell and active_cell == (r_idx, c_idx)
            class_name = "empty-cell"

            if is_active:
                class_name = "active-write" if action_type == "write" else "active-read"
            elif char != "":
                class_name = "filled-cell"

            html_table += f'<td class="{class_name}">{cell_content}</td>'
        html_table += "</tr>"
    html_table += "</table>"

    st.markdown(html_table, unsafe_allow_html=True)


def render_bytes_dynamic(
    grid, key, order, active_cell=None, action_type="read", title="Visualisasi Byte"
):
    """Merender grid HEXADECIMAL."""

    html_table = '<table class="crypto-table">'

    # Header
    safe_key = [html.escape(k) for k in key]
    html_table += (
        "<tr>"
        + "".join([f'<th class="header-cell">{char}</th>' for char in safe_key])
        + "</tr>"
    )

    # Order row
    display_order = [""] * len(key)
    for rank, original_idx in enumerate(order):
        display_order[original_idx] = rank + 1
    html_table += (
        "<tr>"
        + "".join([f'<td class="order-cell">{r}</td>' for r in display_order])
        + "</tr>"
    )

    # Data Rows
    for r_idx, row in enumerate(grid):
        html_table += "<tr>"
        for c_idx, val in enumerate(row):
            if val is None:
                hex_str = "&nbsp;"
            elif isinstance(val, int):
                hex_str = f"{val:02X}"
            else:
                hex_str = "PAD"

            is_active = active_cell and active_cell == (r_idx, c_idx)
            class_name = "empty-cell"
            if is_active:
                class_name = "active-write" if action_type == "write" else "active-read"
            elif val is not None:
                if isinstance(val, int) and val == 0:
                    class_name = "filled-cell padding-cell"
                else:
                    class_name = "filled-cell"
            html_table += f'<td class="{class_name}">{hex_str}</td>'
        html_table += "</tr>"
    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)


def render_output_hex_grid(byte_data, num_cols, title="Output Result"):
    st.markdown(f"#### {title}")

    if not byte_data:
        st.info("Belum ada data output.")
        return

    num_rows = math.ceil(len(byte_data) / num_cols)

    html_table = '<table class="crypto-table">'

    idx = 0
    for r in range(num_rows):
        html_table += "<tr>"
        for c in range(num_cols):
            if idx < len(byte_data):
                val = byte_data[idx]
                hex_str = f"{val:02X}" if isinstance(val, int) else "00"
                class_name = "result-cell"
                idx += 1
            else:
                hex_str = "&nbsp;"
                class_name = "empty-cell"

            html_table += f'<td class="{class_name}">{hex_str}</td>'
        html_table += "</tr>"

    html_table += "</table>"
    st.markdown(html_table, unsafe_allow_html=True)
