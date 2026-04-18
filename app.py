import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime, timedelta

# -----------------------------
# CONFIG PAGE
# -----------------------------
st.set_page_config(
    page_title="Data7 Financial Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------
st.title("📊 Data7 Financial Dashboard")
st.caption("Dashboard executivo para análise financeira, metas e performance")

# -----------------------------
# MOCK DATA (troque depois pelo SQL real)
# -----------------------------
np.random.seed(42)

datas = pd.date_range(start="2026-01-01", periods=120)

clientes = [
    "Movida",
    "Unidas",
    "CS Brasil",
    "Ouro Verde",
    "Localiza",
    "BRK"
]

df = pd.DataFrame({
    "Data": datas,
    "Cliente": np.random.choice(clientes, size=120),
    "Faturamento": np.random.randint(3000, 25000, size=120),
    "OS": np.random.randint(1, 8, size=120)
})

df["Ano"] = df["Data"].dt.year
df["Mes"] = df["Data"].dt.month
df["Semana"] = df["Data"].dt.isocalendar().week.astype(int)

# -----------------------------
# SIDEBAR FILTROS
# -----------------------------
st.sidebar.header("🔎 Filtros")

anos = st.sidebar.multiselect(
    "Ano",
    options=sorted(df["Ano"].unique()),
    default=sorted(df["Ano"].unique())
)

clientes_sel = st.sidebar.multiselect(
    "Cliente",
    options=sorted(df["Cliente"].unique()),
    default=sorted(df["Cliente"].unique())
)

df_filtrado = df[
    (df["Ano"].isin(anos)) &
    (df["Cliente"].isin(clientes_sel))
]

# -----------------------------
# KPIS
# -----------------------------
fat_total = df_filtrado["Faturamento"].sum()
qtd_os = df_filtrado["OS"].sum()
ticket_medio = fat_total / qtd_os if qtd_os > 0 else 0
clientes_ativos = df_filtrado["Cliente"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Faturamento Total", f"R$ {fat_total:,.0f}".replace(",", "."))
col2.metric("📦 Total OS", f"{qtd_os}")
col3.metric("📈 Ticket Médio", f"R$ {ticket_medio:,.0f}".replace(",", "."))
col4.metric("👥 Clientes Ativos", f"{clientes_ativos}")

st.divider()

# -----------------------------
# GRÁFICOS
# -----------------------------
col5, col6 = st.columns(2)

with col5:
    fat_dia = df_filtrado.groupby("Data", as_index=False)["Faturamento"].sum()
    fig1 = px.line(
        fat_dia,
        x="Data",
        y="Faturamento",
        title="Evolução do Faturamento"
    )
    st.plotly_chart(fig1, use_container_width=True)

with col6:
    fat_cliente = df_filtrado.groupby("Cliente", as_index=False)["Faturamento"].sum()
    fig2 = px.bar(
        fat_cliente,
        x="Cliente",
        y="Faturamento",
        title="Ranking de Clientes"
    )
    st.plotly_chart(fig2, use_container_width=True)

# -----------------------------
# META SEMANAL
# -----------------------------
st.subheader("🎯 Meta Semanal")

meta = 90000
fat_semana = df_filtrado.groupby("Semana", as_index=False)["Faturamento"].sum()
fat_semana["Meta"] = meta

fig3 = px.bar(
    fat_semana,
    x="Semana",
    y="Faturamento",
    title="Meta vs Realizado por Semana"
)

fig3.add_scatter(
    x=fat_semana["Semana"],
    y=fat_semana["Meta"],
    mode="lines",
    name="Meta"
)

st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# TABELA FINAL
# -----------------------------
st.subheader("📋 Dados Detalhados")
st.dataframe(df_filtrado, use_container_width=True)

# -----------------------------
# FOOTER
# -----------------------------
st.caption("Desenvolvido por Felipe Nunes | Python + Streamlit + Dados")
