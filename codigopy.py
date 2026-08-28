import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="Consulta de Notas", page_icon="🧬")

@st.cache_data
def carregar_dados():
    # Lê a planilha pulando as 2 primeiras linhas vazias/títulos para pegar o cabeçalho correto
    df = pd.read_excel("Cálculo de Notas - 9ºANO - 2ºTri.xlsx", sheet_name=0, header=2)
    
    # Limpa espaços em branco dos nomes das colunas
    df.columns = [str(c).strip() for c in df.columns]
    
    # Filtra apenas as colunas que importam para o aplicativo
    df = df[['RA', 'Alunos', 'Turma', 'Média']]
    
    # Remove qualquer linha vazia que não tenha RA
    df = df.dropna(subset=['RA'])
    
    # Converte o RA para texto, remove '.0' se o Excel leu como decimal, e tira espaços
    df['RA'] = df['RA'].astype(str).str.replace(r'\.0$', '', regex=True).str.strip()
    
    return df

df = carregar_dados()

st.title("🧬 Consulta de Notas - Biologia")
st.write("Digite seu RA para visualizar sua nota (2º Trimestre).")

# Campo de senha para o aluno digitar o RA
ra_aluno = st.text_input("Digite o seu RA:", type="password")

if st.button("Ver Nota"):
    if ra_aluno:
        # Limpa espaços de quem digitou
        ra_digitado = ra_aluno.strip()
        
        # Busca o RA na planilha
        aluno_encontrado = df[df['RA'] == ra_digitado]
        
        if not aluno_encontrado.empty:
            nome = aluno_encontrado.iloc[0]['Alunos']
            turma = aluno_encontrado.iloc[0]['Turma']
            nota = aluno_encontrado.iloc[0]['Média']
            
            # Formata a nota para mostrar com 1 casa decimal (ex: 8.1)
            nota_formatada = f"{float(nota):.1f}" if pd.notna(nota) else "Sem nota"
            
            st.success(f"Aluno(a): {nome} - Turma: {turma}")
            st.metric(label="Sua Nota Final", value=nota_formatada)
        else:
            st.error("RA não encontrado. Verifique se o número foi digitado corretamente.")
    else:
        st.warning("Por favor, digite um RA válido.")