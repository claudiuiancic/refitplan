import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparație Excel", layout="wide")
st.title("📊 Comparație între două fișiere Excel: 'Refit plan 2025'")

# ===============================
# Configurări
coloane_de_interes = [
    "Nr. mag.",
    "Nume Magazin",
    "Shop Format (alocare)",
    "Cluster Size",
    "Proiect",
    "Data inchidere",
    "Data redeschidere",
    "Orar Luni-Sambata"
]
sheet_nume = "Refit plan 2025"

# ===============================
def incarca_fisier_excel(uploaded_file, label):
    try:
        df_raw = pd.read_excel(uploaded_file, sheet_name=sheet_nume, header=None, dtype=str)

        header_idx = df_raw[df_raw.iloc[:, 0] == "Nr. mag."].index
        if len(header_idx) == 0:
            st.error(f"❌ [{label}] Antetul 'Nr. mag.' nu a fost găsit.")
            return None

        header_row = header_idx[0]
        header = df_raw.iloc[header_row].fillna('').astype(str).tolist()

        df = df_raw.iloc[header_row + 1:].copy()
        df.columns = header
        df.reset_index(drop=True, inplace=True)

        # Păstrează doar coloanele existente
        coloane_existente = [col for col in coloane_de_interes if col in df.columns]
        df = df[coloane_existente].copy()

        # Completează lipsurile pentru consistență
        for col in coloane_de_interes:
            if col not in df.columns:
                df[col] = ""

        return df
    except Exception as e:
        st.error(f"❌ Eroare la citirea fișierului [{label}]: {e}")
        return None

# ===============================
# Încărcare fișiere

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("Încarcă prima versiune (.xlsx)", type="xlsx", key="f1")
with col2:
    file2 = st.file_uploader("Încarcă a doua versiune (.xlsx)", type="xlsx", key="f2")

if file1 and file2:
    df1 = incarca_fisier_excel(file1, "Versiunea 1")
    df2 = incarca_fisier_excel(file2, "Versiunea 2")

    if df1 is not None and df2 is not None:
        id_col = "Nr. mag."
        df1[id_col] = df1[id_col].astype(str).str.zfill(4)
        df2[id_col] = df2[id_col].astype(str).str.zfill(4)

        df1_indexed = df1.set_index(id_col)
        df2_indexed = df2.set_index(id_col)

        iduri_comune = df1_indexed.index.intersection(df2_indexed.index)

        diferente = []
        for idx in sorted(iduri_comune):
            row1 = df1_indexed.loc[idx]
            row2 = df2_indexed.loc[idx]
            for col in coloane_de_interes:
                val1 = str(row1.get(col, "")).strip()
                val2 = str(row2.get(col, "")).strip()
                if val1 != val2:
                    diferente.append({
                        "Nr. mag.": idx,
                        "Coloana": col,
                        "Valoare inițială": val1,
                        "Valoare nouă": val2
                    })

        if diferente:
            df_dif = pd.DataFrame(diferente)
            st.success(f"✅ {len(df_dif)} diferențe găsite.")
            st.dataframe(df_dif)

            csv_data = df_dif.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Descarcă diferențele (.csv)", csv_data, "diferente.csv")
        else:
            st.info("✔️ Nu s-au găsit diferențe între versiunile comparate.")