import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração da página
st.set_page_config(
    page_title="Análise Celulares POÁ",
    page_icon="📱",
    layout="wide"
)

# Título principal
st.title("📱 ANÁLISE - CELULARES SUBTRAÍDOS EM POÁ")
st.markdown("**Dashboard Interativo para Análise de Dados de Segurança Pública**")

# Upload do arquivo
uploaded_file = st.file_uploader("📂 Faça upload do arquivo de dados", type=['xlsx', 'csv'])

@st.cache_data
def carregar_dados(arquivo):
    """Carrega e processa os dados"""
    try:
        if arquivo.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(arquivo, engine='openpyxl')
        else:
            df = pd.read_csv(arquivo)
        
        # Processamento básico
        df.columns = df.columns.str.strip().str.upper().str.replace(' ', '_')
        return df
    except Exception as e:
        st.error(f"Erro ao carregar: {e}")
        return None

if uploaded_file:
    df = carregar_dados(uploaded_file)
    
    if df is not None:
        st.success(f"✅ Dados carregados com sucesso! {len(df)} registros encontrados.")
        
        # Abas principais
        tab1, tab2, tab3, tab4 = st.tabs(["📊 VISÃO GERAL", "📈 ANÁLISES", "📱 CELULARES", "🔍 DADOS BRUTOS"])
        
        with tab1:
            st.header("📊 Visão Geral dos Dados")
            
            # Métricas
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total de Ocorrências", len(df))
            with col2:
                st.metric("Número de Colunas", df.shape[1])
            with col3:
                if 'MARCA_OBJETO' in df.columns:
                    st.metric("Marcas Diferentes", df['MARCA_OBJETO'].nunique())
                else:
                    st.metric("Marcas", "N/D")
            with col4:
                if 'NOME_DELEGACIA' in df.columns:
                    st.metric("Delegacias", df['NOME_DELEGACIA'].nunique())
                else:
                    st.metric("Delegacias", "N/D")
            
            # Primeiros registros
            st.subheader("📋 Primeiros Registros")
            st.dataframe(df.head(10), use_container_width=True)
        
        with tab2:
            st.header("📈 Análises e Estatísticas")
            
            # Gráfico de marcas
            if 'MARCA_OBJETO' in df.columns:
                st.subheader("🏷️ Marcas de Celulares Mais Furtadas")
                marcas_count = df['MARCA_OBJETO'].value_counts().head(10)
                
                fig, ax = plt.subplots(figsize=(12, 6))
                bars = marcas_count.plot(kind='bar', ax=ax, color='skyblue', alpha=0.8)
                ax.set_title('Top 10 Marcas de Celulares Subtraídos')
                ax.set_xlabel('Marca')
                ax.set_ylabel('Quantidade de Ocorrências')
                
                # Adicionar valores nas barras
                for i, v in enumerate(marcas_count):
                    ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
                
                plt.xticks(rotation=45)
                st.pyplot(fig)
            
            # Gráfico de delegacias
            if 'NOME_DELEGACIA' in df.columns:
                st.subheader("🏢 Distribuição por Delegacia")
                delegacias_count = df['NOME_DELEGACIA'].value_counts().head(10)
                
                fig, ax = plt.subplots(figsize=(12, 6))
                bars = delegacias_count.plot(kind='bar', ax=ax, color='lightcoral', alpha=0.8)
                ax.set_title('Top 10 Delegacias com Mais Ocorrências')
                ax.set_xlabel('Delegacia')
                ax.set_ylabel('Quantidade de Ocorrências')
                
                # Adicionar valores nas barras
                for i, v in enumerate(delegacias_count):
                    ax.text(i, v + 0.1, str(v), ha='center', va='bottom', fontweight='bold')
                
                plt.xticks(rotation=45)
                st.pyplot(fig)
        
        with tab3:
            st.header("📱 Análise Detalhada de Celulares")
            
            if 'MARCA_OBJETO' in df.columns:
                # Filtros interativos
                st.subheader("🎛️ Filtros para Análise")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    marcas = ['Todas as Marcas'] + sorted(df['MARCA_OBJETO'].dropna().unique())
                    marca_selecionada = st.selectbox("Selecione a marca:", marcas)
                
                with col2:
                    if 'NOME_DELEGACIA' in df.columns:
                        delegacias = ['Todas as Delegacias'] + sorted(df['NOME_DELEGACIA'].dropna().unique())
                        delegacia_selecionada = st.selectbox("Selecione a delegacia:", delegacias)
                
                # Aplicar filtros
                dados_filtrados = df.copy()
                
                if marca_selecionada != 'Todas as Marcas':
                    dados_filtrados = dados_filtrados[dados_filtrados['MARCA_OBJETO'] == marca_selecionada]
                
                if 'NOME_DELEGACIA' in df.columns and delegacia_selecionada != 'Todas as Delegacias':
                    dados_filtrados = dados_filtrados[dados_filtrados['NOME_DELEGACIA'] == delegacia_selecionada]
                
                # Mostrar estatísticas
                st.subheader(f"📊 Estatísticas dos Dados Filtrados")
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Registros Encontrados", len(dados_filtrados))
                with col2:
                    if 'QUANTIDADE_OBJETO' in dados_filtrados.columns:
                        total_celulares = dados_filtrados['QUANTIDADE_OBJETO'].sum()
                        st.metric("Total de Celulares", total_celulares)
                with col3:
                    if len(dados_filtrados) > 0:
                        percentual = (len(dados_filtrados) / len(df)) * 100
                        st.metric("Percentual do Total", f"{percentual:.1f}%")
        
        with tab4:
            st.header("🔍 Dados Brutos e Exportação")
            
            # Filtros
            st.subheader("🎛️ Filtros Avançados")
            
            col1, col2 = st.columns(2)
            filtered_df = df.copy()
            
            with col1:
                if 'NOME_DELEGACIA' in df.columns:
                    delegacias_filtro = ['Todas'] + sorted(df['NOME_DELEGACIA'].dropna().unique())
                    delegacia_filtro = st.selectbox("Filtrar por delegacia:", delegacias_filtro)
                    
                    if delegacia_filtro != 'Todas':
                        filtered_df = filtered_df[filtered_df['NOME_DELEGACIA'] == delegacia_filtro]
            
            with col2:
                if 'MARCA_OBJETO' in df.columns:
                    marcas_filtro = ['Todas'] + sorted(df['MARCA_OBJETO'].dropna().unique())
                    marca_filtro = st.selectbox("Filtrar por marca:", marcas_filtro)
                    
                    if marca_filtro != 'Todas':
                        filtered_df = filtered_df[filtered_df['MARCA_OBJETO'] == marca_filtro]
            
            # Mostrar dados filtrados
            st.subheader(f"📄 Dados Filtrados ({len(filtered_df)} registros)")
            st.dataframe(filtered_df, use_container_width=True, height=400)
            
            # Download
            if len(filtered_df) > 0:
                csv = filtered_df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "📥 BAIXAR DADOS FILTRADOS (CSV)",
                    csv,
                    "celulares_subtraidos_poa.csv",
                    "text/csv",
                    use_container_width=True
                )

else:
    st.info("👆 Faça upload de um arquivo Excel (.xlsx) ou CSV para começar a análise")

# Rodapé
st.markdown("---")
st.markdown("**Desenvolvido para análise de dados de segurança pública • POÁ**")