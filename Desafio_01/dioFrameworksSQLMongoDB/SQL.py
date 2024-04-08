import sqlalchemy as sqla
import sqlalchemy.orm as orm
import typing as tp


class TabelaBase(orm.DeclarativeBase):
    pass


class Cliente(TabelaBase):
    __tablename__ = "cliente"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    nome: orm.Mapped[str] = orm.mapped_column(sqla.String)
    cpf: orm.Mapped[str] = orm.mapped_column(sqla.String(11))
    endereco: orm.Mapped[str] = orm.mapped_column(sqla.String(30))

    contas: orm.Mapped[tp.List["Conta"]] = (
        orm.relationship(
            back_populates="cliente", cascade="all, delete-orphan"
        )
    )

    def __repr__(self) -> str:
        return f"Cliente(id={self.id!r}, nome={self.nome!r}, cpf={self.cpf!r}, endereço={self.endereco!r})"


class Conta(TabelaBase):
    __tablename__ = "conta"

    id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
    tipo: orm.Mapped[str] = orm.mapped_column(sqla.String(30))
    agencia: orm.Mapped[str] = orm.mapped_column(sqla.String(10))
    numero: orm.Mapped[int] = orm.mapped_column()
    saldo: orm.Mapped[sqla.DECIMAL] = orm.mapped_column(sqla.DECIMAL(precision=12, scale=2))
    id_cliente: orm.Mapped[str] = orm.mapped_column(sqla.ForeignKey("cliente.id"))

    cliente: orm.Mapped[tp.List["Cliente"]] = (
        orm.relationship(
            back_populates="contas"
        )
    )

    def __repr__(self) -> str:
        return (f"{self.tipo!r} ID:{self.id!r} : "
                f"{self.agencia!r}-{self.numero!r} - Saldo: {self.saldo!r}"
                )


engine = sqla.create_engine("sqlite://", echo=True)
TabelaBase.metadata.create_all(engine)

with orm.Session(engine) as session:
    joao = Cliente(
        nome="João Marcos",
        cpf="64596575748",
        endereco="Avenida Paulista",
        contas=[
            Conta(
                tipo="CC",
                agencia="555236",
                numero="231",
                saldo=900.06
            ),
            Conta(
                tipo="CP",
                agencia="555236",
                numero="984",
                saldo=17250.13
            )
        ]
    )
    maria = Cliente(
        nome="Maria Francisca",
        cpf="87902341178",
        endereco="Avenida Tiete",
        contas=[
            Conta(
                tipo="CC",
                agencia="547291",
                numero="256",
                saldo=5230.75
            )
        ]
    )

    session.add_all([joao, maria])
    session.commit()

stmt = sqla.text(
    "SELECT nome, tipo, agencia, numero FROM"
    "(SELECT * FROM cliente JOIN conta ON cliente.id=conta.id_cliente)"
)

conexao = engine.connect()
respostas = conexao.execute(stmt).fetchall()

# retorna todas as contas com o nome do cliente
for resposta in respostas:
    print(f"{resposta[0]}: {resposta[1]} {resposta[2]}-{resposta[3]}")

