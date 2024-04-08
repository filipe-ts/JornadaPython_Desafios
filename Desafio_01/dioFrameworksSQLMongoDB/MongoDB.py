import pymongo as pm

uri = "mongodb+srv://<user>:<password>@clustertest.u7a6s0p.mongodb.net/?retryWrites=true&w=majority"

client = pm.MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

data_base = client.dio
colecao = data_base.dio_colection

post = {
    "cliente": "João Marcos",
    "cpf": "64596575748",
    "endereco": "Avenida Paulista",
    "contas": {"conta_1": {
                "tipo": "CC",
                "agencia": "555236",
                "numero": "231",
                "saldo": "900.06"
            },
            "conta_2":
            {
                "tipo": "CP",
                "agencia": "555236",
                "numero": "984",
                "saldo": "17250.13"
            }
    }
}

post = {
    "cliente": "Maria Francisca",
    "cpf": "87902341178",
    "endereco": "Avenida Tiete",
    "contas": {"conta_1": {
                "tipo": "CC",
                "agencia": "547291",
                "numero": "256",
                "saldo": "5230.75"
            }
    }
}

colecao.insert_one(post).inserted_id

consulta = colecao.find(projection={"_id": False,"cliente": True, "contas": True})

for c in consulta:
    for chave, valor in c['contas'].items():
        print(f"{c['cliente']}: {valor['tipo']} {valor['agencia']}-{valor['numero']}")

