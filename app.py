"""
Aplicação Streamlit - Assistente Jurídico com IA
"""
import streamlit as st
import os
import sys
import pandas as pd
from pathlib import Path
from datetime import datetime
import io

# Adicionar o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent))

from src.pdf_processor import PDFProcessor
from src.ai_extractor import LegalAIExtractor, DocumentoJuridico
from src.document_chat import LegalDocumentChat, QuickQuestions
from src.protocol_extractor import ProtocolExtractor, DadosProtocolo


# Configuração da página
st.set_page_config(
    page_title="Assistente Jurídico IA",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #64748B;
        text-align: center;
        margin-bottom: 2rem;
    }
    .info-box {
        background-color: #F0F9FF;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3B82F6;
        margin: 1rem 0;
    }
    .success-box {
        background-color: #F0FDF4;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #10B981;
        margin: 1rem 0;
    }
    .chat-message-user {
        background-color: #EFF6FF;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .chat-message-assistant {
        background-color: #F9FAFB;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 3px solid #3B82F6;
    }
    </style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Inicializa variáveis de estado da sessão."""
    if 'document_text' not in st.session_state:
        st.session_state.document_text = None
    if 'document_info' not in st.session_state:
        st.session_state.document_info = None
    if 'chat' not in st.session_state:
        st.session_state.chat = None
    if 'extracted_data' not in st.session_state:
        st.session_state.extracted_data = None
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'df_protocolos' not in st.session_state:
        st.session_state.df_protocolos = None
    if 'resultados_protocolos' not in st.session_state:
        st.session_state.resultados_protocolos = None


def process_pdf(uploaded_file):
    """Processa o PDF enviado."""
    temp_path = f"data/input/temp_{uploaded_file.name}"
    os.makedirs("data/input", exist_ok=True)
    
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    with st.spinner("📄 Extraindo texto do documento..."):
        processor = PDFProcessor(temp_path)
        text = processor.extract_text()
        summary = processor.get_summary()
    
    os.remove(temp_path)
    
    return text, summary


def extract_with_ai(text):
    """Extrai informações estruturadas com IA."""
    with st.spinner("🤖 Analisando documento com IA..."):
        extractor = LegalAIExtractor()
        extracted_data = extractor.extract_information(text)
    return extracted_data


def render_analise_documento():
    """Renderiza a página de análise de documento único."""
    st.header("1️⃣ Upload do Documento")
    
    uploaded_file = st.file_uploader(
        "Selecione um documento PDF jurídico",
        type=['pdf'],
        help="Formatos aceitos: PDF",
        key="single_pdf_upload"
    )
    
    if uploaded_file:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.success(f"✅ Arquivo carregado: {uploaded_file.name}")
        
        with col2:
            if st.button("🚀 Processar Documento", type="primary", use_container_width=True):
                try:
                    text, summary = process_pdf(uploaded_file)
                    st.session_state.document_text = text
                    st.session_state.document_info = summary
                    st.session_state.chat = LegalDocumentChat(text)
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Erro ao processar documento: {str(e)}")
    
    if st.session_state.document_text:
        st.divider()
        
        tab1, tab2, tab3, tab4 = st.tabs([
            "📊 Análise Automática",
            "💬 Chat Interativo",
            "⚡ Perguntas Rápidas",
            "📄 Documento Original"
        ])
        
        # Tab 1: Análise Automática
        with tab1:
            st.header("📊 Análise Automática do Documento")
            
            if st.button("🔍 Extrair Informações com IA", use_container_width=True):
                try:
                    extracted = extract_with_ai(st.session_state.document_text)
                    st.session_state.extracted_data = extracted
                except Exception as e:
                    st.error(f"Erro: {str(e)}")
            
            if st.session_state.extracted_data:
                data = st.session_state.extracted_data
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📋 Informações do Processo")
                    st.markdown(f"**Tipo de Documento:** {data.tipo_documento}")
                    if data.dados_processo:
                        st.markdown(f"**Número do Processo:** {data.dados_processo.numero_processo or 'N/A'}")
                        st.markdown(f"**Classe:** {data.dados_processo.classe or 'N/A'}")
                        st.markdown(f"**Assunto:** {data.dados_processo.assunto or 'N/A'}")
                        st.markdown(f"**Vara:** {data.dados_processo.vara or 'N/A'}")
                    
                    st.divider()
                    
                    st.subheader("👥 Partes")
                    if data.partes:
                        st.markdown(f"**Autor:** {data.partes.autor}")
                        st.markdown(f"**Réu:** {data.partes.reu}")
                        if data.partes.advogado_autor:
                            st.markdown(f"**Advogado do Autor:** {data.partes.advogado_autor}")
                        if data.partes.advogado_reu:
                            st.markdown(f"**Advogado do Réu:** {data.partes.advogado_reu}")
                
                with col2:
                    st.subheader("📝 Resumo Executivo")
                    st.markdown(f'<div class="info-box">{data.resumo}</div>', unsafe_allow_html=True)
                    
                    st.divider()
                    
                    st.subheader("🎯 Pontos Principais")
                    for i, ponto in enumerate(data.pontos_principais, 1):
                        st.markdown(f"{i}. {ponto}")
                
                if data.prazos:
                    st.divider()
                    st.subheader("⏰ Prazos Identificados")
                    for prazo in data.prazos:
                        st.warning(f"**{prazo.descricao}** - Data Limite: {prazo.data_limite}")
        
        # Tab 2: Chat Interativo
        with tab2:
            st.header("💬 Chat Interativo com o Documento")
            
            st.markdown("""
            <div class="info-box">
            💡 <b>Dica:</b> Faça perguntas sobre o documento. O assistente responderá 
            baseado no conteúdo do PDF analisado.
            </div>
            """, unsafe_allow_html=True)
            
            for msg in st.session_state.chat.get_history():
                if msg["role"] == "user":
                    st.markdown(f'<div class="chat-message-user">👤 <b>Você:</b> {msg["content"]}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="chat-message-assistant">🤖 <b>Assistente:</b> {msg["content"]}</div>', unsafe_allow_html=True)
            
            col1, col2 = st.columns([5, 1])
            
            with col1:
                question = st.text_input(
                    "Faça sua pergunta:",
                    key="chat_input",
                    placeholder="Ex: Qual é o valor da causa?"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("Enviar", use_container_width=True):
                    if question:
                        answer = st.session_state.chat.ask(question)
                        st.rerun()
            
            with st.expander("💡 Ver sugestões de perguntas"):
                suggested = st.session_state.chat.get_suggested_questions()
                for suggestion in suggested:
                    if st.button(suggestion, key=f"sug_{suggestion[:20]}"):
                        st.session_state.chat.ask(suggestion)
                        st.rerun()
        
        # Tab 3: Perguntas Rápidas
        with tab3:
            st.header("⚡ Perguntas Rápidas")
            
            quick = QuickQuestions(st.session_state.document_text)
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("📋 Número do Processo", use_container_width=True):
                    with st.spinner("Buscando..."):
                        result = quick.get_numero_processo()
                        st.success(result)
                
                if st.button("👥 Partes do Processo", use_container_width=True):
                    with st.spinner("Buscando..."):
                        result = quick.get_partes()
                        st.success(result)
                
                if st.button("📊 Tipo de Ação", use_container_width=True):
                    with st.spinner("Buscando..."):
                        result = quick.get_tipo_acao()
                        st.success(result)
            
            with col2:
                if st.button("💰 Valor da Causa", use_container_width=True):
                    with st.spinner("Buscando..."):
                        result = quick.get_valor_causa()
                        st.success(result)
                
                if st.button("⏰ Prazos", use_container_width=True):
                    with st.spinner("Buscando..."):
                        result = quick.get_prazos()
                        st.success(result)
        
        # Tab 4: Documento Original
        with tab4:
            st.header("📄 Documento Original")
            
            if st.session_state.document_info:
                info = st.session_state.document_info
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Páginas", info['num_paginas'])
                
                with col2:
                    st.metric("Palavras", f"{info['num_palavras']:,}")
                
                with col3:
                    st.metric("Tamanho", f"{info['tamanho_kb']:.1f} KB")
            
            st.divider()
            
            with st.expander("📝 Ver texto completo"):
                st.text_area(
                    "Texto extraído do PDF:",
                    st.session_state.document_text,
                    height=400
                )
    
    else:
        st.info("""
        👆 **Como usar:**
        
        1. Faça upload de um documento PDF jurídico
        2. Clique em "Processar Documento"
        3. Explore as análises e faça perguntas!
        
        **Exemplos de documentos:**
        - Petições iniciais
        - Sentenças
        - Acórdãos
        - Contratos
        - Pareceres jurídicos
        """)


def render_extrator_protocolos():
    """Renderiza a página de extração de protocolos em lote."""
    st.header("📋 Extrator de Protocolos Judiciais")
    
    st.markdown("""
    <div class="info-box">
    <b>📌 Instruções:</b><br>
    1. Faça upload de um ou mais PDFs de protocolos da Justiça Estadual<br>
    2. Clique em <b>Processar Protocolos</b><br>
    3. Visualize os dados extraídos na tabela<br>
    4. Baixe o arquivo CSV ou Excel com todos os dados
    </div>
    """, unsafe_allow_html=True)
    
    # Upload múltiplo de arquivos
    uploaded_files = st.file_uploader(
        "📁 Selecione os PDFs de protocolo",
        type=['pdf'],
        accept_multiple_files=True,
        help="Você pode selecionar múltiplos arquivos de uma vez (Ctrl+Click ou Shift+Click)",
        key="protocol_pdf_upload"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} arquivo(s) selecionado(s)")
        
        # Mostrar lista de arquivos
        with st.expander("📄 Ver arquivos selecionados"):
            for i, file in enumerate(uploaded_files, 1):
                st.write(f"{i}. {file.name}")
        
        # Botão para processar
        if st.button("🚀 Processar Protocolos", type="primary", use_container_width=True, key="btn_process_protocols"):
            
            extractor = ProtocolExtractor()
            resultados = []
            
            # Barra de progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, pdf_file in enumerate(uploaded_files):
                status_text.text(f"Processando: {pdf_file.name} ({i+1}/{len(uploaded_files)})")
                
                try:
                    dados = extractor.extract_protocol_data(pdf_file)
                    resultados.append(dados)
                except Exception as e:
                    st.error(f"❌ Erro ao processar {pdf_file.name}: {e}")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Processamento concluído!")
            
            if resultados:
                st.session_state.resultados_protocolos = resultados
                st.session_state.df_protocolos = extractor.to_dataframe(resultados)
                st.rerun()
    
    # Mostrar resultados se existirem
    if st.session_state.df_protocolos is not None and not st.session_state.df_protocolos.empty:
        st.markdown("---")
        st.subheader("📊 Dados Extraídos")
        
        df = st.session_state.df_protocolos
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("📋 Total de Protocolos", len(df))
        with col2:
            comarcas = df['comarca'].nunique() if 'comarca' in df.columns else 0
            st.metric("🏛️ Comarcas", comarcas)
        with col3:
            autores = df['autor'].nunique() if 'autor' in df.columns else 0
            st.metric("👤 Autores Únicos", autores)
        with col4:
            if 'valor_causa' in df.columns:
                # Tentar calcular soma dos valores
                try:
                    valores = df['valor_causa'].str.replace('R$', '').str.replace('.', '').str.replace(',', '.').str.strip()
                    soma = pd.to_numeric(valores, errors='coerce').sum()
                    st.metric("💰 Valor Total", f"R$ {soma:,.2f}")
                except:
                    st.metric("💰 Valor Total", "N/A")
            else:
                st.metric("💰 Valor Total", "N/A")
        
        # Tabela de dados
        st.markdown("### 📋 Tabela de Protocolos")
        
        # Selecionar colunas para exibir
        colunas_principais = [
            'numero_processo',
            'data_envio',
            'comarca',
            'autor',
            'reu',
            'valor_causa',
            'advogado',
            'oab'
        ]
        
        # Filtrar apenas colunas que existem
        colunas_existentes = [c for c in colunas_principais if c in df.columns]
        
        # Renomear colunas para exibição
        colunas_renomeadas = {
            'numero_processo': 'Número do Processo',
            'data_envio': 'Data Ajuizamento',
            'comarca': 'Comarca',
            'autor': 'Autor',
            'reu': 'Réu',
            'valor_causa': 'Valor da Causa',
            'advogado': 'Advogado',
            'oab': 'OAB'
        }
        
        df_display = df[colunas_existentes].rename(columns=colunas_renomeadas)
        
        st.dataframe(
            df_display,
            use_container_width=True,
            hide_index=True
        )
        
        # Botões de download
        st.markdown("### 💾 Download dos Dados")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            # CSV
            csv_data = df.to_csv(index=False, sep=';', encoding='utf-8-sig')
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            st.download_button(
                label="📥 Baixar CSV",
                data=csv_data,
                file_name=f"protocolos_{timestamp}.csv",
                mime="text/csv",
                use_container_width=True
            )
        
        with col2:
            # Excel
            try:
                buffer = io.BytesIO()
                df.to_excel(buffer, index=False, engine='openpyxl')
                buffer.seek(0)
                
                st.download_button(
                    label="📥 Baixar Excel",
                    data=buffer,
                    file_name=f"protocolos_{timestamp}.xlsx",
                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    use_container_width=True
                )
            except Exception as e:
                st.warning(f"Excel não disponível: {e}")
        
        with col3:
            # Limpar dados
            if st.button("🗑️ Limpar Dados", use_container_width=True, type="secondary"):
                st.session_state.resultados_protocolos = None
                st.session_state.df_protocolos = None
                st.rerun()
        
        # Expandir para ver todos os dados
        with st.expander("🔍 Ver todos os campos extraídos"):
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Estatísticas adicionais
        with st.expander("📊 Estatísticas"):
            col1, col2 = st.columns(2)
            
            with col1:
                if 'comarca' in df.columns:
                    st.markdown("**Processos por Comarca:**")
                    comarca_counts = df['comarca'].value_counts()
                    st.bar_chart(comarca_counts)
            
            with col2:
                if 'data_envio' in df.columns:
                    st.markdown("**Distribuição por Data:**")
                    try:
                        df['data_envio_dt'] = pd.to_datetime(df['data_envio'], format='%d/%m/%Y', errors='coerce')
                        data_counts = df['data_envio_dt'].dt.date.value_counts().sort_index()
                        st.line_chart(data_counts)
                    except:
                        st.write("Não foi possível gerar gráfico de datas")
    
    else:
        st.info("""
        👆 **Como usar o Extrator de Protocolos:**
        
        1. Clique em "Browse files" ou arraste os arquivos PDF
        2. Selecione múltiplos arquivos usando Ctrl+Click
        3. Clique em "Processar Protocolos"
        4. Baixe o CSV ou Excel com os dados extraídos
        
        **Dados extraídos:**
        - Número do processo
        - Data de ajuizamento
        - Comarca
        - Autor e Réu
        - Valor da causa
        - Advogado e OAB
        - Órgão julgador
        - Magistrado
        """)


def main():
    initialize_session_state()
    
    # Cabeçalho
    st.markdown('<div class="main-header">⚖️ Assistente Jurídico com IA</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">Analise documentos jurídicos com Inteligência Artificial</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.header("📋 Menu Principal")
        
        # Seleção de funcionalidade
        funcionalidade = st.radio(
            "Escolha a ferramenta:",
            options=[
                "📄 Análise de Documento",
                "📋 Extrator de Protocolos"
            ],
            index=0,
            key="menu_principal"
        )
        
        st.divider()
        
        st.header("ℹ️ Sobre o Projeto")
        st.markdown("""
        Este assistente utiliza IA para:
        - 📄 Extrair texto de PDFs
        - 🔍 Identificar informações-chave
        - 💬 Responder perguntas sobre o documento
        - 📊 Gerar resumos automaticamente
        - 📋 Extrair dados de protocolos em lote
        
        **Tecnologias:**
        - Python
        - LangChain
        - Groq (LLaMA 3.1)
        - Streamlit
        """)
        
        st.divider()
        
        # Configurações
        with st.expander("⚙️ Configurações"):
            groq_key = st.text_input(
                "Groq API Key",
                type="password",
                help="Sua chave de API da Groq",
                value=os.getenv("GROQ_API_KEY", "")
            )
            
            if groq_key:
                os.environ["GROQ_API_KEY"] = groq_key
        
        st.divider()
        
        # Informações do desenvolvedor
        st.markdown("""
        **Desenvolvedor:**  
        Bruno Daniel Goettems
        
        [GitHub](https://github.com/goettemsb) | [LinkedIn](https://linkedin.com/in/goettemsb)
        """)
    
    # Renderizar página selecionada
    if funcionalidade == "📄 Análise de Documento":
        render_analise_documento()
    elif funcionalidade == "📋 Extrator de Protocolos":
        render_extrator_protocolos()


if __name__ == "__main__":
    main()