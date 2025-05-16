from pydantic import BaseModel
from typing import List, Optional


# Modelo de entrada (sem o ID)
class ManutencaoCreate(BaseModel):
    nome: str
    email: str 
    senha: str

# Modelo de saída (com ID)
class Manutencao(ManutencaoCreate):
    id_usuario: int
