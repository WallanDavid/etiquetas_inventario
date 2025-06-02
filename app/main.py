from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel
from typing import List
from pathlib import Path
from io import BytesIO
from weasyprint import HTML as WeasyHTML
import secrets

from app.db import get_db, engine, Base
from app.models import Item
from app.utils import gerar_qrcode

app = FastAPI()
security = HTTPBasic()
USERNAME = "admin"
PASSWORD = "senha123"

app.mount("/static", StaticFiles(directory="qrcodes"), name="static")

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

class ItemCreate(BaseModel):
    nome: str
    codigo: str
    quantidade: int

class ItemUpdate(BaseModel):
    nome: str | None = None
    quantidade: int | None = None

def autenticar(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, USERNAME)
    correct_password = secrets.compare_digest(credentials.password, PASSWORD)

    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas",
            headers={"WWW-Authenticate": "Basic"},
        )

@app.post("/items", response_model=dict)
async def criar_item(item: ItemCreate, db: AsyncSession = Depends(get_db)):
    novo_item = Item(**item.dict())
    db.add(novo_item)
    try:
        await db.commit()
        gerar_qrcode(item.codigo, item.dict())
    except:
        await db.rollback()
        raise HTTPException(status_code=400, detail="Código duplicado")
    return {"message": "Item cadastrado com sucesso"}

@app.get("/items", response_model=List[dict])
async def listar_itens(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item))
    itens = result.scalars().all()
    return [
        {"id": i.id, "nome": i.nome, "codigo": i.codigo, "quantidade": i.quantidade}
        for i in itens
    ]

@app.put("/items/{codigo}", response_model=dict)
async def atualizar_item(codigo: str, dados: ItemUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.codigo == codigo))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    if dados.nome is not None:
        item.nome = dados.nome
    if dados.quantidade is not None:
        item.quantidade = dados.quantidade

    await db.commit()
    return {"message": "Item atualizado com sucesso"}

@app.delete("/items/{codigo}", response_model=dict)
async def remover_item(codigo: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Item).where(Item.codigo == codigo))
    item = result.scalar_one_or_none()
    if not item:
        raise HTTPException(status_code=404, detail="Item não encontrado")

    await db.delete(item)
    await db.commit()
    return {"message": "Item removido com sucesso"}

@app.get("/etiquetas", response_class=HTMLResponse)
async def exportar_etiquetas(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(autenticar)
):
    result = await db.execute(select(Item))
    itens = result.scalars().all()

    html = """
    <html>
    <head>
        <style>
            body { font-family: sans-serif; padding: 20px; }
            .etiqueta {
                display: inline-block;
                width: 200px;
                height: 220px;
                border: 1px solid #ccc;
                margin: 10px;
                text-align: center;
                padding: 10px;
            }
            img {
                width: 150px;
                height: 150px;
            }
            button {
                position: fixed;
                top: 20px;
                right: 20px;
                padding: 10px 20px;
                background: black;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
        </style>
    </head>
    <body>
        <h1>Etiquetas</h1>
        <button onclick="window.print()">Imprimir</button>
    """

    for item in itens:
        img_path = Path(f"qrcodes/{item.codigo}.png")
        if img_path.exists():
            html += f"""
            <div class="etiqueta">
                <p><strong>{item.nome}</strong></p>
                <img src="/static/{item.codigo}.png" alt="QR">
                <p>{item.codigo}</p>
            </div>
            """

    html += "</body></html>"
    return HTMLResponse(content=html)

@app.get("/etiquetas/pdf")
async def exportar_etiquetas_pdf(
    db: AsyncSession = Depends(get_db),
    credentials: HTTPBasicCredentials = Depends(autenticar)
):
    result = await db.execute(select(Item))
    itens = result.scalars().all()

    html = """
    <html>
    <head>
        <style>
            body { font-family: sans-serif; padding: 20px; }
            .etiqueta {
                display: inline-block;
                width: 200px;
                height: 220px;
                border: 1px solid #ccc;
                margin: 10px;
                text-align: center;
                padding: 10px;
            }
            img {
                width: 150px;
                height: 150px;
            }
        </style>
    </head>
    <body>
        <h1>Etiquetas</h1>
    """

    for item in itens:
        img_path = Path(f"qrcodes/{item.codigo}.png")
        if img_path.exists():
            html += f"""
            <div class="etiqueta">
                <p><strong>{item.nome}</strong></p>
                <img src="file://{img_path.resolve()}" alt="QR">
                <p>{item.codigo}</p>
            </div>
            """

    html += "</body></html>"
    pdf_io = BytesIO()
    WeasyHTML(string=html).write_pdf(pdf_io)
    pdf_io.seek(0)

    return StreamingResponse(
        content=pdf_io,
        media_type="application/pdf",
        headers={"Content-Disposition": "inline; filename=etiquetas.pdf"}
    )
