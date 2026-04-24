from fastapi import FastAPI
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic import BaseModel, field_validator

app = FastAPI()

@app.get("/")
def home():
    return {"mensagem": "API funcionando"}

convidados = [
    {"id": 1, "nome": "Ana Martins", "cpf": "12345678901", "mesa": 3, "checkin": False},
    {"id": 2, "nome": "Bruno Costa", "cpf": "23456789012", "mesa": 4, "checkin": True},
    {"id": 3, "nome": "Carla Souza", "cpf": "34567890123", "mesa": 2, "checkin": False}
]

@app.get("/convidados")
def listar_convidados():
    return convidados


@app.get("/convidados/{id}")
def buscar_convidado(id: int):
    for convidado in convidados:
        if convidado["id"] == id:
            return convidado
    raise HTTPException(status_code=404, detail="Convidado não encontrado")

class ConvidadoSchema(BaseModel):
    nome: str
    cpf: str
    mesa: int

    @field_validator("nome")
    @classmethod
    def validar_nome(cls, value):
        if len(value.strip()) < 3:
            raise ValueError("Nome inválido")
        return value
    @field_validator("cpf")
    @classmethod
    def validar_cpf(cls, value):
        if not value.isdigit() or len(value) != 11:
            raise ValueError("CPF inválido")
        return value
    
@app.post("/convidados")
def criar_convidado(dados: ConvidadoSchema):
    for convidado in convidados:
        if convidado["cpf"] == dados.cpf:
            raise HTTPException(status_code=400, detail="CPF já cadastrado")

    novo = {
        "id": len(convidados) + 1,
        "nome": dados.nome,
        "cpf": dados.cpf,
        "mesa": dados.mesa,
        "checkin": False
    }
    convidados.append(novo)
    return novo

@app.put("/convidados/{id}")
def atualizar_convidado(id: int, dados: ConvidadoSchema):
    for convidado in convidados:
        if convidado["id"] == id:
            convidado["nome"] = dados.nome
            convidado["cpf"] = dados.cpf
            convidado["mesa"] = dados.mesa
            return convidado
    raise HTTPException(status_code=404, detail="Convidado não encontrado")

@app.delete("/convidados/{id}")
def remover_convidado(id: int):
    for convidado in convidados:
        if convidado["id"] == id:
            convidados.remove(convidado)
            return {"mensagem": "Convidado removido com sucesso"}
    raise HTTPException(status_code=404, detail="Convidado não encontrado")

@app.post("/convidados/{id}/checkin")
def fazer_checkin(id: int):
    for convidado in convidados:
        if convidado["id"] == id:
            if convidado["checkin"]:
                raise HTTPException(status_code=400, detail="Check-in já realizado")
            convidado["checkin"] = True
            return {"mensagem": "Check-in realizado com sucesso"}
    raise HTTPException(status_code=404, detail="Convidado não encontrado")

@app.get("/convidados/confirmados")
def listar_confirmados():
    return [c for c in convidados if c["checkin"]]

@app.get("/relatorio")
def relatorio():
    total = len(convidados)
    confirmados = len([c for c in convidados if c["checkin"]])
    pendentes = total - confirmados

    return {
        "total": total,
        "confirmados": confirmados,
        "pendentes": pendentes
    }

@app.get("/convidados/mesa/{numero}")
def listar_por_mesa(numero: int):
    return [c for c in convidados if c["mesa"] == numero]