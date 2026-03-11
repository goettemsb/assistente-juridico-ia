# ⚡ Guia Rápido de Uso

## 🎯 Para Começar Agora (5 minutos)

### 1. Configure a API Key

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o arquivo .env e adicione sua chave
OPENAI_API_KEY=sk-sua-chave-aqui
```

**Onde conseguir a chave?**
- Acesse: https://platform.openai.com
- Vá em "API Keys"
- Clique em "Create new secret key"

### 2. Instale as Dependências

```bash
# Crie ambiente virtual
python -m venv venv

# Ative (Windows)
venv\Scripts\activate

# Ative (Linux/Mac)
source venv/bin/activate

# Instale
pip install -r requirements.txt
```

### 3. Execute a Aplicação

```bash
streamlit run app.py
```

Pronto! A aplicação abrirá em `http://localhost:8501`

## 📖 Como Usar a Interface

### Upload de Documento
1. Clique em "Browse files"
2. Selecione um PDF jurídico
3. Clique em "Processar Documento"

### Análise Automática
1. Vá para aba "Análise Automática"
2. Clique em "Extrair Informações com IA"
3. Veja as informações estruturadas extraídas

### Chat Interativo
1. Acesse a aba "Chat Interativo"
2. Digite uma pergunta no campo de texto
3. Pressione Enter ou clique em "Enviar"

**Exemplos de perguntas:**
- "Qual é o número do processo?"
- "Quem são as partes?"
- "Me explique o objeto da ação"
- "Quais são os prazos?"
- "Qual é o valor da causa?"

### Perguntas Rápidas
Use os botões para obter respostas instantâneas sobre:
- Número do processo
- Partes
- Tipo de ação
- Valor da causa
- Prazos

## 🔧 Usando como Biblioteca Python

### Exemplo 1: Processar PDF

```python
from src.pdf_processor import PDFProcessor

# Processar PDF
processor = PDFProcessor("documento.pdf")
texto = processor.extract_text()
print(texto)
```

### Exemplo 2: Extrair Informações

```python
from src.ai_extractor import LegalAIExtractor

extractor = LegalAIExtractor()
dados = extractor.extract_information(texto)

print(f"Número: {dados.dados_processo.numero_processo}")
print(f"Autor: {dados.partes.autor}")
```

### Exemplo 3: Chat

```python
from src.document_chat import LegalDocumentChat

chat = LegalDocumentChat(texto)
resposta = chat.ask("Qual é o objeto da ação?")
print(resposta)
```

## 🎨 Exemplos de Documentos Suportados

- ✅ Petições iniciais
- ✅ Sentenças
- ✅ Acórdãos  
- ✅ Contratos
- ✅ Pareceres jurídicos
- ✅ Recursos
- ✅ Atas de audiência

## 💡 Dicas de Uso

### Para Melhores Resultados:

1. **PDFs com texto selecionável** funcionam melhor
2. **Documentos organizados** produzem melhores extrações
3. **Faça perguntas específicas** no chat
4. **Use os botões rápidos** para informações comuns

### Economize Tokens ($$):

- Use "Perguntas Rápidas" em vez do chat quando possível
- Extraia informações uma vez e salve
- Use resumos em vez de texto completo

## 🐛 Solução Rápida de Problemas

### Erro: "API key not found"
**Solução:** Configure o arquivo `.env` com sua chave

### Erro ao processar PDF
**Solução:** Certifique-se que o PDF tem texto selecionável (não é imagem)

### Interface não abre
**Solução:** Verifique se a porta 8501 está livre
```bash
streamlit run app.py --server.port 8502
```

### Resposta lenta
**Solução:** Normal para documentos grandes. Aguarde alguns segundos.

## 📊 Custos Estimados (OpenAI)

Com GPT-3.5-turbo (modelo padrão):
- Upload e extração: ~$0.01 por documento
- Pergunta no chat: ~$0.001 por pergunta
- Resumo: ~$0.005 por resumo

**Total estimado:** ~$0.05 por documento completo

Para economizar, use GPT-3.5-turbo em vez de GPT-4.

## 🚀 Próximos Passos

Depois de testar o básico:

1. **Personalize os prompts** em `src/ai_extractor.py`
2. **Modifique a interface** em `app.py`
3. **Adicione novos campos** aos modelos de dados
4. **Integre com seus sistemas** via API

## 📚 Recursos

- [README completo](README.md)
- [Guia de instalação](INSTALACAO.md)
- [Código de exemplo](demo.py)

## 🆘 Precisa de Ajuda?

- 📧 Email: goettemsb@gmail.com
- 💬 GitHub Issues: [Abrir issue](https://github.com/goettemsb/assistente-juridico-ia/issues)
- 💼 LinkedIn: [/in/goettemsb](https://linkedin.com/in/goettemsb)

---

**Desenvolvido por Bruno Daniel Goettems** | 2025
