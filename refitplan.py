import streamlit as st
import pandas as pd

st.set_page_config(page_title="Comparație CSV", layout="wide")
st.title("Comparație versiuni de refitplan")

uploaded_file1 = st.file_uploader("Încarcă prima versiune CSV", type="csv", key="f1")
uploaded_file2 = st.file_uploader("Încarcă a doua versiune CSV", type="csv", key="f2")

def load_csv(file, label):
    try:
        df = pd.read_csv(file, header=3)
        df.iloc[:, 0] = df.iloc[:, 0].astype(str).str.zfill(4)
        return df
    except Exception as e:
        st.error(f"Eroare la încărcarea fișierului {label}: {e}")
        return None

if uploaded_file1 and uploaded_file2:
    df1 = load_csv(uploaded_file1, "prima versiune")
    df2 = load_csv(uploaded_file2, "a doua versiune")

    if df1 is not None and df2 is not None:
        try:
            id_col = df1.columns[0]

            df1_indexed = df1.set_index(id_col)
            df2_indexed = df2.set_index(id_col)

            common_ids = df1_indexed.index.intersection(df2_indexed.index)
            st.success(f"{len(common_ids)} ID-uri comune găsite.")

            all_columns = [col for col in df1.columns if col != id_col]
            selected_columns = st.multiselect("Alege coloanele de comparat", all_columns, default=all_columns)

            if selected_columns:
                diffs = []
                for idx in common_ids:
                    row1 = df1_indexed.loc[idx]
                    row2 = df2_indexed.loc[idx]

                    for col in selected_columns:
                        val1 = str(row1[col]) if col in row1 else ''
                        val2 = str(row2[col]) if col in row2 else ''
                        if pd.isna(val1): val1 = ''
                        if pd.isna(val2): val2 = ''
                        if val1 != val2:
                            diffs.append({
                                "Cod ID": idx,
                                "Coloana": col,
                                "Valoare veche": val1,
                                "Valoare nouă": val2
                            })

                if diffs:
                    diffs_df = pd.DataFrame(diffs)
                    st.dataframe(diffs_df)
                    csv_out = diffs_df.to_csv(index=False).encode("utf-8")
                    st.download_button("📥 Descarcă diferențele CSV", data=csv_out, file_name="diferente.csv")
                else:
                    st.info("Nu s-au găsit diferențe în coloanele selectate.")
        except Exception as e:
            st.error(f"A apărut o eroare în timpul comparației: {e}")