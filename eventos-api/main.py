from fastapi import FastAPI
from models.database import Base, engine
from routes.eventos_routes import router as eventos_router
from routes.ingressos_routes import router as ingressos_router

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="API de Controle de Lotação em Eventos",
    description="""
## Bilheteria Digital com Controle de Capacidade

Sistema de gerenciamento de eventos com **bloqueio automático** ao atingir lotação máxima.

### Regras de Negócio
- ❌ Não é possível comprar ingresso para evento **lotado**
- ❌ Não é possível cadastrar o **mesmo CPF** duas vezes no mesmo evento
- ❌ Não é possível criar evento com **capacidade zero ou negativa**
- ❌ Campos obrigatórios não podem ser **vazios**

### Desenvolvido para
Tech Challenge UNINASSAU — Disciplina: Back-end Frameworks 2026.1
    """,
    version="1.0.0",
)

app.include_router(eventos_router)
app.include_router(ingressos_router)


@app.get("/", tags=["Status"])
def root():
    return {
        "status": "online",
        "mensagem": "API de Controle de Lotação em Eventos",
        "docs": "/docs",
    }
