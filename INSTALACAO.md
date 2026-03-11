# 🚀 Guia de Instalação Passo a Passo

Este guia irá te ajudar a configurar e executar o projeto **Assistente Jurídico com IA** do zero.

## 📋 Pré-requisitos

Antes de começar, você precisa ter instalado:

- **Python 3.10 ou superior** - [Download aqui](https://www.python.org/downloads/)
- **Git** - [Download aqui](https://git-scm.com/downloads)
- **Editor de código** (recomendado: VS Code) - [Download aqui](https://code.visualstudio.com/)

## 🔧 Instalação

### Passo 1: Verificar Python

Abra o terminal/prompt de comando e verifique a versão do Python:

```bash
python --version
# ou
python3 --version
```

Deve mostrar algo como `Python 3.10.x` ou superior.

### Passo 2: Clonar o Repositório

Se você ainda não tem o projeto:

```bash
git clone https://github.com/goettemsb/assistente-juridico-ia.git
cd assistente-juridico-ia
```

Se você já tem o projeto localmente, apenas navegue até a pasta:

```bash
cd assistente-juridico-ia
```

### Passo 3: Criar Ambiente Virtual

**No Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**No Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Você saberá que funcionou quando ver `(venv)` no início da linha do terminal.

### Passo 4: Instalar Dependências

Com o ambiente virtual ativado:

```bash
pip install -r requirements.txt
```

Este processo pode levar alguns minutos. Aguarde até concluir.

### Passo 5: Configurar API Key

#### Opção A: Obter API Key da OpenAI (Recomendado)

1. Acesse [platform.openai.com](https://platform.openai.com)
2. Crie uma conta ou faça login
3. Vá em "API Keys" no menu lateral
4. Clique em "Create new secret key"
5. Copie a chave (começa com `sk-...`)

**IMPORTANTE:** Guarde esta chave em local seguro. Você não poderá vê-la novamente!

#### Opção B: Usar Claude API (Alternativa)

Se preferir usar Claude da Anthropic:

1. Acesse [console.anthropic.com](https://console.anthropic.com)
2. Crie uma conta
3. Vá em "API Keys"
4. Crie uma nova chave

### Passo 6: Configurar Arquivo .env

1. Copie o arquivo de exemplo:

```bash
# Windows
copy .env.example .env

# Linux/Mac
cp .env.example .env
```

2. Abra o arquivo `.env` com um editor de texto

3. Adicione sua API key:

```
OPENAI_API_KEY=sk-sua-chave-aqui
```

**⚠️ NUNCA compartilhe este arquivo ou commite no Git!**

### Passo 7: Testar a Instalação

Execute o teste básico:

```bash
python src/ai_extractor.py
```

Se tudo estiver correto, você verá uma mensagem de teste.

### Passo 8: Executar a Aplicação

Agora você pode executar a aplicação:

```bash
streamlit run app.py
```

A aplicação abrirá automaticamente no navegador em `http://localhost:8501`

## ✅ Verificação

Se você conseguiu:
- ✅ Ativar o ambiente virtual
- ✅ Instalar as dependências sem erros
- ✅ Configurar a API key
- ✅ Executar a aplicação

**Parabéns! 🎉 Você está pronto para usar o Assistente Jurídico!**

## 🐛 Problemas Comuns

### Erro: "python não é reconhecido"

**Solução:** Python não está no PATH. 
- Windows: Reinstale o Python marcando "Add Python to PATH"
- Mac: Use `python3` em vez de `python`

### Erro: "No module named 'langchain'"

**Solução:** Ambiente virtual não está ativado ou dependências não foram instaladas.

```bash
# Ativar ambiente
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

# Reinstalar dependências
pip install -r requirements.txt
```

### Erro: "API key não fornecida"

**Solução:** Arquivo `.env` não foi configurado corretamente.

1. Verifique se o arquivo `.env` existe
2. Abra e verifique se contém `OPENAI_API_KEY=sk-...`
3. Certifique-se de não ter espaços extras

### Erro ao processar PDF

**Solução:** Algumas dependências podem precisar de bibliotecas extras.

**No Ubuntu/Debian:**
```bash
sudo apt-get install python3-dev
```

**No Mac:**
```bash
brew install python3
```

### Porta 8501 já em uso

**Solução:** Outra aplicação Streamlit está rodando.

```bash
# Especifique outra porta
streamlit run app.py --server.port 8502
```

## 🔄 Próximos Passos

Agora que você instalou o projeto:

1. **Teste com um PDF real:**
   - Coloque um PDF jurídico em `data/input/`
   - Faça upload na interface
   - Experimente as funcionalidades

2. **Explore o código:**
   - Leia os arquivos em `src/`
   - Entenda como funciona cada módulo
   - Faça modificações e experimente

3. **Personalize:**
   - Ajuste os prompts em `src/ai_extractor.py`
   - Modifique a interface em `app.py`
   - Adicione novas funcionalidades

4. **Suba para o GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

## 📚 Recursos Adicionais

- [Documentação LangChain](https://python.langchain.com/)
- [Documentação Streamlit](https://docs.streamlit.io/)
- [OpenAI API Docs](https://platform.openai.com/docs)

## 💡 Dicas

- Use `Ctrl+C` no terminal para parar a aplicação
- Sempre ative o ambiente virtual antes de trabalhar
- Mantenha suas dependências atualizadas: `pip install --upgrade -r requirements.txt`
- Leia os logs no terminal para debugar problemas

## 🆘 Precisa de Ajuda?

Se encontrar problemas:

1. Verifique os logs no terminal
2. Leia a documentação das bibliotecas
3. Abra uma issue no GitHub
4. Entre em contato: goettemsb@gmail.com

---

**Boa sorte com o projeto! 🚀**
