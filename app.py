import streamlit as st
import pandas as pd
st.set_page_config(
    page_title="Data Cleaner",
    page_icon="🧹",
    layout="wide"           # "centered" ou "wide"
)

st.title("🧹 Data Cleaning App")
# 1. On crée le menu dans la barre latérale

DEFAULTS = {
  "df_raw": None,
  "df_clean": None,
  "cleaning_config": {},
  "file_name": "",
  "outliers_removed": False
}
for key, val in DEFAULTS.items():
  if key not in st.session_state:
    st.session_state[key] = val
    
choix_menu = st.sidebar.radio(
    "Navigation",
    ["Chargement du fichier", "Diagnostic automatique"]
)    

if choix_menu == "Chargement du fichier":
    st.header("📂 Chargement du fichier")

    uploaded_file = st.file_uploader(
        "Importe ton fichier",
        type=["csv", "xlsx"],
        help="Formats acceptés : CSV et Excel"
    )

    if uploaded_file is not None:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file, sep=None, engine="python") 
        else:
            df = pd.read_excel(uploaded_file)
        st.success(f"✅ Fichier chargé : {uploaded_file.name}")
        
        metrics_container=st.container()
        colSelectionner=st.multiselect("Choisir plusieurs colonnes",options=df.columns.tolist(),default=df.columns.tolist())
        if colSelectionner:
            df_filtered = df[colSelectionner]
            doublons = df_filtered.duplicated().sum()
            pct_nan = df_filtered.isna().mean().mean() * 100
        else:
            df_filtered = pd.DataFrame()
            doublons = 0
            pct_nan = 0.0
        with metrics_container:
            col1, col2, col3, col4=st.columns(4)
            col1.metric("Lignes", df.shape[0])
            col2.metric("Colonnes", df_filtered.shape[1])
            col3.metric("Doublons", doublons)
            col4.metric("% NaN", f"{pct_nan:.1f}%")
        
        st.session_state.df_raw = df_filtered
        st.session_state.df_clean = df_filtered.copy()
        
        
        st.dataframe(df_filtered, use_container_width=True)
    

    

