#!/usr/bin/env python3
"""Tarjeta de probabilidades para X (1600x900).
Uso: python3 tarjeta_probabilidades.py datos.json salida.png
datos.json: {"etiqueta": "...", "titulo": "...", "opciones": [{"nombre": "...", "prob": 62}], "pregunta": "...", "fuente": "...", "ejemplo": false}
"""
import json, sys, random
from PIL import Image, ImageDraw, ImageFont

W, H = 1600, 900
NEGRO, AZUL, LIMA, BLANCO, GRIS = (8, 8, 10), (31, 59, 255), (200, 240, 49), (255, 255, 255), (150, 150, 160)
G = "/usr/share/fonts/truetype/sand-box/google/"
ANTON = G + "Anton/Anton-Regular.ttf"
BARLOW_B = G + "Barlow Condensed/BarlowCondensed-Bold.ttf"
BARLOW_SB = G + "Barlow Condensed/BarlowCondensed-SemiBold.ttf"
f = lambda p, s: ImageFont.truetype(p, s)

def franjas(d):
    rnd = random.Random(7)
    for x0, col in [(-470, AZUL), (-410, LIMA), (1380, AZUL), (1460, LIMA)]:
        for i in range(4):
            off = x0 + i * 26 + rnd.randint(-8, 8)
            w = rnd.randint(6, 16)
            d.polygon([(off, H), (off + w, H), (off + w + 420, 0), (off + 420, 0)], fill=col)
    for y in range(0, H, 14):  # trama de puntos esquina
        for x in range(1180, W, 14):
            r = max(0, (x - 1180) / 420 * 3 - (y / H) * 2)
            if r > 0.4: d.ellipse([x - r, y - r, x + r, y + r], fill=(31, 59, 255))

def render(datos, salida):
    img = Image.new("RGB", (W, H), NEGRO)
    d = ImageDraw.Draw(img)
    franjas(d)
    d.rectangle([0, 0, W, 10], fill=LIMA)
    # cabecera
    d.text((90, 60), datos.get("etiqueta", "").upper(), font=f(BARLOW_B, 38), fill=LIMA)
    d.text((90, 105), datos["titulo"].upper(), font=f(ANTON, 76), fill=BLANCO)
    if datos.get("ejemplo"):
        d.text((W - 90, 70), "DATOS DE EJEMPLO", font=f(BARLOW_B, 32), fill=(255, 90, 90), anchor="ra")
    # barras
    ops = datos["opciones"][:4]
    top, alto, gap = 240, 84, 28
    x0, x1 = 90, 1300
    lider = max(o["prob"] for o in ops)
    for i, o in enumerate(ops):
        y = top + i * (alto + gap)
        d.rounded_rectangle([x0, y, x1, y + alto], 14, fill=(28, 28, 34))
        ancho = int((x1 - x0) * max(o["prob"], 1) / 100)
        col = LIMA if o["prob"] == lider else AZUL
        d.rounded_rectangle([x0, y, x0 + max(ancho, 30), y + alto], 14, fill=col)
        tcol = NEGRO if col == LIMA else BLANCO
        nf = f(BARLOW_B, 52)
        nombre = o["nombre"].upper()
        # Etiqueta siempre en la misma posición; sobre la barra lima va en negro (recortado al ancho de la barra)
        pos = (x0 + 26, y + alto / 2)
        d.text(pos, nombre, font=nf, fill=BLANCO, anchor="lm")
        if col == LIMA:
            m = Image.new("L", (W, H), 0)
            ImageDraw.Draw(m).text(pos, nombre, font=nf, fill=255, anchor="lm")
            caja = (x0, y, x0 + max(ancho, 30), y + alto)
            img.paste(Image.new("RGB", (caja[2] - caja[0], caja[3] - caja[1]), NEGRO), caja[:2], m.crop(caja))
        d.text((x1 + 30, y + alto / 2), (f"{o['prob']:.0f}%" if float(o['prob']).is_integer() else f"{o['prob']:.1f}".replace('.', ',') + "%"), font=f(ANTON, 72), fill=LIMA if o["prob"] == lider else BLANCO, anchor="lm")
    # pie
    yb = top + len(ops) * (alto + gap) + 10
    d.text((90, yb), datos.get("pregunta", ""), font=f(BARLOW_B, 50), fill=BLANCO)
    d.text((90, H - 60), "Fuente: " + datos.get("fuente", ""), font=f(BARLOW_SB, 30), fill=GRIS, anchor="lm")
    d.rounded_rectangle([W - 350, H - 120, W - 40, H - 30], 45, fill=NEGRO)
    import os; logo = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.jpg")).convert("RGB").resize((90, 90))
    mask = Image.new("L", (90, 90), 0); ImageDraw.Draw(mask).ellipse([0, 0, 89, 89], fill=255)
    img.paste(logo, (W - 330, H - 105), mask)
    d.text((W - 225, H - 60), "@holdcloudG21", font=f(BARLOW_B, 36), fill=BLANCO, anchor="lm")
    img.save(salida)

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
