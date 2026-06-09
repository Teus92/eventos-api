from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from models.database import get_db
from controllers.ingressos_controller import (
    IngressoCreate,
    listar_ingressos, buscar_ingresso,
    comprar_ingresso, cancelar_ingresso
)

router = APIRouter(prefix="/ingressos", tags=["Ingressos"])


@router.get("/", summary="Listar todos os ingressos")
def get_ingressos(db: Session = Depends(get_db)):
    return listar_ingressos(db)


@router.get("/{ingresso_id}", summary="Buscar ingresso por ID")
def get_ingresso(ingresso_id: int, db: Session = Depends(get_db)):
    return buscar_ingresso(ingresso_id, db)


@router.post("/", summary="Comprar ingresso (bloqueia se lotado)")
def post_ingresso(dados: IngressoCreate, db: Session = Depends(get_db)):
    return comprar_ingresso(dados, db)


@router.delete("/{ingresso_id}", summary="Cancelar ingresso")
def delete_ingresso(ingresso_id: int, db: Session = Depends(get_db)):
    return cancelar_ingresso(ingresso_id, db)
