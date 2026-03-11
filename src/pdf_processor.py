"""
Módulo para processamento de documentos PDF jurídicos.
"""
import pdfplumber
import PyPDF2
from typing import Dict, List, Optional
from pathlib import Path


class PDFProcessor:
    """Classe para extrair texto e metadados de PDFs jurídicos."""
    
    def __init__(self, pdf_path: str):
        """
        Inicializa o processador de PDF.
        
        Args:
            pdf_path: Caminho para o arquivo PDF
        """
        self.pdf_path = Path(pdf_path)
        if not self.pdf_path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {pdf_path}")
    
    def extract_text(self) -> str:
        """
        Extrai todo o texto do PDF.
        
        Returns:
            Texto completo do documento
        """
        text = ""
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n\n"
        except Exception as e:
            print(f"Erro ao extrair texto com pdfplumber: {e}")
            # Fallback para PyPDF2
            text = self._extract_with_pypdf2()
        
        return text.strip()
    
    def _extract_with_pypdf2(self) -> str:
        """Método alternativo de extração usando PyPDF2."""
        text = ""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n\n"
        except Exception as e:
            print(f"Erro ao extrair texto com PyPDF2: {e}")
        
        return text.strip()
    
    def extract_metadata(self) -> Dict:
        """
        Extrai metadados do PDF.
        
        Returns:
            Dicionário com metadados do documento
        """
        metadata = {}
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                info = pdf_reader.metadata
                
                metadata = {
                    'titulo': info.get('/Title', 'N/A'),
                    'autor': info.get('/Author', 'N/A'),
                    'criador': info.get('/Creator', 'N/A'),
                    'produtor': info.get('/Producer', 'N/A'),
                    'criacao': info.get('/CreationDate', 'N/A'),
                    'modificacao': info.get('/ModDate', 'N/A'),
                    'num_paginas': len(pdf_reader.pages),
                    'tamanho_arquivo': self.pdf_path.stat().st_size
                }
        except Exception as e:
            print(f"Erro ao extrair metadados: {e}")
            metadata = {'erro': str(e)}
        
        return metadata
    
    def extract_text_by_page(self) -> List[str]:
        """
        Extrai texto separado por página.
        
        Returns:
            Lista com texto de cada página
        """
        pages = []
        try:
            with pdfplumber.open(self.pdf_path) as pdf:
                for i, page in enumerate(pdf.pages):
                    page_text = page.extract_text()
                    if page_text:
                        pages.append({
                            'numero': i + 1,
                            'texto': page_text.strip()
                        })
        except Exception as e:
            print(f"Erro ao extrair páginas: {e}")
        
        return pages
    
    def get_summary(self) -> Dict:
        """
        Retorna um resumo do documento.
        
        Returns:
            Dicionário com informações resumidas
        """
        text = self.extract_text()
        metadata = self.extract_metadata()
        
        return {
            'arquivo': self.pdf_path.name,
            'tamanho_kb': metadata.get('tamanho_arquivo', 0) / 1024,
            'num_paginas': metadata.get('num_paginas', 0),
            'num_caracteres': len(text),
            'num_palavras': len(text.split()),
            'preview': text[:500] + '...' if len(text) > 500 else text
        }


# Exemplo de uso
if __name__ == "__main__":
    # Teste básico
    pdf_path = "../data/input/exemplo.pdf"
    
    if Path(pdf_path).exists():
        processor = PDFProcessor(pdf_path)
        
        print("=== RESUMO DO DOCUMENTO ===")
        summary = processor.get_summary()
        for key, value in summary.items():
            print(f"{key}: {value}")
        
        print("\n=== METADADOS ===")
        metadata = processor.extract_metadata()
        for key, value in metadata.items():
            print(f"{key}: {value}")
    else:
        print(f"Arquivo de exemplo não encontrado em {pdf_path}")
