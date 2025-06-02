# 📦 Etiquetas & Inventário

Sistema de controle de inventário com geração de etiquetas e QRCode, construído com **FastAPI**, **SQLite** e exportação em **PDF/HTML** via **WeasyPrint**. Ideal para pequenos comércios e controle interno de produtos.

## 🚀 Funcionalidades

- ✅ Cadastro de itens com nome, código e quantidade
- 📦 Listagem, atualização e remoção de itens
- 🖨️ Exportação de etiquetas com QRCode (HTML e PDF)
- 🔐 Autenticação HTTP Basic nas rotas protegidas
- 🧪 Testes com cobertura
- 🐳 Docker e Railway para deploy automático

## 🛠️ Tecnologias

- FastAPI
- SQLAlchemy Async
- SQLite
- WeasyPrint
- Docker + Docker Compose
- Railway (deploy)
- Pytest

## 📦 Instalação local via Docker

```bash
git clone https://github.com/WallanDavid/etiquetas_inventario.git
cd etiquetas_inventario
docker-compose up --build
```

O app estará disponível em `http://localhost:8000`

## 📫 Endpoints disponíveis

| Método | Rota                  | Autenticação | Descrição                         |
|--------|-----------------------|--------------|-----------------------------------|
| POST   | `/items`              | ❌           | Cadastra novo item                |
| GET    | `/items`              | ❌           | Lista todos os itens              |
| PUT    | `/items/{codigo}`     | ❌           | Atualiza nome/quantidade          |
| DELETE | `/items/{codigo}`     | ❌           | Remove item                       |
| GET    | `/etiquetas`          | ✅ Basic     | Visualiza etiquetas em HTML       |
| GET    | `/etiquetas/pdf`      | ✅ Basic     | Exporta etiquetas em PDF          |

## 🔐 Credenciais (dev)

```
Usuário: admin
Senha: senha123
```

## 🧪 Executar testes

```bash
pytest --cov=app --cov-report=term-missing
```

## 🌍 Deploy

Projeto hospedado gratuitamente via Railway:

👉 https://etiquetasinventario-production.up.railway.app

## 🖼️ Exemplo de etiquetas

```
<h1>Etiquetas</h1>
+------------------------+
| Caneta Azul            |
| [ QRCode ]             |
| CA456                  |
+------------------------+
```

---

🕓 Última atualização: 2025-06-02
