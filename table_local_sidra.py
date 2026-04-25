import streamlit as st
import pandas as pd
import altair as alt

st.set_page_config(page_title="Efetivo dos Rebanhos por Estado", layout="wide")

st.markdown("<h3>.   Tamanho Efetivo dos Rebanhos por Estado - SIDRA / IBGE</h3>", unsafe_allow_html=True)

@st.cache_data
def carregar_dados():
    return pd.read_excel("sidra.xlsx")

dados = carregar_dados()

# Filtros
st.sidebar.header("Filtros")

tipo = st.sidebar.selectbox(
    "Tipo de rebanho",
    sorted(dados["Tipo de rebanho"].unique())
)

estados = st.sidebar.multiselect(
    "Estado",
    sorted(dados["Estado"].unique()),
    default=[dados["Estado"].unique()[0]]
)

periodo = st.sidebar.slider(
    "Período",
    int(dados["Ano"].min()),
    int(dados["Ano"].max()),
    (2000, int(dados["Ano"].max()))
)

# Filtrar
df = dados[
    (dados["Tipo de rebanho"] == tipo) &
    (dados["Estado"].isin(estados)) &
    (dados["Ano"].between(periodo[0], periodo[1]))
]

# Gráfico
chart = alt.Chart(df).mark_line(point=True).encode(
    x="Ano:O",
    y="Valor:Q",
    color="Estado:N",
    tooltip=["Estado", "Ano", "Valor"]
).properties(height=450)

st.altair_chart(chart, use_container_width=True)

# Tabela
st.dataframe(df, use_container_width=True)