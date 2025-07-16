import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparație Excel – complet", layout="wide")
st.title("Comparație între două versiuni de fișiere xlsx")

# ===============================
# Setări
coloane_default = [
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
id_col = "Nr. mag."

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

        df[id_col] = df[id_col].astype(str).str.zfill(4)

        return df
    except Exception as e:
        st.error(f"❌ Eroare la citirea fișierului [{label}]: {e}")
        return None

# ===============================
# Încărcare fișiere

col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("🔹 Încarcă versiunea VECHE (.xlsx)", type="xlsx", key="f1")
with col2:
    file2 = st.file_uploader("🔸 Încarcă versiunea NOUA (.xlsx)", type="xlsx", key="f2")

if file1 and file2:
    df1 = incarca_fisier_excel(file1, "Versiunea 1")
    df2 = incarca_fisier_excel(file2, "Versiunea 2")

    if df1 is not None and df2 is not None:
        toate_coloanele = sorted(set(df1.columns).union(df2.columns) - {id_col})

        st.subheader("🧩 Selectează coloanele pentru comparație")
        selected_columns = st.multiselect(
            "Coloane de comparat:",
            toate_coloanele,
            default=[col for col in coloane_default if col in toate_coloanele]
        )

        if not selected_columns:
            st.warning("⚠️ Selectează cel puțin o coloană pentru comparație.")
        else:
            df1_indexed = df1.set_index(id_col)
            df2_indexed = df2.set_index(id_col)

            iduri_1 = set(df1_indexed.index)
            iduri_2 = set(df2_indexed.index)
            toate_idurile = sorted(iduri_1.union(iduri_2))

            diferente = []

            for idx in toate_idurile:
                in_v1 = idx in df1_indexed.index
                in_v2 = idx in df2_indexed.index

                if in_v1 and not in_v2:
                    diferente.append({
                        id_col: idx,
                        "Coloana": "(toate)",
                        "Valoare inițială": "EXISTĂ",
                        "Valoare nouă": "NU EXISTĂ",
                        "Tip": "ID dispărut"
                    })
                elif not in_v1 and in_v2:
                    diferente.append({
                        id_col: idx,
                        "Coloana": "(toate)",
                        "Valoare inițială": "NU EXISTĂ",
                        "Valoare nouă": "EXISTĂ",
                        "Tip": "ID nou"
                    })
                else:
                    row1 = df1_indexed.loc[idx]
                    row2 = df2_indexed.loc[idx]
                    for col in selected_columns:
                        val1 = str(row1.get(col, "")).strip()
                        val2 = str(row2.get(col, "")).strip()
                        if val1 != val2:
                            diferente.append({
                                id_col: idx,
                                "Coloana": col,
                                "Valoare inițială": val1,
                                "Valoare nouă": val2,
                                "Tip": "Modificare"
                            })

            if diferente:
                df_dif = pd.DataFrame(diferente)

                st.subheader("📂 Filtru tip diferență")
                tip_selectat = st.selectbox("Afișează doar:", ["Toate", "ID-uri noi", "ID-uri dispărute", "ID-uri cu modificări"])

                if tip_selectat != "Toate":
                    map_tip = {
                        "ID-uri noi": "ID nou",
                        "ID-uri dispărute": "ID dispărut",
                        "ID-uri cu modificări": "Modificare"
                    }
                    df_dif = df_dif[df_dif["Tip"] == map_tip[tip_selectat]]

                st.success(f"✅ {len(df_dif)} diferențe afișate.")

                # Evidențiere stil
                def color_rows(row):
                    if row["Tip"] == "ID nou":
                        return ['background-color: #e0f7fa'] * len(row)
                    elif row["Tip"] == "ID dispărut":
                        return ['background-color: #f0f0f0'] * len(row)
                    elif row["Tip"] == "Modificare":
                        return [
                            'background-color: #ffe6e6' if col in ["Valoare inițială", "Valoare nouă"] else ''
                            for col in row.index
                        ]
                    else:
                        return [''] * len(row)

                styled_df = df_dif.style.apply(color_rows, axis=1)
                st.dataframe(styled_df)

            else:
                st.info("✔️ Nu s-au găsit diferențe.")