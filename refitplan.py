import streamlit as st
import pandas as pd

st.set_page_config(page_title="Încărcare XLSX – Sheet fix", layout="wide")
st.title("📂 Încărcare fișier Excel: sheet 'Refit plan 2025' și filtrare coloane")

uploaded_file = st.file_uploader("Încarcă fișierul Excel (.xlsx)", type="xlsx")

if uploaded_file:
    try:
        st.write("📥 Se încarcă doar sheet-ul 'Refit plan 2025'...")

        # Încarcă doar sheet-ul specific
        df_raw = pd.read_excel(uploaded_file, sheet_name="Refit plan 2025", header=None, dtype=str)

        st.write(f"✅ Sheet încărcat: {df_raw.shape[0]} rânduri × {df_raw.shape[1]} coloane")

        # Caută rândul unde prima coloană este "Nr. mag."
        header_row_index = df_raw[df_raw.iloc[:, 0] == "Nr. mag."].index

        if len(header_row_index) == 0:
            st.error("❌ Nu s-a găsit rândul unde prima coloană este 'Nr. mag.'")
        else:
            header_row = header_row_index[0]
            st.success(f"✅ Rândul {header_row} a fost identificat ca antet.")

            new_header = df_raw.iloc[header_row].fillna('').astype(str).tolist()
            df_clean = df_raw.iloc[header_row + 1:].copy()
            df_clean.columns = new_header
            df_clean.reset_index(drop=True, inplace=True)

            # Coloanele relevante
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
                st.warning(f"⚠️ Următoarele coloane lipsesc din sheet: {coloane_lipsa}")

            if not coloane_existente:
                st.error("❌ Nicio coloană relevantă nu a fost găsită.")
            else:
                df_filtrat = df_clean[coloane_existente].copy()
                st.success(f"✅ {len(coloane_existente)} coloane păstrate.")
                st.dataframe(df_filtrat.head())

    except ValueError as ve:
        st.error(f"❌ Sheet 'Refit plan 2025' nu există în fișierul Excel. Asigură-te că numele este exact.")
    except Exception as e:
        st.exception(f"❌ Eroare la procesare: {e}")