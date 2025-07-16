import streamlit as st
import pandas as pd
import io

st.title("🧪 Încărcare CSV cu antet personalizat")

uploaded_file = st.file_uploader("Încarcă fișierul CSV", type="csv")

if uploaded_file:
    # Citește tot fișierul în memorie
    content = uploaded_file.read().decode("utf-8", errors="replace")
    raw_data = list(csv_line for csv_line in content.splitlines())
    total_lines = len(raw_data)

    # Afișează primele 10 rânduri ca previzualizare
    st.subheader("📍 Primele 10 rânduri (raw text)")
    for i, line in enumerate(raw_data[:10]):
        st.text(f"{i}: {line}")

    header_row = st.slider("Selectează indexul rândului care conține antetul (începând de la 0)", 0, min(total_lines - 1, 20), value=3)

    try:
        # Reîncarcă în DataFrame cu header=None
        df_full = pd.read_csv(io.StringIO(content), header=None)
        custom_header = df_full.iloc[header_row].astype(str).tolist()

        # Elimină rândurile de deasupra antetului și setează noul header
        df_clean = df_full.iloc[header_row + 1:].copy()
        df_clean.columns = custom_header
        df_clean.reset_index(drop=True, inplace=True)

        st.success("✅ Fișier citit corect cu antet personalizat.")
        st.write("🔹 Coloane detectate:", list(df_clean.columns))
        st.dataframe(df_clean.head())
    except Exception as e:
        st.exception(f"❌ Eroare: {e}")