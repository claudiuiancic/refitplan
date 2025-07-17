import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparație Excel – complet", layout="wide")
st.title("📊 Comparație între două fișiere Excel (.xlsx)")

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
alt_id_col = "Nume Magazin"
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
        df[alt_id_col] = df[alt_id_col].astype(str).str.strip()

        # ID combinat: Nr. mag. dacă valid, altfel Nume Magazin
        df["_ID"] = df[id_col].where(~df[id_col].isin(["nan", "0nan", "None", "NaN", "", "0000"]), df[alt_id_col])
        return df
    except Exception as e:
        st.error(f"❌ Eroare la citirea fișierului [{label}]: {e}")
        return None

# ============ ÎNCĂRCARE FISIERE ===============
col1, col2 = st.columns(2)
with col1:
    file1 = st.file_uploader("🔹 Încarcă PRIMA versiune (.xlsx)", type="xlsx", key="f1")
with col2:
    file2 = st.file_uploader("🔸 Încarcă A DOUA versiune (.xlsx)", type="xlsx", key="f2")

if file1 and file2:
    df1 = incarca_fisier_excel(file1, "Versiunea 1")
    df2 = incarca_fisier_excel(file2, "Versiunea 2")

    if df1 is not None and df2 is not None:
        toate_coloanele = sorted(set(df1.columns).union(df2.columns) - {id_col, "_ID"})
        st.subheader("🧩 Selectează coloanele pentru comparație")
        selected_columns = st.multiselect(
            "Coloane de comparat:",
            toate_coloanele,
            default=[col for col in coloane_default if col in toate_coloanele]
        )

        if selected_columns:
            df1_indexed = df1.set_index("_ID")
            df2_indexed = df2.set_index("_ID")

            iduri_1 = set(df1_indexed.index)
            iduri_2 = set(df2_indexed.index)
            toate_idurile = sorted(iduri_1.union(iduri_2))

            rezultate_mod = []
            rezultate_nou_disparut = []
            styling_mask = []

            for idx in toate_idurile:
                in_1 = idx in df1_indexed.index
                in_2 = idx in df2_indexed.index

                # ➕ ID nou
                if not in_1 and in_2:
                    row2 = df2_indexed.loc[idx]
                    entry = {
                        "Nr. mag.": row2.get("Nr. mag.", ""),
                        "Nume Magazin": row2.get("Nume Magazin", ""),
                        "Status": "🆕 ID nou"
                    }
                    rezultate_nou_disparut.append(entry)
                    continue

                # ➖ ID dispărut
                if in_1 and not in_2:
                    row1 = df1_indexed.loc[idx]
                    entry = {
                        "Nr. mag.": row1.get("Nr. mag.", ""),
                        "Nume Magazin": row1.get("Nume Magazin", ""),
                        "Status": "❌ ID dispărut"
                    }
                    rezultate_nou_disparut.append(entry)
                    continue

                # 🔁 Modificări reale
                row1 = df1_indexed.loc[idx]
                row2 = df2_indexed.loc[idx]
                modificari = {}
                style_row = {}

                for col in selected_columns:
                    val1 = str(row1.get(col, "")).strip()
                    val2 = str(row2.get(col, "")).strip()
                    if val1 != val2:
                        modificari[col] = f"{val1}{sag}{val2}"
                        style_row[col] = "background-color: #ffe6e6"

                if modificari:
                    entry = {
                        "Nr. mag.": row1.get("Nr. mag.", ""),
                        "Nume Magazin": row1.get("Nume Magazin", "")
                    }
                    entry.update(modificari)
                    rezultate_mod.append(entry)
                    styling_mask.append(style_row)

            tabs = st.tabs(["🟥 Doar modificări reale", "📁 ID-uri noi și dispărute"])

            with tabs[0]:
                if rezultate_mod:
                    df_mod = pd.DataFrame(rezultate_mod).fillna("-")

                    def apply_style(df):
                        def highlighter(row):
                            idx = row.name
                            style = styling_mask[idx]
                            return [style.get(col, "") for col in df.columns]
                        return df.style.apply(highlighter, axis=1)

                    st.success(f"✅ {len(df_mod)} rânduri cu modificări")
                    st.dataframe(apply_style(df_mod), use_container_width=True)
                else:
                    st.info("✔️ Nu s-au găsit modificări.")

            with tabs[1]:
                if rezultate_nou_disparut:
                    df_ids = pd.DataFrame(rezultate_nou_disparut)
                    st.success(f"🔄 {len(df_ids)} ID-uri noi sau dispărute")
                    st.dataframe(df_ids, use_container_width=True)
                else:
                    st.info("✔️ Nu există ID-uri complet noi sau complet dispărute.")
        else:
            st.warning("⚠️ Selectează cel puțin o coloană pentru comparație.")