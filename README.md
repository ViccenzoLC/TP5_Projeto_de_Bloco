PEDI PARA A IA FAZER UM README CASO ALGO FIQUE EM ABERTO E PARA MIM NAO ME PERDER DEPOIS QUANDO EU FOR VER O CODIGO( FEITA PELA IA DO VScode)!
# TP5 - Projeto de Bloco

Projeto desenvolvido para a disciplina de Projeto de Bloco, utilizando Python para integração com banco de dados PostgreSQL, processamento de dados e análise de transações financeiras.

## Sobre o projeto

O projeto realiza a integração entre uma aplicação Python e um banco de dados PostgreSQL utilizando SQLAlchemy.

Além da conexão e manipulação do banco de dados, o projeto realiza o processamento de dados financeiros provenientes de arquivos CSV e identifica possíveis transações fraudulentas de acordo com critérios definidos para o projeto.

Os dados processados podem ser armazenados no banco de dados e também exportados para arquivos JSON para geração de relatórios.

## Tecnologias utilizadas

* Python
* PostgreSQL
* SQLAlchemy
* Pandas
* psycopg2
* python-dotenv
* Git e GitHub
* DataGrip

## Estrutura do projeto

```text
TP5 DE PROJETO DE BLOCO/
│
├── Arquivo_CSV_Professor/
│   └── credit_card_transactions.csv
│
├── Banco/
│   └── conexao_banco.py
│
├── venv/
│
├── .env
├── .gitignore
└── README.md
```

## Banco de dados

O projeto utiliza PostgreSQL como banco de dados.

Entre as tabelas utilizadas no projeto estão:

* `bancos_parceiros`
* `clientes`
* `perfis_seguranca`
* `cartoes_credito`
* `produtos_financeiros`

Também é utilizada uma tabela de auditoria para armazenar os registros identificados durante o processamento das transações.

## Conexão com o banco de dados

As informações de conexão não ficam diretamente no código-fonte.

O projeto utiliza um arquivo `.env` para armazenar as variáveis de ambiente:

```env
DB_DRIVE=postgresql+psycopg2
DB_USERNAME=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```

O arquivo `.env` está incluído no `.gitignore` para evitar que informações sensíveis, como a senha do banco de dados, sejam enviadas para o GitHub.

A conexão é criada utilizando SQLAlchemy:

```python
engine_url = f"{driver}://{usuario}:{senha}@{host}:{porta}/{banco}"

engine = create_engine(engine_url)
```

## Processamento dos dados

Os dados das transações são carregados utilizando Pandas.

O projeto utiliza processamento em partes (`chunksize`) para permitir o tratamento de arquivos CSV de grande volume sem precisar carregar todo o arquivo na memória de uma única vez.

Exemplo:

```python
pd.read_csv(
    arquivo,
    chunksize=100000
)
```

Os dados podem ser tratados, filtrados e posteriormente enviados para o banco de dados utilizando `to_sql()`.

## Identificação de possíveis fraudes

Para este projeto, foi definido um critério para identificar possíveis fraudes relacionadas ao número do cartão.

São considerados possíveis registros fraudulentos aqueles cujo número do cartão possui mais de 16 dígitos.

O relatório gerado pode ser armazenado em uma tabela de auditoria no PostgreSQL e também exportado para JSON.

## Exportação para JSON

Os registros identificados podem ser exportados utilizando o formato `records`:

```python
df.to_json(
    "fraudes.json",
    orient="records",
    indent=4
)
```

Esse formato organiza os dados como uma lista de objetos JSON, facilitando a leitura e utilização posterior dos resultados.

## Inserção de dados no banco

O projeto utiliza o método `to_sql()` do Pandas para inserir DataFrames no PostgreSQL.

Exemplo:

```python
df.to_sql(
    "bancos_parceiros",
    engine,
    if_exists="append",
    index=False
)
```

O parâmetro `if_exists` pode ser utilizado para definir o comportamento quando a tabela já existe:

* `fail` - gera um erro caso a tabela exista.
* `replace` - remove a tabela existente e cria uma nova.
* `append` - adiciona os novos registros à tabela existente.

## Configuração do ambiente

### 1. Clonar o repositório

```bash
git clone https://github.com/ViccenzoLC/TP5_Projeto_de_Bloco.git
```

### 2. Entrar na pasta

```bash
cd TP5_Projeto_de_Bloco
```

### 3. Criar o ambiente virtual

```bash
python -m venv venv
```

### 4. Ativar o ambiente virtual

No Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

No Git Bash:

```bash
source venv/Scripts/activate
```

### 5. Instalar as dependências

```bash
pip install pandas sqlalchemy psycopg2-binary python-dotenv
```

### 6. Configurar as variáveis de ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
DB_DRIVE=postgresql+psycopg2
DB_USERNAME=postgres
DB_PASSWORD=sua_senha
DB_HOST=localhost
DB_PORT=5432
DB_NAME=postgres
```

Substitua os valores pelos dados do seu banco PostgreSQL.

### 7. Executar o projeto

Com o ambiente virtual ativado:

```bash
python Banco/conexao_banco.py
```

Se a conexão estiver funcionando, será exibida uma mensagem indicando que a conexão foi realizada com sucesso.

## Segurança

Informações sensíveis não devem ser armazenadas diretamente no código.

O projeto utiliza:

```text
.env
```

para armazenar credenciais locais.

O `.env` está incluído no `.gitignore`:

```gitignore
.env
venv/
__pycache__/
```

Portanto, o arquivo `.env` não deve ser enviado para o GitHub.

## Objetivos do projeto

* Praticar integração entre Python e PostgreSQL.
* Utilizar SQLAlchemy para conexão com banco de dados.
* Utilizar Pandas para processamento de dados.
* Trabalhar com arquivos CSV de grande volume.
* Realizar tratamento e análise de dados.
* Identificar possíveis transações fraudulentas.
* Armazenar resultados no banco de dados.
* Exportar resultados para JSON.
* Utilizar variáveis de ambiente para proteger informações de conexão.

## Autor

**Viccenzo Lunelli Comoretto**

Estudante de Engenharia de Software.

GitHub: https://github.com/ViccenzoLC
