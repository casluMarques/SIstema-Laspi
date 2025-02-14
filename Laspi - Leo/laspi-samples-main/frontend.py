import streamlit as st
import requests
from urllib.parse import urlparse, parse_qs

# Configuração da página
st.set_page_config(page_title="Visualizador de Amostras", layout="centered")

def get_amostra_id_from_url():
    # Pega a URL atual do Streamlit usando o novo método
    query_params = st.query_params
    
    # Se tiver um ID na URL, retorna ele
    if 'id' in query_params:
        return query_params['id']
    return None

def fetch_amostra(amostra_id):
    try:
        response = requests.get(f"http://localhost:8000/amostras/{amostra_id}")
        if response.status_code == 200:
            return response.json()
        return None
    except requests.RequestException:
        return None

def main():
    st.title("📦 Detalhes da Amostra")
    
    # Tenta pegar o ID da amostra da URL
    amostra_id = get_amostra_id_from_url()
    
    if amostra_id:
        # Busca os dados da amostra
        amostra = fetch_amostra(amostra_id)
        
        if amostra and 'erro' not in amostra:
            # Exibe as informações em um layout organizado
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("ID da Amostra", amostra['id'])
                st.metric("Nome", amostra['nome'])
                st.metric("Fabricante", amostra['fabricante'])
            
            with col2:
                st.metric("Processo", amostra['processo'])
                st.metric("Data de Entrada", amostra['data_entrada'])
                st.metric("Tipo", amostra['tipo'])
            
            # Descrição em uma seção separada
            st.subheader("Descrição")
            st.write(amostra['descricao'])
            
        else:
            st.error("❌ Amostra não encontrada ou erro ao buscar dados.")
    else:
        st.info("ℹ️ Escaneie um QR code válido para visualizar os detalhes da amostra.")

if __name__ == "__main__":
    main()