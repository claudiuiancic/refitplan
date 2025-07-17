import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparație Excel – vizual compact", layout="wide")
st.title("📊 Comparație compactă între două fișiere Excel")

# ============ CONFIG ===============
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
nume_col = "Nume Magazin"
sag = " ➡️ "

# ============ FUNCȚII ===============
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

# ============ ÎNCĂRCARE ===============
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("🔹 Încarcă PRIMA versiune (.xlsx)", type="xlsx", key="f1")
with col2:
    file2 = st.file_uploader("🔸 Încarcă A DOUA versiune (.xlsx)", type="xlsx", key="f2")

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

            rezultate = []
            styling_mask = []

            for idx in toate_idurile:
                row = {id_col: idx}
                style_row = {}

                in_1 = idx in df1_indexed.index
                in_2 = idx in df2_indexed.index

                if not in_1 and in_2:
                    row[nume_col] = df2_indexed.loc[idx].get(nume_col, "(nou)")
                    for col in selected_columns:
                        row[col] = f"🆕 {df2_indexed.loc[idx].get(col, '')}"
                        style_row[col] = "background-color: #e0f7fa"
                    rezultate.append(row)
                    styling_mask.append(style_row)
                    continue

                if in_1 and not in_2:
                    row[nume_col] = df1_indexed.loc[idx].get(nume_col, "(dispărut)")
                    for col in selected_columns:
                        row[col] = f"{df1_indexed.loc[idx].get(col, '')} ❌"
                        style_row[col] = "background-color: #f0f0f0"
                    rezultate.append(row)
                    styling_mask.append(style_row)
                    continue

                row[nume_col] = df2_indexed.loc[idx].get(nume_col, df1_indexed.loc[idx].get(nume_col, ""))
                for col in selected_columns:
                    val1 = str(df1_indexed.loc[idx].get(col, "")).strip()
                    val2 = str(df2_indexed.loc[idx].get(col, "")).strip()
                    if val1 != val2:
                        row[col] = f"{val1}{sag}{val2}"
                        style_row[col] = "background-color: #ffe6e6"
                    else:
                        row[col] = "-"
                rezultate.append(row)
                styling_mask.append(style_row)

            if rezultate:
                df_final = pd.DataFrame(rezultate)

                def apply_style(df):
                    def highlighter(row):
                        idx = row.name
                        style = styling_mask[idx]
                        return [style.get(col, "") for col in df.columns]
                    return df.style.apply(highlighter, axis=1)

                st.subheader("🔎 Tabel cu diferențele detectate")
                st.dataframe(apply_style(df_final), use_container_width=True)
            else:
                st.info("✔️ Nu s-au găsit diferențe.")