# AWS Glue com DynamoDB

Este projeto utiliza o **AWS Glue** para ler dados de uma tabela do catálogo e inserir os registros no **Amazon DynamoDB**. O ambiente é preparado para rodar **localmente**, utilizando a biblioteca `awsglue` com suporte via `extract_awsglue.sh`.

---

## 🛠️ Pré-requisitos

- **Python** 3.9+
- **Java** 8 ou 11
- **pip**
- **virtualenv** (caso não tenha, instale com: `python -m pip install virtualenv`)

---

## 🚀 Inicialização do Projeto

### 1. Configurar o `JAVA_HOME` (Java 8 ou 11)

**No terminal:**

```bash
export JAVA_HOME=/caminho/para/sua/versao/java
export PATH=$JAVA_HOME/bin:$PATH
```

**Na IDE (ex: IntelliJ, VSCode):**
Configure o JAVA_HOME nas variáveis de ambiente do projeto, apontando para o diretório do Java 8 ou 11.

### 2. Criar ambiente virtual com venv

```bash
python -m venv .venv
source .venv/bin/activate  # Para Linux/macOS
.venv\Scripts\activate     # Para Windows
```

### 3. Instalar dependências
Há dois arquivos requirements.txt, um na pasta src/ e outro na pasta tests/. Ambos devem ser instalados:

```bash
pip install -r src/requirements.txt
pip install -r tests/requirements.txt
```

### 4. Rodar o script de inicialização do Glue local
Este script prepara o ambiente para executar jobs Glue localmente:

```bash
./extract_awsglue.sh
```

* Depois de rodar esse script:
* Você terá a lib awsglue extraída em ./awsglue.
* Isso permite que você importe os módulos do AWS Glue localmente (como from awsglue.context import GlueContext) mesmo fora do ambiente da AWS.
* O container usado para extração será removido, mantendo o ambiente limpo.

✅ Rodar Testes Unitários
Com o ambiente virtual ativado, execute:

```bash
pytest tests/
```

📂 Estrutura do Projeto
```bash
.
├── runrun.sh                 # Script para preparar o Glue local
├── src/
│   ├── glue_job.py           # Código principal do Glue Job
│   └── requirements.txt      # Dependências do job
├── tests/
│   ├── test_glue_job.py      # Testes unitários
│   └── requirements.txt      # Dependências para testes
└── README.md
```