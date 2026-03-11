"""
Módulo para extração de dados de protocolos judiciais.
"""
import re
import pdfplumber
from typing import Dict, List, Optional
from dataclasses import dataclass, asdict
from datetime import datetime
import csv
import io


@dataclass
class DadosProtocolo:
    """Estrutura de dados do protocolo judicial."""
    numero_processo: str = ""
    chave_consulta: str = ""
    advogado: str = ""
    oab: str = ""
    data_envio: str = ""
    hora_envio: str = ""
    evento: str = ""
    autor: str = ""
    reu: str = ""
    valor_causa: str = ""
    orgao_julgador: str = ""
    comarca: str = ""
    magistrado: str = ""
    data_impressao: str = ""


class ProtocolExtractor:
    """Extrator de dados de protocolos da Justiça Estadual."""
    
    def __init__(self):
        self.patterns = {
            'numero_processo': r'Número do Processo:\s*([0-9.\-]+)',
            'chave_consulta': r'Chave para consulta:\s*(\d+)',
            'advogado': r'Nome:\s*([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+?)(?=\n|OAB)',
            'oab': r'OAB/Sigla:\s*([A-Z]{2}\d+)',
            'data_envio': r'Data Envio:\s*(\d{2}/\d{2}/\d{4})',
            'hora_envio': r'Hora de Envio:\s*(\d{2}:\d{2}:\d{2})',
            'evento': r'Evento:\s*(.+?)(?=\n)',
            'valor_causa': r'Valor da Causa:\s*R\$\s*([\d.,]+)',
            'orgao_julgador': r'Órgão Julgador:\s*(.+?)(?=\n)',
            'magistrado': r'Magistrado:\s*([A-ZÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+?)(?=\n)',
            'data_impressao': r'Data de Impressão:\s*(\d{2}/\d{2}/\d{4}\s*\d{2}:\d{2}:\d{2})',
        }
    
    def extract_text_from_pdf(self, pdf_file) -> str:
        """Extrai texto do PDF."""
        text = ""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            print(f"Erro ao extrair texto: {e}")
        return text
    
    def extract_partes(self, text: str) -> tuple:
        """Extrai autor e réu do texto."""
        autor = ""
        reu = ""
        
        # Padrão para Nome da(s) Parte(s)
        partes_match = re.search(
            r'Nome da\(s\) Parte\(s\):\s*(.+?)(?=Valor da Causa|Órgão Julgador)',
            text,
            re.DOTALL | re.IGNORECASE
        )
        
        if partes_match:
            partes_text = partes_match.group(1).strip()
            
            # Procurar AUTOR
            autor_match = re.search(r'(.+?)\s*[-–]\s*AUTOR', partes_text, re.IGNORECASE)
            if autor_match:
                autor = autor_match.group(1).strip()
            
            # Procurar RÉU
            reu_match = re.search(r'(.+?)\s*[-–]\s*R[ÉE]U', partes_text, re.IGNORECASE)
            if reu_match:
                reu = reu_match.group(1).strip()
                # Remover "X" que aparece antes do réu
                reu = re.sub(r'^X\s*', '', reu).strip()
        
        return autor, reu
    
    def extract_comarca(self, text: str) -> str:
        """Extrai a comarca do órgão julgador."""
        orgao_match = re.search(self.patterns['orgao_julgador'], text, re.IGNORECASE)
        if orgao_match:
            orgao = orgao_match.group(1)
            # Extrair comarca do texto do órgão
            comarca_match = re.search(r'Comarca de\s*([A-Za-záàâãéèêíïóôõöúçñÁÀÂÃÉÈÊÍÏÓÔÕÖÚÇÑ\s]+)', orgao, re.IGNORECASE)
            if comarca_match:
                return comarca_match.group(1).strip()
            # Se não encontrar "Comarca de", retorna o órgão inteiro
            return orgao.strip()
        return ""
    
    def extract_protocol_data(self, pdf_file) -> DadosProtocolo:
        """Extrai todos os dados do protocolo."""
        text = self.extract_text_from_pdf(pdf_file)
        
        dados = DadosProtocolo()
        
        # Extrair campos usando regex
        for field, pattern in self.patterns.items():
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                setattr(dados, field, match.group(1).strip())
        
        # Extrair partes (autor e réu)
        dados.autor, dados.reu = self.extract_partes(text)
        
        # Extrair comarca
        dados.comarca = self.extract_comarca(text)
        
        # Limpar valor da causa (remover pontos de milhar, manter vírgula decimal)
        if dados.valor_causa:
            dados.valor_causa = f"R$ {dados.valor_causa}"
        
        return dados
    
    def process_multiple_pdfs(self, pdf_files: List) -> List[DadosProtocolo]:
        """Processa múltiplos PDFs e retorna lista de dados."""
        resultados = []
        for pdf_file in pdf_files:
            try:
                dados = self.extract_protocol_data(pdf_file)
                resultados.append(dados)
            except Exception as e:
                print(f"Erro ao processar {pdf_file.name}: {e}")
        return resultados
    
    def to_dataframe(self, dados_list: List[DadosProtocolo]):
        """Converte lista de dados para DataFrame."""
        import pandas as pd
        return pd.DataFrame([asdict(d) for d in dados_list])
    
    def to_csv(self, dados_list: List[DadosProtocolo]) -> str:
        """Converte lista de dados para string CSV."""
        if not dados_list:
            return ""
        
        output = io.StringIO()
        fieldnames = [
            'numero_processo', 
            'data_envio', 
            'comarca', 
            'autor', 
            'reu', 
            'valor_causa',
            'advogado',
            'oab',
            'orgao_julgador',
            'magistrado',
            'evento',
            'chave_consulta'
        ]
        
        writer = csv.DictWriter(output, fieldnames=fieldnames, delimiter=';')
        writer.writeheader()
        
        for dados in dados_list:
            row = {field: getattr(dados, field, '') for field in fieldnames}
            writer.writerow(row)
        
        return output.getvalue()


# Teste
if __name__ == "__main__":
    extractor = ProtocolExtractor()
    print("Extrator de protocolos criado com sucesso!")