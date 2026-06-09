from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.models import Evento
from pydantic import BaseModel
from typing import Optional


# ── Schemas ────────────────────────────────────────────────────────────────────

class EventoCreate(BaseModel):
    nome: str
    local: str
    data: str
    capacidade_maxima: int


class EventoUpdate(BaseModel):
    nome: Optional[str] = None
    local: Optional[str] = None
    data: Optional[str] = None
    capacidade_maxima: Optional[int] = None


# ── Controller ─────────────────────────────────────────────────────────────────

def listar_eventos(db: Session):
    eventos = db.query(Evento).all()
    resultado = []
    for e in eventos:
        vagas_ocupadas = len(e.ingressos)
        resultado.append({
            "id": e.id,
            "nome": e.nome,
            "local": e.local,
            "data": e.data,
            "capacidade_maxima": e.capacidade_maxima,
            "vagas_ocupadas": vagas_ocupadas,
            "vagas_restantes": e.capacidade_maxima - vagas_ocupadas,
            "lotado": vagas_ocupadas >= e.capacidade_maxima,
        })
    return resultado


def buscar_evento(evento_id: int, db: Session):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
    vagas_ocupadas = len(evento.ingressos)
    return {
        "id": evento.id,
        "nome": evento.nome,
        "local": evento.local,
        "data": evento.data,
        "capacidade_maxima": evento.capacidade_maxima,
        "vagas_ocupadas": vagas_ocupadas,
        "vagas_restantes": evento.capacidade_maxima - vagas_ocupadas,
        "lotado": vagas_ocupadas >= evento.capacidade_maxima,
    }


def criar_evento(dados: EventoCreate, db: Session):
    # ── Regra de negócio: campos obrigatórios ──────────────────────────────────
    if not dados.nome.strip():
        raise HTTPException(status_code=422, detail="O nome do evento não pode ser vazio.")
    if not dados.local.strip():
        raise HTTPException(status_code=422, detail="O local do evento não pode ser vazio.")
    if not dados.data.strip():
        raise HTTPException(status_code=422, detail="A data do evento não pode ser vazia.")
    if dados.capacidade_maxima <= 0:
        raise HTTPException(status_code=422, detail="A capacidade máxima deve ser maior que zero.")

    evento = Evento(**dados.model_dump())
    db.add(evento)
    db.commit()
    db.refresh(evento)
    return {"mensagem": "Evento criado com sucesso!", "evento": evento}


def atualizar_evento(evento_id: int, dados: EventoUpdate, db: Session):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")

    if dados.capacidade_maxima is not None and dados.capacidade_maxima <= 0:
        raise HTTPException(status_code=422, detail="A capacidade máxima deve ser maior que zero.")

    for campo, valor in dados.model_dump(exclude_unset=True).items():
        setattr(evento, campo, valor)

    db.commit()
    db.refresh(evento)
    return {"mensagem": "Evento atualizado com sucesso!", "evento": evento}


def deletar_evento(evento_id: int, db: Session):
    evento = db.query(Evento).filter(Evento.id == evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")
    db.delete(evento)
    db.commit()
    return {"mensagem": f"Evento '{evento.nome}' deletado com sucesso."}
