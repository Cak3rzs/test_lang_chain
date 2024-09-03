import time
from sqlalchemy import create_engine
import os
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_groq import ChatGroq

# Configuração do ambiente
os.environ["GROQ_API_KEY"] = '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'

llm2 = ChatGroq(
    model="llama3-70b-8192",
    temperature=1
)

# Conexão com o banco de dados
db_user = "root"
db_password = ""
db_host = "localhost:3306"
db_name = "bd_empresa"
uri_empresas = f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}"
engine = create_engine(uri_empresas)

db = SQLDatabase(engine)

# Função para executar perguntas e obter respostas diretamente


# Criação do agente executor
agent_executor = create_sql_agent(llm2, db=db)

# Exemplo de perguntas e respostas
examples = [
    {
        "INPUT": "Quantas empresas no DF têm atividades relacionadas ao setor de saúde?",
        "SQLQUERY": "SELECT COUNT(*) AS 'Quantidade' FROM bd_empresa.estabelecimentos_cnae cn INNER JOIN bd_empresa.estabelecimentos es ON cn.CNPJ = es.CNPJ WHERE cn.FISCAL IN (SELECT ID FROM bd_empresa.cnaes WHERE MATCH(ID, DESCRICAO) AGAINST('*Saude*' IN BOOLEAN MODE)) AND es.UF = 'DF';",
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
    },
    {
        "INPUT": "Quantas consultorias em Tecnologia da Informação existem no DF?",
        "SQLQUERY": "SELECT COUNT(*) AS 'Quantidade' FROM bd_empresa.estabelecimentos_cnae cn INNER JOIN bd_empresa.estabelecimentos es ON cn.CNPJ = es.CNPJ WHERE cn.FISCAL IN (SELECT ID FROM bd_empresa.cnaes WHERE MATCH(ID, DESCRICAO) AGAINST('*Consultoria em Tecnologia da Informação*' IN BOOLEAN MODE)) AND es.UF = 'DF';",
        "response": "No DF existem: 2964 empresas de Consultoria em Tecnologia da Informação."
    },
    {
        "INPUT": "Quantos restaurantes existem no DF?",
        "SQLQUERY": "SELECT COUNT(*) AS 'Quantidade' FROM bd_empresa.estabelecimentos_cnae cn INNER JOIN bd_empresa.estabelecimentos es ON cn.CNPJ = es.CNPJ WHERE cn.FISCAL IN (SELECT ID FROM bd_empresa.cnaes WHERE MATCH(ID, DESCRICAO) AGAINST('*Restaurante*' IN BOOLEAN MODE)) AND es.UF = 'DF';",
        "response": "Existem 738 empresas no DF com 'Restaurante' na descrição do CNAE no DF."
    },
    {
        "INPUT": "Qual é o bairro com o maior número de empresas de tecnologia no DF?",
        "SQLQUERY": "SELECT es.BAIRRO, COUNT(*) AS NUMERO_EMPRESAS FROM bd_empresa.estabelecimentos_cnae cn INNER JOIN bd_empresa.estabelecimentos es ON cn.CNPJ = es.CNPJ WHERE cn.FISCAL IN (SELECT ID FROM bd_empresa.cnaes WHERE MATCH(ID, DESCRICAO) AGAINST('*Tecnologia*' IN BOOLEAN MODE)) AND es.UF = 'DF' GROUP BY es.BAIRRO ORDER BY NUMERO_EMPRESAS DESC LIMIT 1",
        "response": "O Bairro com o maior número de empresas de tecnologia no DF e: Asa Sul com 121 empresas abertas"
    },
    {
        "INPUT": "Quantas micro empresas existem no DF?", 
        "SQLQUERY": "SELECT COUNT(*) AS 'Quantidade' FROM bd_empresa.empresas WHERE PORTE_EMPRESA = 'MICRO EMPRESA';", 
        "response": "Existem aproximadamente 750223 micro empresas no DF"
    },

]

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
        print()
