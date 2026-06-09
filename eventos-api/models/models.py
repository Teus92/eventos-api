from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from models.database import Base


class Evento(Base):
    __tablename__ = "eventos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    local = Column(String, nullable=False)
    data = Column(String, nullable=False)
    capacidade_maxima = Column(Integer, nullable=False)

    ingressos = relationship("Ingresso", back_populates="evento", cascade="all, delete")


class Ingresso(Base):
    __tablename__ = "ingressos"

    id = Column(Integer, primary_key=True, index=True)
    nome_participante = Column(String, nullable=False)
    cpf = Column(String, nullable=False)
    evento_id = Column(Integer, ForeignKey("eventos.id"), nullable=False)

    evento = relationship("Evento", back_populates="ingressos")
