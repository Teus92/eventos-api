from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.models import Ingresso, Evento
from pydantic import BaseModel


# ── Schemas ────────────────────────────────────────────────────────────────────

class IngressoCreate(BaseModel):
    nome_participante: str
    cpf: str
    evento_id: int


# ── Controller ─────────────────────────────────────────────────────────────────

def listar_ingressos(db: Session):
    return db.query(Ingresso).all()


def buscar_ingresso(ingresso_id: int, db: Session):
    ingresso = db.query(Ingresso).filter(Ingresso.id == ingresso_id).first()
    if not ingresso:
        raise HTTPException(status_code=404, detail="Ingresso não encontrado.")
    return ingresso


def comprar_ingresso(dados: IngressoCreate, db: Session):
    # ── Regra de negócio: campos obrigatórios ──────────────────────────────────
    if not dados.nome_participante.strip():
        raise HTTPException(status_code=422, detail="O nome do participante não pode ser vazio.")
    if not dados.cpf.strip():
        raise HTTPException(status_code=422, detail="O CPF não pode ser vazio.")

    # ── Regra de negócio: evento deve existir ──────────────────────────────────
    evento = db.query(Evento).filter(Evento.id == dados.evento_id).first()
    if not evento:
        raise HTTPException(status_code=404, detail="Evento não encontrado.")

    # ── Regra de negócio: CPF duplicado no mesmo evento ───────────────────────
    cpf_ja_cadastrado = db.query(Ingresso).filter(
        Ingresso.evento_id == dados.evento_id,
        Ingresso.cpf == dados.cpf
    ).first()
    if cpf_ja_cadastrado:
        raise HTTPException(
            status_code=409,
            detail=f"CPF {dados.cpf} já possui ingresso para este evento."
        )

    # ── Regra de negócio: BLOQUEIO POR LOTAÇÃO ────────────────────────────────
    vagas_ocupadas = db.query(Ingresso).filter(Ingresso.evento_id == dados.evento_id).count()
    if vagas_ocupadas >= evento.capacidade_maxima:
        raise HTTPException(
            status_code=409,
            detail=f"Evento '{evento.nome}' está lotado! Capacidade máxima de {evento.capacidade_maxima} pessoas atingida."
        )

    ingresso = Ingresso(**dados.model_dump())
    db.add(ingresso)
    db.commit()
    db.refresh(ingresso)
    return {"mensagem": "Ingresso comprado com sucesso!", "ingresso": ingresso}


def cancelar_ingresso(ingresso_id: int, db: Session):
    ingresso = db.query(Ingresso).filter(Ingresso.id == ingresso_id).first()
    if not ingresso:
        raise HTTPException(status_code=404, detail="Ingresso não encontrado.")
    db.delete(ingresso)
    db.commit()
    return {"mensagem": f"Ingresso de '{ingresso.nome_participante}' cancelado com sucesso."}
