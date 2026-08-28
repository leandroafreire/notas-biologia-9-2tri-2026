import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta de Notas", page_icon="🧬")

@st.cache_data
def carregar_dados():
    # Carrega a aba 'Notas', pulando as linhas de cabeçalho iniciais da sua formatação
    df = pd.read_excel("Cálculo de Notas - 9ºANO - 2ºTri.xlsx", sheet_name='Notas', header=11)
    
    # Limpa as colunas renomeando as principais para facilitar
    df.columns = ['Nº', 'RA', 'INSCRIÇÃO', 'Aluno', 'Turma', 'Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5', 'Item 6', 'Item 7', 'Item 8', 'Item 9', 'Item 10', 'Soma Nota', 'Nota ClassOn', 'Observação']
    return df

df = carregar_dados()

st.title("🧬 Consulta de Notas - Biologia")
st.write("Digite seu RA para visualizar sua nota da Tarefa 2 (2º Trimestre).")

# Campo de senha para o aluno digitar o RA
ra_aluno = st.text_input("Digite o seu RA:", type="password")

if st.button("Ver Nota"):
    if ra_aluno:
        # Busca o RA na planilha (convertendo para texto para evitar erros de formatação)
        aluno_encontrado = df[df['RA'].astype(str) == ra_aluno.strip()]
        
        if not aluno_encontrado.empty:
            nome = aluno_encontrado.iloc[0]['Aluno']
            turma = aluno_encontrado.iloc[0]['Turma']
            nota = aluno_encontrado.iloc[0]['Nota ClassOn']
            
            st.success(f"Aluno: {nome} - Turma: {turma}")
            st.metric(label="Sua Nota", value=nota)
        else:
            st.error("RA não encontrado. Verifique se o número foi digitado corretamente.")
    else:
        st.warning("Por favor, digite um RA válido.")