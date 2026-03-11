"""
Módulo de chat interativo com documentos jurídicos.
"""
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage
from typing import List, Dict
import os


class LegalDocumentChat:
    """Sistema de chat para interagir com documentos jurídicos."""
    
    def __init__(self, document_text: str, api_key: str = None):
        """
        Inicializa o sistema de chat.
        
        Args:
            document_text: Texto completo do documento
            api_key: Chave da API Groq
        """
        self.document_text = document_text
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0.3,
            api_key=self.api_key
        )
        
        # Histórico de mensagens
        self.messages_history: List = []
        
        # Histórico para interface
        self.chat_history: List[Dict[str, str]] = []
        
        # Configurar o prompt do sistema
        self.system_prompt = f"""Você é um assistente jurídico especializado em direito brasileiro.
        
Você está analisando o seguinte documento:

=== DOCUMENTO ===
{document_text[:10000]}
=== FIM DO DOCUMENTO ===

Suas responsabilidades:
1. Responder perguntas sobre o documento de forma clara e precisa
2. Citar trechos relevantes quando apropriado
3. Explicar termos jurídicos quando necessário
4. Se a informação não estiver no documento, dizer claramente
5. Manter um tom profissional mas acessível

Sempre baseie suas respostas no conteúdo do documento fornecido."""
    
    def ask(self, question: str) -> str:
        """
        Faz uma pergunta sobre o documento.
        
        Args:
            question: Pergunta do usuário
            
        Returns:
            Resposta do assistente
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("user", "{input}")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({
                "chat_history": self.messages_history,
                "input": question
            })
            
            self.messages_history.append(HumanMessage(content=question))
            self.messages_history.append(AIMessage(content=response.content))
            
            self.chat_history.append({
                "role": "user",
                "content": question
            })
            self.chat_history.append({
                "role": "assistant",
                "content": response.content
            })
            
            return response.content
            
        except Exception as e:
            error_msg = f"Erro ao processar pergunta: {str(e)}"
            print(error_msg)
            return error_msg
    
    def get_history(self) -> List[Dict[str, str]]:
        """Retorna o histórico da conversa."""
        return self.chat_history
    
    def clear_history(self):
        """Limpa o histórico da conversa."""
        self.messages_history = []
        self.chat_history = []
    
    def get_suggested_questions(self) -> List[str]:
        """
        Gera sugestões de perguntas baseadas no documento.
        
        Returns:
            Lista de perguntas sugeridas
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Com base no documento jurídico fornecido, sugira 5 perguntas
            relevantes que um usuário poderia fazer.
            
            Retorne apenas as perguntas, uma por linha, sem numeração."""),
            ("user", f"Documento:\n\n{self.document_text[:5000]}")
        ])
        
        chain = prompt | self.llm
        
        try:
            response = chain.invoke({})
            questions = [q.strip() for q in response.content.split('\n') if q.strip()]
            return questions[:5]
        except:
            return [
                "Qual é o número do processo?",
                "Quem são as partes envolvidas?",
                "Qual é o objeto da ação?",
                "Existem prazos a serem cumpridos?",
                "Qual é a situação atual do processo?"
            ]


class QuickQuestions:
    """Respostas rápidas para perguntas comuns."""
    
    def __init__(self, document_text: str, api_key: str = None):
        self.document_text = document_text
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.llm = ChatGroq(
            model="llama-3.1-8b-instant",
            temperature=0,
            api_key=self.api_key
        )
    
    def _ask_quick(self, question: str) -> str:
        """Faz uma pergunta rápida sem contexto de conversa."""
        prompt = ChatPromptTemplate.from_messages([
            ("system", """Responda de forma direta e objetiva baseado no documento.
            Use no máximo 2-3 frases."""),
            ("user", f"""Documento:
{self.document_text[:10000]}

Pergunta: {question}

Resposta breve:""")
        ])
        
        chain = prompt | self.llm
        response = chain.invoke({})
        return response.content
    
    def get_numero_processo(self) -> str:
        """Extrai o número do processo."""
        return self._ask_quick("Qual é o número do processo?")
    
    def get_partes(self) -> str:
        """Extrai as partes do processo."""
        return self._ask_quick("Quem são autor e réu?")
    
    def get_tipo_acao(self) -> str:
        """Identifica o tipo de ação."""
        return self._ask_quick("Qual é o tipo/classe desta ação?")
    
    def get_valor_causa(self) -> str:
        """Extrai o valor da causa."""
        return self._ask_quick("Qual é o valor da causa?")
    
    def get_prazos(self) -> str:
        """Identifica prazos."""
        return self._ask_quick("Quais são os prazos mencionados?")


if __name__ == "__main__":
    documento_exemplo = """
    TRIBUNAL DE JUSTIÇA DO ESTADO DO RIO GRANDE DO SUL
    COMARCA DE SANTA ROSA
    VARA CÍVEL
    
    Processo nº 1000123-45.2024.8.21.0001
    
    AÇÃO DE COBRANÇA
    
    AUTOR: João da Silva, brasileiro, casado, CPF 123.456.789-00
    RÉU: Empresa ABC Ltda, CNPJ 12.345.678/0001-90
    
    VALOR DA CAUSA: R$ 50.000,00
    
    PRAZO: O réu tem 15 dias para apresentar contestação.
    """
    
    print("=== TESTE DO CHAT ===\n")
    
    try:
        chat = LegalDocumentChat(documento_exemplo)
        resposta = chat.ask("Qual é o número do processo?")
        print(f"Resposta: {resposta}")
        
    except Exception as e:
        print(f"Erro: {e}")
        print("Configure GROQ_API_KEY no arquivo .env")