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
  "dfFull": None,
  "selected_columns": None,
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
        if st.session_state.file_name != uploaded_file.name:
            if uploaded_file.name.endswith(".csv"):
                df = pd.read_csv(uploaded_file, sep=None, engine="python") 
            else:
                df = pd.read_excel(uploaded_file)
            st.success(f"✅ Fichier chargé : {uploaded_file.name}")
            st.session_state.dfFull = df.copy()
            st.session_state.file_name = uploaded_file.name
            st.session_state.selected_columns = df.columns.tolist()
            
    if st.session_state.dfFull is not None:
        df = st.session_state.dfFull.copy()
    
        metrics_container=st.container()
        colSelectionner=st.multiselect("Choisir plusieurs colonnes",options=df.columns.tolist(),default=st.session_state.selected_columns)
        st.session_state.selected_columns = colSelectionner
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
    
elif choix_menu == "Diagnostic automatique":
    st.header("📊 Diagnostic automatique")
    
    if st.session_state.df_raw is not None:
        df = st.session_state.df_raw
        
        diagnostic_df = pd.DataFrame({
            "Colonne": df.columns,
            "Type": df.dtypes.astype(str).values,
            "% NaN": (df.isna().mean() * 100).values,
            "Uniques": df.nunique().values
        })
        
        def highlight_nan(val):
            color = "#dd2100" if val > 0 else "#00cf3e"
            return f'color: {color}'
            
        styled_df = diagnostic_df.style.format({"% NaN": "{:.1f}%"}).map(highlight_nan, subset=["% NaN"])
        st.write("### Résumé des variables")
        st.dataframe(styled_df, use_container_width=True, hide_index=True )
        
    else:
        st.info("👋 Veuillez d'abord charger un fichier dans la section 'Chargement du fichier'.")
    

