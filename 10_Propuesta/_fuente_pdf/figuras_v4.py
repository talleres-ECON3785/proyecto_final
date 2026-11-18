# -*- coding: utf-8 -*-
"""Figuras del borrador de propuesta v4 (esquemas conceptuales; no contienen resultados).

Uso: python figuras_v4.py <carpeta_salida>
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle

from matplotlib import font_manager as _fm
for _f in (Path(__file__).parent / "fuentes").glob("Montserrat-*.ttf"):
    _fm.fontManager.addfont(str(_f))
plt.rcParams["font.family"] = ["Montserrat", "DejaVu Sans"]
plt.rcParams["mathtext.fontset"] = "stix"

AZUL = "#2E6B4F"
AZUL_C = "#EEF3EF"
ROJO_C = "#9DBFAE"
ROJO = "#16382B"
AMBAR_C = "#D9E6DD"
AMBAR = "#5E7A6B"
VERDE_C = "#F1F5F2"
GRIS_C = "#F8F9F8"
GRIS = "#666666"
TINTA = "#222222"

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "fig")
OUT.mkdir(parents=True, exist_ok=True)


def caja(ax, x, y, w, h, texto, fc=AZUL_C, ec=AZUL, fs=8.5, bold=False, color=TINTA, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.012,rounding_size=0.015",
                                fc=fc, ec=ec, lw=1.1, ls=ls))
    ax.text(x + w / 2, y + h / 2, texto, ha="center", va="center", fontsize=fs,
            fontweight="bold" if bold else "normal", color=color, wrap=True)


def flecha(ax, x0, y0, x1, y1, color=GRIS, ls="-"):
    ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                arrowprops=dict(arrowstyle="-|>", color=color, lw=1.1, ls=ls, shrinkA=2, shrinkB=2))


def lienzo(w, h):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(-0.02, 1.02)
    ax.set_ylim(-0.02, 1.02)
    ax.axis("off")
    return fig, ax


def guardar(fig, nombre):
    fig.savefig(OUT / nombre, dpi=220, bbox_inches="tight", facecolor="white")
    plt.close(fig)


# ---------------------------------------------------------------- 1. Olas
def fig_olas():
    fig, ax = lienzo(7.2, 2.6)
    ax.set_ylim(-0.05, 1.08)
    ax.add_patch(Rectangle((0.335, 0.53), 0.07, 0.14, fc=ROJO_C, ec="none"))
    ax.text(0.37, 0.50, "Crisis 1998 (IFLS2+ no es pública)", ha="center", va="top", fontsize=7.2, color=ROJO)
    ax.plot([0.04, 0.98], [0.6, 0.6], color=AZUL, lw=2)
    olas = [(0.08, "IFLS1 · 1993", "Tendencias previas", 0.80),
            (0.27, "IFLS2 · 1997", "Línea base y X (627\nhogares entrevistados en 1998)", 0.93),
            (0.48, "IFLS3 · 2000", "Precio post; ΔHAZ", 0.80),
            (0.70, "IFLS4 · 2007-08", "Cognición (secundaria)", 0.93),
            (0.91, "IFLS5 · 2014-15", "Escolaridad, estatura,\ncognición", 0.80)]
    for x, t, sub, ys in olas:
        ax.plot(x, 0.6, "o", color=AZUL, ms=8)
        ax.text(x, 0.67, t, ha="center", fontsize=8.3, fontweight="bold", color=AZUL)
        ax.text(x, ys, sub, ha="center", va="bottom", fontsize=7, color=GRIS)
    flecha(ax, 0.27, 0.27, 0.91, 0.27, color=TINTA)
    ax.text(0.59, 0.31, "Cohorte de 0-5 años en 1997 → 15-25 años en 2014 (ancla: ΔHAZ 1997-2000)",
            ha="center", fontsize=7.3)
    flecha(ax, 0.27, 0.05, 0.91, 0.05, color=TINTA)
    ax.text(0.59, 0.09, "Cohortes de 5-21 años en 1997 → 22-38 en 2014 (primario: escolaridad completada)",
            ha="center", fontsize=7.3)
    guardar(fig, "f1_olas.png")


# ---------------------------------------------------------------- 2. Mapa de evidencia
def fig_mapa():
    estudios = ["Elmira y\nQaim 2026", "Frankenberg\ny Thomas\n2017", "Frankenberg,\nSmith y\nThomas 2003",
                "Friedman y\nLevinsohn\n2002", "Friedman y\nThomas\n2009", "Este\nproyecto"]
    expos = ["Δ precio arroz\ncomunidad", "Zona y\ncohorte", "Choque gasto\nkecamatan",
             "Δ precios\nprovincia", "Δ gasto\nprovincia", "Δ precio\narroz"]
    resul = ["HAZ,\nestatura", "Escolaridad,\nHAZ", "Consumo", "Bienestar\nex ante", "Angustia\nadultos",
             "Escol., HAZ,\ncognición"]
    filas = ["Urbano", "Comprador neto /\nsin tierra", "Pobre\n(gasto bajo)", "Baja educación\n(madre o jefe)",
             "Edad temprana", "Sexo", "Sin oro\nni tierra", "Composición\ndel hogar"]
    R, A, G, B = "r", "a", "g", "b"
    celdas = [
        [(R, "Más daño\nen HAZ\n(p. 5)"), (A, "Escolaridad sí;\nHAZ no\n(p. 12; c. 3)"), (R, "Consumo cae\n5-15 pp más\n(p. 295)"),
         (R, "Pobres urb. 109 %\nvs. rurales 70 %\n(p. 408)"), (R, "Más angustia;\npendiente urbana\n(p. 72-74)"), (B, "H1")],
        [(G, "No\nevaluado"), (R, "Consumidores\nnetos golpeados\n(p. 6-7)"), (R, "Productores\nganan\n(p. 295)"),
         (R, "Sin producción\npropia: 130 %\n(p. 414)"), (R, "Sin tierra:\n+19 % tristeza\n(p. 71)"), (B, "H2")],
        [(A, "No pobres ≥\npobres, n.s.\n(p. 5)"), (A, "Escolaridad: pobres\nurb.; gasto: ricos\ncaen más (p. 8)"), (A, "Mejor situados\ncaen más en %\n(p. 295)"),
         (R, "Pobres urbanos,\npeor\n(p. 408)"), (G, "No\ncentral"), (B, "H3")],
        [(R, "Madre con\nprimaria o menos\n(p. 5)"), (G, "No\nevaluado"), (R, "Jefe educado\nsuaviza, rural\n(p. 313)"),
         (G, "No\nevaluado"), (R, "Más\nansiedad\n(p. 70)"), (B, "H4")],
        [(A, "2014: 3-5 años\ny gestación\n(asoc., p. 6)"), (A, "≤ 30 meses sin\ndaño; escol.:\n8 años (c. 3)"), (G, "No\nevaluado"),
         (G, "No\nevaluado"), (G, "Solo\nadultos"), (B, "H5")],
        [(R, "Niños más\nque niñas\n(p. 5)"), (A, "Sin diferencia\nen matrícula\n(p. 9)"), (G, "No\nevaluado"),
         (G, "No\nevaluado"), (A, "Mujeres más\nangustia\n(p. 69-70)"), (B, "H6")],
        [(G, "No\nevaluado"), (R, "Oro protegió\nsalud y educ.\n(p. 11)"), (R, "Oro y tierra\nsuavizan, solo\nrural (p. 316)"),
         (G, "No\nevaluado"), (R, "Tierra\namortigua\n(p. 71)"), (B, "H7")],
        [(G, "No\nevaluado"), (R, "Hermano mayor\nen escuela →\nmenor fuera (p. 9)"), (R, "Mujeres\nmayores suavizan\n(p. 313)"),
         (R, "Niños pequeños\n→ más exposición\n(p. 419)"), (G, "No\nevaluado"), (B, "H8")],
    ]
    col = {R: (ROJO_C, ROJO), A: (AMBAR_C, AMBAR), G: (GRIS_C, GRIS), B: (AZUL_C, AZUL)}
    nF = len(filas)
    anchos = [1, 1.12, 1, 1.05, 1, 0.55]
    fig, ax = plt.subplots(figsize=(8.0, 7.4))
    ax.axis("off")
    w0 = 0.15
    tot = sum(anchos); xs = [w0]
    for a in anchos:
        xs.append(xs[-1] + (1 - w0) * a / tot)
    hh = [0.085, 0.06, 0.06]
    top = 1 - sum(hh)
    hr = top / nF
    for j in range(len(anchos)):
        x, wc = xs[j], xs[j + 1] - xs[j]
        fc = AZUL if j == len(anchos) - 1 else "#16382B"
        ax.add_patch(Rectangle((x + 0.002, 1 - hh[0]), wc - 0.004, hh[0], fc=fc, ec="white"))
        ax.text(x + wc / 2, 1 - hh[0] / 2, estudios[j], ha="center", va="center", fontsize=6.3, color="white", fontweight="bold")
        ax.text(x + wc / 2, 1 - hh[0] - hh[1] / 2, expos[j], ha="center", va="center", fontsize=5.8, color=GRIS)
        ax.text(x + wc / 2, 1 - hh[0] - hh[1] - hh[2] / 2, resul[j], ha="center", va="center", fontsize=5.8, color=GRIS, style="italic")
    ax.text(w0 - 0.01, 1 - hh[0] - hh[1] / 2, "Exposición", ha="right", va="center", fontsize=6.3, color=GRIS)
    ax.text(w0 - 0.01, 1 - hh[0] - hh[1] - hh[2] / 2, "Resultado", ha="right", va="center", fontsize=6.3, color=GRIS)
    for i in range(nF):
        y = top - (i + 1) * hr
        ax.text(w0 - 0.01, y + hr / 2, filas[i], ha="right", va="center", fontsize=6.6, fontweight="bold")
        for j in range(len(anchos)):
            k, t = celdas[i][j]
            fc, ec = col[k]
            x, wc = xs[j], xs[j + 1] - xs[j]
            ax.add_patch(Rectangle((x + 0.002, y + 0.002), wc - 0.004, hr - 0.004, fc=fc, ec="white"))
            ax.text(x + wc / 2, y + hr / 2, t, ha="center", va="center", fontsize=5.6 if k != B else 8.5,
                    color=ec, fontweight="bold" if k == B else "normal", linespacing=1.15)
    ax.set_xlim(0, 1)
    ax.set_ylim(-0.05, 1)
    ley = [(ROJO_C, ROJO, "Más daño en el grupo de la fila"), (AMBAR_C, AMBAR, "Nulo, n.s., mixto o asociación"),
           (GRIS_C, GRIS, "No evaluado"), (AZUL_C, AZUL, "Hipótesis pre-declarada")]
    for k, (fc, ec, t) in enumerate(ley):
        xx = 0.03 + k * 0.245
        ax.add_patch(Rectangle((xx, -0.04), 0.018, 0.02, fc=fc, ec=ec))
        ax.text(xx + 0.024, -0.03, t, va="center", fontsize=6.2)
    guardar(fig, "f2_mapa_evidencia.png")


# ---------------------------------------------------------------- 3. Tres capas
def fig_capas():
    fig, ax = lienzo(7.2, 2.9)
    ax.text(0.265, 0.95, "Alza ALTA (tercil 3)", ha="center", fontsize=9, fontweight="bold", color=ROJO)
    ax.text(0.565, 0.95, "Alza BAJA (tercil 1)", ha="center", fontsize=9, fontweight="bold", color=AZUL)
    ax.text(0.04, 0.70, "Cohorte\nexpuesta", ha="center", va="center", fontsize=7.5)
    ax.text(0.04, 0.30, "Cohorte no\nexpuesta", ha="center", va="center", fontsize=7.5)
    caja(ax, 0.13, 0.55, 0.27, 0.30, "Compradores netos\n\nProductores", fc=ROJO_C, ec=ROJO)
    caja(ax, 0.43, 0.55, 0.27, 0.30, "Compradores netos\n\nProductores", fc=AZUL_C, ec=AZUL)
    caja(ax, 0.13, 0.15, 0.27, 0.25, "Cohorte mayor de la\nmisma comunidad", fc="white", ec=GRIS)
    caja(ax, 0.43, 0.15, 0.27, 0.25, "Cohorte mayor de la\nmisma comunidad", fc="white", ec=GRIS)
    flecha(ax, 0.40, 0.70, 0.43, 0.70, color=TINTA)
    flecha(ax, 0.265, 0.55, 0.265, 0.40, color=AMBAR)
    flecha(ax, 0.565, 0.55, 0.565, 0.40, color=AMBAR)
    ax.annotate("", xy=(0.35, 0.64), xytext=(0.35, 0.77), arrowprops=dict(arrowstyle="<->", color="#2E6B4F"))
    caja(ax, 0.74, 0.70, 0.26, 0.16, "1 · Entre comunidades\n(Elmira y Qaim)", fc="white", ec=TINTA, fs=7)
    caja(ax, 0.74, 0.45, 0.26, 0.18, "2 · Entre cohortes\n(F-T 2017; Maccini y Yang)", fc="white", ec=AMBAR, fs=7)
    caja(ax, 0.74, 0.20, 0.26, 0.18, "3 · Dentro de la comunidad:\ncomprador vs. productor\n(F-L; Yamauchi y Larson)", fc="white", ec="#2E6B4F", fs=7)
    ax.text(0.46, 0.03, "Capa 2 elimina lo fijo de la comunidad; capa 3 elimina todo choque común a la comunidad (sequía, humo, disturbios).",
            ha="center", fontsize=7, color=GRIS)
    guardar(fig, "f3_tres_capas.png")


# ---------------------------------------------------------------- 4. Flujo de inferencia
def fig_flujo():
    fig, ax = lienzo(7.4, 3.0)
    caja(ax, 0.00, 0.40, 0.19, 0.36, "IFLS 1993-2014\nExposición: alza del\nprecio del arroz\nCaracterísticas\nde 1997", fs=6.8)
    caja(ax, 0.23, 0.40, 0.20, 0.36, "Resultado en\ndiferencias:\ntalla 1997-2000;\nescolaridad frente a\ncohorte mayor", fs=6.8)
    caja(ax, 0.47, 0.40, 0.19, 0.36, "Bosque causal\nhonesto,\nagrupado por\ncomunidad", fc=AZUL, ec=AZUL, color="white", bold=True, fs=7)
    flecha(ax, 0.19, 0.58, 0.23, 0.58)
    flecha(ax, 0.43, 0.58, 0.47, 0.58)
    preguntas = [("1 · ¿Hay diferencias reales\nen el efecto?", 0.80), ("2 · ¿Quién sufre más?\nHipótesis H1-H8", 0.56),
                 ("3 · ¿Aparece el grupo de\n8 años sin buscarlo?", 0.32), ("4 · ¿A quién proteger primero?\nBosque vs. reglas simples", 0.08)]
    for t, y in preguntas:
        caja(ax, 0.71, y, 0.29, 0.15, t, fc="white", ec=AZUL, fs=6.8)
        flecha(ax, 0.66, 0.58, 0.71, y + 0.075)
    ax.text(0.0, 0.18, "Antes: pruebas de\ntendencias previas,\nbalance y placebos", fontsize=6.5, color=ROJO, va="center")
    guardar(fig, "f4_flujo.png")


# ---------------------------------------------------------------- 5. Honestidad por comunidad
def fig_honestidad():
    fig, ax = lienzo(7.0, 2.2)
    caja(ax, 0.00, 0.35, 0.20, 0.32, "Comunidades\ncompletas\n(commid97)", fc=GRIS_C, ec=GRIS, fs=7.5)
    caja(ax, 0.27, 0.60, 0.27, 0.32, "Mitad A\nrpart(score ~ X)\nelige los cortes", fc=AMBAR_C, ec=AMBAR, fs=7.5)
    caja(ax, 0.27, 0.06, 0.27, 0.32, "Mitad B\nfeols(score ~ 0 + hoja,\ncluster = ~commid97)", fc=AZUL_C, ec=AZUL, fs=7.5)
    caja(ax, 0.62, 0.35, 0.38, 0.32, "Efecto por hoja con IC válidos:\nlos datos que eligen el corte\nno son los que estiman el efecto", fc="white", ec=TINTA, fs=7.5)
    flecha(ax, 0.20, 0.55, 0.27, 0.75)
    flecha(ax, 0.20, 0.45, 0.27, 0.23)
    flecha(ax, 0.40, 0.60, 0.40, 0.38, color=AMBAR, ls="--")
    ax.text(0.415, 0.49, "estructura", fontsize=7, color=AMBAR)
    flecha(ax, 0.54, 0.23, 0.62, 0.48)
    guardar(fig, "f5_honestidad.png")


# ---------------------------------------------------------------- 6. TOC esquemática
def fig_toc():
    import numpy as np
    q = np.linspace(0.02, 1, 100)
    fig, ax = plt.subplots(figsize=(5.4, 2.7))
    ax.axhline(0, color=GRIS, lw=0.8)
    ax.plot(q, 0.9 * (1 - q) ** 1.6, color=AZUL, lw=2, label="Regla del bosque (−τ̂ de la mitad A)")
    ax.plot(q, 0.45 * (1 - q) ** 1.2, color=AMBAR, lw=2, ls="--", label="Regla simple: «pobre» o «urbano»")
    ax.plot(q, 0 * q, color=GRIS, lw=1.5, ls=":", label="Al azar")
    ax.fill_between(q, 0.45 * (1 - q) ** 1.2, 0.9 * (1 - q) ** 1.6, color=AZUL_C, alpha=0.6)
    ax.set_xlabel("Fracción priorizada (q)", fontsize=8)
    ax.set_ylabel("TOC(q): daño del grupo\npriorizado − daño promedio", fontsize=8)
    ax.text(0.42, 0.42, "Diferencia de RATE (AUTOC)\n= valor agregado del bosque", fontsize=7.5, color=AZUL)
    ax.set_yticks([])
    ax.tick_params(labelsize=7)
    for s in ["top", "right"]:
        ax.spines[s].set_visible(False)
    ax.legend(fontsize=7, frameon=False, loc="upper right")
    ax.set_title("Forma hipotética, no resultados", fontsize=8, color=ROJO, loc="left")
    guardar(fig, "f6_toc.png")


# ---------------------------------------------------------------- 7. Árbol esperado
def fig_arbol():
    fig, ax = lienzo(7.0, 3.0)
    caja(ax, 0.30, 0.80, 0.30, 0.15, "¿Hogar comprador neto\nde arroz en 1997? (H2)", fc="white", ec=TINTA, fs=7.6)
    caja(ax, 0.02, 0.47, 0.24, 0.17, "Hoja 1 · productor\nτ ≈ 0 o positivo", fc=VERDE_C, ec="#2E6B4F", fs=7.4)
    caja(ax, 0.42, 0.47, 0.20, 0.15, "¿Urbano? (H1)", fc="white", ec=TINTA, fs=7.6)
    caja(ax, 0.22, 0.08, 0.22, 0.17, "Hoja 2 · rural\ndaño moderado", fc=AMBAR_C, ec=AMBAR, fs=7.4)
    caja(ax, 0.52, 0.10, 0.26, 0.16, "¿Madre con primaria\no menos? (H4)", fc="white", ec=TINTA, fs=7.4)
    caja(ax, 0.84, 0.30, 0.15, 0.14, "Hoja 4\nmás daño", fc=ROJO_C, ec=ROJO, fs=7.2)
    caja(ax, 0.84, 0.00, 0.15, 0.14, "Hoja 3\ndaño moderado", fc=AMBAR_C, ec=AMBAR, fs=7.0)
    flecha(ax, 0.40, 0.80, 0.16, 0.64); ax.text(0.24, 0.74, "No", fontsize=7)
    flecha(ax, 0.50, 0.80, 0.52, 0.62); ax.text(0.52, 0.71, "Sí", fontsize=7)
    flecha(ax, 0.48, 0.47, 0.35, 0.25); ax.text(0.37, 0.38, "No", fontsize=7)
    flecha(ax, 0.56, 0.47, 0.64, 0.26); ax.text(0.62, 0.38, "Sí", fontsize=7)
    flecha(ax, 0.78, 0.22, 0.84, 0.35); ax.text(0.79, 0.31, "Sí", fontsize=7)
    flecha(ax, 0.78, 0.14, 0.84, 0.08); ax.text(0.79, 0.05, "No", fontsize=7)
    ax.text(0.70, 0.90, "Esquema de las hipótesis\nH1, H2 y H4. No son resultados.", fontsize=7, color=ROJO)
    guardar(fig, "f7_arbol.png")


if __name__ == "__main__":
    fig_olas(); fig_mapa(); fig_capas(); fig_flujo(); fig_honestidad(); fig_toc(); fig_arbol()
    print("figuras en", OUT)
