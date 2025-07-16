import streamlit as st
import pandas as pd
import io
from collections import Counter

st.set_page_config(page_title="CSV: Detectare automată antet", layout="wide")
st.title("📊 Încărcare CSV cu antet detectat automat")

uploaded_file = st.file_uploader("Încarcă fișierul CSV exportat din Excel", type="csv")

if uploaded_file:
    try:
        content = uploaded_file.read().decode("utf-8", errors="replace")
        df_all = pd.read_csv(io.StringIO(content), header=None)

        # Caută rândul unde prima coloană este "Nr. mag."
        header_idx = df_all[df_all.iloc[:, 0] == "Nr. mag."].index

        if len(header_idx) == 0:
            st.error("❌ Nu s-a găsit niciun rând unde prima coloană este 'Nr. mag.'")
        else:
            header_row = header_idx[0]
            st.info(f"🔍 Antet detectat automat pe rândul {header_row} (index {header_row})")

            # Extrage antetul și curăță
            raw_header = df_all.iloc[header_row].astype(str).fillna('').tolist()
            cleaned_header = [col.strip() if col.strip() else f"Col_{i}" for i, col in enumerate(raw_header)]

            # Rezolvă duplicate
            counter = Counter()
            final_header = []
            for col in cleaned_header:
                count = counter[col]
                final_col = f"{col}_{count}" if count > 0 else col
                final_header.append(final_col)
                counter[col] += 1

            # Tăiere rânduri de deasupra + reindexare
            df_clean = df_all.iloc[header_row + 1:].copy()
            df_clean.columns = final_header
            df_clean.reset_index(drop=True, inplace=True)

            st.success("✅ Fișier procesat cu succes!")
            st.write("🔹 Coloane detectate:", final_header)
            st.dataframe(df_clean.head())

    except Exception as e:
        st.exception(f"❌ Eroare la procesare: {e}")