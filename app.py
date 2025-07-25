import streamlit as st
import pandas as pd
from datetime import datetime

# Carrega os dados principais
leads_path = "dados_leads.csv"
historico_path = "historico_leads.csv"

# Carrega ou cria os DataFrames
if Path(leads_path).exists():
    leads_df = pd.read_csv(leads_path)
else:
    leads_df = pd.DataFrame(columns=["Nome", "Telefone", "Renda", "Status", "Última Ação", "Data Atualização"])

if Path(historico_path).exists():
    historico_df = pd.read_csv(historico_path)
else:
    historico_df = pd.DataFrame(columns=["Telefone", "Ação", "Data/Hora", "Observação"])

# Função para registrar ações
def registrar_acao(telefone, acao, obs=""):
    global historico_df
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    historico_df = historico_df.append({
        "Telefone": telefone,
        "Ação": acao,
        "Data/Hora": now,
        "Observação": obs
    }, ignore_index=True)
    historico_df.to_csv(historico_path, index=False)

# Sidebar para adicionar lead
st.sidebar.header("Adicionar novo lead")
nome = st.sidebar.text_input("Nome")
telefone = st.sidebar.text_input("Telefone (somente números)")
renda = st.sidebar.number_input("Renda mensal", min_value=0)
if st.sidebar.button("Salvar Lead"):
    if telefone not in leads_df["Telefone"].values:
        nova_linha = {
            "Nome": nome,
            "Telefone": telefone,
            "Renda": renda,
            "Status": "Novo",
            "Última Ação": "Lead criado",
            "Data Atualização": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        leads_df = leads_df.append(nova_linha, ignore_index=True)
        leads_df.to_csv(leads_path, index=False)
        registrar_acao(telefone, "Lead criado")
        st.sidebar.success("Lead salvo com sucesso!")
    else:
        st.sidebar.warning("Este telefone já está cadastrado.")

# Exibição dos leads
st.title("📋 Gestão de Leads - VivaMatch")

if not leads_df.empty:
    for index, row in leads_df.iterrows():
        with st.expander(f"{row['Nome']} - R$ {row['Renda']} - {row['Status']}"):
            st.write(f"**Telefone:** {row['Telefone']}")
            st.write(f"**Última Ação:** {row['Última Ação']} em {row['Data Atualização']}")
            novo_status = st.selectbox("Atualizar etapa do funil", ["Novo", "Contato", "Simulação", "Visita", "Negociação", "Vendido"], index=["Novo", "Contato", "Simulação", "Visita", "Negociação", "Vendido"].index(row["Status"]), key=f"status_{index}")
            if novo_status != row["Status"]:
                leads_df.at[index, "Status"] = novo_status
                leads_df.at[index, "Última Ação"] = f"Status alterado para {novo_status}"
                leads_df.at[index, "Data Atualização"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                leads_df.to_csv(leads_path, index=False)
                registrar_acao(row["Telefone"], f"Status alterado para {novo_status}")
                st.success("Status atualizado.")

            st.markdown("**Adicionar anotação manual:**")
            anotacao = st.text_input("Digite a observação", key=f"anotacao_{index}")
            if st.button("Salvar anotação", key=f"btn_anotacao_{index}"):
                registrar_acao(row["Telefone"], "Anotação manual", anotacao)
                st.success("Anotação salva!")

            # Mostrar histórico completo
            st.markdown("---")
            st.markdown("📜 Histórico completo:")
            historico_filtrado = historico_df[historico_df["Telefone"] == row["Telefone"]]
            for _, h_row in historico_filtrado.iterrows():
                st.write(f"- {h_row['Data/Hora']} | {h_row['Ação']}" + (f" | Obs: {h_row['Observação']}" if h_row['Observação'] else ""))

else:
    st.info("Nenhum lead cadastrado ainda.")