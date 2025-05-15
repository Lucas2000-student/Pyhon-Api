from fastapi import FastAPI, HTTPException
from typing import List
from Manutencao import Manutencao, ManutencaoCreate
from fastapi.middleware.cors import CORSMiddleware
import oracledb
import os
from dotenv import load_dotenv


# Carrega as variáveis do .env
load_dotenv()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Pode colocar domínios específicos aqui no futuro
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_SID = os.getenv("DB_SID")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


proximo_id: int = 0  # contador de ID automático

@app.get("/ola")
def katia():
    return({
        "mensagem": "alguma coisa"
    })

# Rota para criar uma nova tarefa (ID gerado automaticamente no backend Python)
@app.post("/Manutencao", response_model=Manutencao)
def criar_manutencao(manutencao: ManutencaoCreate):
    global proximo_id
    proximo_id += 1
    nova_manutencao = Manutencao(id_usuario=proximo_id, **manutencao.dict())


    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()


    cursor.execute("INSERT INTO T_HFLL_USUARIO (ID_USUARIO, NOME, EMAIL, SENHA, PREFERENCIAS) VALUES (:valor1, :valor2, :valor3, :valor4, :valor5)", valor1=nova_manutencao.id_usuario, valor2=nova_manutencao.nome, valor3=nova_manutencao.email, valor4=nova_manutencao.senha, valor5=nova_manutencao.preferencias)
    conn.commit()


    cursor.close()
    conn.close()


    return nova_manutencao    
   


# Rota para listar todas as tarefas
@app.get("/Manutencao", response_model=List[Manutencao])
def listar_manutencao():


    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()


    cursor.execute('SELECT * FROM T_HFLL_USUARIO')


    rows = cursor.fetchall()


    cursor.close()
    conn.close()

    return[
        {
            "id_usuario": row[0],
            "nome": row[1],
            "email": row[2],
            "senha": row[3],
            "preferencias": row[4]
        }
        for row in rows
    ]



# Rota para obter uma tarefa específica
@app.get("/Manutencao/{manutencao_id_usuario}", response_model=Manutencao)
def obter_manutencao(manutencao_id_usuario: int):
    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()


    cursor.execute('SELECT * FROM T_HFLL_USUARIO WHERE ID_USUARIO = :valor1', valor1=manutencao_id_usuario)

    row = cursor.fetchone()
   
    if row:
        return {
            "id_usuario": row[0],
            "nome": row[1],
            "email": row[2],
            "senha": row[3],
            "preferencias": row[4]
        }
    raise HTTPException(status_code=404, detail="Usuário não encontrado.")

# Rota para atualizar uma tarefa completa
@app.put("/Manutencao/{manutencao_id_usuario}")
def atualizar_manutencao(manutencao_id_usuario: int, manutencao_atualizada: ManutencaoCreate):
    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()

    cursor.execute("UPDATE T_HFLL_USUARIO SET NOME=:valor2, EMAIL=:valor3, SENHA=:valor4, PREFERENCIAS=:valor5 WHERE ID_USUARIO=:valor1", valor1=manutencao_id_usuario, valor2=manutencao_atualizada.nome, valor3=manutencao_atualizada.email, valor4=manutencao_atualizada.senha, valor5=manutencao_atualizada.preferencias)
    conn.commit()


    cursor.close()
    conn.close()


    return {"mensagem": "Usuario atualizado com sucesso!"}


# Rota para excluir uma tarefa
@app.delete("/Manutencao/{manutencao_id_usuario}")
def deletar_Manutencao(manutencao_id_usuario: int):
    dsn = oracledb.makedsn(host=DB_HOST, port=DB_PORT, sid=DB_SID)
    conn = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=dsn)


    cursor = conn.cursor()


    cursor.execute("DELETE FROM T_HFLL_USUARIO WHERE ID_USUARIO=:valor1", valor1=manutencao_id_usuario)
    conn.commit()


    cursor.close()
    conn.close()


    return {"mensagem": "Usuario excluído com sucesso"}