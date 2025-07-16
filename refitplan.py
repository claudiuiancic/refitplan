import streamlit as st
import pandas as pd
import io

st.set_page_config(page_title="Încărcare CSV cu antet personalizat", layout="wide")
st.title("🧪 Încărcare fișier CSV cu antet pe rând selectabil")

uploaded_file = st.file_uploader("Încarcă fișierul CSV", type="csv")

if uploaded_file:
    content = uploaded_file.read().decode("utf-8", errors="replace")
    lines = content.splitlines()

    st.subheader("📄 Primele 10 rânduri (text brut)")
    for i, line in enumerate(lines[:10]):
        st.text(f"{i}: {line}")

    max_row = min(len(lines) - 1, 20)
    header_row = st.slider("Alege rândul care conține antetul", 0, max_row, value=3)

    try:
        df_full = pd.read_csv(io.StringIO(content), header=None)

        # Extract header și curățare
        raw_header = df_full.iloc[header_row].astype(str).fillna('').tolist()

        # Înlocuiește golurile
        header_clean = [
            col if col.strip() != '' else f"Col_{i}"
            for i, col in enumerate(raw_header)
        ]

        # Verifică duplicate și redenumește
        from collections import Counter
        counter = Counter()
        final_header = []
        for col in header_clean:
            count = counter[col]
            final_name = f"{col}_{count}" if count > 0 else col
            final_header.append(final_name)
            counter[col] += 1

        df_clean = df_full.iloc[header_row + 1:].copy()
        df_clean.columns = final_header
        df_clean.reset_index(drop=True, inplace=True)

        st.success("✅ Antet aplicat și tabelul a fost citit corect!")
        st.write("🔹 Coloane detectate:", final_header)
        st.dataframe(df_clean.head())

    except Exception as e:
        st.exception(f"❌ Eroare: {e}")