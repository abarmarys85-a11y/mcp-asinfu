import streamlit as st
import pandas as pd
from pathlib import Path

DATA_PATH = Path(__file__).parent / "data" / "portales_gub_uy.csv"

st.set_page_config(page_title="Portales gub.uy por Grupos", page_icon="🌐", layout="wide")
st.title("🌐 Portales gub.uy")
st.caption("Consultá el catálogo de portales por grupo, tipo y ambiente.")

df = pd.read_csv(DATA_PATH, dtype=str, encoding="latin-1", on_bad_lines="skip", sep=";").fillna("")

# ── Filtros ───────────────────────────────────────────────────────────────────
col1, col2, col3 = st.columns(3)

with col1:
    busqueda = st.text_input("🔍 Buscar", placeholder="nombre, sigla, URL...")

with col2:
    grupos = ["Todos"] + sorted(df["grupo_portales"].unique().tolist())
    grupo = st.selectbox("Grupo", grupos)

with col3:
    ambientes = ["Todos", "produccion", "staging"]
    ambiente = st.selectbox("Ambiente", ambientes)

# ── Filtrado ──────────────────────────────────────────────────────────────────
resultado = df.copy()

if busqueda:
    t = busqueda.lower()
    mask = (
        resultado["url"].str.lower().str.contains(t) |
        resultado["nombre_largo"].str.lower().str.contains(t) |
        resultado["sigla"].str.lower().str.contains(t)
    )
    resultado = resultado[mask]

if grupo != "Todos":
    resultado = resultado[resultado["grupo_portales"] == grupo]

if ambiente != "Todos":
    resultado = resultado[resultado["ambiente_portal"] == ambiente]

# ── Resultados ────────────────────────────────────────────────────────────────
st.divider()
st.markdown(f"**{len(resultado)}** portales encontrados")

tab_tabla, tab_grafico = st.tabs(["📋 Tabla", "📊 Gráfico por grupo"])

with tab_tabla:
    st.dataframe(
        resultado[["nombre_largo", "sigla", "grupo_portales", "tipo_ambiente", "ambiente_portal", "url"]],
        use_container_width=True,
        hide_index=True,
    )

with tab_grafico:
    conteo = (
        resultado.groupby("grupo_portales")
        .size()
        .reset_index(name="cantidad")
        .sort_values("cantidad", ascending=False)
    )
    st.bar_chart(conteo.set_index("grupo_portales")["cantidad"])