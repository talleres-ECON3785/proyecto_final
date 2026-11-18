# -*- coding: utf-8 -*-
# Hallmark v2.0.0 · redesign: full · genre: editorial · theme: grid (dealt 3/3) · medio: PDF 16:9 (ReportLab)
# critique: P4 H4 E4 S4 R4 V4 · weakest: E, la matriz de evidencia (cuerpo de 9 pt) es la única lámina con letra pequeña; se deja porque es referencia y no se lee en voz alta
# kept: todo el contenido y las cifras de la versión anterior; cambian el sistema y la composición
# dropped: ninguno · reworded: los títulos de las láminas 5 y 6 salen de partir en el punto y coma el título único de la matriz
"""Borrador de propuesta v4, formato consultor (16:9), rediseñado con la skill Hallmark (tema Grid).

Papel blanco, tinta azul-negra, campos planos de ultramarino y un solo rojo para lo elegido.
Todas las figuras son vectoriales y se dibujan aquí: no hay imágenes externas.

Uso: python construir_propuesta_consultor.py [salida.pdf]
Las fuentes (Radio Canada y Radio Canada Big, licencia OFL; Liberation Sans como respaldo de símbolos)
viven en la carpeta fuentes/ junto a este archivo.
"""
import math
import sys
from pathlib import Path

from reportlab.lib.colors import Color
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily, stringWidth
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph

SALIDA = sys.argv[1] if len(sys.argv) > 1 else "propuesta_presentacion.pdf"
FUENTES = Path(__file__).parent / "fuentes"

# ------------------------------------------------------------------ tokens
# Todo color sale de aquí, escrito en OKLCH como en el tema. Ningún literal de color más abajo.


def oklch(L, C, h):
    a, b = C * math.cos(math.radians(h)), C * math.sin(math.radians(h))
    l_, m_, s_ = L + 0.3963377774 * a + 0.2158037573 * b, L - 0.1055613458 * a - 0.0638541728 * b, L - 0.0894841775 * a - 1.2914855480 * b
    l, m, s = l_ ** 3, m_ ** 3, s_ ** 3
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s,
           -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)

    def g(v):
        v = max(0.0, min(1.0, v))
        return 12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055
    return Color(*[g(v) for v in rgb])


def luminancia(c):
    def f(v):
        return v / 12.92 if v <= 0.04045 else ((v + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(c.red) + 0.7152 * f(c.green) + 0.0722 * f(c.blue)


def contraste(a, b):
    la, lb = sorted([luminancia(a), luminancia(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)


T = {
    "paper": oklch(0.975, 0.005, 90), "paper2": oklch(0.942, 0.006, 90), "paper3": oklch(0.905, 0.008, 90),
    "ink": oklch(0.19, 0.022, 266), "ink2": oklch(0.31, 0.02, 266), "muted": oklch(0.47, 0.016, 266),
    "rule": oklch(0.80, 0.008, 90),
    "field": oklch(0.44, 0.20, 266), "field_ink": oklch(0.975, 0.005, 90), "field_dim": oklch(0.84, 0.07, 266),
    "tint": oklch(0.90, 0.045, 266), "tint2": oklch(0.82, 0.085, 266),
    "mark": oklch(0.55, 0.215, 29), "mark_ink": oklch(0.975, 0.005, 90),
}
INK, INK2, MUTED, PAPER, PAPER2, PAPER3 = T["ink"], T["ink2"], T["muted"], T["paper"], T["paper2"], T["paper3"]
FIELD, FIELD_INK, FIELD_DIM, MARK, MARK_INK, RULE, TINT, TINT2 = (T["field"], T["field_ink"], T["field_dim"], T["mark"],
                                                                    T["mark_ink"], T["rule"], T["tint"], T["tint2"])

# escala de espacio (pt) y rejilla de 12 columnas
SP = {"xs": 4, "sm": 8, "md": 16, "lg": 24, "xl": 40}
W, H = 960, 540
M = 48
NC, GUT = 12, 16
CW = (W - 2 * M - (NC - 1) * GUT) / NC


def cx(i):
    return M + i * (CW + GUT)


def span(n):
    return n * CW + (n - 1) * GUT


BOTTOM = 62  # límite inferior del contenido (el pie ocupa 0-48)

# ------------------------------------------------------------------ tipografía
for nombre, archivo in [("RCB7", "RCBig-700"), ("RCB4", "RCBig-400"), ("RC4", "RC-400"), ("RC5", "RC-500"),
                        ("RC6", "RC-600"), ("RC4i", "RC-400i"), ("FB", "LiberationSans-Regular"),
                        ("FBB", "LiberationSans-Bold")]:
    pdfmetrics.registerFont(TTFont(nombre, str(FUENTES / f"{archivo}.ttf")))
registerFontFamily("RC4", normal="RC4", bold="RC6", italic="RC4i", boldItalic="RC4i")
registerFontFamily("RC5", normal="RC5", bold="RC6", italic="RC4i", boldItalic="RC4i")
registerFontFamily("RC6", normal="RC6", bold="RC6", italic="RC4i", boldItalic="RC4i")
from fontTools.ttLib import TTFont as _FT
_cm = _FT(str(FUENTES / "RC-400.ttf")).getBestCmap()
SIN_GLIFO = lambda ch: ord(ch) not in _cm and ch not in "\n\r\t"

DISPLAY, DISPLAY_L, BODY, LABEL, BOLD = "RCB7", "RCB4", "RC4", "RC5", "RC6"


def fx(s):
    """Envuelve en la fuente de respaldo los símbolos que Radio Canada no trae (Δ, τ, ≈, ≥, →)."""
    return "".join(f'<font name="FB">{ch}</font>' if SIN_GLIFO(ch) else ch for ch in s)


def est(nombre, fuente=BODY, tam=13, lead=None, color=INK, **kw):
    kw.setdefault("alignment", TA_LEFT)
    return ParagraphStyle(nombre, fontName=fuente, fontSize=tam, leading=lead or round(tam * 1.42, 1),
                          textColor=color, **kw)


def para(c, html, x, y_top, w, estilo):
    p = Paragraph(fx(html), estilo)
    _, h = p.wrap(w, 2000)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def alto_para(html, w, estilo):
    p = Paragraph(fx(html), estilo)
    return p.wrap(w, 2000)[1]


# texto en canvas con seguimiento negativo (titulares) y respaldo de símbolos
def trk(tam):
    return -0.03 * tam


def ancho(s, fuente, tam, track=0.0):
    return sum(stringWidth(ch, "FB" if SIN_GLIFO(ch) else fuente, tam) for ch in s) + track * len(s)


def envolver(texto, fuente, tam, w, track=0.0):
    lineas, actual = [], ""
    for palabra in texto.split():
        prueba = (actual + " " + palabra).strip()
        if ancho(prueba, fuente, tam, track) <= w or not actual:
            actual = prueba
        else:
            lineas.append(actual)
            actual = palabra
    if actual:
        lineas.append(actual)
    return lineas


def texto(c, s, x, y, fuente, tam, color, track=0.0, ancla="l"):
    """Dibuja una línea; ancla l, r o c."""
    w = ancho(s, fuente, tam, track)
    x0 = x if ancla == "l" else (x - w if ancla == "r" else x - w / 2)
    c.setFillColor(color)
    cur = x0
    run, run_f = "", None
    def vaciar():
        nonlocal cur, run
        if run:
            c.saveState()  # el seguimiento (Tc) no debe filtrarse a los párrafos que se dibujan después
            t = c.beginText(cur, y)
            t.setFont(run_f, tam)
            t.setCharSpace(track)
            t.textOut(run)
            c.drawText(t)
            c.restoreState()
            cur += sum(stringWidth(ch, run_f, tam) for ch in run) + track * len(run)
            run = ""
    for ch in s:
        f = "FB" if SIN_GLIFO(ch) else fuente
        if f != run_f:
            vaciar()
            run_f = f
        run += ch
    vaciar()
    return w


def lineas_texto(c, lineas, x, y_top, fuente, tam, lead, color, track=0.0):
    y = y_top - tam * 0.86
    for ln in lineas:
        texto(c, ln, x, y, fuente, tam, color, track)
        y -= lead
    return y + lead - tam * 0.25


def titular(c, s, y_top=H - 38, w=None, tamanos=(28, 26, 24, 23, 22), max_lineas=2, color=INK, x=M):
    w = w or (W - 2 * M)
    for tam in tamanos:
        lns = envolver(s, DISPLAY, tam, w, trk(tam))
        if len(lns) <= max_lineas:
            break
    else:
        tam = tamanos[-1]
        lns = envolver(s, DISPLAY, tam, w, trk(tam))
    for ln in lns:
        assert not any(SIN_GLIFO(ch) for ch in ln), f"símbolo sin glifo en el titular: {ln}"
    return lineas_texto(c, lns, x, y_top, DISPLAY, tam, tam * 1.06, color, trk(tam))


# ------------------------------------------------------------------ estilos de cuerpo
S = {
    "cuerpo": est("cuerpo", BODY, 13.5, 19.5, INK),
    "cuerpo2": est("cuerpo2", BODY, 12.5, 17.5, INK2),
    "campo": est("campo", BODY, 13.5, 19.5, FIELD_INK),
    "etq": est("etq", LABEL, 12, 15, MUTED),
    "etq_campo": est("etq_campo", LABEL, 12, 15, FIELD_DIM),
    "nota": est("nota", BODY, 10.5, 13.5, MUTED),
    "nota_campo": est("nota_campo", BODY, 10.5, 13.5, FIELD_DIM),
    "tab": est("tab", BODY, 12, 15.5, INK),
    "tab_l": est("tab_l", BODY, 12.5, 16, INK),
    "tab_xl": est("tab_xl", BODY, 13.5, 18, INK),
    "tabh": est("tabh", LABEL, 11, 14, MUTED),
    "ref": est("ref", BODY, 10.8, 14, INK2),
    "lead": est("lead", DISPLAY, 17, 20, INK),
    "stm": est("stm", DISPLAY_L, 21, 27, INK),
    "stm_campo": est("stm_campo", DISPLAY_L, 21, 27, FIELD_INK),
}


# ------------------------------------------------------------------ marco de cada lámina
class Deck:
    def __init__(self):
        self.c = canvas.Canvas(SALIDA, pagesize=(W, H))
        self.c.setTitle("¿A quién golpeó más el arroz caro? Borrador de propuesta v4")
        self.c.setAuthor("Equipo proyecto final ECON-3785")
        self.c.setSubject("Presentación de consultoría, Ciencia de Datos y Econometría Aplicada (ECON-3785)")
        self.n = 0

    def nueva(self, fondo=PAPER):
        c = self.c
        if self.n:
            c.showPage()
        self.n += 1
        c.setFillColor(fondo)
        c.rect(0, 0, W, H, fill=1, stroke=0)
        return c

    def pie(self, seccion="", izq_campo=False, der_campo=False):
        c = self.c
        sq = FIELD_INK if izq_campo else MARK
        tinta = FIELD_INK if izq_campo else INK
        c.setFillColor(sq)
        c.rect(M, 18, 24, 24, fill=1, stroke=0)
        texto(c, "Proyecto final", M + 31, 32, DISPLAY, 10, tinta, -0.2)
        texto(c, "ECON-3785", M + 31, 20.5, DISPLAY_L, 10, tinta, -0.2)
        col = FIELD_DIM if izq_campo else MUTED
        if seccion:
            texto(c, seccion, cx(3), 26, LABEL, 11, col)
        texto(c, str(self.n), W - M, 26, LABEL, 11, FIELD_DIM if der_campo else MUTED, ancla="r")

    def campo(self, x0, y0, x1, y1, color=FIELD):
        self.c.setFillColor(color)
        self.c.rect(x0, y0, x1 - x0, y1 - y0, fill=1, stroke=0)

    def sobreimpresion(self, lineas, x, y_top, tam, lead, x_campo, track):
        """Titular que cambia de tinta a papel al cruzar el borde del campo (el efecto del tema)."""
        c = self.c
        for color, (cl, cr) in ((INK, (0, x_campo)), (FIELD_INK, (x_campo, W))):
            c.saveState()
            p = c.beginPath()
            p.rect(cl, 0, cr - cl, H)
            c.clipPath(p, stroke=0, fill=0)
            lineas_texto(c, lineas, x, y_top, DISPLAY, tam, lead, color, track)
            c.restoreState()


d = Deck()
c = d.c


def hair(c, x0, x1, y, color=RULE, w=0.7):
    c.setStrokeColor(color)
    c.setLineWidth(w)
    c.line(x0, y, x1, y)


def tabla(c, filas, anchos, x, y_top, cabecera=True, estilo="tab", pad=7, color_hair=RULE, tinta_codigo=None):
    """Tabla con filetes de 1 punto entre filas; sin fondos ni cajas. Devuelve la y inferior."""
    y = y_top
    for i, fila in enumerate(filas):
        es_cab = cabecera and i == 0
        ps = []
        for j, v in enumerate(fila):
            if es_cab:
                e = S["tabh"]
            elif tinta_codigo is not None and j == 0:
                e = est("cod", DISPLAY, 15, 17, tinta_codigo)
            else:
                e = S[estilo]
            ps.append(Paragraph(fx(v), e))
        hs = [p.wrap(a - 12, 1000)[1] for p, a in zip(ps, anchos)]
        h = max(hs) + 2 * pad
        xx = x
        for p, a in zip(ps, anchos):
            p.drawOn(c, xx + 0, y - pad - p.wrap(a - 12, 1000)[1])
            xx += a
        y -= h
        hair(c, x, x + sum(anchos), y, color_hair if not es_cab else MUTED, 0.7 if not es_cab else 0.9)
    return y


# ================================================================== 1. Portada
c = d.nueva()
XC = cx(6)
d.campo(XC, 0, W, H)
# nombre del proyecto (la marca del tema: dos líneas y un cuadrado rojo de la misma altura)
c.setFillColor(MARK)
c.rect(M, H - 62, 30, 30, fill=1, stroke=0)
texto(c, "Proyecto final", M + 38, H - 45, DISPLAY, 12.5, INK, -0.2)
texto(c, "ECON-3785", M + 38, H - 59, DISPLAY_L, 12.5, INK, -0.2)
texto(c, "Ciencia de Datos y Econometría Aplicada", cx(7), H - 45, LABEL, 13, FIELD_INK)
tam = 68
d.sobreimpresion(["¿A quién golpeó más", "el arroz caro?"], M, H - 168, tam, tam * 0.96, XC, -0.042 * tam)
yy = para(c, "Efectos heterogéneos de largo plazo de la crisis de 1997-98 en Indonesia, estimados con bosques causales honestos",
          M, 232, span(6) - 24, est("sub", BODY, 17, 23, INK))
para(c, "Propuesta para una agencia que focaliza ayuda ante choques de precios de alimentos", M, yy - SP["md"], span(6) - 24,
     est("cli", BODY, 13, 18, MUTED))
texto(c, "Borrador de propuesta", cx(7), 84, LABEL, 14, FIELD_INK)
texto(c, "versión 4, noviembre de 2026", cx(7), 64, BODY, 14, FIELD_DIM)

# ================================================================== 2. Resumen ejecutivo
c = d.nueva()
FB_TOP = 206  # tope del campo inferior
d.campo(0, 0, W, FB_TOP)
y = titular(c, "Una misma crisis, impactos opuestos: el arroz caro devastó a unos hogares y benefició a otros. "
               "Nadie ha medido con rigor a quién proteger primero", max_lineas=3, tamanos=(26, 24, 23, 22))
cifras = [("+83 %", "alza nominal media del arroz por comunidad, 1997-2000", "Elmira y Qaim (2026), cuadro 1", INK),
          ("109 / 70 %", "del gasto previo para compensar a pobres urbanos vs. rurales", "Friedman y Levinsohn (2002), p. 408", INK),
          ("~1/3", "de los hogares gastaba más en 1998 que en 1997", "Frankenberg, Smith y Thomas (2003), p. 295", INK),
          ("−1,95 años", "de escolaridad en una sola cohorte: urbanos pobres de 8 años", "Frankenberg y Thomas (2017), cuadro 3", MARK)]
fila_h = (y - FB_TOP - 28) / 2
for i, (n, t, f, col) in enumerate(cifras):
    gx = cx(0) if i % 2 == 0 else cx(6)
    gy = y - 14 - (i // 2) * fila_h
    texto(c, n, gx, gy - 38, DISPLAY, 40, col, trk(40))
    yy = para(c, t, gx + 236, gy - 6, span(6) - 236, est("ct", BODY, 13, 17, INK))
    para(c, f, gx + 236, yy - 3, span(6) - 236, S["nota"])
cols = [("La pregunta", "¿Quiénes cargaron, años después, con haber vivido donde el arroz subió más, y qué características de 1997 predicen un daño mayor?"),
        ("Qué aportamos", "Una prueba global de heterogeneidad, ocho hipótesis pre-declaradas y la verificación de si el subgrupo más citado de la literatura resiste un método honesto."),
        ("Para el cliente", "Una regla de priorización con variables observables y cuánto daño evita frente a «focalizar en pobres».")]
for i, (e, t) in enumerate(cols):
    x = cx(i * 4)
    yy = para(c, e, x, FB_TOP - 24, span(4), est("e2", BOLD, 13, 16, FIELD_INK))
    para(c, t, x, yy - 5, span(4) - 4, est("c2", BODY, 12.5, 17.5, FIELD_INK))
d.pie("Resumen ejecutivo", izq_campo=True, der_campo=True)

# ================================================================== separadores
AGENDA = ["Resumen ejecutivo", "Lo que se sabe y lo que falta", "Datos y estrategia empírica",
          "Heterogeneidad con bosques honestos", "Alcance, riesgos y plan"]


def separador(activo):
    c = d.nueva()
    XF = cx(5)
    d.campo(XF, 0, W, H)
    tam = 56
    lns = envolver(AGENDA[activo], DISPLAY, tam, span(7), -0.04 * tam)
    d.sobreimpresion(lns, M, H - 120, tam, tam * 0.98, XF, -0.04 * tam)
    y = 226
    for i, it in enumerate(AGENDA):
        if i == activo:
            c.setFillColor(FIELD_INK)
            c.rect(cx(7) - 20, y - 1, 10, 10, fill=1, stroke=0)
            texto(c, it, cx(7), y, BOLD, 16, FIELD_INK)
        else:
            texto(c, it, cx(7), y, BODY, 16, FIELD_DIM)
        y -= 30
    d.pie(der_campo=True)


separador(1)

# ================================================================== 4. ATE en disputa
c = d.nueva()
y = titular(c, "El efecto promedio es replicable pero está en disputa: un estudio halla daño en estatura y otro halla "
               "resiliencia, salvo en una cohorte")
tw = span(6)
tablas = [
    ("Elmira y Qaim (2026)", "Precio del arroz por comunidad",
     [["Resultado", "Efecto por +100 % de precio"], ["Talla-para-edad 1997-2000", "−0,135 DE (real: −0,251)"],
      ["Retraso en talla", "+3,5 pp"], ["Estatura adulta 2014", "−0,65 cm (asociación)"],
      ["Más daño en…", "urbanos, madres con primaria o menos, niños varones; pobreza n.s."]],
     "Panel con efectos fijos individuales, 312 comunidades (p. 1-6)."),
    ("Frankenberg y Thomas (2017)", "Zona y cohorte",
     [["Resultado", "Hallazgo"], ["Talla-para-edad", "Sin daño; los menores de 30 meses, más altos en 2000"],
      ["Escolaridad 2014, 7-12 años pobres", "+0,002 años (EE 0,17)"],
      ["Cohorte de 8 años, urbana, cuartil pobre", "−1,95 (0,63); −1,24 (0,69) con EF de hogar"],
      ["Mecanismos", "migración, venta de oro, protección de los hermanos mayores"]],
     "Sin precios: la zona urbana es el proxy del choque (p. 12; cuadro 3).")]
ys = y - SP["md"]
for i, (nom, sub, filas, nota) in enumerate(tablas):
    x = cx(0) if i == 0 else cx(6)
    texto(c, nom, x, ys - 15, DISPLAY, 17, INK, trk(17))
    texto(c, sub, x, ys - 33, BODY, 12.5, MUTED)
    yy = tabla(c, filas, [tw * 0.40, tw * 0.60], x, ys - 42, pad=5.5)
    para(c, nota, x, yy - 8, tw, S["nota"])
BAND = 136
d.campo(0, 0, W, BAND)
para(c, "<b>Implicación:</b> replicar primero el efecto de Elmira y Qaim valida el pipeline; aplicar la misma exposición a la escolaridad "
        "permite reconciliar ambos estudios. Un resultado nulo bien documentado también es un resultado.",
     cx(2), BAND - 20, span(9), est("imp", DISPLAY_L, 17.5, 23, FIELD_INK))
d.pie("Lo que se sabe", izq_campo=True, der_campo=True)

# ================================================================== 5. Mapa de evidencia
c = d.nueva()
y = titular(c, "La literatura halló la heterogeneidad a mano y una dimensión a la vez", tamanos=(28, 26, 24, 23))
estudios = ["Elmira y Qaim 2026", "Frankenberg y Thomas 2017", "Frankenberg, Smith y Thomas 2003", "Friedman y Levinsohn 2002",
            "Friedman y Thomas 2009", "Este proyecto"]
expos = ["Δ precio arroz comunidad", "Zona y cohorte", "Choque gasto kecamatan", "Δ precios provincia", "Δ gasto provincia",
         "Δ precio arroz"]
resul = ["HAZ, estatura", "Escolaridad, HAZ", "Consumo", "Bienestar ex ante", "Angustia adultos", "Escol., HAZ, cognición"]
filas = ["Urbano", "Comprador neto / sin tierra", "Pobre (gasto bajo)", "Baja educación (madre o jefe)", "Edad temprana", "Sexo",
         "Sin oro ni tierra", "Composición del hogar"]
Rr, A, G, B = "r", "a", "g", "b"
celdas = [
    [(Rr, "Más daño en HAZ (p. 5)"), (A, "Escolaridad sí; HAZ no (p. 12; c. 3)"), (Rr, "Consumo cae 5-15 pp más (p. 295)"),
     (Rr, "Pobres urb. 109 % vs. rurales 70 % (p. 408)"), (Rr, "Más angustia; pendiente urbana (p. 72-74)"), (B, "H1")],
    [(G, "No evaluado"), (Rr, "Consumidores netos golpeados (p. 6-7)"), (Rr, "Productores ganan (p. 295)"),
     (Rr, "Sin producción propia: 130 % (p. 414)"), (Rr, "Sin tierra: +19 % tristeza (p. 71)"), (B, "H2")],
    [(A, "No pobres ≥ pobres, n.s. (p. 5)"), (A, "Escolaridad: pobres urb.; gasto: ricos caen más (p. 8)"),
     (A, "Mejor situados caen más en % (p. 295)"), (Rr, "Pobres urbanos, peor (p. 408)"), (G, "No central"), (B, "H3")],
    [(Rr, "Madre con primaria o menos (p. 5)"), (G, "No evaluado"), (Rr, "Jefe educado suaviza, rural (p. 313)"),
     (G, "No evaluado"), (Rr, "Más ansiedad (p. 70)"), (B, "H4")],
    [(A, "2014: 3-5 años y gestación (asoc., p. 6)"), (A, "≤ 30 meses sin daño; escol.: 8 años (c. 3)"), (G, "No evaluado"),
     (G, "No evaluado"), (G, "Solo adultos"), (B, "H5")],
    [(Rr, "Niños más que niñas (p. 5)"), (A, "Sin diferencia en matrícula (p. 9)"), (G, "No evaluado"),
     (G, "No evaluado"), (A, "Mujeres más angustia (p. 69-70)"), (B, "H6")],
    [(G, "No evaluado"), (Rr, "Oro protegió salud y educ. (p. 11)"), (Rr, "Oro y tierra suavizan, solo rural (p. 316)"),
     (G, "No evaluado"), (Rr, "Tierra amortigua (p. 71)"), (B, "H7")],
    [(G, "No evaluado"), (Rr, "Hermano mayor en escuela → menor fuera (p. 9)"), (Rr, "Mujeres mayores suavizan (p. 313)"),
     (Rr, "Niños pequeños → más exposición (p. 419)"), (G, "No evaluado"), (B, "H8")],
]
rel = [1, 1.12, 1, 1.05, 1, 0.82]
RH_W = 104
cw_all = W - 2 * M - RH_W
colw = [cw_all * a / sum(rel) for a in rel]
xs = [M + RH_W]
for a in colw:
    xs.append(xs[-1] + a)
top = y - SP["md"]
hs = est("hs", DISPLAY, 11, 12.5, FIELD_INK)
he = est("he", BODY, 9.5, 11.5, MUTED)
alt_cab = 34
for j in range(6):
    fc = MARK if j == 5 else FIELD
    c.setFillColor(fc)
    c.rect(xs[j] + 1, top - alt_cab, colw[j] - 2, alt_cab, fill=1, stroke=0)
    p = Paragraph(estudios[j], est("hs%d" % j, DISPLAY, 10.5, 11.8, FIELD_INK if j < 5 else MARK_INK))
    hh = p.wrap(colw[j] - 12, 100)[1]
    p.drawOn(c, xs[j] + 7, top - alt_cab / 2 - hh / 2)
    para(c, fx(expos[j]) + "<br/>" + resul[j], xs[j] + 7, top - alt_cab - 4, colw[j] - 12, he)
alt_ex = 38
texto(c, "Exposición", xs[0] - 8, top - alt_cab - 13, LABEL, 10, MUTED, ancla="r")
texto(c, "Resultado", xs[0] - 8, top - alt_cab - 25, LABEL, 10, MUTED, ancla="r")
y0 = top - alt_cab - alt_ex - 4
RHT = 38.4
fills = {Rr: TINT2, A: PAPER3, G: PAPER}
for i, nom in enumerate(filas):
    yy = y0 - i * RHT
    p = Paragraph(nom, est("rh", BOLD, 10.5, 12, INK))
    hh = p.wrap(RH_W - 14, 100)[1]
    p.drawOn(c, M, yy - RHT / 2 - hh / 2)
    for j in range(6):
        k, t = celdas[i][j]
        c.setFillColor(MARK if k == B else fills[k])
        c.rect(xs[j] + 1, yy - RHT + 1.5, colw[j] - 2, RHT - 3, fill=1, stroke=0)
        if k == B:
            texto(c, t, xs[j] + colw[j] / 2, yy - RHT / 2 - 5, DISPLAY, 16, MARK_INK, ancla="c")
        else:
            est_c = est("cel", BODY, 9.2, 10.8, MUTED if k == G else INK)
            p = Paragraph(fx(t), est_c)
            hh = p.wrap(colw[j] - 14, 100)[1]
            p.drawOn(c, xs[j] + 7, yy - RHT / 2 - hh / 2)
ley = [(TINT2, "Más daño en el grupo de la fila"), (PAPER3, "Nulo, n.s., mixto o asociación"), (PAPER, "No evaluado"),
       (MARK, "Hipótesis pre-declarada")]
lx = M
for sw, t in ley:
    c.setFillColor(sw)
    c.rect(lx, 53, 11, 11, fill=1, stroke=0)
    if sw == PAPER:
        c.setStrokeColor(RULE)
        c.setLineWidth(0.7)
        c.rect(lx, 53, 11, 11, fill=0, stroke=1)
    w = texto(c, t, lx + 17, 55, BODY, 10.5, INK2)
    lx += 17 + w + 22
d.pie("Lo que se sabe")
texto(c, "Cada celda cita página o cuadro, cotejados con los PDF originales.", W - M - 40, 26, BODY, 10.5, MUTED, ancla="r")

# ================================================================== 6. Lectura de la matriz
c = d.nueva()
y = titular(c, "La posición en el mercado de arroz, los activos y la composición del hogar nunca se probaron sobre los niños")
lect = [("Urbano", "es lo más consistente, salvo en talla según Frankenberg y Thomas."),
        ("Pobreza y edad", "dan señales contradictorias según el resultado y la zona."),
        ("Comprador neto, oro y composición", "tienen buena teoría, pero no hay evidencia sobre los niños.")]
yy = y - SP["lg"]
for lead, txt in lect:
    h1 = alto_para(lead, span(4), est("l1", DISPLAY, 21, 24, INK))
    para(c, lead, cx(0), yy, span(4), est("l1", DISPLAY, 21, 24, INK))
    para(c, txt, cx(4), yy - 1, span(8), est("l2", BODY, 20, 27, INK2))
    yy -= max(h1, 74) + SP["md"]
    hair(c, cx(0), W - M, yy + 6)
    yy -= SP["xs"]
BAND = 150
d.campo(0, 0, W, BAND)
para(c, "Ningún estudio hace una prueba global ni corrige por todas las comparaciones.", cx(2), BAND - 28, span(9),
     est("imp", DISPLAY_L, 24, 30, FIELD_INK))
d.pie("Lo que se sabe", izq_campo=True, der_campo=True)

# ================================================================== 7. Vacíos
c = d.nueva()
y = titular(c, "Cinco vacíos concretos convierten el proyecto en un aporte, no en una replicación", tamanos=(28, 26, 24))
vac = [("V1", "Prueba global", "Nadie ha probado si la heterogeneidad es real o ruido.", "Calibración del bosque causal"),
       ("V2", "Comprador vs. productor", "Es el canal más claro, pero nunca se ha probado sobre los niños con el precio comunitario.", "Covariable + efecto por grupo + contraste dentro de la comunidad"),
       ("V3", "Mecanismos de suavización", "El oro, la tierra, los hermanos y las mujeres mayores protegieron el consumo. ¿Protegieron a los niños?", "Hipótesis H7-H8"),
       ("V4", "La cohorte de 8 años", "Una celda entre ~68 revisadas a mano.", "Prueba de recuperación + bosque placebo"),
       ("V5", "Reglas de focalización", "«Focalizar solo en pobres puede no bastar» (E-Q, p. 7), pero nadie lo ha probado.", "RATE: bosque vs. pobre / urbano / comprador")]
ya = y - SP["md"]
texto(c, "Cómo lo atacamos", cx(9), ya - 10, LABEL, 11.5, MUTED)
hair(c, cx(0), W - M, ya - 18, MUTED, 0.9)
ya -= 18
fh = (ya - BOTTOM + 6) / 5
for i, (k, t, q, a) in enumerate(vac):
    top_r = ya - i * fh
    texto(c, k, cx(0), top_r - 40, DISPLAY, 40, FIELD, trk(40))
    para(c, t, cx(2), top_r - 12, span(2) + 20, est("vt", DISPLAY, 15.5, 18, INK))
    para(c, q, cx(4) + 20, top_r - 12, span(5) - 20, est("vq", BODY, 13.5, 18.5, INK2))
    para(c, a, cx(9), top_r - 12, span(3), est("va", BOLD, 13, 17.5, INK))
    hair(c, cx(0), W - M, top_r - fh + 4)
d.pie("Lo que falta")

separador(2)

# ================================================================== 9. Datos
c = d.nueva()
y = titular(c, "La IFLS sigue a los mismos niños de 1997 a 2014: la escolaridad tiene tres veces más muestra que la estatura")
# línea de tiempo de las olas (vectorial)
tx0, tw_ = cx(0), span(8)
ty = y - 82
fr = [0.07, 0.27, 0.48, 0.70, 0.92]
olas = [("IFLS1", "1993", "Tendencias previas"), ("IFLS2", "1997", "Línea base y X (627 hogares entrevistados en 1998)"),
        ("IFLS3", "2000", "Precio post; ΔHAZ"), ("IFLS4", "2007-08", "Cognición (secundaria)"),
        ("IFLS5", "2014-15", "Escolaridad, estatura, cognición")]
xo = [tx0 + f * tw_ for f in fr]
c.setStrokeColor(INK)
c.setLineWidth(1.6)
c.line(tx0, ty, tx0 + tw_, ty)
c.setFillColor(MARK)
c.rect(xo[1], ty - 3.5, xo[2] - xo[1], 7, fill=1, stroke=0)
texto(c, "Crisis 1998 (IFLS2+ no es pública)", (xo[1] + xo[2]) / 2, ty - 76, BODY, 11, MARK, ancla="c")
for x, (nom, año, sub) in zip(xo, olas):
    c.setFillColor(FIELD)
    c.rect(x - 5, ty - 5, 10, 10, fill=1, stroke=0)
    texto(c, nom, x, ty + 26, DISPLAY, 14, INK, ancla="c")
    texto(c, año, x, ty + 11, LABEL, 11, MUTED, ancla="c")
    p = Paragraph(fx(sub), est("sb", BODY, 10.5, 12.5, MUTED, alignment=1))
    hh = p.wrap(118, 100)[1]
    p.drawOn(c, x - 59, ty - 14 - hh)
def flecha_h(c, x0, x1, y, color=INK):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(1.4)
    c.line(x0, y, x1 - 7, y)
    p = c.beginPath(); p.moveTo(x1, y); p.lineTo(x1 - 9, y + 4.5); p.lineTo(x1 - 9, y - 4.5); p.close()
    c.drawPath(p, fill=1, stroke=0)
yc = ty - 108
texto(c, "Cohorte de 0-5 años en 1997 → 15-25 años en 2014 (ancla: ΔHAZ 1997-2000)", xo[1], yc + 8, BODY, 11.5, INK)
flecha_h(c, xo[1], xo[4], yc)
yc2 = yc - 40
texto(c, "Cohortes de 5-21 años en 1997 → 22-38 en 2014 (primario: escolaridad completada)", xo[1], yc2 + 8, BODY, 11.5, INK)
flecha_h(c, xo[1], xo[4], yc2)
# tres cifras
kx = cx(9)
kw = span(3)
ky = y - 14
for i, (n, t) in enumerate([("7.925", "con escolaridad en 2014 (cohortes de 5-21 años en 1997)"),
                            ("2.586", "con talla en 2014 (cohorte de 0-5 años)"),
                            ("312", "comunidades con precio: unidad de tratamiento")]):
    yy = ky - i * 78
    texto(c, n, kx, yy - 30, DISPLAY, 34, FIELD if i == 0 else INK, trk(34))
    para(c, t, kx, yy - 38, kw, est("kt", BODY, 11.5, 14.5, INK2))
# tratamiento y covariables
py = ty - 190
c.setFillColor(PAPER2)
c.rect(0, BOTTOM - 18, W, py - BOTTOM + 14, fill=1, stroke=0)
txt1 = ("Precio del arroz por comunidad en 1997 y 2000, en dos construcciones: (a) mediana de las fuentes presentes en ambos años, calidad media y en kg; "
        "(b) réplica de Elmira y Qaim. El libro PKK de 2000 no tiene precios, y 27 comunidades tienen el de 1997 levantado en 1998.")
txt2 = ("Zona, educación de los padres, gasto (agregado propio), compra vs. producción propia de arroz (5.075 hogares compran y 1.511 producen), "
        "oro, tierra, composición del hogar y choques de sequía.")
yy = para(c, "Tratamiento", cx(0), py - 6, span(6), est("h3", DISPLAY, 15, 17, INK))
yy = para(c, txt1, cx(0), yy - 5, span(6), est("p3", BODY, 12, 16.5, INK2))
yy2 = para(c, "Covariables de 1997", cx(6), py - 6, span(6), est("h3", DISPLAY, 15, 17, INK))
yy2 = para(c, txt2, cx(6), yy2 - 5, span(6), est("p3", BODY, 12, 16.5, INK2))
para(c, "Fuente: revisión de las cinco olas (Datos/00_sintesis_revision_IFLS.md). Licencia RAND: los datos no se redistribuyen.",
     cx(0), min(yy, yy2) - 8, span(12), S["nota"])
d.pie("Datos")

# ================================================================== 10. Tres capas
c = d.nueva()
y = titular(c, "Identificamos más alza frente a menos alza, no el efecto de la crisis, y lo defendemos con tres capas de comparación")
gx0 = cx(0) + 98
bw, bh = 198, 92
gap = 24
ty0 = y - 34
texto(c, "Alza alta (tercil 3)", gx0, ty0, DISPLAY, 13.5, INK)
texto(c, "Alza baja (tercil 1)", gx0 + bw + gap, ty0, DISPLAY, 13.5, INK)
texto(c, "Cohorte", cx(0), ty0 - 44, LABEL, 12, MUTED)
texto(c, "expuesta", cx(0), ty0 - 58, LABEL, 12, MUTED)
texto(c, "Cohorte no", cx(0), ty0 - 150, LABEL, 12, MUTED)
texto(c, "expuesta", cx(0), ty0 - 164, LABEL, 12, MUTED)
by = ty0 - 12
for j, (fill, ink_) in enumerate([(FIELD, FIELD_INK), (TINT2, INK)]):
    bx = gx0 + j * (bw + gap)
    c.setFillColor(fill)
    c.rect(bx, by - bh, bw, bh, fill=1, stroke=0)
    texto(c, "Compradores netos", bx + 14, by - 30, LABEL, 13, ink_)
    hair(c, bx + 14, bx + bw - 50, by - bh / 2, ink_, 0.5)
    texto(c, "Productores", bx + 14, by - 70, LABEL, 13, ink_)
    c.setFillColor(PAPER2)
    c.rect(bx, by - bh - 62 - 74, bw, 74, fill=1, stroke=0)
    para(c, "Cohorte mayor de la misma comunidad", bx + 14, by - bh - 62 - 14, bw - 28, est("cm", LABEL, 12.5, 15.5, INK))
def marca_num(c, x, y, n):
    c.setFillColor(INK)
    c.rect(x - 9, y - 9, 18, 18, fill=1, stroke=0)
    texto(c, str(n), x, y - 4.2, DISPLAY, 12, PAPER, ancla="c")
def flecha_v(c, x, y0, y1, color=INK):
    c.setStrokeColor(color); c.setFillColor(color); c.setLineWidth(1.4)
    c.line(x, y0, x, y1 + 7)
    p = c.beginPath(); p.moveTo(x, y1); p.lineTo(x - 4.5, y1 + 9); p.lineTo(x + 4.5, y1 + 9); p.close()
    c.drawPath(p, fill=1, stroke=0)
# capa 1: entre comunidades
flecha_h(c, gx0 + bw + 2, gx0 + bw + gap - 2, by - 28, INK)
marca_num(c, gx0 + bw + gap / 2, by - 54, 1)
# capa 2: entre cohortes
for j in range(2):
    xx = gx0 + j * (bw + gap) + bw / 2
    flecha_v(c, xx, by - bh - 4, by - bh - 58)
marca_num(c, gx0 + bw / 2 + 24, by - bh - 31, 2)
# capa 3: dentro de la comunidad
c.setStrokeColor(MARK_INK)
marca_num(c, gx0 + bw - 30, by - bh / 2, 3)
# etiquetas a la derecha
lx = cx(8) + 8
lw = W - M - lx
capas = [("1", "Entre comunidades", "Elmira y Qaim"), ("2", "Entre cohortes", "F-T 2017; Maccini y Yang"),
         ("3", "Dentro de la comunidad: comprador vs. productor", "F-L; Yamauchi y Larson")]
cy = y - SP["md"]
for n_, t, f in capas:
    texto(c, n_, lx, cy - 32, DISPLAY, 34, FIELD, trk(34))
    yy = para(c, t, lx + 30, cy - 4, lw - 30, est("ct", DISPLAY, 14.5, 17, INK))
    para(c, f, lx + 30, yy - 2, lw - 30, est("cf", BODY, 12, 15, MUTED))
    cy -= 104
para(c, "Capa 2 elimina lo fijo de la comunidad; capa 3 elimina todo choque común a la comunidad (sequía, humo, disturbios).",
     cx(0), by - bh - 62 - 74 - 12, span(8), est("n1", BODY, 12, 16, INK2))
para(c, "Tratados: tercil alto de Δlog(precio) 1997-2000 por comunidad de 1997; controles: tercil bajo. Con dosis continua haría falta el "
        "supuesto de «tendencias paralelas fuertes» (Callaway, Goodman-Bacon y Sant'Anna).",
     cx(0), 118, span(8), S["nota"])
d.pie("Estrategia empírica")

# ================================================================== 11. Amenazas y pruebas previas
c = d.nueva()
XF = cx(6)
d.campo(XF, 0, W, H)
y = titular(c, "Las amenazas principales y las pruebas que corren antes de cualquier CATE", w=span(6) - 8, tamanos=(28, 26), max_lineas=4)
amenazas = ["Sequía de El Niño e incendios justo antes de la crisis (la producción de arroz cayó 4 % en 1997).",
            "La exposición se confunde con lo urbano.",
            "Programas focalizados (alimentación complementaria, becas).",
            "El precio de 2000 no es el pico de la crisis."]
pruebas = ["Tendencias previas 1993-97", "Prueba de Yamauchi y Larson", "Balance y traslape por tercil",
           "Desgaste hasta 2014 por tercil", "Placebos: adultos en 1997 y bosque placebo",
           "Sin Sumatra ni Kalimantan; dosis continua"]
yy = y - SP["lg"]
texto(c, "Amenazas principales", cx(0), yy - 14, DISPLAY, 19, INK, trk(19))
yy -= 28
hair(c, cx(0), XF - 24, yy, MUTED, 0.9)
for a in amenazas:
    h = alto_para(a, span(6) - 24, est("am", BODY, 14, 19, INK2))
    para(c, a, cx(0), yy - 9, span(6) - 24, est("am", BODY, 14, 19, INK2))
    yy -= h + 18
    hair(c, cx(0), XF - 24, yy)
yy = H - 62
texto(c, "Antes de cualquier CATE", XF + 28, yy - 14, DISPLAY, 19, FIELD_INK, trk(19))
yy -= 28
hair(c, XF + 28, W - M, yy, FIELD_DIM, 0.9)
for p_ in pruebas:
    h = alto_para(p_, span(5) - 8, est("pr", BODY, 14.5, 19, FIELD_INK))
    para(c, p_, XF + 28, yy - 9, span(5) - 8, est("pr", BODY, 14.5, 19, FIELD_INK))
    yy -= h + 18
    hair(c, XF + 28, W - M, yy, FIELD_DIM, 0.5)
d.pie("Estrategia empírica", der_campo=True)

separador(3)

# ================================================================== 13. Flujo del bosque
c = d.nueva()
y = titular(c, "Un bosque causal honesto, agrupado por comunidad, responde cuatro preguntas y termina en una priorización para el cliente")
fw = span(8)
bwid = (fw - 2 * 28) / 3
by_ = y - SP["lg"]
bh_ = 112
cajas = [("IFLS 1993-2014", "Exposición: alza del precio del arroz. Características de 1997.", PAPER3, INK),
         ("Resultado en diferencias", "Talla 1997-2000; escolaridad frente a cohorte mayor.", PAPER3, INK),
         ("Bosque causal honesto", "Agrupado por comunidad.", FIELD, FIELD_INK)]
for i, (a, b_, fc, tc) in enumerate(cajas):
    bx = cx(0) + i * (bwid + 28)
    c.setFillColor(fc)
    c.rect(bx, by_ - bh_, bwid, bh_, fill=1, stroke=0)
    yy = para(c, a, bx + 14, by_ - 14, bwid - 28, est("fa", DISPLAY, 15, 17.5, tc))
    para(c, b_, bx + 14, yy - 6, bwid - 28, est("fb", BODY, 12.5, 17, tc))
    if i < 2:
        flecha_h(c, bx + bwid + 4, bx + bwid + 26, by_ - bh_ / 2, INK)
texto_y = by_ - bh_ - 8
para(c, "Antes: pruebas de tendencias previas, balance y placebos.", cx(0), texto_y, span(5), est("an", BODY, 11.5, 15, MUTED))
preg = [("1", "¿Hay diferencias reales en el efecto?"), ("2", "¿Quién sufre más? Hipótesis H1-H8"),
        ("3", "¿Aparece el grupo de 8 años sin buscarlo?"), ("4", "¿A quién proteger primero? Bosque vs. reglas simples")]
py_ = texto_y - 38
# conector del bosque a la lista
c.setStrokeColor(FIELD)
c.setLineWidth(1.6)
bxf = cx(0) + 2 * (bwid + 28) + bwid / 2
c.line(bxf, by_ - bh_, bxf, py_ + 6)
rh = (py_ - BOTTOM) / 4 + 2
for i, (n_, q) in enumerate(preg):
    yy = py_ - i * rh
    texto(c, n_, cx(0), yy - 28, DISPLAY, 30, FIELD, trk(30))
    para(c, q, cx(0) + 40, yy - 6, fw - 40, est("pq", DISPLAY, 16, 19, INK))
    hair(c, cx(0), cx(0) + fw, yy - rh + 6)
# caja derecha
RX = cx(8) + 12
RW = W - M - RX
c.setFillColor(PAPER2)
c.rect(RX - 14, BOTTOM - 8, RW + 14 + M, y - BOTTOM - 4, fill=1, stroke=0)
yy = para(c, "Que el bosque herede el diseño", RX, y - 16, RW - 4, est("bh", DISPLAY, 16, 19, INK))
yy = para(c, "Un bosque compara en corte transversal. Por eso transformamos el resultado:", RX, yy - 8, RW - 4, est("bp", BODY, 12.5, 17.5, INK2))
for lead, t in [("Estatura:", "HAZ 2000 − HAZ 1997, equivalente a los efectos fijos individuales de Elmira y Qaim."),
                ("Escolaridad:", "años en 2014 − media de la cohorte no expuesta (22-30 años en 1997) de la misma comunidad."),
                ("Placebo:", "el mismo bosque solo con la cohorte no expuesta debe dar cero.")]:
    yy = para(c, f"<b>{lead}</b> {t}", RX, yy - 9, RW - 4, est("bp", BODY, 12.5, 17.5, INK2))
para(c, "grf (Laboratorio 10): causal_forest con clusters = commid97, test_calibration, rank_average_treatment_effect. "
        "Ampliaciones: get_scores, best_linear_projection.", RX, BOTTOM + 52, RW - 4, S["nota"])
d.pie("Heterogeneidad")

# ================================================================== 14. Hipótesis
c = d.nueva()
y = titular(c, "Nueve hipótesis declaradas antes de ver los datos, cada una con su fuente, limitan la búsqueda de subgrupos a posteriori")
filas_h = [["", "Modificador (1997)", "Predicción", "Base en la literatura"],
           ["H1", "Urbano", "Más daño urbano", "E-Q p. 5; F-L p. 408; en contra para talla: F-T 2017 p. 12"],
           ["H2", "Comprador neto de arroz", "Más daño; productores ≈ 0 o positivo", "F-L p. 414; FST p. 295; F-T 2017 p. 6-7"],
           ["H3", "Gasto per cápita", "Ambiguo: interactúa con la zona", "F-L p. 408; FST p. 295; E-Q p. 5"],
           ["H4", "Madre con primaria o menos", "Más daño", "E-Q p. 5; FST p. 313"],
           ["H5", "Edad en 1997", "Escolaridad: cerca de 8 años; talla: 3-5", "F-T 2017 cuadro 3; E-Q p. 6"],
           ["H6", "Sexo", "Sin predicción", "E-Q p. 5 vs. F-T 2017 p. 9"],
           ["H7", "Oro y tierra", "Menos daño, sobre todo rural", "FST p. 316-317; F-T 2017 p. 11"],
           ["H8", "Hermanos mayores; mujeres de 50+; niños menores de 5", "Más daño / menos / más", "F-T 2017 p. 9-10; FST p. 313; F-L p. 419"],
           ["H9", "Regla de focalización", "La regla del bosque supera a «pobre» y «urbano»", "E-Q p. 5 y 7"]]
yb = tabla(c, filas_h, [44, 270, 270, W - 2 * M - 584], M, y - SP["md"], estilo="tab_l", pad=5.6, tinta_codigo=FIELD)
para(c, "H1-H8: efectos por grupo con puntajes doblemente robustos (AIPW), errores agrupados por comunidad y corrección de Holm. τ &lt; 0 = daño.",
     M, yb - 9, W - 2 * M, S["nota"])
d.pie("Heterogeneidad")

# ================================================================== 15. Focalización (gráfica vectorial)
c = d.nueva()
y = titular(c, "El entregable: a quién proteger primero y cuánto daño evita esa priorización frente a focalizar en pobres")
ch_x, ch_w = cx(0) + 40, span(7) - 40
ch_top = y - 66
ch_h = ch_top - 118
texto(c, "Comparación de reglas de priorización", cx(0), y - 22, DISPLAY, 15, INK, trk(15))
texto(c, "Forma hipotética, no resultados", cx(0), y - 40, BODY, 11.5, MUTED)
qs = [i / 100 for i in range(2, 101)]
f1 = lambda q: 0.9 * (1 - q) ** 1.6
f2 = lambda q: 0.45 * (1 - q) ** 1.2
px = lambda q: ch_x + q * ch_w
py = lambda v: (ch_top - ch_h) + v / 0.95 * ch_h
# banda entre curvas
c.setFillColor(TINT)
p = c.beginPath()
p.moveTo(px(qs[0]), py(f2(qs[0])))
for q in qs:
    p.lineTo(px(q), py(f1(q)))
for q in reversed(qs):
    p.lineTo(px(q), py(f2(q)))
p.close()
c.drawPath(p, fill=1, stroke=0)
# ejes
c.setStrokeColor(MUTED); c.setLineWidth(0.9)
c.line(ch_x, py(0), ch_x + ch_w, py(0))
c.line(ch_x, py(0), ch_x, ch_top)
for k in range(6):
    q = k / 5
    c.line(px(q), py(0), px(q), py(0) - 4)
    texto(c, f"{q:.1f}".replace(".", ","), px(q), py(0) - 18, BODY, 10.5, MUTED, ancla="c")
texto(c, "Fracción priorizada (q)", ch_x + ch_w / 2, py(0) - 36, LABEL, 11.5, INK2, ancla="c")
c.saveState()
c.translate(ch_x - 18, (ch_top - ch_h) + ch_h / 2)
c.rotate(90)
texto(c, "TOC(q): daño del grupo priorizado − daño promedio", 0, 0, LABEL, 11, INK2, ancla="c")
c.restoreState()
def curva(f, color, w, dash=None):
    c.setStrokeColor(color); c.setLineWidth(w)
    c.setDash(*(dash or ([],)) if dash else [])
    p = c.beginPath()
    p.moveTo(px(qs[0]), py(f(qs[0])))
    for q in qs[1:]:
        p.lineTo(px(q), py(f(q)))
    c.drawPath(p, fill=0, stroke=1)
    c.setDash([])
curva(f1, FIELD, 3)
curva(f2, INK2, 2.2, [6, 4])
c.setStrokeColor(MUTED); c.setLineWidth(1.8); c.setDash([1.5, 3.5]); c.line(px(0.02), py(0), px(1), py(0)); c.setDash([])
leg_x = ch_x + ch_w * 0.50
leg_y = ch_top - 4
for k, (txt_, col, dash) in enumerate([("Regla del bosque (−τ̂ de la mitad A)", FIELD, None), ("Regla simple: «pobre» o «urbano»", INK2, [6, 4]),
                                       ("Al azar", MUTED, [1.5, 3.5])]):
    yy = leg_y - k * 18
    c.setStrokeColor(col); c.setLineWidth(2.4 if k == 0 else 2); c.setDash(dash or [])
    c.line(leg_x, yy - 3, leg_x + 28, yy - 3); c.setDash([])
    texto(c, txt_, leg_x + 36, yy - 7, BODY, 11, INK2)
texto(c, "Diferencia de RATE (AUTOC)", px(0.42), py(0.50), LABEL, 11.5, FIELD)
texto(c, "= valor agregado del bosque", px(0.42), py(0.50) - 15, BODY, 11.5, FIELD)
# texto de la derecha
RX = cx(7) + 28
RW = W - M - RX
c.setFillColor(PAPER2)
c.rect(RX - 20, BOTTOM - 10, RW + 20 + M, y - BOTTOM - 6, fill=1, stroke=0)
yy = para(c, "Cómo se construye", RX, y - 18, RW, est("cs", DISPLAY, 16, 19, INK))
for t in ["Entrenamos el bosque con la mitad de las comunidades y lo usamos para ordenar a los niños de la otra mitad, de mayor a menor daño esperado.",
          "Medimos cuánto más daño sufrió el 10 %, 20 % o 30 % priorizado que el promedio, y repetimos el ejercicio con las reglas que una agencia usaría sin el bosque: priorizar a los pobres, a los urbanos o a quienes compran arroz.",
          "Al cliente le entregamos esa comparación y el perfil de los hogares priorizados, descrito con características que puede observar."]:
    yy = para(c, t, RX, yy - 9, RW, est("cp", BODY, 12, 16.5, INK2))
para(c, "<i>Las curvas son un esquema de cómo se leerá el resultado, no resultados.</i>", RX, yy - 9, RW, est("cp", BODY, 12, 16.5, INK))
d.pie("Heterogeneidad")

separador(4)

# ================================================================== 17. Alcance y riesgos
c = d.nueva()
y = titular(c, "Alcance mínimo protegido: el resultado primario y el ancla no se recortan; el resto se ordena por prioridad")
cw2 = span(6)
yl = tabla(c, [["Papel", "Resultado"], ["Primario", "Escolaridad completada en 2014 (7.925 obs.)"],
               ["Ancla", "ΔHAZ 1997-2000: replicación de Elmira y Qaim"],
               ["Secundarios", "Estatura adulta y cognición 2014 (exploratorios)"],
               ["Extensión", "Salud mental de adultos 1993-2000, sin CATEs"]], [110, cw2 - 110], cx(0), y - SP["md"], estilo="tab_xl", pad=8)
tabla(c, [["Riesgo", "Mitigación"], ["~208 comunidades: poca potencia", "Calibración antes de interpretar; dosis continua con las 312"],
          ["Choques simultáneos", "Tres capas; placebos; sin Sumatra ni Kalimantan"],
          ["Medición del precio", "Fuentes comunes; versión réplica; indicadores de 1998"],
          ["Comparaciones múltiples", "Un primario; Holm sobre H1-H8"],
          ["Variables por construir", "Gasto y posición neta de 1997; índice de activos como respaldo"]],
      [176, cw2 - 176], cx(6), y - SP["md"], estilo="tab_xl", pad=8)
BAND = 124
d.campo(0, 0, W, BAND)
texto(c, "Recorte en orden", cx(0), BAND - 26, DISPLAY, 17, FIELD_INK, trk(17))
pasos = ["CES-D 2014", "salud mental de adultos", "cognición", "estatura adulta"]
xx = cx(0)
for i, t in enumerate(pasos):
    w = texto(c, t, xx, BAND - 62, DISPLAY_L, 20, FIELD_INK)
    xx += w + 14
    if i < 3:
        c.setFillColor(FIELD_DIM)
        pth = c.beginPath(); pth.moveTo(xx, BAND - 62 + 14); pth.lineTo(xx + 9, BAND - 62 + 9.5); pth.lineTo(xx, BAND - 62 + 5); pth.close()
        c.drawPath(pth, fill=1, stroke=0)
        xx += 9 + 14
d.pie("Alcance, riesgos y plan", izq_campo=True, der_campo=True)

# ================================================================== 18. Próximos pasos
c = d.nueva()
y = titular(c, "Próximos pasos: cuatro decisiones del equipo desbloquean la construcción de las bases")
cw2 = span(6) - 8
tabla(c, [["Decisión", "Recomendación"], ["Resultado primario", "Escolaridad completada en 2014"],
          ["Hipótesis", "Aprobar H1-H9 por escrito antes de correr el bosque"],
          ["Precio del arroz", "Principal (fuentes comunes) + réplica de Elmira y Qaim"],
          ["Cliente", "Agencia de asistencia alimentaria (tipo PMA)"]], [150, cw2 - 150], cx(0), y - SP["lg"], estilo="tab_xl", pad=10)
tabla(c, [["Etapa", "Entregable", "Días"], ["Tratamiento", "Precio por comunidad, distribución, balance", "2-3"],
          ["Asesoría, semana 15", "Este documento + pruebas 1-5 de validez", ""],
          ["Bases", "Variables de 1997, ΔHAZ, escolaridad 2014", "4-6"],
          ["Estimación", "Réplica, bosque causal, grupo de 8 años, reglas", "3-4"],
          ["Semana 16", "Presentación de 20 min + README reproducible", ""]],
      [140, span(6) - 140 - 48, 48], cx(6) + 8, y - SP["lg"], estilo="tab_xl", pad=10)
d.pie("Alcance, riesgos y plan")

# ================================================================== 19. Referencias
c = d.nueva()
y = titular(c, "Referencias y alcance de la verificación")
refs = [
    "Athey, S., Tibshirani, J. y Wager, S. (2019). Generalized random forests. <i>Annals of Statistics</i>, 47(2), 1148-1178.",
    "Athey, S. y Wager, S. (2019). Estimating treatment effects with causal forests: An application. <i>Observational Studies</i>, 5, 36-51.",
    "Callaway, B., Goodman-Bacon, A. y Sant'Anna, P. H. C. Difference-in-differences with a continuous treatment. NBER WP 32117.",
    "Elmira, E. S. y Qaim, M. (2026). Macroeconomic shocks and long-term nutritional outcomes. <i>Global Food Security</i>, 48, 100900.",
    "Frankenberg, E., Smith, J. P. y Thomas, D. (2003). Economic shocks, wealth, and welfare. <i>Journal of Human Resources</i>, 38(2), 280-321.",
    "Frankenberg, E. y Thomas, D. (2017). Human capital and shocks. NBER Working Paper 23347.",
    "Friedman, J. y Levinsohn, J. (2002). The distributional impacts of Indonesia's financial crisis. <i>World Bank Economic Review</i>, 16(3), 397-423.",
    "Friedman, J. y Thomas, D. (2009). Psychological health before, during, and after an economic crisis. <i>WBER</i>, 23(1), 57-76.",
    "Giles, J. y Satriawan, E. (2015). Protecting child nutritional status in the aftermath of a financial crisis. <i>JDE</i>, 114, 97-106.",
    "Semenova, V. y Chernozhukov, V. (2021). Debiased machine learning of CATEs. <i>Econometrics Journal</i>, 24(2), 264-289.",
    "Thomas, D. et al. (2004). Education in a crisis. <i>Journal of Development Economics</i>, 74(1), 53-85.",
    "Wager, S. y Athey, S. (2018). Estimation and inference of heterogeneous treatment effects using random forests. <i>JASA</i>, 113(523), 1228-1242.",
    "Yadlowsky, S. et al. (2025). Evaluating treatment prioritization rules via rank-weighted average treatment effects. <i>JASA</i>, 120(549), 38-51.",
    "Yamauchi, F. y Larson, D. F. (2019). Long-term impacts of an unanticipated spike in food prices on child growth in Indonesia. <i>World Development</i>, 113, 330-343.",
]
cw2 = span(6)
ya = y - SP["md"]
yy = ya
for r in refs[:7]:
    yy = para(c, r, cx(0), yy, cw2, S["ref"]) - 7
yy = ya
for r in refs[7:]:
    yy = para(c, r, cx(6), yy, cw2, S["ref"]) - 7
BANDV = 112
c.setFillColor(PAPER2)
c.rect(0, BOTTOM - 8, W, BANDV, fill=1, stroke=0)
para(c, "<b>Verificación.</b> Las cifras de la literatura se cotejaron con los PDF de Elmira y Qaim, Frankenberg y Thomas, Frankenberg, Smith y "
        "Thomas, Friedman y Levinsohn, y Friedman y Thomas (páginas impresas). Giles y Satriawan, Thomas et al. y Yamauchi y Larson se citan "
        "sin PDF local. Los tamaños de muestra vienen de la revisión de los datos. Este borrador no contiene estimaciones propias. La "
        "ausencia de CATEs previos para este choque sale de una búsqueda acotada, sin Google Scholar.",
     cx(0), BOTTOM - 8 + BANDV - 14, W - 2 * M, est("ver", BODY, 11.8, 16, INK2))
d.pie("Anexo")

d.c.save()
print("PDF:", SALIDA, "páginas:", d.n)

# ------------------------------------------------------------------ comprobación de contraste (WCAG)
if "--contraste" in sys.argv:
    for nombre, a, b in [("ink/paper", INK, PAPER), ("ink2/paper", INK2, PAPER), ("muted/paper", MUTED, PAPER),
                         ("field_ink/field", FIELD_INK, FIELD), ("field_dim/field", FIELD_DIM, FIELD),
                         ("mark_ink/mark", MARK_INK, MARK), ("mark/paper", MARK, PAPER), ("ink/tint2", INK, TINT2),
                         ("muted/paper2", MUTED, PAPER2), ("muted/paper3", MUTED, PAPER3), ("ink2/paper2", INK2, PAPER2),
                         ("field/paper", FIELD, PAPER), ("mark/paper3", MARK, PAPER3), ("field_ink/mark", FIELD_INK, MARK)]:
        print(f"{nombre:18s} {contraste(a, b):5.2f}")
