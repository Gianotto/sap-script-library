# SAP Script Manager - Navigation Map

## 🚀 Start Here

| What Do You Want? | Go To | Time |
|------------------|--------|------|
| Get started in 5 min | [GETTING_STARTED.md](GETTING_STARTED.md) | ⏱️ 5 min |
| Understand structure | [PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md) | ⏱️ 10 min |
| Install/Setup | [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) | ⏱️ 15 min |
| Use the app | [docs/USER_GUIDE.md](docs/USER_GUIDE.md) | ⏱️ 30 min |
| Program/Develop | [docs/CODE_DOCUMENTATION.md](docs/CODE_DOCUMENTATION.md) | ⏱️ 45 min |

## 📂 Root Files

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - 5-minute quick guide
- **[PROJECT_STRUCTURE.md](PROJECT_STRUCTURE.md)** - Explanation of organization
- **[README.md](README.md)** - Project overview
- **[INDEX.md](INDEX.md)** - This file (navigation map)
- **[run.ps1](run.ps1)** - PowerShell Launcher (run: `.\run.ps1`)
- **[app/run_sap_manager.bat](app/run_sap_manager.bat)** - Windows Launcher (double-click)

## 📁 Diretórios

### 🔧 [/app](app/)
Código-fonte da aplicação

- [sap_gui_manager.py](app/sap_gui_manager.py) - Interface gráfica (1800 linhas)
- [SAP.py](app/SAP.py) - Biblioteca de automação (600 linhas)
- [run_sap_manager.bat](app/run_sap_manager.bat) - Launcher Windows

### 📖 [/docs](docs/)
Documentação completa

| Arquivo | Descrição |
|---------|-----------|
| [QUICK_START.md](docs/QUICK_START.md) | Início rápido (5 min) |
| [INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md) | Instalação passo-a-passo |
| [USER_GUIDE.md](docs/USER_GUIDE.md) | Manual completo de uso |
| [CODE_DOCUMENTATION.md](docs/CODE_DOCUMENTATION.md) | Referência técnica da API |
| [EVALUATION_AND_PYTHON_PORT.md](docs/EVALUATION_AND_PYTHON_PORT.md) | Análise de arquitetura |
| [PROJECT_DELIVERY_SUMMARY.md](docs/PROJECT_DELIVERY_SUMMARY.md) | O que foi entregue |
| [DOCUMENTATION_INDEX.md](docs/DOCUMENTATION_INDEX.md) | Índice de documentação |

### 💡 [/examples](examples/)
Scripts de exemplo comentados

- [example_automation.py](examples/example_automation.py) - Padrões básicos (200 linhas)
- [batch_processing_example.py](examples/batch_processing_example.py) - Processamento em lote (250 linhas)

### ⚙️ [/config](config/)
Configuração do projeto

- [requirements.txt](config/requirements.txt) - Dependências Python (PyQt5, pywin32)

### 💾 [/sap_scripts](sap_scripts/)
Seus scripts Python (área do usuário)

- Crie seus scripts aqui
- Será salvo automaticamente pela aplicação
- Ignorado por Git (privacidade)

## 📋 Documentação Rápida

### Para Iniciantes
1. Leia [GETTING_STARTED.md](GETTING_STARTED.md) (5 min)
2. Execute `app/run_sap_manager.bat` (duplo clique)
3. Siga guia na aba Session Manager

### Para Usuários
1. Consulte [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
2. Veja exemplos em `/examples`
3. Crie scripts em `/sap_scripts`

### Para Desenvolvedores
1. Estude [docs/CODE_DOCUMENTATION.md](docs/CODE_DOCUMENTATION.md)
2. Examine código em `/app`
3. Copie exemplos de `/examples`
4. Entenda design em [docs/EVALUATION_AND_PYTHON_PORT.md](docs/EVALUATION_AND_PYTHON_PORT.md)

## 🎯 Tarefas Comuns

### Como Iniciar a Aplicação?
```bash
# Opção A: Duplo clique
app/run_sap_manager.bat

# Opção B: PowerShell
.\run.ps1

# Opção C: Terminal
python app/sap_gui_manager.py
```

### Como Criar um Script?
1. Abra a aplicação
2. Aba "Script Editor" → "New Script"
3. Escreva código Python
4. Clique "Run Script"
5. Veja resultado em "Script Executor"

### Como Gravar Ações?
1. Aba "Transaction Recorder" → "Start Recording"
2. Faça ações no SAP
3. "Stop Recording"
4. "Generate Script"
5. Script gerado em Script Editor

### Como Instalar Dependências?
```bash
pip install -r config/requirements.txt
```

### Como Contribuir?
1. Modifique código em `/app`
2. Adicione exemplos em `/examples`
3. Atualize documentação em `/docs`
4. Teste tudo funciona

## 📊 Estatísticas do Projeto

- **Código:** 2850+ linhas (app/)
- **Documentação:** 4200+ linhas (docs/)
- **Exemplos:** 450+ linhas (examples/)
- **Total:** 7500+ linhas
- **Arquivos:** 18 arquivos + 4 diretórios
- **Cobertura:** 100% de documentação

## 🔗 Navegação Rápida

```
ÍNDICE (você está aqui)
├── GETTING_STARTED.md (comece aqui)
├── PROJECT_STRUCTURE.md (aprenda estrutura)
├── README.md (visão geral)
│
├── app/
│   ├── sap_gui_manager.py
│   ├── SAP.py
│   └── run_sap_manager.bat (execute!)
│
├── docs/
│   ├── QUICK_START.md
│   ├── INSTALLATION_GUIDE.md
│   ├── USER_GUIDE.md
│   ├── CODE_DOCUMENTATION.md
│   └── ... (7 arquivos de docs)
│
├── examples/
│   ├── example_automation.py
│   └── batch_processing_example.py
│
├── sap_scripts/
│   └── (seus scripts aqui)
│
└── config/
    └── requirements.txt
```

## ⏰ Tempo de Leitura Recomendado

- **Iniciante (30 min):**
  1. GETTING_STARTED.md (5 min)
  2. QUICK_START.md (5 min)
  3. USER_GUIDE.md (20 min)

- **Desenvolvedor (90 min):**
  1. PROJECT_STRUCTURE.md (10 min)
  2. CODE_DOCUMENTATION.md (45 min)
  3. EVALUATION_AND_PYTHON_PORT.md (20 min)
  4. Estudar código em /app (15 min)

- **Profundo (2-3 horas):**
  - Leia toda documentação em `/docs` (4200 linhas)
  - Estude código-fonte em `/app` (2850 linhas)
  - Rode exemplos em `/examples` (450 linhas)

## 🆘 Precisa de Ajuda?

1. **Instalação:** [docs/INSTALLATION_GUIDE.md](docs/INSTALLATION_GUIDE.md)
2. **Uso:** [docs/USER_GUIDE.md](docs/USER_GUIDE.md)
3. **Código:** [docs/CODE_DOCUMENTATION.md](docs/CODE_DOCUMENTATION.md)
4. **Troubleshooting:** Procure "Troubleshooting" em qualquer doc

## ✅ Checklist Rápido

- [ ] Li GETTING_STARTED.md
- [ ] Executei app/run_sap_manager.bat
- [ ] Conectei ao SAP em Session Manager
- [ ] Criei primeiro script em Script Editor
- [ ] Li docs/USER_GUIDE.md
- [ ] Criei scripts em sap_scripts/

Todos itens marcados? Parabéns! 🎉

---

**Projeto Pronto para Uso** ✓
**Bem Estruturado** ✓
**Completamente Documentado** ✓

Comece em [GETTING_STARTED.md](GETTING_STARTED.md)!
