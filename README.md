# Integração de Linguagem Natural com SQL

Este código demonstra como usar o `LangChain` e o `Groq` para criar um agente que converte perguntas em consultas SQL, permitindo uma interação intuitiva com um banco de dados.

## Estrutura do Código

### 1. Importações

O código começa importando as bibliotecas necessárias:

```python
import time
from sqlalchemy import create_engine
import os
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq
````
SQLAlchemy: 
Usado para interagir com bancos de dados SQL.

LangChain: 
Permite a criação de agentes que convertem linguagem natural em consultas SQL.

Documentação LangChain: `https://python.langchain.com/docs/introduction/`

Groq: 
Facilita a modelagem de linguagem com IA.

Documentação Groq: `https://console.groq.com/docs/quickstart`


###  2. Configuração do Ambiente

O código configura a chave da API do Groq:

```python
os.environ["GROQ_API_KEY"] = 'Sua API Key aqui'
````
###  3. Modelo de Linguagem

O modelo de linguagem ultilizado foi Llama 3 instalado localmente através do Ollama, logo abaixo irei deixar as suas documentações:

Documentação Ollama: ``https://github.com/ollama/ollama/tree/main/docs``
Documentação Llama3: ``https://www.llama.com/docs/model-cards-and-prompt-formats/llama-guard-3``

O modelo de linguagem é instanciado com um parâmetro de temperatura:


````python
llm2 = ChatGroq(model="llama3-70b-8192", temperature=1)
````

###  4. Conexão com o Banco de Dados

Uma string de conexão é montada para acessar um banco de dados MySQL:
````python
db_user = ""
db_password = ""
db_host = ""
db_name = ""
uri_empresas = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(uri_empresas)
db = SQLDatabase(engine)
````
###  5. Criação do Agente Executor
O agente SQL é criado para processar perguntas e gerar consultas:

````python
agent_executor = create_sql_agent(llm2, db=db)
````
###  6. Exemplos de Consultas
Um conjunto de perguntas e suas consultas SQL são definidos:

````python
examples = [
    {
        "INPUT": "Quantas empresas no DF têm atividades relacionadas ao setor de saúde?",
        "SQLQUERY": "SELECT COUNT(*) AS 'Quantidade' FROM bd_empresa.estabelecimentos_cnae cn ...",
        "response": "Existem 7261 empresas no DF relacionadas ao setor de saúde."
    },
    {
        "INPUT": "De quem é esse CNPJ: '29445181'",
        "SQLQUERY": "SELECT * FROM empresa WHERE cnpj_base = '29445181'",
        "response": "O CNPJ é do seguinte dono: VANTUIR SILVA DE JESUS"
    },
    {
        "INPUT": "Quais são os logradouros com maior número de empresas no DF?",
        "SQLQUERY": "SELECT LOGRADOURO, COUNT(*) AS NUMERO_EMPRESAS FROM bd_empresa.estabelecimentos WHERE UF = 'DF' GROUP BY LOGRADOURO ORDER BY NUMERO_EMPRESAS DESC",
        "response": "Os 3 principais LOGRADOUROS com maiores números de empresas: HABITACIONAL SOL NASCENTE: '6259', QUADRA 1: '1804', DAS ARAUCARIAS: 1532"
    },
    {
        "INPUT": "Quantas empresas no DF foram abertas nos últimos 5 anos?",
        "SQLQUERY": "SELECT COUNT(*) AS NUMERO_EMPRESAS_ABERTAS FROM bd_empresa.estabelecimentos WHERE UF = 'DF' AND DT_INICIO_ATIV >= DATE_SUB(CURDATE(), INTERVAL 5 YEAR)",
        "response": "Foram abertas: 319127 no DF nos últimos 5 anos."
    },
    {
        "INPUT": "Quantas empresas estão ativas no DF?",
        "SQLQUERY": "SELECT COUNT(*) AS 'Quantidade' FROM bd_empresa.estabelecimentos WHERE SITU_CADASTRAL = '8' AND DATE_SUB(CURDATE(), INTERVAL 5 YEAR) AND UF = 'DF'",
        "response": "Foram abertas: 423764 no DF nos últimos 5 anos."
    }
]
````
### 7. Execução de Consultas
O loop final percorre cada exemplo, executando as consultas e imprimindo os resultados:

````python
for example in examples:
    input_question = example["INPUT"]
    sql_query = example["SQLQUERY"]
    
    print(f"Pergunta: {input_question}")
    print(f"SQL Query: {sql_query}")
    
    try:
        response = ask_question(agent_executor, sql_query)
        if "response" in example:
            expected_response = example["response"]
            print(f"Resposta esperada: {expected_response}")
        print(f"Resposta obtida: {response}")
        print()
    except Exception as e:
        print(f"Erro ao executar a consulta: {e}")
````
Tratamento de Erros: O código captura exceções para garantir que erros durante a execução sejam reportados adequadamente.

## Conclusão

Este código ilustra a integração eficaz entre processamento de linguagem natural e consultas SQL, demonstrando como tecnologias avançadas podem transformar a interação com bancos de dados. Ao permitir que usuários façam perguntas em linguagem natural, elimina a necessidade de conhecimentos técnicos em SQL, tornando a análise de dados mais acessível e intuitiva. Essa abordagem não apenas simplifica a busca por informações, mas também potencializa a tomada de decisões informadas, destacando o papel crescente da inteligência artificial na democratização do acesso a dados.
