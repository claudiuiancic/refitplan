import streamlit as st
import pandas as pd

st.set_page_config(page_title="Test CSV dinamic", layout="wide")
st.title("🧪 Test inteligent încărcare fișier CSV")

uploaded_file = st.file_uploader("Încarcă un fișier CSV", type="csv")

if uploaded_file:
    st.subheader("📍 Conținut brut (primele 10 rânduri)")

    try:
        raw_preview = pd.read_csv(uploaded_file, header=None, nrows=10, encoding="utf-8")
        st.dataframe(raw_preview)

        max_row = raw_preview.shape[0] - 1
        header_row = st.slider("Alege rândul care conține antetul real", min_value=0, max_value=max_row, value=3)

        df = pd.read_csv(uploaded_file, header=header_row, encoding="utf-8")
        st.success(f"✅ Fișier citit cu antet pe rândul {header_row} (index={header_row})")
        st.write("🔹 Coloane detectate:", list(df.columns))
        st.dataframe(df.head())

    except Exception as e:
        st.exception(f"❌ Eroare la citirea fișierului: {e}")