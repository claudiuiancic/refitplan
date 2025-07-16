import streamlit as st
import pandas as pd

st.set_page_config(page_title="Test CSV", layout="wide")
st.title("🧪 Test încărcare fișiere CSV (UTF-8)")

uploaded_file1 = st.file_uploader("Încarcă PRIMUL CSV (cu header pe rândul 4)", type="csv", key="csv1")
uploaded_file2 = st.file_uploader("Încarcă AL DOILEA CSV (cu header pe rândul 4)", type="csv", key="csv2")

def safe_read(file, label):
    try:
        df = pd.read_csv(file, header=3)
        st.success(f"✅ {label} încărcat: {df.shape[0]} rânduri, {df.shape[1]} coloane.")
        st.write("🔹 Antet:", list(df.columns))
        st.dataframe(df.head())
        return df
    except Exception as e:
        st.error(f"❌ Eroare la citirea fișierului {label}: {e}")
        return None

if uploaded_file1:
    st.subheader("📂 Informații fișier 1")
    df1 = safe_read(uploaded_file1, "Fișier 1")

if uploaded_file2:
    st.subheader("📂 Informații fișier 2")
    df2 = safe_read(uploaded_file2, "Fișier 2")