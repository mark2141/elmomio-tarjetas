#!/usr/bin/env python3
"""Balance semanal de predicciones (1600x900).
Uso: python3 tarjeta_balance.py datos.json salida.png
datos.json: {"semana": "...", "predicciones": [{"partido": "...", "pick": "...", "prob": 62, "acierto": true}], "fuente": "...", "ejemplo": false}
"""
import json, sys
from PIL import Image, ImageDraw
from tarjeta_probabilidades import W, H, NEGRO, AZUL, LIMA, BLANCO, GRIS, ANTON, BARLOW_B, BARLOW_SB, f, franjas
ROJO = (255, 80, 80)

def render(datos, salida):
    img = Image.new("RGB", (W, H), NEGRO); d = ImageDraw.Draw(img)
    franjas(d); d.rectangle([0, 0, W, 10], fill=LIMA)
    preds = datos["predicciones"][:6]
    ok = sum(p["acierto"] for p in preds); tot = len(preds)
    d.text((90, 60), ("Balance semanal · " + datos.get("semana", "")).upper(), font=f(BARLOW_B, 38), fill=LIMA)
    d.text((90, 105), "MIS PREDICCIONES", font=f(ANTON, 76), fill=BLANCO)
    if datos.get("ejemplo"):
        d.text((W - 90, 70), "DATOS DE EJEMPLO", font=f(BARLOW_B, 32), fill=ROJO, anchor="ra")
    # marcador grande
    d.rounded_rectangle([1060, 240, 1420, 620], 24, fill=(28, 28, 34))
    d.text((1240, 330), f"{ok}/{tot}", font=f(ANTON, 130), fill=LIMA, anchor="mm")
    d.text((1240, 450), "ACIERTOS", font=f(BARLOW_B, 44), fill=BLANCO, anchor="mm")
    d.text((1240, 540), f"{(ok / tot * 100 if tot else 0):.0f}%", font=f(ANTON, 80), fill=BLANCO, anchor="mm")
    # lista
    y = 240
    for p in preds:
        col = LIMA if p["acierto"] else ROJO
        d.rounded_rectangle([90, y, 990, y + 56], 12, fill=(22, 22, 28))
        d.rectangle([90, y, 100, y + 56], fill=col)
        d.text((120, y + 28), p["partido"], font=f(BARLOW_B, 34), fill=BLANCO, anchor="lm")
        d.text((760, y + 28), f"{p['pick']} {p['prob']:.0f}%", font=f(BARLOW_SB, 30), fill=GRIS, anchor="rm")
        d.text((960, y + 28), "✓" if p["acierto"] else "✗", font=f("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 38), fill=col, anchor="rm")
        y += 66
    d.text((90, H - 60), "Fuente: " + datos.get("fuente", ""), font=f(BARLOW_SB, 30), fill=GRIS, anchor="lm")
    d.rounded_rectangle([W - 350, H - 120, W - 40, H - 30], 45, fill=NEGRO)
    import os
    logo = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "logo.jpg")).convert("RGB").resize((90, 90))
    mask = Image.new("L", (90, 90), 0); ImageDraw.Draw(mask).ellipse([0, 0, 89, 89], fill=255)
    img.paste(logo, (W - 330, H - 105), mask)
    d.text((W - 225, H - 60), "@holdcloudG21", font=f(BARLOW_B, 36), fill=BLANCO, anchor="lm")
    img.save(salida)

if __name__ == "__main__":
    render(json.load(open(sys.argv[1])), sys.argv[2])
