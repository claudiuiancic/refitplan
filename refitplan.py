import streamlit as st
import pandas as pd
import io
import csv

st.set_page_config(page_title="Încărcare CSV - sigur", layout="wide")
st.title("📂 Încărcare fișier CSV cu antet 'Nr. mag.' și filtrare coloane")

uploaded_file = st.file_uploader("Încarcă fișierul CSV", type="csv")

def detect_separator(text_sample):
    try:
        dialect = csv.Sniffer().sniff(text_sample)
        return dialect.delimiter
    except:
        return ','  # fallback

if uploaded_file:
    try:
        content = uploaded_file.read()
        text = content.decode("utf-8", errors="replace")
        st.write(f"✔️ Fișier decodat, lungime: {len(text)} caractere")

        # Eșantion pentru detectare separator
        sample = "\n".join(text.splitlines()[:50])
        separator = detect_separator(sample)
        st.info(f"🧭 Separator detectat: `{separator}`")

        # Încearcă citirea completă cu separatorul detectat
        df_raw = pd.read_csv(io.StringIO(text), header=None, sep=separator)
        st.write(f"✅ DataFrame citit: {df_raw.shape[0]} rânduri, {df_raw.shape[1]} coloane")

        # Caută rândul cu "Nr. mag."
        header_row_index = df_raw[df_raw.iloc[:, 0] == "Nr. mag."].index
        if len(header_row_index) == 0:
            st.error("❌ Nu s-a găsit rândul cu antet 'Nr. mag.' în prima coloană.")
        else:
            header_row = header_row_index[0]
            st.success(f"✅ Rândul {header_row} a fost identificat ca antet.")

            new_header = df_raw.iloc[header_row].astype(str).fillna('').tolist()
            df_clean = df_raw.iloc[header_row + 1:].copy()
            df_clean.columns = new_header
            df_clean.reset_index(drop=True, inplace=True)

            # Coloane de păstrat
            coloane_de_pastrat = [
                "Nr. mag.",
                "Nume Magazin",
                "Shop Format (alocare)",
                "Cluster Size",
                "Proiect",
                "Data inchidere",
                "Data redeschidere",
                "Orar Luni-Sambata"
            ]

            coloane_existente = [col for col in coloane_de_pastrat if col in df_clean.columns]
            coloane_lipsa = [col for col in coloane_de_pastrat if col not in df_clean.columns]

            if coloane_lipsa:
                st.warning(f"⚠️ Următoarele coloane lipsesc din fișier: {coloane_lipsa}")

            if not coloane_existente:
                st.error("❌ Nicio coloană relevantă nu a fost găsită.")
            else:
                df_filtrat = df_clean[coloane_existente].copy()
                st.success(f"✅ {len(coloane_existente)} coloane păstrate.")
                st.dataframe(df_filtrat.head())

    except Exception as e:
        st.exception(f"❌ Eroare generală: {e}")