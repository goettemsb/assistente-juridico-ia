#!/usr/bin/env python3
"""
Script de demonstração rápida do Assistente Jurídico IA

Este script mostra como usar as funcionalidades principais do projeto
sem precisar executar a interface web.
"""
import os
import sys
from pathlib import Path

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.pdf_processor import PDFProcessor
from src.ai_extractor import LegalAIExtractor
from src.document_chat import LegalDocumentChat, QuickQuestions


def print_header(title):
    """Imprime um cabeçalho formatado."""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")


def demo_extraction():
    """Demonstração de extração de informações."""
    print_header("DEMONSTRAÇÃO: Extração de Informações com IA")
    
    # Texto de exemplo
    texto = """
    TRIBUNAL DE JUSTIÇA DO RIO GRANDE DO SUL
    COMARCA DE SANTA ROSA - 1ª VARA CÍVEL
    
    Processo nº 1000123-45.2024.8.21.0001
    
    AÇÃO DE COBRANÇA
    
    AUTOR: João da Silva Santos
    CPF: 123.456.789-00
    ADVOGADO: Dr. Carlos Alberto Santos (OAB/RS 12345)
    
    RÉU: Empresa ABC Comércio e Serviços Ltda
    CNPJ: 12.345.678/0001-90
    ADVOGADO: Dra. Maria Fernanda Oliveira (OAB/RS 67890)
    
    VALOR DA CAUSA: R$ 50.000,00
    
    RESUMO DOS FATOS:
    
    Trata-se de ação de cobrança movida pelo autor em face da ré, objetivando
    o recebimento de valores devidos em razão de contrato de prestação de serviços
    firmado entre as partes em 15/01/2023.
    
    O autor alega que prestou serviços de consultoria à ré no período de janeiro
    a dezembro de 2023, conforme contrato anexo, totalizando o valor de R$ 50.000,00.
    
    Contudo, a ré não efetuou o pagamento dos valores devidos, razão pela qual
    o autor pleiteia a condenação da ré ao pagamento do valor principal, acrescido
    de correção monetária e juros de mora.
    
    PEDIDOS:
    
    a) Condenação da ré ao pagamento de R$ 50.000,00;
    b) Aplicação de correção monetária e juros de mora;
    c) Condenação da ré ao pagamento de custas processuais e honorários advocatícios.
    
    PRAZOS:
    - Citação da ré: 30 dias
    - Contestação: 15 dias após a citação
    - Próxima audiência: 15/03/2025
    
    Santa Rosa, 15 de janeiro de 2025.
    
    Dr. Carlos Alberto Santos
    OAB/RS 12345
    """
    
    print("📄 Processando documento de exemplo...")
    
    try:
        # Inicializar extrator
        extractor = LegalAIExtractor()
        
        # Extrair informações
        print("\n🤖 Extraindo informações com IA...\n")
        resultado = extractor.extract_information(texto)
        
        # Exibir resultados
        print("✅ INFORMAÇÕES EXTRAÍDAS:\n")
        
        print(f"📋 Tipo de Documento: {resultado.tipo_documento}")
        print(f"\n👥 PARTES:")
        print(f"   Autor: {resultado.partes.autor}")
        print(f"   Réu: {resultado.partes.reu}")
        if resultado.partes.advogado_autor:
            print(f"   Advogado do Autor: {resultado.partes.advogado_autor}")
        if resultado.partes.advogado_reu:
            print(f"   Advogado do Réu: {resultado.partes.advogado_reu}")
        
        print(f"\n📊 DADOS DO PROCESSO:")
        print(f"   Número: {resultado.dados_processo.numero_processo}")
        print(f"   Classe: {resultado.dados_processo.classe}")
        print(f"   Assunto: {resultado.dados_processo.assunto}")
        print(f"   Vara: {resultado.dados_processo.vara}")
        
        print(f"\n📝 RESUMO:")
        print(f"   {resultado.resumo}")
        
        print(f"\n🎯 PONTOS PRINCIPAIS:")
        for i, ponto in enumerate(resultado.pontos_principais, 1):
            print(f"   {i}. {ponto}")
        
        if resultado.prazos:
            print(f"\n⏰ PRAZOS:")
            for prazo in resultado.prazos:
                print(f"   • {prazo.descricao} - {prazo.data_limite}")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        print("\n💡 Dica: Certifique-se de ter configurado OPENAI_API_KEY no arquivo .env")
        return False


def demo_chat():
    """Demonstração do sistema de chat."""
    print_header("DEMONSTRAÇÃO: Chat Interativo")
    
    texto = """
    PROCESSO Nº 5001234-56.2024.8.21.0001
    AÇÃO TRABALHISTA
    
    RECLAMANTE: Maria Santos
    RECLAMADA: Empresa XYZ Ltda
    
    OBJETO: Horas extras não pagas no período de 2020-2023
    VALOR DA CAUSA: R$ 100.000,00
    
    A reclamante trabalhou na reclamada de 2018 a 2023, realizando
    frequentemente horas extras que não foram devidamente pagas.
    """
    
    try:
        chat = LegalDocumentChat(texto)
        
        perguntas = [
            "Qual é o número do processo?",
            "Quem são as partes?",
            "Qual é o objeto da ação?"
        ]
        
        for pergunta in perguntas:
            print(f"👤 Pergunta: {pergunta}")
            resposta = chat.ask(pergunta)
            print(f"🤖 Resposta: {resposta}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def demo_quick_questions():
    """Demonstração de perguntas rápidas."""
    print_header("DEMONSTRAÇÃO: Perguntas Rápidas")
    
    texto = """
    Processo: 7001111-22.2024.8.21.0001
    Autor: Pedro Rodrigues
    Réu: Banco ABC S.A.
    Valor da Causa: R$ 30.000,00
    Tipo: Ação Revisional de Contrato
    Prazo para contestação: 15 dias
    """
    
    try:
        quick = QuickQuestions(texto)
        
        print("📋 Número do Processo:")
        print(f"   {quick.get_numero_processo()}\n")
        
        print("👥 Partes:")
        print(f"   {quick.get_partes()}\n")
        
        print("📊 Tipo de Ação:")
        print(f"   {quick.get_tipo_acao()}\n")
        
        print("💰 Valor da Causa:")
        print(f"   {quick.get_valor_causa()}\n")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False


def main():
    """Função principal."""
    print_header("🔧 ASSISTENTE JURÍDICO IA - DEMONSTRAÇÃO")
    
    print("""
Este script demonstra as principais funcionalidades do projeto:
1. Extração automática de informações
2. Sistema de chat interativo
3. Perguntas rápidas

Certifique-se de ter configurado a API key no arquivo .env antes de executar.
    """)
    
    input("Pressione ENTER para continuar...")
    
    # Demo 1: Extração
    success1 = demo_extraction()
    
    if not success1:
        print("\n⚠️ A demonstração encontrou problemas.")
        print("Verifique a configuração da API key e tente novamente.")
        return
    
    input("\nPressione ENTER para ver a próxima demonstração...")
    
    # Demo 2: Chat
    demo_chat()
    
    input("\nPressione ENTER para ver a última demonstração...")
    
    # Demo 3: Quick Questions
    demo_quick_questions()
    
    print_header("✅ DEMONSTRAÇÃO CONCLUÍDA")
    
    print("""
Para usar a interface web completa, execute:

    streamlit run app.py

Obrigado por testar o Assistente Jurídico IA! 🚀
    """)


if __name__ == "__main__":
    main()
