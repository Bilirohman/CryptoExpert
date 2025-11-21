# styles.py

# Warna Tema Utama 
THEME_COLOR = "#4B0082"  # Indigo
ACCENT_COLOR = "#d63384"  # Pinkish for details
BG_LIGHT = "#f8f9fa"  # Light Gray


def get_global_css():
    return f"""
<style>
    /* --- 1. LAYOUT UMUM (Dari app.py) --- */
    .main-title {{ font-size: 3em; color: {THEME_COLOR}; text-align: center; font-weight: 700; }}
    .sub-title {{ font-size: 1.2em; color: #666; text-align: center; margin-bottom: 20px; }}
    .stButton>button {{ width: 100%; border-radius: 5px; font-weight: bold; }}
    
    /* --- 2. KOMPONEN STEP INFO (Dari app.py/components) --- */
    .step-box {{ 
        padding: 15px; 
        border-radius: 8px; 
        margin-top: 15px; 
        margin-bottom: 15px;
        background-color: {BG_LIGHT}; 
        border-left: 6px solid {THEME_COLOR};
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        color: #333;
    }}
    .step-title {{ font-weight: bold; color: {THEME_COLOR}; font-size: 1.1em; display: block; margin-bottom: 5px; }}
    
    /* --- 3. TABEL KRIPTOGRAFI (Dari visuals.py) --- */
    .crypto-table {{
        border-collapse: separate;
        border-spacing: 4px;
        width: 100%;
        table-layout: fixed;
        margin-bottom: 15px;
        font-family: 'Courier New', monospace;
        background-color: transparent;
    }}
    .crypto-table td, .crypto-table th {{
        border: 1px solid #444;
        padding: 8px;
        text-align: center;
        height: 50px;
        font-weight: bold;
        font-size: 1.1em;
        border-radius: 4px;
        word-wrap: break-word;
    }}
    
    /* Header & Order Styles */
    .header-cell {{ background-color: #2c3e50 !important; color: #ecf0f1 !important; border: 1px solid #2c3e50 !important; }}
    .order-cell {{ background-color: #34495e !important; color: #f1c40f !important; border: 1px solid #34495e !important; }}
    
    /* Cell Styles */
    .filled-cell {{ 
        background-color: #ecf0f1 !important; 
        color: #2c3e50 !important; 
        border: 1px solid #bdc3c7 !important; 
    }}
    
    .result-cell {{ 
        background-color: #ecf0f1 !important; 
        color: #2c3e50 !important; 
        border: 2px solid #bdc3c7 !important; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }} 
    
    .empty-cell {{ background-color: {BG_LIGHT} !important; border: 1px dashed #ccc !important; color: transparent !important; }}
    .padding-cell {{ color: #95a5a6 !important; font-style: italic; background-color: #eef2f3 !important; }}
    
    /* Animation Styles */
    .active-write {{ background-color: #3498db !important; color: #ffffff !important; transform: scale(1.05); border: 2px solid #2980b9 !important; z-index: 10; }}
    .active-read {{ background-color: #e74c3c !important; color: #ffffff !important; transform: scale(1.05); border: 2px solid #c0392b !important; z-index: 10; }}
</style>
"""
