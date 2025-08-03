# ARQV30 Enhanced v2.0 - Sistema de Análise Ultra-Detalhada

Sistema avançado de análise de mercado com IA, pesquisa web profunda e geração de relatórios detalhados.

## 🚀 Características Principais

- **Sistema Autônomo**: Funciona sem dependências externas obrigatórias
- **Análise com IA**: Suporte para múltiplas APIs (Gemini, OpenAI, Groq, HuggingFace)
- **Pesquisa Web Profunda**: Múltiplos provedores de busca + web scraping
- **Armazenamento Local**: Sistema robusto de arquivos locais
- **Relatórios PDF**: Geração automática de relatórios profissionais
- **Interface Moderna**: UI neumórfica responsiva

## 📋 Requisitos Mínimos

- Python 3.8+
- 2GB RAM
- 1GB espaço em disco

## ⚡ Instalação Rápida

### Windows
```bash
# 1. Clone o repositório
git clone <repository-url>
cd arqv30-enhanced

# 2. Execute o instalador
install.bat

# 3. Inicie o sistema
run.bat
```

### Linux/Mac
```bash
# 1. Clone o repositório
git clone <repository-url>
cd arqv30-enhanced

# 2. Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# 3. Instale dependências
pip install -r requirements.txt

# 4. Inicie o sistema
python src/run.py
```

## 🔧 Configuração (Opcional)

O sistema funciona sem configuração, mas você pode adicionar APIs para funcionalidades avançadas:

1. Copie `.env.example` para `.env`
2. Configure as APIs desejadas:

```env
# APIs de IA (opcional - melhora qualidade)
GEMINI_API_KEY=sua-chave-gemini
OPENAI_API_KEY=sua-chave-openai
GROQ_API_KEY=sua-chave-groq

# APIs de Busca (opcional - melhora pesquisa)
GOOGLE_SEARCH_KEY=sua-chave-google
GOOGLE_CSE_ID=seu-cse-id
SERPER_API_KEY=sua-chave-serper
```

## 🎯 Como Usar

1. **Acesse**: http://localhost:5000
2. **Preencha** os dados do projeto:
   - Segmento de mercado (obrigatório)
   - Produto/serviço
   - Público-alvo
   - Preço e objetivos
3. **Anexe** documentos (opcional):
   - PDFs, DOCs, planilhas
   - Dados de pesquisa
4. **Execute** a análise
5. **Baixe** o relatório em PDF

## 📊 Funcionalidades

### Análise Básica (sem APIs)
- ✅ Estruturação de dados
- ✅ Análise básica de mercado
- ✅ Relatórios em PDF
- ✅ Armazenamento local

### Análise Avançada (com APIs)
- 🚀 Avatar ultra-detalhado
- 🧠 Drivers mentais customizados
- 🎯 Sistema anti-objeção
- 🔮 Predições de futuro
- 📈 Análise competitiva profunda
- 🌐 Pesquisa web massiva

## 🛠️ Dependências Opcionais

Para funcionalidades avançadas, instale:

```bash
# IA Avançada
pip install google-generativeai openai groq

# Extração de Conteúdo
pip install trafilatura newspaper3k readability-lxml

# Análise de Documentos
pip install pandas openpyxl python-docx PyPDF2

# Extração Dinâmica
pip install playwright selenium webdriver-manager
```

## 📁 Estrutura do Projeto

```
arqv30-enhanced/
├── src/
│   ├── routes/          # Endpoints da API
│   ├── services/        # Serviços de análise
│   ├── static/          # Assets frontend
│   ├── templates/       # Templates HTML
│   └── run.py          # Aplicação principal
├── logs/               # Logs do sistema
├── analyses_data/      # Análises salvas
├── relatorios_intermediarios/  # Dados temporários
└── requirements.txt    # Dependências
```

## 🔍 Testes do Sistema

O sistema inclui ferramentas de teste integradas:

- **Teste de Extração**: Verifica extração de conteúdo
- **Teste de Busca**: Valida provedores de busca
- **Health Check**: Status geral do sistema
- **Estatísticas**: Performance dos componentes

## 🚨 Solução de Problemas

### Erro de Dependências
```bash
# Instale dependências básicas
pip install Flask Flask-CORS python-dotenv requests beautifulsoup4
```

### Erro de Encoding
```bash
# Configure locale UTF-8 (Linux)
export LANG=pt_BR.UTF-8
export LC_ALL=pt_BR.UTF-8
```

### Performance Lenta
- Configure pelo menos uma API de IA
- Configure APIs de busca
- Verifique conexão com internet

## 📈 Monitoramento

- **Logs**: `logs/arqv30.log`
- **Dados**: `analyses_data/`
- **Status**: Interface web em tempo real

## 🔒 Segurança

- Dados armazenados localmente
- Sem dependências de serviços externos obrigatórias
- Logs detalhados de todas as operações
- Validação rigorosa de entrada

## 🆘 Suporte

1. Verifique os logs em `logs/`
2. Execute health check na interface
3. Consulte a documentação dos serviços
4. Reporte problemas com logs detalhados

## 📝 Changelog v2.0

- ✅ Removida dependência obrigatória do Supabase
- ✅ Sistema totalmente autônomo
- ✅ Melhor tratamento de erros
- ✅ Imports condicionais para todas as dependências
- ✅ Fallbacks robustos para todos os componentes
- ✅ Interface de testes integrada

## 🎉 Pronto para Usar!

O sistema está configurado para funcionar imediatamente após a instalação, sem necessidade de configuração adicional.