"""
Módulo src - Componentes do Assistente Jurídico
"""
from .pdf_processor import PDFProcessor
from .ai_extractor import LegalAIExtractor, DocumentoJuridico
from .document_chat import LegalDocumentChat, QuickQuestions
from .protocol_extractor import ProtocolExtractor, DadosProtocolo

__all__ = [
    'PDFProcessor',
    'LegalAIExtractor',
    'DocumentoJuridico',
    'LegalDocumentChat',
    'QuickQuestions',
    'ProtocolExtractor',
    'DadosProtocolo'
]