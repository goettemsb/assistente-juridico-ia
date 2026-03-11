"""
Módulo de extração de informações jurídicas usando LangChain e LLM.
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List, Optional
import os
from dotenv import load_dotenv

load_dotenv()


class PartesProcesso(BaseModel):
    """Modelo para partes do processo."""
    autor: Optional[str] = Field(default="Não identificado", description="Nome do autor/requerente")
    reu: Optional[str] = Field(default="Não identificado", description="Nome do réu/requerido")
    advogado_autor: Optional[str] = Field(default=None, description="Advogado do autor")
    advogado_reu: Optional[str] = Field(default=None, description="Advogado do réu")


class DadosProcesso(BaseModel):
    """Modelo para dados principais do processo."""
    numero_processo: Optional[str] = Field(default=None, description="Número do processo judicial")
    classe: Optional[str] = Field(default=None, description="Classe processual")
    assunto: Optional[str] = Field(default=None, description="Assunto/tema do processo")
    vara: Optional[str] = Field(default=None, description="Vara ou comarca")
    data_distribuicao: Optional[str] = Field(default=None, description="Data de distribuição")


class Prazos(BaseModel):
    """Modelo para prazos processuais."""
    descricao: Optional[str] = Field(default="Não especificado", description="Descrição do prazo")
    data_limite: Optional[str] = Field(default="Não especificado", description="Data limite do prazo")
    dias_restantes: Optional[int] = Field(default=None, description="Dias restantes até o prazo")


class DocumentoJuridico(BaseModel):
    """Modelo completo do documento jurídico."""
    tipo_documento: Optional[str] = Field(default="Documento jurídico", description="Tipo de documento (petição, sentença, acórdão, etc.)")
    partes: Optional[PartesProcesso] = Field(default=None, description="Partes envolvidas no processo")
    dados_processo: Optional[DadosProcesso] = Field(default=None, description="Dados do processo")
    prazos: List[Prazos] = Field(default=[], description="Prazos identificados")
    resumo: Optional[str] = Field(default="Resumo não disponível", description="Resumo executivo do documento")
    pontos_principais: List[str] = Field(default=[], description="Principais pontos do documento")


class LegalAIExtractor:
    """Extrator de informações jurídicas usando IA."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "llama-3.1-8b-instant"):
        """
        Inicializa o extrator com LLM.
        
        Args:
            api_key: Chave da API Groq (opcional, pode vir do .env)
            model: Nome do modelo a usar
        """
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        if not self.api_key:
            raise ValueError("API key não fornecida. Configure GROQ_API_KEY no .env")
        
        self.model = model
        self.llm = ChatGroq(
            model=self.model,
            temperature=0,
            api_key=self.api_key
        )
        self.parser = PydanticOutputParser(pydantic_object=DocumentoJuridico)
    
    def extract_information(self, text: str) -> DocumentoJuridico:
        """
        Extrai informações estruturadas do texto jurídico.
        
        Args:
            text: Texto do documento jurídico
            
        Returns:
            Objeto DocumentoJuridico com informações extraídas
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um assistente jurídico especializado em análise de documentos.
            Sua tarefa é extrair informações estruturadas de documentos jurídicos brasileiros.
            
            IMPORTANTE: 
            - Se alguma informação não estiver presente, use string vazia "" ao invés de null
            - Para campos de texto ausentes, use "Não identificado" ou "Não especificado"
            - Nunca retorne null para campos de string
            
            Para prazos, identifique qualquer menção a datas limites, audiências, ou 
            obrigações com prazo determinado.
            
            {format_instructions}
            """),
            ("user", "Analise o seguinte documento jurídico:\n\n{text}")
        ])
        
        chain = prompt | self.llm | self.parser
        
        try:
            result = chain.invoke({
                "text": text[:15000],
                "format_instructions": self.parser.get_format_instructions()
            })
            return result
        except Exception as e:
            print(f"Erro ao extrair informações: {e}")
            # Retorna um documento padrão em caso de erro
            return DocumentoJuridico(
                tipo_documento="Documento jurídico",
                partes=PartesProcesso(
                    autor="Não identificado",
                    reu="Não identificado"
                ),
                dados_processo=DadosProcesso(),
                prazos=[],
                resumo="Não foi possível extrair informações automaticamente.",
                pontos_principais=[]
            )
    
    def generate_summary(self, text: str, max_words: int = 200) -> str:
        """
        Gera um resumo do documento.
        
        Args:
            text: Texto completo do documento
            max_words: Número máximo de palavras no resumo
            
        Returns:
            Resumo do documento
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""Você é um assistente jurídico especializado.
            Crie um resumo executivo do documento em até {max_words} palavras.
            Foque nos pontos mais importantes e relevantes.
            Use linguagem clara e objetiva."""),
            ("user", "Documento:\n\n{text}")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({"text": text[:15000]})
            return response.content
        except Exception as e:
            print(f"Erro ao gerar resumo: {e}")
            return "Erro ao gerar resumo."
    
    def answer_question(self, text: str, question: str) -> str:
        """
        Responde uma pergunta sobre o documento.
        
        Args:
            text: Texto do documento
            question: Pergunta do usuário
            
        Returns:
            Resposta à pergunta
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Você é um assistente jurídico especializado em direito brasileiro.
            Responda à pergunta do usuário baseando-se APENAS nas informações contidas 
            no documento fornecido.
            
            Se a informação não estiver no documento, diga claramente que não foi possível
            encontrar essa informação no documento fornecido.
            
            Seja preciso, objetivo e cite trechos do documento quando relevante."""),
            ("user", """Documento:
{text}

Pergunta: {question}

Resposta:""")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "text": text[:15000],
                "question": question
            })
            return response.content
        except Exception as e:
            print(f"Erro ao responder pergunta: {e}")
            return "Desculpe, ocorreu um erro ao processar sua pergunta."
    
    def extract_specific_field(self, text: str, field: str) -> str:
        """
        Extrai um campo específico do documento.
        
        Args:
            text: Texto do documento
            field: Campo a ser extraído (ex: "número do processo", "valor da causa")
            
        Returns:
            Valor extraído
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"""Extraia APENAS a informação solicitada: {field}
            
            Se não encontrar, retorne "Não encontrado".
            Retorne apenas o valor, sem explicações adicionais."""),
            ("user", "Documento:\n\n{text}")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({"text": text[:15000]})
            return response.content.strip()
        except Exception as e:
            print(f"Erro ao extrair campo: {e}")
            return "Erro na extração."


# Exemplo de uso
if __name__ == "__main__":
    texto_exemplo = """
    PROCESSO Nº 1000123-45.2024.8.21.0001
    
    AUTOR: João da Silva
    ADVOGADO: Dr. Carlos Santos (OAB/RS 12345)
    
    RÉU: Empresa XYZ Ltda
    ADVOGADO: Dra. Maria Oliveira (OAB/RS 67890)
    
    Trata-se de ação trabalhista visando o pagamento de horas extras...
    Prazo para contestação: 15 dias a contar da intimação.
    """
    
    try:
        extractor = LegalAIExtractor()
        
        print("=== TESTE DE EXTRAÇÃO ===")
        resultado = extractor.extract_information(texto_exemplo)
        print(f"\nTipo: {resultado.tipo_documento}")
        print(f"Autor: {resultado.partes.autor}")
        print(f"Réu: {resultado.partes.reu}")
        print(f"\nResumo: {resultado.resumo}")
        
    except Exception as e:
        print(f"Erro no teste: {e}")
        print("\nCertifique-se de configurar GROQ_API_KEY no arquivo .env")