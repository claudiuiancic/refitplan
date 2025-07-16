import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Pas 1 - Încărcare și curățare CSV", layout="wide")
st.title("📂 Pas 1: Încărcare fișier și extragere antet 'Nr. mag.'")

uploaded_file = st.file_uploader("Încarcă fișierul CSV", type="csv")

if uploaded_file:
    try:
        # Citim conținutul CSV ca text
        content = uploaded_file.read().decode("utf-8", errors="replace")

        # Îl transformăm într-un DataFrame brut fără antet
        df_raw = pd.read_csv(io.StringIO(content), header=None)

        # Căutăm primul rând unde prima coloană este exact "Nr. mag."
        header_row_index = df_raw[df_raw.iloc[:, 0] == "Nr. mag."].index

        if len(header_row_index) == 0:
            st.error("❌ Nu s-a găsit niciun rând unde prima coloană este 'Nr. mag.'")
        else:
            header_row = header_row_index[0]

            # Extragem antetul
            new_header = df_raw.iloc[header_row].astype(str).tolist()

            # Păstrăm doar rândurile de sub antet
            df_clean = df_raw.iloc[header_row + 1:].copy()
            df_clean.columns = new_header
            df_clean.reset_index(drop=True, inplace=True)

            st.success(f"✅ Rândul {header_row} a fost folosit ca antet.")
            st.subheader("🔎 Primele 5 rânduri din tabelul curățat:")
            st.dataframe(df_clean.head())

    except Exception as e:
        st.exception(f"❌ Eroare la procesare: {e}")