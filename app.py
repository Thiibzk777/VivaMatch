import streamlit as st
import pandas as pd

st.set_page_config(page_title="VivaMatch", layout="wide")

st.title("🏠 VivaMatch - Encontre o imóvel ideal")
st.markdown("Simule seu crédito e veja os imóveis disponíveis!")

# Simulação de entrada de dados
with st.form("simulador"):
    st.subheader("💳 Simule seu crédito")
    nome = st.text_input("Nome completo")
    renda = st.number_input("Renda mensal familiar (R$)", min_value=0)
    score = st.slider("Score de crédito", 0, 1000, 600)
    dependentes = st.selectbox("Número de dependentes", [0,1,2,3,4,5])
    financiamento = st.selectbox("Pretende usar financiamento?", ["Sim", "Não"])
    enviar = st.form_submit_button("Ver imóveis compatíveis")

if enviar:
    st.success(f"Simulação enviada para {nome}")
    imoveis = pd.read_csv("imoveis.csv")
    filtrados = imoveis[imoveis['renda_min'] <= renda]
    st.subheader("🏢 Imóveis sugeridos:")
    st.dataframe(filtrados)
