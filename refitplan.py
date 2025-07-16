import streamlit as st
import pandas as pd
import io
import csv

st.set_page_config(page_title="Pas 1 – Încărcare CSV curățat", layout="wide")
st.title("📂 Încărcare fișier CSV cu antet detectat și coloane filtrate")

uploaded_file = st.file_uploader("Încarcă un fișier CSV", type="csv")

def try_read_csv(text, sep):
    try:
        return pd.read_csv(io.StringIO(text), header=None, sep=sep)
    except Exception as e:
        st.warning(f"Eșec la parsare cu separator '{sep}': {e}")
        return None

def detect_separator(text_sample):
    try:
        dialect = csv.Sniffer().sniff(text_sample)
        return dialect.delimiter
    except:
        return ','

if uploaded_file:
    try:
        content = uploaded_file.read()
        text = content.decode("utf-8", errors="replace")
        st.write(f"✔️ Fișier decodat, lungime: {len(text)} caractere")

        # Încearcă automat să detecteze separatorul
        st.write("🔍 Încearcă sep=';'...")
        df_raw = try_read_csv(text, sep=';')

        if df_raw is None:
            st.write("🔍 Încearcă sep=','...")
            df_raw = try_read_csv(text, sep=',')

        if df_raw is None:
            st.write("🧪 Încercare cu detectare automată...")
            sample = "\n".join(text.splitlines()[:20])
            detected_sep = detect_separator(sample)
            st.info(f"🧭 Separator detectat automat: '{detected_sep}'")
            df_raw = try_read_csv(text, sep=detected_sep)

        if df_raw is None:
            st.error("❌ Nu s-a putut citi fișierul cu niciun separator.")
        else:
            st.write(f"✅ DataFrame citit: {df_raw.shape[0]} rânduri, {df_raw.shape[1]} coloane")

            # Caută rândul unde prima coloană este "Nr. mag."
            header_row_index = df_raw[df_raw.iloc[:, 0] == "Nr. mag."].index

            if len(header_row_index) == 0:
                st.error("❌ Nu s-a găsit rândul cu antet 'Nr. mag.' în prima coloană.")
            else:
                header_row = header_row_index[0]
                st.success(f"✅ Antet detectat pe rândul {header_row}")

                # Extrage antetul
                new_header = df_raw.iloc[header_row].astype(str).fillna('').tolist()

                # Construiește DataFrame curățat
                df_clean = df_raw.iloc[header_row + 1:].copy()
                df_clean.columns = new_header
                df_clean.reset_index(drop=True, inplace=True)

                # Coloanele de păstrat
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

                # Verificare coloane lipsă
                coloane_existente = [col for col in coloane_de_pastrat if col in df_clean.columns]
                coloane_lipsa = [col for col in coloane_de_pastrat if col not in df_clean.columns]

                if coloane_lipsa:
                    st.warning(f"⚠️ Următoarele coloane lipsesc din fișier: {coloane_lipsa}")

                if not coloane_existente:
                    st.error("❌ Nicio coloană relevantă nu a fost găsită în fișier.")
                else:
                    df_filtrat = df_clean[coloane_existente].copy()
                    st.success(f"✅ {len(coloane_existente)} coloane păstrate: {coloane_existente}")
                    st.dataframe(df_filtrat.head())

    except Exception as e:
        st.exception(f"❌ Eroare generală: {e}")