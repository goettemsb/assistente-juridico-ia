"""
Testes unitários para o Assistente Jurídico IA
"""
import pytest
from pathlib import Path
import sys

# Adicionar src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pdf_processor import PDFProcessor
from ai_extractor import LegalAIExtractor, DocumentoJuridico


# Texto de exemplo para testes
TEXTO_EXEMPLO = """
TRIBUNAL DE JUSTIÇA DO RIO GRANDE DO SUL
COMARCA DE SANTA ROSA

Processo nº 1000123-45.2024.8.21.0001

AÇÃO DE COBRANÇA

AUTOR: João da Silva, CPF 123.456.789-00
ADVOGADO: Dr. Carlos Santos (OAB/RS 12345)

RÉU: Empresa ABC Ltda, CNPJ 12.345.678/0001-90
ADVOGADO: Dra. Maria Oliveira (OAB/RS 67890)

VALOR DA CAUSA: R$ 50.000,00

Trata-se de ação de cobrança...
"""


class TestPDFProcessor:
    """Testes para o processador de PDF."""
    
    def test_pdf_processor_initialization(self):
        """Testa se o processador é inicializado corretamente."""
        # Criar arquivo temporário para teste
        test_file = Path("test_temp.txt")
        test_file.write_text("Teste")
        
        try:
            processor = PDFProcessor(str(test_file))
            assert processor.pdf_path.exists()
        finally:
            if test_file.exists():
                test_file.unlink()
    
    def test_pdf_processor_file_not_found(self):
        """Testa se levanta erro quando arquivo não existe."""
        with pytest.raises(FileNotFoundError):
            PDFProcessor("arquivo_inexistente.pdf")


class TestLegalAIExtractor:
    """Testes para o extrator de IA."""
    
    @pytest.fixture
    def extractor(self):
        """Fixture para criar extrator."""
        # Nota: Precisa de API key configurada
        try:
            return LegalAIExtractor()
        except ValueError:
            pytest.skip("API key não configurada")
    
    def test_extractor_initialization(self, extractor):
        """Testa inicialização do extrator."""
        assert extractor is not None
        assert extractor.llm is not None
    
    def test_extract_information_structure(self, extractor):
        """Testa se a extração retorna estrutura correta."""
        result = extractor.extract_information(TEXTO_EXEMPLO)
        
        assert isinstance(result, DocumentoJuridico)
        assert hasattr(result, 'tipo_documento')
        assert hasattr(result, 'partes')
        assert hasattr(result, 'dados_processo')
        assert hasattr(result, 'resumo')
    
    def test_generate_summary(self, extractor):
        """Testa geração de resumo."""
        summary = extractor.generate_summary(TEXTO_EXEMPLO)
        
        assert isinstance(summary, str)
        assert len(summary) > 0
    
    def test_answer_question(self, extractor):
        """Testa resposta a perguntas."""
        answer = extractor.answer_question(
            TEXTO_EXEMPLO,
            "Qual é o número do processo?"
        )
        
        assert isinstance(answer, str)
        assert len(answer) > 0
        # Deve conter o número do processo
        assert "1000123-45.2024.8.21.0001" in answer or "número" in answer.lower()


class TestDataModels:
    """Testa os modelos de dados."""
    
    def test_documento_juridico_creation(self):
        """Testa criação de um documento jurídico."""
        from ai_extractor import PartesProcesso, DadosProcesso
        
        partes = PartesProcesso(
            autor="João da Silva",
            reu="Empresa ABC",
            advogado_autor="Dr. Carlos",
            advogado_reu="Dra. Maria"
        )
        
        dados = DadosProcesso(
            numero_processo="1000123-45.2024.8.21.0001",
            classe="Ação de Cobrança",
            assunto="Cobrança",
            vara="1ª Vara Cível",
            data_distribuicao="01/01/2024"
        )
        
        doc = DocumentoJuridico(
            tipo_documento="Petição Inicial",
            partes=partes,
            dados_processo=dados,
            prazos=[],
            resumo="Teste de resumo",
            pontos_principais=["Ponto 1", "Ponto 2"]
        )
        
        assert doc.tipo_documento == "Petição Inicial"
        assert doc.partes.autor == "João da Silva"
        assert doc.dados_processo.numero_processo == "1000123-45.2024.8.21.0001"


# Testes de integração
class TestIntegration:
    """Testes de integração end-to-end."""
    
    @pytest.fixture
    def setup_api_key(self):
        """Configura API key para testes."""
        import os
        if not os.getenv("OPENAI_API_KEY"):
            pytest.skip("OPENAI_API_KEY não configurada")
    
    def test_full_workflow(self, setup_api_key):
        """Testa fluxo completo de processamento."""
        extractor = LegalAIExtractor()
        
        # 1. Extrair informações
        doc = extractor.extract_information(TEXTO_EXEMPLO)
        assert doc is not None
        
        # 2. Gerar resumo
        summary = extractor.generate_summary(TEXTO_EXEMPLO)
        assert len(summary) > 50
        
        # 3. Responder pergunta
        answer = extractor.answer_question(TEXTO_EXEMPLO, "Quem é o autor?")
        assert "João" in answer or "Silva" in answer


# Executar testes
if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
