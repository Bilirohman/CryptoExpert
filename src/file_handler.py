import io


class FileHandler:
    """
    Menangani input/output file byte-per-byte.
    """

    @staticmethod
    def read_file(uploaded_file):
        """Membaca Streamlit UploadedFile sebagai bytes."""
        if uploaded_file is not None:
            return uploaded_file.getvalue()
        return None

    @staticmethod
    def create_download_link(data: bytes, filename: str):
        """
        Fungsi ini biasanya ditangani langsung oleh st.download_button,
        tapi di sini kita siapkan objek BytesIO-nya.
        """
        return io.BytesIO(data)
