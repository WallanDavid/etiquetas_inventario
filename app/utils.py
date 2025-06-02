import qrcode
from pathlib import Path

def gerar_qrcode(codigo: str, dados: dict):
    caminho = Path("qrcodes") / f"{codigo}.png"
    caminho.parent.mkdir(exist_ok=True)

    img = qrcode.make(dados)
    img.save(caminho)
