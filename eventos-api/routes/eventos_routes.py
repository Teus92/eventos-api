from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from controllers.eventos_controller import (
    EventoCreate, EventoUpdate,
    listar_eventos, buscar_evento,
    criar_evento, atualizar_evento, deletar_evento
)

router = APIRouter(prefix="/eventos", tags=["Eventos"])


@router.get("/", summary="Listar todos os eventos")
def get_eventos(db: Session = Depends(get_db)):
    return listar_eventos(db)


@router.get("/{evento_id}", summary="Buscar evento por ID")
def get_evento(evento_id: int, db: Session = Depends(get_db)):
    return buscar_evento(evento_id, db)


@router.post("/", summary="Criar novo evento")
def post_evento(dados: EventoCreate, db: Session = Depends(get_db)):
    return criar_evento(dados, db)


@router.patch("/{evento_id}", summary="Atualizar evento")
def patch_evento(evento_id: int, dados: EventoUpdate, db: Session = Depends(get_db)):
    return atualizar_evento(evento_id, dados, db)


@router.delete("/{evento_id}", summary="Deletar evento")
def delete_evento(evento_id: int, db: Session = Depends(get_db)):
    return deletar_evento(evento_id, db)
