from sqlalchemy import create_engine
import os
from langchain_community.agent_toolkits import create_sql_agent
from langchain.utilities import SQLDatabase
from sqlalchemy import create_engine

os.environ["GROQ_API_KEY"] = 'sua_chave_groq'
from langchain_groq import ChatGroq

llm2 = ChatGroq(
            model="llama3-70b-8192",
            temperature=1
        )

uri_empresas = "mariadb+pymysql://root:my-secret-pw@192.168.1.126/empresa?charset=utf8mb4"
engine = create_engine(uri_empresas)

db = SQLDatabase(engine)


agent_executor = create_sql_agent(llm2, db=db, verbose=True)

response = agent_executor.invoke(
    """Levando em consideração que os dados das empresas do DF estão na tabela estabelecimentos_df, e que os dados de endereço
    estão nos campos LOGRADOURO, que representa a rua, quadra, etc. complemento, número, bairro, cep, UF e município, responda
    O CNAE, o Código nacional de atividade empresarial, indica quais as atividaes empresariais da empresa, a descrição de 
    cada código fica na tabela tabela cnaes, onde a descricao indica o que é cada atividade no campo DESCRICAO. Essa tabela tem um relacionamento
    com a tabela de estabelecimentos. Cada estabelecimento tem um ou mais códigos CNAE, cuja descricao está na tabela CNAE 
    Todas as respostas devem ser em português.
    Quantas empresas existem no DF?""")

