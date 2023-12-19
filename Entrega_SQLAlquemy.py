from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy import func


Base = declarative_base()

# Criar a tabela "user_account" como uma classe do python
class Cliente(Base):
    __tablename__ = "cliente"
    id_cliente = Column(Integer, primary_key=True)
    nome = Column(String)
    cpf = Column(Integer)
    endereco = Column(String)

    # Relacionamento entre as tabelas
    contas = relationship("Conta", back_populates="cliente")

    # Representação da tabela
    def __repr__(self):
        return f"Cliente(id={self.id_cliente}, name={self.nome}, cpf{self.cpf}, endereco{self.endereco})"

# Criar a tabela "address" como uma classe do python
class Conta(Base):
    __tablename__ = "conta"
    id = Column(Integer, primary_key=True)
    tipo = Column(String)
    agencia = Column(Integer)
    saldo = Column(Integer)
    id_cliente = Column(Integer, ForeignKey("cliente.id_cliente"), nullable=False)

    cliente = relationship("Cliente", back_populates="contas")

    def __repr__(self):
        return f"Conta(id={self.id}, tipo={self.tipo}, agencia{self.agencia}, id_cliente{self.id_cliente}, saldo{self.saldo})"
    
print(Cliente.__tablename__)
print(Conta.__tablename__)

# Conexão com o banco de dados
engine = create_engine("sqlite://")

# Criando as classes como tabelas no banco de dados
Base.metadata.create_all(engine)

inspetor_engine = inspect(engine)

print(inspetor_engine.has_table("cliente"))
print(inspetor_engine.get_table_names())
print(inspetor_engine.default_schema_name)

# Populando as tabelas (Classes)
with Session(engine) as session:
    jose = Cliente(nome="Jose", cpf="12345678901", endereco="Rua Oiapoc, 1257, São Miguel do Oeste-SC",
                   contas=[Conta(tipo="conta corrente", agencia="1515015", saldo=5000)])
    mauricio = Cliente(nome="Mauricio", cpf="12345678902", endereco="Rua das flores, 123, São Paulo-SP",
                       contas=[Conta(tipo="conta poupança", agencia="1500542", saldo=1500)])
    maria = Cliente(nome="Maria", cpf="12345678903", endereco="Rua Amarela, 432, Rio de Janeiro-RJ",contas=[Conta(agencia="5845851", saldo=20000)])

    # Enviando os dados para o DB (persistência dos dados)
    session.add_all([jose,mauricio,maria])
    # Commitando o envio
    session.commit()

    # "select" para recuperar dados, da classe Cliente, filtrando por name = 'Jose' e 'Mauricio'
stmt = select(Cliente).where(Cliente.nome.in_(['Jose','Mauricio']))
print("Recuperando dados da tabela User, filtrando por nome de Jose e Mauricio")
for user in session.scalars(stmt):
    print(user)
print()

    # "select" para recuperar dados, da classe Conta, filtrando por id_cliente = 2
stmt_address = select(Conta).where(Conta.id_cliente.in_([2]))
print("Recuperando dados da tabela Conta, filtrando por user_id = 2")
for address in session.scalars(stmt_address):
    print(address)
print()


stmt_order = select(Cliente).order_by(Cliente.id_cliente.desc())
print("Recuperando dados da tabela Cliente, ordernando por id desc")
for user in session.scalars(stmt_order):    
    print(user)
print()

# O método SCALARS pega o primeiro resultado. Mesmo recebendo 2 "colunas" como resultado de um join, ele retorna apenas o primeiro argumento
stmt_join = select(Cliente.nome, Conta.tipo).join_from(Conta, Cliente)
for result in session.scalars(stmt_join):
    print(result)
print(stmt_join)

# Nesse caso, é preciso usar o connect e o fetchall para retornar todos os dados
connection = engine.connect()
results = connection.execute(stmt_join).fetchall()
print("Executando consulta a partir da connection")
for result in results:
    print(result)
print()

stmt_count = select(func.count('*')).select_from(Cliente)
print("Consulta de count da tabela User")
for result in session.scalars(stmt_count):
    print(result)
print(stmt_count)
