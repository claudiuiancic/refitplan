import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparație CSV", layout="wide")
st.title("📊 Comparație versiuni CSV (export Excel UTF-8)")

uploaded_file1 = st.file_uploader("Încarcă prima versiune CSV", type="csv", key="f1")
uploaded_file2 = st.file_uploader("Încarcă a doua versiune CSV", type="csv", key="f2")

def load_csv(file, label):
    try:
        df = pd.read_csv(file, header=3)
        st.success(f"{label} încărcat cu succes: {df.shape[0]} rânduri, {df.shape[1]} coloane.")
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.zfill(4)
        return df
    except Exception as e:
        st.error(f"Eroare la încărcarea fișierului {label}: {e}")
        return None

if uploaded_file1 and uploaded_file2:
    df1 = load_csv(uploaded_file1, "Prima versiune")
    df2 = load_csv(uploaded_file2, "A doua versiune")

    if df1 is not None and df2 is not None:
        all_columns = [col for col in df1.columns[1:]]  # excludem coloana de ID
        selected_columns = st.multiselect("Alege coloanele care te interesează pentru comparație:", all_columns, default=all_columns)

        if st.button("🔍 Compară fișierele"):
            with st.status("🔄 Procesare în curs...", expanded=True) as status:
                try:
                    st.write("📌 Se identifică coloana de ID...")
                    id_col = df1.columns[0]

                    df1_indexed = df1.set_index(id_col)
                    df2_indexed = df2.set_index(id_col)

                    st.write("🔎 Se determină ID-urile comune...")
                    common_ids = df1_indexed.index.intersection(df2_indexed.index)
                    st.write(f"✅ {len(common_ids)} ID-uri comune găsite.")

                    if not selected_columns:
                        st.warning("Nicio coloană selectată pentru comparație.")
                        status.update(label="⚠️ Selectează cel puțin o coloană.", state="error")
                    else:
                        diffs = []
                        st.write("🔧 Se compară coloanele selectate...")

                        for idx in common_ids:
                            row1 = df1_indexed.loc[idx]
                            row2 = df2_indexed.loc[idx]

                            for col in selected_columns:
                                val1 = str(row1.get(col, '')).strip()
                                val2 = str(row2.get(col, '')).strip()
                                if val1 != val2:
                                    diffs.append({
                                        "Cod ID": idx,
                                        "Coloana": col,
                                        "Valoare veche": val1,
                                        "Valoare nouă": val2
                                    })

                        if diffs:
                            diffs_df = pd.DataFrame(diffs)
                            st.success(f"✅ S-au găsit {len(diffs)} diferențe.")
                            st.dataframe(diffs_df)
                            st.download_button("📥 Descarcă diferențele CSV", diffs_df.to_csv(index=False).encode("utf-8"), "diferente.csv")
                            status.update(label="✅ Comparația s-a încheiat cu succes.", state="complete")
                        else:
                            st.info("✔️ Nu s-au găsit diferențe.")
                            status.update(label="Comparație finalizată fără diferențe.", state="complete")
                except Exception as e:
                    st.exception(f"Eroare în timpul comparației: {e}")
                    status.update(label="❌ Eroare în timpul comparației.", state="error")