import streamlit as st
import pandas as pd
import io
import csv

st.set_page_config(page_title="CSV – detectare separator", layout="wide")
st.title("📂 Încărcare fișier și extragere antet 'Nr. mag.' cu detectare automată separator")

uploaded_file = st.file_uploader("Încarcă fișierul CSV", type="csv")

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

        # Testare separator ; apoi , apoi detectare automată
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
            st.write(f"✅ Fișier citit: {df_raw.shape[0]} rânduri, {df_raw.shape[1]} coloane")

            # Caută rândul cu antet
            header_row_index = df_raw[df_raw.iloc[:, 0] == "Nr. mag."].index

            if len(header_row_index) == 0:
                st.error("❌ Nu s-a găsit rândul cu antet 'Nr. mag.' în prima coloană.")
            else:
                header_row = header_row_index[0]
                st.success(f"✅ Rândul {header_row} a fost identificat ca antet.")

                new_header = df_raw.iloc[header_row].astype(str).tolist()
                df_clean = df_raw.iloc[header_row + 1:].copy()
                df_clean.columns = new_header
                df_clean.reset_index(drop=True, inplace=True)

                st.dataframe(df_clean.head())

    except Exception as e:
        st.exception(f"❌ Eroare generală: {e}")