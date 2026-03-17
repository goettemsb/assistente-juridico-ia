# ⚖️ Assistente Jurídico com IA

Sistema inteligente para análise automatizada de documentos jurídicos usando Inteligência Artificial e Processamento de Linguagem Natural.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![LangChain](https://img.shields.io/badge/LangChain-0.1.0-green.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

## Sobre o Projeto

Este projeto foi desenvolvido como parte do portfólio de **Bruno Daniel Goettems** para demonstrar habilidades em:
- Desenvolvimento de aplicações com IA Generativa
- Implementação de agentes inteligentes com LangChain
- Processamento de documentos e extração de informações
- Criação de interfaces web interativas

O assistente automatiza tarefas que tradicionalmente levam horas de trabalho manual, como:
-  Extração de informações-chave de documentos jurídicos
-  Identificação de partes, prazos e dados processuais
-  Geração automática de resumos executivos
- Sistema de perguntas e respostas sobre documentos

## Screenshots

### Tela Inicial
![Tela Inicial](screenshots/tela-inicial.png)

### Analise de Documento
![Analise de Documento](screenshots/analise-documento.png)

### Dados Extraidos
![Dados Extraidos](screenshots/dados-extraidos.png)

### Protocolos Carregados
![Protocolos Carregados](screenshots/protocolos-carregados.png)

## Funcionalidades

### Processamento de PDFs
- Upload e extração de texto de documentos jurídicos
- Suporte a múltiplos formatos de PDF
- Extração de metadados

###  Análise com IA
- Extração estruturada de informações:
  - Número do processo
  - Partes (autor, réu, advogados)
  - Classe processual e assunto
  - Prazos e datas importantes
  - Valor da causa
- Geração automática de resumos
- Identificação de pontos principais

###  Chat Interativo
- Converse com seus documentos
- Faça perguntas em linguagem natural
- Respostas contextualizadas baseadas no documento
- Histórico de conversa

###  Consultas Rápidas
- Botões de acesso rápido para informações comuns
- Respostas instantâneas
- Interface otimizada para produtividade

## Tecnologias Utilizadas

- **Python 3.10+** - Linguagem principal
- **LangChain** - Framework para aplicações com LLM
- **OpenAI GPT** - Modelo de linguagem
- **Streamlit** - Interface web
- **pdfplumber / PyPDF2** - Processamento de PDF
- **Pydantic** - Validação de dados

## Estrutura do Projeto

```
assistente-juridico-ia/
├── src/
│   ├── __init__.py
│   ├── pdf_processor.py       # Processamento de PDFs
│   ├── ai_extractor.py         # Extração com IA
│   └── document_chat.py        # Sistema de chat
├── data/
│   ├── input/                  # PDFs de entrada
│   └── output/                 # Resultados processados
├── tests/
│   └── test_extraction.py      # Testes unitários
├── app.py                      # Interface Streamlit
├── requirements.txt            # Dependências
├── .env.example                # Exemplo de variáveis de ambiente
└── README.md                   # Este arquivo
```

## Instalação e Uso

### 1. Clone o Repositório

```bash
git clone https://github.com/goettemsb/assistente-juridico-ia.git
cd assistente-juridico-ia
```

### 2. Crie um Ambiente Virtual

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as Dependências

```bash
pip install -r requirements.txt
```

### 4. Configure as Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e adicione sua chave de API:

```bash
cp .env.example .env
```

Edite o arquivo `.env`:
```
OPENAI_API_KEY=sua_chave_aqui
```

Para obter uma chave de API da OpenAI:
1. Acesse [platform.openai.com](https://platform.openai.com)
2. Crie uma conta ou faça login
3. Vá em "API Keys" e crie uma nova chave

OBS.: Para Este projeto foi usado o Groq AI. (https://groq.com/)

### 5. Execute a Aplicação

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente em seu navegador em `http://localhost:8501`

## Como Usar

### Passso 0: Execute o arquivo *** Assistente_Juridico_IA *** que se encontra dentro da pasta raíz do projeto, ele iniciará o projeto diretamente no navagedor.

### Passo 1: Upload do Documento
1. Clique em "Browse files" ou arraste um PDF
2. Clique em "Processar Documento"

### Passo 2: Análise Automática
1. Vá para a aba "Análise Automática"
2. Clique em "Extrair Informações com IA"
3. Visualize os dados estruturados extraídos

### Passo 3: Chat Interativo
1. Acesse a aba "Chat Interativo"
2. Digite suas perguntas no campo de texto
3. Veja sugestões de perguntas clicando em "Ver sugestões"

### Passo 4: Perguntas Rápidas
1. Use os botões de atalho para informações específicas
2. Respostas instantâneas sem necessidade de digitar

## Demonstração

### Exemplo de Uso

```python
from src.pdf_processor import PDFProcessor
from src.ai_extractor import LegalAIExtractor

# Processar PDF
processor = PDFProcessor("documento.pdf")
texto = processor.extract_text()

# Extrair informações com IA
extractor = LegalAIExtractor()
dados = extractor.extract_information(texto)

print(f"Número do Processo: {dados.dados_processo.numero_processo}")
print(f"Autor: {dados.partes.autor}")
print(f"Resumo: {dados.resumo}")
```

### Exemplos de Perguntas

- "Qual é o número do processo?"
- "Quem são as partes envolvidas?"
- "Existe algum prazo a ser cumprido?"
- "Qual é o valor da causa?"
- "Me explique o objeto da ação"
- "Quais são os principais argumentos do autor?"

## 🧪 Testes

```bash
# Executar testes
python -m pytest tests/

# Com cobertura
python -m pytest tests/ --cov=src
```

## 📊 Casos de Uso

Este sistema é ideal para:

- **Advogados**: Análise rápida de petições e sentenças
- **Escritórios**: Triagem automática de documentos
- **Estudantes**: Estudo de casos e peças processuais
- **Departamentos Jurídicos**: Gestão de portfólio processual

## 🔮 Roadmap

- [ ] Suporte a múltiplos documentos simultâneos
- [ ] Comparação entre documentos
- [ ] Geração automática de minutas
- [ ] Integração com sistemas de gestão processual
- [ ] Suporte a mais formatos (DOCX, RTF)
- [ ] API REST para integração
- [ ] Deploy em cloud (AWS/GCP)
- [ ] Sistema de RAG para consulta em base de conhecimento

## 🤝 Contribuindo

Contribuições são bem-vindas! Para contribuir:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

## 👤 Autor

**Bruno Daniel Goettems**

- 🌐 [LinkedIn](https://linkedin.com/in/goettemsb)
- 💻 [GitHub](https://github.com/goettemsb)
- 📧 Email: goettemsb@gmail.com
- 📱 WhatsApp: +55 55 99715-5283

## Agradecimentos

- Comunidade LangChain
- Streamlit pelo framework incrível
- Todos que contribuíram com feedback

##  Referências

- [LangChain Documentation](https://python.langchain.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Streamlit Documentation](https://docs.streamlit.io/)

---

⭐ **Se este projeto foi útil, considere dar uma estrela no GitHub!**

Desenvolvido por Bruno Daniel Goettems
