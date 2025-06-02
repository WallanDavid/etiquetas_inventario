# 🏷️ Etiquetas & Inventário

Sistema de controle de inventário com geração de etiquetas, exportação HTML/PDF e autenticação básica.

![Badge: Docker](https://img.shields.io/badge/docker-ready-blue)
![Badge: FastAPI](https://img.shields.io/badge/FastAPI-async--ready-green)
![Badge: PDF](https://img.shields.io/badge/export-PDF-blue)
![Badge: Testes](https://img.shields.io/badge/tests-100%25-success)

---

## 🚀 Tecnologias

- [x] Python 3.11
- [x] FastAPI
- [x] SQLAlchemy + SQLite
- [x] Jinja2 (HTML)
- [x] WeasyPrint (PDF)
- [x] Pytest
- [x] Docker

---

## 📦 Funcionalidades

- ✅ Cadastro de itens com nome, código e quantidade
- ✅ Listagem de inventário
- ✅ Exportação das etiquetas em **HTML** ou **PDF**
- ✅ Proteção com autenticação básica (usuário/senha via `.env`)
- ✅ Testes automatizados
- ✅ Dockerização completa

---

## 🛠️ Instalação Local

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/etiquetas_inventario.git
cd etiquetas_inventario


2. Crie e ative o ambiente virtual
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Linux/macOS


3. Instale as dependências
pip install -r requirements.txt


4. Rode a API
uvicorn app.main:app --reload


Acesse: http://localhost:8000/docs