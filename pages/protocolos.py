"""
Página para extração em lote de protocolos judiciais.
"""
import streamlit as st
import pandas as pd
from src.protocol_extractor import ProtocolExtractor, DadosProtocolo
from datetime import datetime


def main():
    st.set_page_config(
        page_title="Extrator de Protocolos",
        page_icon="📋",
        layout="wide"
    )
    
    st.title("📋 Extrator de Protocolos Judiciais")
    st.markdown("---")
    
    st.markdown("""
    ### Como usar:
    1. Faça upload de um ou mais PDFs de protocolos da Justiça Estadual
    2. Clique em **Processar Protocolos**
    3. Visualize os dados extraídos
    4. Baixe o arquivo CSV com todos os dados
    """)
    
    # Upload múltiplo de arquivos
    uploaded_files = st.file_uploader(
        "📁 Selecione os PDFs de protocolo",
        type=['pdf'],
        accept_multiple_files=True,
        help="Você pode selecionar múltiplos arquivos de uma vez"
    )
    
    if uploaded_files:
        st.success(f"✅ {len(uploaded_files)} arquivo(s) selecionado(s)")
        
        # Mostrar lista de arquivos
        with st.expander("📄 Arquivos selecionados"):
            for i, file in enumerate(uploaded_files, 1):
                st.write(f"{i}. {file.name}")
        
        # Botão para processar
        if st.button("🚀 Processar Protocolos", type="primary", use_container_width=True):
            
            extractor = ProtocolExtractor()
            resultados = []
            
            # Barra de progresso
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            for i, pdf_file in enumerate(uploaded_files):
                status_text.text(f"Processando: {pdf_file.name} ({i+1}/{len(uploaded_files)})")
                
                try:
                    dados = extractor.extract_protocol_data(pdf_file)
                    dados.arquivo_origem = pdf_file.name  # Adicionar nome do arquivo
                    resultados.append(dados)
                except Exception as e:
                    st.error(f"❌ Erro ao processar {pdf_file.name}: {e}")
                
                progress_bar.progress((i + 1) / len(uploaded_files))
            
            status_text.text("✅ Processamento concluído!")
            
            if resultados:
                # Guardar no session_state
                st.session_state.resultados_protocolos = resultados
                st.session_state.df_protocolos = extractor.to_dataframe(resultados)
    
    # Mostrar resultados se existirem
    if 'df_protocolos' in st.session_state and not st.session_state.df_protocolos.empty:
        st.markdown("---")
        st.subheader("📊 Dados Extraídos")
        
        df = st.session_state.df_protocolos
        
        # Métricas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total de Protocolos", len(df))
        with col2:
            comarcas = df['comarca'].nunique()
            st.metric("Comarcas", comarcas)
        with col3:
            autores = df['autor'].nunique()
            st.metric("Autores Únicos", autores)
        with col4:
            reus = df['reu'].nunique()
            st.metric("Réus Únicos", reus)
        
        # Tabela de dados
        st.markdown("### 📋 Tabela de Protocolos")
        
        # Selecionar colunas para exibir
        colunas_exibir = [
            'numero_processo',
            'data_envio',
            'comarca',
            'autor',
            'reu',
            'valor_causa',
            'advogado'
        ]
        
        # Filtrar apenas colunas que existem
        colunas_existentes = [c for c in colunas_exibir if c in df.columns]
        
        st.dataframe(
            df[colunas_existentes],
            use_container_width=True,
            hide_index=True
        )
        
        # Botões de download
        st.markdown("### 💾 Download dos Dados")
        
        col1, col2 = st.columns(2)
        
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
                import io
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
                st.warning("Excel não disponível. Instale openpyxl.")
        
        # Expandir para ver todos os dados
        with st.expander("🔍 Ver todos os campos"):
            st.dataframe(df, use_container_width=True, hide_index=True)
        
        # Limpar dados
        if st.button("🗑️ Limpar Dados"):
            del st.session_state.resultados_protocolos
            del st.session_state.df_protocolos
            st.rerun()


if __name__ == "__main__":
    main()