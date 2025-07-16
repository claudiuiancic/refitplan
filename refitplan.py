# utilitare pentru compararea schimbarilor intre doua versiuni

import streamlit as st
import pandas as pd

st.title("Comparație versiuni CSV (Export Excel UTF-8)")

# Încarcă cele două fișiere
uploaded_file1 = st.file_uploader("Încarcă prima versiune a fișierului CSV", type=["csv"], key="file1")
uploaded_file2 = st.file_uploader("Încarcă a doua versiune a fișierului CSV", type=["csv"], key="file2")

if uploaded_file1 and uploaded_file2:
    # Citire CSV, cu rândul 4 ca header (index 3)
    df1 = pd.read_csv(uploaded_file1, header=3)
    df2 = pd.read_csv(uploaded_file2, header=3)

    # Asigură-te că ID-ul este citit ca string (coduri din 4 cifre)
    df1.iloc[:, 0] = df1.iloc[:, 0].astype(str).str.zfill(4)
    df2.iloc[:, 0] = df2.iloc[:, 0].astype(str).str.zfill(4)

    id_col = df1.columns[0]  # Presupunem că prima coloană este ID-ul
    common_ids = set(df1[id_col]).intersection(set(df2[id_col]))

    st.success(f"Fișierele conțin {len(common_ids)} ID-uri comune.")

    # Alegerea coloanelor relevante pentru comparație
    all_columns = list(df1.columns[1:])  # Excludem coloana ID
    selected_columns = st.multiselect("Selectează coloanele care te interesează pentru comparație", all_columns, default=all_columns)

    if selected_columns:
        diffs = []

        # Indexare după ID pentru comparație rapidă
        df1_indexed = df1.set_index(id_col)
        df2_indexed = df2.set_index(id_col)

        for id_val in sorted(common_ids):
            row1 = df1_indexed.loc[id_val]
            row2 = df2_indexed.loc[id_val]

            for col in selected_columns:
                val1 = row1[col] if col in row1 else None
                val2 = row2[col] if col in row2 else None
                if pd.isna(val1): val1 = ''
                if pd.isna(val2): val2 = ''
                if val1 != val2:
                    diffs.append({
                        "Cod ID": id_val,
                        "Coloana": col,
                        "Valoare veche": val1,
                        "Valoare nouă": val2
                    })

        if diffs:
            diffs_df = pd.DataFrame(diffs)
            st.subheader("Diferențe detectate")
            st.dataframe(diffs_df)
        else:
            st.info("Nu s-au găsit diferențe în coloanele selectate.")