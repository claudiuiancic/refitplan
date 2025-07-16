import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Pas 1 - CSV robust", layout="wide")
st.title("📂 Pas 1: Încărcare fișier și detecție antet 'Nr. mag.'")

uploaded_file = st.file_uploader("Încarcă un fișier CSV", type="csv")

if uploaded_file:
    try:
        st.write("📥 Fișierul a fost încărcat. Se citește conținutul...")

        content = uploaded_file.read()
        st.write(f"✔️ Fișier citit, lungime: {len(content)} bytes")

        text = content.decode("utf-8", errors="replace")
        st.write("✔️ Conținut decodat în UTF-8")

        st.write("🔄 Se construiește DataFrame brut (fără antet, sep=';')...")
        df_raw = pd.read_csv(io.StringIO(text), header=None, sep=";")
        st.write(f"✔️ DataFrame citit: {df_raw.shape[0]} rânduri, {df_raw.shape[1]} coloane")

        st.write("🔍 Se caută rândul cu antet care începe cu 'Nr. mag.'...")
        header_row_index = df_raw[df_raw.iloc[:, 0] == "Nr. mag."].index

        if len(header_row_index) == 0:
            st.error("❌ Nu s-a găsit niciun rând unde prima coloană este 'Nr. mag.'")
        else:
            header_row = header_row_index[0]
            st.write(f"✅ Antet găsit pe rândul index {header_row}")

            new_header = df_raw.iloc[header_row].astype(str).tolist()
            st.write("🧾 Antet extras:", new_header)

            st.write("✂️ Se păstrează doar rândurile sub antet...")
            df_clean = df_raw.iloc[header_row + 1:].copy()
            df_clean.columns = new_header
            df_clean.reset_index(drop=True, inplace=True)

            st.success("✅ Datele au fost curățate cu succes. Mai jos sunt primele 5 rânduri:")
            st.dataframe(df_clean.head())

    except Exception as e:
        st.exception(f"❌ Eroare detectată: {e}")