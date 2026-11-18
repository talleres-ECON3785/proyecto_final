# -*- coding: utf-8 -*-
"""Borrador de propuesta v4, formato consultor (16:9), inspirado en la línea gráfica de
Insumos/full-presentation-reference-JPMC.pdf: fondo claro, verde como único color, títulos de acción.

Uso: python figuras_v4.py <fig>; python construir_propuesta_consultor.py <fig> <salida.pdf>
"""
import sys
from pathlib import Path

from PIL import Image as PI
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.pdfmetrics import registerFontFamily
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph, Table, TableStyle

FIG = Path(sys.argv[1] if len(sys.argv) > 1 else "fig")
SALIDA = sys.argv[2] if len(sys.argv) > 2 else "propuesta_borrador.pdf"

L = "/usr/share/fonts/truetype/liberation/"
for n, f in [("S", "LiberationSans-Regular"), ("SB", "LiberationSans-Bold"), ("SI", "LiberationSans-Italic"),
             ("SBI", "LiberationSans-BoldItalic"), ("R", "LiberationSerif-Regular"), ("RI", "LiberationSerif-Italic"),
             ("RB", "LiberationSerif-Bold")]:
    pdfmetrics.registerFont(TTFont(n, L + f + ".ttf"))
registerFontFamily("S", normal="S", bold="SB", italic="SI", boldItalic="SBI")
registerFontFamily("R", normal="R", bold="RB", italic="RI", boldItalic="RI")

W, H = 960, 540
CAFE = colors.HexColor("#2E6B4F")
OSCURO = colors.HexColor("#16382B")
CREMA = colors.HexColor("#EEF3EF")
ARENA = colors.HexColor("#9DBFAE")
TINTA = colors.HexColor("#222222")
GRIS = colors.HexColor("#6E6E6E")
LINEA = colors.HexColor("#C3D3C9")
M = 42  # margen


def est(nombre, **kw):
    base = dict(fontName="S", fontSize=11, leading=14.5, textColor=TINTA, alignment=TA_LEFT)
    base.update(kw)
    return ParagraphStyle(nombre, **base)


S = {
    "accion": est("a", fontSize=19, leading=24),
    "cuerpo": est("c", fontSize=11, leading=15),
    "chico": est("ch", fontSize=10, leading=13.5),
    "nota": est("n", fontSize=7.5, leading=9.5, textColor=GRIS),
    "etq": est("e", fontName="SB", fontSize=9, leading=11, textColor=CAFE),
    "kpi": est("k", fontName="R", fontSize=34, leading=38, textColor=colors.white, alignment=TA_CENTER),
    "kpit": est("kt", fontName="RI", fontSize=11.5, leading=14, textColor=colors.white, alignment=TA_CENTER),
    "kpis": est("ks", fontSize=8, leading=10, textColor=colors.HexColor("#CFE0D6"), alignment=TA_CENTER),
    "tab": est("tb", fontSize=10.5, leading=13.5),
    "tabh": est("th", fontName="SB", fontSize=10.5, leading=13.5, textColor=colors.white),
    "ref": est("r", fontSize=8.2, leading=10.5),
}
B = lambda t: f'<font name="SB" color="#2E6B4F">{t}</font>'  # énfasis café, como en la referencia


def txt(c, html, x, y_top, w, st="cuerpo"):
    p = Paragraph(html, S[st] if isinstance(st, str) else st)
    _, h = p.wrap(w, 1000)
    p.drawOn(c, x, y_top - h)
    return y_top - h


def img(c, nombre, x, y_top, w=None, h=None):
    ruta = FIG / nombre
    iw, ih = PI.open(ruta).size
    if w is None:
        w = h * iw / ih
    if h is None:
        h = w * ih / iw
    c.drawImage(str(ruta), x, y_top - h, w, h, mask="auto")
    return y_top - h


class Deck:
    def __init__(self):
        self.c = canvas.Canvas(SALIDA, pagesize=(W, H))
        self.c.setTitle("¿A quién golpeó más el arroz caro? Borrador de propuesta v4")
        self.c.setAuthor("Equipo proyecto final ECON-3785")
        self.n = 0

    def nueva(self, accion, seccion=""):
        c = self.c
        if self.n:
            c.showPage()
        self.n += 1
        c.setFillColor(colors.white); c.rect(0, 0, W, H, fill=1, stroke=0)
        y = txt(c, accion, M, H - 30, W - 2 * M, "accion")
        c.setStrokeColor(CAFE); c.setLineWidth(1.2); c.line(M, y - 8, W - M, y - 8)
        c.setFont("RB", 9.5); c.setFillColor(OSCURO); c.drawString(M, 18, "Proyecto final ECON-3785")
        c.setFont("S", 8); c.setFillColor(GRIS)
        c.drawString(M + 120, 18, seccion)
        c.drawRightString(W - M, 18, str(self.n))
        return y - 22

    def separador(self, titulo, items, activo):
        c = self.c
        c.showPage(); self.n += 1
        c.setFillColor(CREMA); c.rect(0, 0, W, H, fill=1, stroke=0)
        c.setFillColor(CAFE); c.rect(0, 0, W, 62, fill=1, stroke=0)
        c.setFont("RB", 14); c.setFillColor(colors.white); c.drawString(M, 25, "Proyecto final ECON-3785")
        c.setFont("R", 46); c.setFillColor(OSCURO); c.drawString(300, 330, titulo)
        c.setStrokeColor(CAFE); c.setLineWidth(0.8); c.line(300, 312, W - M, 312)
        y = 285
        for i, it in enumerate(items):
            if i == activo:
                c.setFillColor(CAFE); p = c.beginPath(); p.moveTo(300, y - 1); p.lineTo(300, y + 9); p.lineTo(308, y + 4); p.close(); c.drawPath(p, fill=1, stroke=0)
                c.setFont("SB", 11); c.setFillColor(TINTA)
            else:
                c.setFont("S", 11); c.setFillColor(GRIS)
            c.drawString(316, y, it); y -= 20

    def guardar(self):
        self.c.save()


def tabla(c, filas, anchos, x, y_top, cab=True):
    datos = [[Paragraph(v, S["tabh"] if (i == 0 and cab) else S["tab"]) for v in f] for i, f in enumerate(filas)]
    t = Table(datos, colWidths=anchos)
    estilo = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LINEBELOW", (0, 0), (-1, -1), 0.4, LINEA),
              ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
              ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    if cab:
        estilo += [("BACKGROUND", (0, 0), (-1, 0), OSCURO)]
    t.setStyle(TableStyle(estilo))
    _, h = t.wrap(sum(anchos), 1000)
    t.drawOn(c, x, y_top - h)
    return y_top - h


def tile(c, x, y, w, h, numero, titulo, fuente, fondo=OSCURO):
    c.setFillColor(fondo); c.rect(x, y, w, h, fill=1, stroke=0)
    yy = txt(c, numero, x + 8, y + h - 18, w - 16, "kpi")
    yy = txt(c, titulo, x + 10, yy - 6, w - 20, "kpit")
    txt(c, fuente, x + 10, y + 26, w - 20, "kpis")


def caja(c, x, y, w, h, etiqueta, cuerpo, fondo=CREMA):
    c.setFillColor(fondo); c.rect(x, y, w, h, fill=1, stroke=0)
    c.setFillColor(CAFE); c.rect(x, y + h - 3, w, 3, fill=1, stroke=0)
    yy = txt(c, etiqueta.upper(), x + 12, y + h - 14, w - 24, "etq")
    txt(c, cuerpo, x + 12, yy - 6, w - 24, "chico")


AGENDA = ["Resumen ejecutivo", "Lo que se sabe y lo que falta", "Datos y estrategia empírica",
          "Heterogeneidad con bosques honestos", "Alcance, riesgos y plan"]

d = Deck()
c = d.c

# ---------------------------------------------------------------- Portada
d.n = 1
c.setFillColor(CREMA); c.rect(0, 0, W, H, fill=1, stroke=0)
c.setFillColor(CAFE); c.rect(0, 0, W, 62, fill=1, stroke=0)
c.setFont("RB", 14); c.setFillColor(colors.white); c.drawString(M, 25, "Proyecto final ECON-3785")
c.setFont("S", 10); c.drawRightString(W - M, 25, "Borrador de propuesta · versión 4 · noviembre de 2026")
c.setFont("R", 26); c.setFillColor(CAFE); c.drawRightString(W - M, 470, "Ciencia de Datos y Econometría Aplicada")
c.setStrokeColor(CAFE); c.line(W - M - 380, 458, W - M, 458)
c.setFont("R", 50); c.setFillColor(OSCURO)
c.drawString(M, 300, "¿A quién golpeó más")
c.drawString(M, 245, "el arroz caro?")
txt(c, "Efectos heterogéneos de largo plazo de la crisis de 1997-98 en Indonesia, "
       "estimados con bosques causales honestos", M, 210, 560,
    est("pt", fontName="RI", fontSize=16, leading=21, textColor=TINTA))
txt(c, "Propuesta para una agencia que focaliza ayuda ante choques de precios de alimentos", M, 150, 560,
    est("pt2", fontSize=11, textColor=GRIS))

# ---------------------------------------------------------------- 2. Resumen ejecutivo (hook)
y = d.nueva(f"Una misma crisis, impactos opuestos: el arroz caro {B('devastó a unos hogares y benefició a otros')}. "
            f"Nadie ha medido con rigor {B('a quién proteger primero')}", "Resumen ejecutivo")
tw, th, gap = 206, 182, 12
datos = [("+83 %", "alza nominal media del arroz por comunidad, 1997-2000", "Elmira y Qaim (2026), cuadro 1"),
         ("109 / 70 %", "del gasto previo para compensar a pobres urbanos vs. rurales", "Friedman y Levinsohn (2002), p. 408"),
         ("~1/3", "de los hogares gastaba más en 1998 que en 1997", "Frankenberg, Smith y Thomas (2003), p. 295"),
         ("−1,95 años", "de escolaridad en una sola cohorte: urbanos pobres de 8 años", "Frankenberg y Thomas (2017), cuadro 3")]
for i, (n, t, f) in enumerate(datos):
    tile(c, M + i * (tw + gap), y - th, tw, th, n, t, f, fondo=OSCURO if i != 3 else CAFE)
yb = y - th - 22
cols = [("La pregunta", "¿Quiénes cargaron, años después, con haber vivido donde el arroz subió más, y qué características de 1997 predicen un daño mayor?"),
        ("Qué aportamos", "Una prueba global de heterogeneidad, ocho hipótesis pre-declaradas y la verificación de si el subgrupo más citado de la literatura resiste un método honesto."),
        ("Para el cliente", "Una regla de priorización con variables observables y cuánto daño evita frente a «focalizar en pobres».")]
cw = (W - 2 * M - 2 * 16) / 3
for i, (e, t) in enumerate(cols):
    caja(c, M + i * (cw + 16), 60, cw, yb - 60, e, t)

# ---------------------------------------------------------------- Separador 1
d.separador("Contenido", AGENDA, 1)

# ---------------------------------------------------------------- 3. ATE en disputa
y = d.nueva(f"El efecto promedio {B('es replicable pero está en disputa')}: un estudio halla daño en estatura y otro "
            f"halla resiliencia, salvo en una cohorte", "Lo que se sabe")
cw = (W - 2 * M - 30) / 2
for i, (tit, filas, nota) in enumerate([
    ("Elmira y Qaim (2026) · precio del arroz por comunidad",
     [["Resultado", "Efecto por +100 % de precio"], ["Talla-para-edad 1997-2000", "−0,135 DE (real: −0,251)"],
      ["Retraso en talla", "+3,5 pp"], ["Estatura adulta 2014", "−0,65 cm (asociación)"],
      ["Más daño en…", "urbanos, madres con primaria o menos, niños varones; pobreza n.s."]],
     "Panel con efectos fijos individuales, 312 comunidades (p. 1-6)."),
    ("Frankenberg y Thomas (2017) · zona y cohorte",
     [["Resultado", "Hallazgo"], ["Talla-para-edad", "Sin daño; los menores de 30 meses, más altos en 2000"],
      ["Escolaridad 2014, 7-12 años pobres", "+0,002 años (EE 0,17)"],
      ["Cohorte de 8 años, urbana, cuartil pobre", "−1,95 (0,63); −1,24 (0,69) con EF de hogar"],
      ["Mecanismos", "migración, venta de oro, protección de los hermanos mayores"]],
     "Sin precios: la zona urbana es el proxy del choque (p. 12; cuadro 3).")]):
    x = M + i * (cw + 30)
    c.setFont("SB", 11.5); c.setFillColor(CAFE); c.drawString(x, y - 4, tit)
    yy = tabla(c, filas, [cw * 0.42, cw * 0.58], x, y - 16)
    txt(c, nota, x, yy - 8, cw, "nota")
c.setFillColor(CREMA); c.rect(M, 52, W - 2 * M, 54, fill=1, stroke=0)
txt(c, f"{B('Implicación:')} replicar primero el efecto de Elmira y Qaim valida el pipeline; aplicar la misma exposición a la escolaridad "
       "permite reconciliar ambos estudios. Un resultado nulo bien documentado también es un resultado.", M + 14, 96, W - 2 * M - 28)

# ---------------------------------------------------------------- 4. Mapa de evidencia
y = d.nueva(f"La literatura halló la heterogeneidad {B('a mano y una dimensión a la vez')}; la posición en el mercado de arroz, "
            f"los activos y la composición del hogar {B('nunca se probaron sobre los niños')}", "Lo que se sabe")
yi = img(c, "f2_mapa_evidencia.png", M, y + 4, h=y - 46)
xr = M + (y - 42) * 1414 / 1310 + 24
xr = max(xr, 560)
txt(c, "LECTURA", xr, y, W - M - xr, "etq")
yy = txt(c, f"• {B('Urbano')} es lo más consistente, salvo en talla según Frankenberg y Thomas.<br/><br/>"
            f"• {B('Pobreza y edad')} dan señales contradictorias según el resultado y la zona.<br/><br/>"
            f"• {B('Comprador neto, oro y composición')} tienen buena teoría, pero no hay evidencia sobre los niños.<br/><br/>"
            f"• Ningún estudio hace una prueba global ni corrige por todas las comparaciones.",
         xr, y - 16, W - M - xr, "chico")
txt(c, "Cada celda cita página o cuadro, cotejados con los PDF originales.", xr, 60, W - M - xr, "nota")

# ---------------------------------------------------------------- 5. Vacíos
y = d.nueva(f"Cinco vacíos concretos convierten el proyecto en {B('un aporte, no en una replicación')}", "Lo que falta")
vac = [("V1", "Prueba global", "Nadie ha probado si la heterogeneidad es real o ruido.", "Calibración del bosque causal"),
       ("V2", "Comprador vs. productor", "Es el canal más claro, pero nunca se ha probado sobre los niños con el precio comunitario.", "Covariable + efecto por grupo + contraste dentro de la comunidad"),
       ("V3", "Mecanismos de suavización", "El oro, la tierra, los hermanos y las mujeres mayores protegieron el consumo. ¿Protegieron a los niños?", "Hipótesis H7-H8"),
       ("V4", "La cohorte de 8 años", "Una celda entre ~68 revisadas a mano.", "Prueba de recuperación + bosque placebo"),
       ("V5", "Reglas de focalización", "«Focalizar solo en pobres puede no bastar» (E-Q, p. 7), pero nadie lo ha probado.", "RATE: bosque vs. pobre / urbano / comprador")]
cw = (W - 2 * M - 4 * 12) / 5
for i, (k, t, q, a) in enumerate(vac):
    x = M + i * (cw + 12)
    c.setFillColor(OSCURO); c.rect(x, y - 70, cw, 70, fill=1, stroke=0)
    c.setFont("R", 30); c.setFillColor(colors.white); c.drawString(x + 12, y - 40, k)
    txt(c, t, x + 12, y - 46, cw - 24, est("vt", fontName="SB", fontSize=10, textColor=colors.HexColor("#CFE0D6")))
    c.setFillColor(CREMA); c.rect(x, 70, cw, y - 70 - 70, fill=1, stroke=0)
    txt(c, q, x + 12, y - 84, cw - 24, "chico")
    c.setStrokeColor(CAFE); c.line(x + 12, 160, x + cw - 12, 160)
    txt(c, "CÓMO", x + 12, 152, cw - 24, "etq")
    txt(c, a, x + 12, 138, cw - 24, est("va", fontName="SB", fontSize=9.5, leading=12, textColor=TINTA))

# ---------------------------------------------------------------- Separador 2
d.separador("Contenido", AGENDA, 2)

# ---------------------------------------------------------------- 6. Datos
y = d.nueva(f"La IFLS sigue a los mismos niños de 1997 a 2014: {B('la escolaridad tiene tres veces más muestra')} "
            f"que la estatura", "Datos")
img(c, "f1_olas.png", M, y, w=560)
xr = 640
for i, (n, t) in enumerate([("7.925", "con escolaridad en 2014<br/>(cohortes de 5-21 años en 1997)"),
                            ("2.586", "con talla en 2014<br/>(cohorte de 0-5 años)"),
                            ("312", "comunidades con precio:<br/>unidad de tratamiento")]):
    yy = y - i * 105
    c.setFillColor(OSCURO if i == 0 else CREMA); c.rect(xr, yy - 92, W - M - xr, 92, fill=1, stroke=0)
    c.setFont("R", 34); c.setFillColor(colors.white if i == 0 else CAFE); c.drawString(xr + 16, yy - 46, n)
    txt(c, t, xr + 16, yy - 54, W - M - xr - 32, est(f"d{i}", fontSize=9.5, leading=12, textColor=colors.white if i == 0 else TINTA))
txt(c, f"{B('Tratamiento.')} Precio del arroz por comunidad en 1997 y 2000, en dos construcciones: (a) mediana de las fuentes presentes en "
       "ambos años, calidad media y en kg; (b) réplica de Elmira y Qaim. El libro PKK de 2000 no tiene precios, y 27 comunidades tienen el "
       f"de 1997 levantado en 1998.<br/>{B('Covariables de 1997.')} Zona, educación de los padres, gasto (agregado propio), compra vs. "
       "producción propia de arroz (5.075 hogares compran y 1.511 producen), oro, tierra, composición del hogar y choques de sequía.",
    M, 175, 570, "chico")
txt(c, "Fuente: revisión de las cinco olas (Datos/00_sintesis_revision_IFLS.md). Licencia RAND: los datos no se redistribuyen.", M, 52, 570, "nota")

# ---------------------------------------------------------------- 7. Estrategia
y = d.nueva(f"Identificamos {B('más alza frente a menos alza')}, no el efecto de la crisis, y lo defendemos con "
            f"{B('tres capas de comparación')}", "Estrategia empírica")
img(c, "f3_tres_capas.png", M, y, w=540)
xr = M + 570
caja(c, xr, y - 150, W - M - xr, 150, "Amenazas principales",
     "• Sequía de El Niño e incendios justo antes de la crisis (la producción de arroz cayó 4 % en 1997).<br/>"
     "• La exposición se confunde con lo urbano.<br/>• Programas focalizados (alimentación complementaria, becas).<br/>"
     "• El precio de 2000 no es el pico de la crisis.")
caja(c, xr, 60, W - M - xr, y - 170 - 60, "Antes de cualquier CATE",
     "• Tendencias previas 1993-97<br/>• Prueba de Yamauchi y Larson<br/>• Balance y traslape por tercil<br/>"
     "• Desgaste hasta 2014 por tercil<br/>• Placebos: adultos en 1997 y bosque placebo<br/>• Sin Sumatra ni Kalimantan; dosis continua")
txt(c, "Tratados: tercil alto de Δlog(precio) 1997-2000 por comunidad de 1997; controles: tercil bajo. Con dosis continua haría falta el "
       "supuesto de «tendencias paralelas fuertes» (Callaway, Goodman-Bacon y Sant'Anna).", M, 100, 540, "nota")

# ---------------------------------------------------------------- Separador 3
d.separador("Contenido", AGENDA, 3)

# ---------------------------------------------------------------- 8. Flujo bosque
y = d.nueva(f"Un bosque causal honesto, agrupado por comunidad, responde {B('cuatro preguntas')} y termina en "
            f"{B('una priorización para el cliente')}", "Heterogeneidad")
img(c, "f4_flujo.png", M, y, w=600)
xr = M + 625
caja(c, xr, 60, W - M - xr, y - 60, "Que el bosque herede el diseño",
     f"Un bosque compara en corte transversal. Por eso transformamos el resultado:<br/><br/>"
     f"{B('Estatura:')} HAZ 2000 − HAZ 1997, equivalente a los efectos fijos individuales de Elmira y Qaim.<br/><br/>"
     f"{B('Escolaridad:')} años en 2014 − media de la cohorte no expuesta (22-30 años en 1997) de la misma comunidad.<br/><br/>"
     f"{B('Placebo:')} el mismo bosque solo con la cohorte no expuesta debe dar cero.")
txt(c, "grf (Laboratorio 10): causal_forest con clusters = commid97, test_calibration, rank_average_treatment_effect. Ampliaciones: "
       "get_scores, best_linear_projection.", M, 62, 600, "nota")

# ---------------------------------------------------------------- 9. Hipótesis
y = d.nueva(f"Nueve hipótesis {B('declaradas antes de ver los datos')}, cada una con su fuente, limitan la búsqueda de "
            f"subgrupos a posteriori", "Heterogeneidad")
filas = [["", "Modificador (1997)", "Predicción", "Base en la literatura"],
         ["H1", "Urbano", "Más daño urbano", "E-Q p. 5; F-L p. 408 · en contra para talla: F-T 2017 p. 12"],
         ["H2", "Comprador neto de arroz", "Más daño; productores ≈ 0 o positivo", "F-L p. 414; FST p. 295; F-T 2017 p. 6-7"],
         ["H3", "Gasto per cápita", "Ambiguo: interactúa con la zona", "F-L p. 408; FST p. 295; E-Q p. 5"],
         ["H4", "Madre con primaria o menos", "Más daño", "E-Q p. 5; FST p. 313"],
         ["H5", "Edad en 1997", "Escolaridad: cerca de 8 años; talla: 3-5", "F-T 2017 cuadro 3; E-Q p. 6"],
         ["H6", "Sexo", "Sin predicción", "E-Q p. 5 vs. F-T 2017 p. 9"],
         ["H7", "Oro y tierra", "Menos daño, sobre todo rural", "FST p. 316-317; F-T 2017 p. 11"],
         ["H8", "Hermanos mayores; mujeres de 50+; niños menores de 5", "Más daño / menos / más", "F-T 2017 p. 9-10; FST p. 313; F-L p. 419"],
         ["H9", "Regla de focalización", "La regla del bosque supera a «pobre» y «urbano»", "E-Q p. 5 y 7"]]
tabla(c, filas, [36, 230, 250, W - 2 * M - 516], M, y)
txt(c, "H1-H8: efectos por grupo con puntajes doblemente robustos (AIPW), errores agrupados por comunidad y corrección de Holm. "
       "τ < 0 = daño.", M, 62, W - 2 * M, "nota")

# ---------------------------------------------------------------- 10. Focalización
y = d.nueva(f"El entregable: {B('a quién proteger primero')} y cuánto daño evita esa priorización frente a "
            f"focalizar en pobres", "Heterogeneidad")
cw = (W - 2 * M - 30) / 2
c.setFont("SB", 11); c.setFillColor(CAFE); c.drawString(M, y - 4, "Comparación de reglas de priorización")
img(c, "f6_toc.png", M, y - 14, w=cw)
caja(c, M + cw + 30, 60, cw, y - 60, "Cómo se construye",
     "Entrenamos el bosque con la mitad de las comunidades y lo usamos para ordenar a los niños de la otra mitad, de mayor a menor "
     "daño esperado.<br/><br/>Medimos cuánto más daño sufrió el 10 %, 20 % o 30 % priorizado que el promedio, y repetimos el ejercicio con "
     "las reglas que una agencia usaría sin el bosque: priorizar a los pobres, a los urbanos o a quienes compran arroz.<br/><br/>"
     "Al cliente le entregamos esa comparación y el perfil de los hogares priorizados, descrito con características que puede observar.<br/><br/>"
     "<i>Las curvas son un esquema de cómo se leerá el resultado, no resultados.</i>")

# ---------------------------------------------------------------- Separador 4
d.separador("Contenido", AGENDA, 4)

# ---------------------------------------------------------------- 11. Alcance y riesgos
y = d.nueva(f"Alcance mínimo {B('protegido')}: el resultado primario y el ancla no se recortan; el resto se ordena por "
            f"prioridad", "Alcance, riesgos y plan")
cw = (W - 2 * M - 30) / 2
tabla(c, [["Papel", "Resultado"], ["Primario", "Escolaridad completada en 2014 (7.925 obs.)"],
          ["Ancla", "ΔHAZ 1997-2000: replicación de Elmira y Qaim"],
          ["Secundarios", "Estatura adulta y cognición 2014 (exploratorios)"],
          ["Extensión", "Salud mental de adultos 1993-2000, sin CATEs"]], [90, cw - 90], M, y)
tabla(c, [["Riesgo", "Mitigación"], ["~208 comunidades: poca potencia", "Calibración antes de interpretar; dosis continua con las 312"],
          ["Choques simultáneos", "Tres capas; placebos; sin Sumatra ni Kalimantan"],
          ["Medición del precio", "Fuentes comunes; versión réplica; indicadores de 1998"],
          ["Comparaciones múltiples", "Un primario; Holm sobre H1-H8"],
          ["Variables por construir", "Gasto y posición neta de 1997; índice de activos como respaldo"]],
      [150, cw - 150], M + cw + 30, y)
txt(c, f"{B('Recorte en orden:')} CES-D 2014 → salud mental de adultos → cognición → estatura adulta.", M, 150, cw, "cuerpo")

# ---------------------------------------------------------------- 12. Plan y decisiones
y = d.nueva(f"Próximos pasos: {B('cuatro decisiones del equipo')} desbloquean la construcción de las bases", "Alcance, riesgos y plan")
cw = (W - 2 * M - 30) / 2
tabla(c, [["Decisión", "Recomendación"], ["Resultado primario", "Escolaridad completada en 2014"],
          ["Hipótesis", "Aprobar H1-H9 por escrito antes de correr el bosque"],
          ["Precio del arroz", "Principal (fuentes comunes) + réplica de Elmira y Qaim"],
          ["Cliente", "Agencia de asistencia alimentaria (tipo PMA)"]], [130, cw - 130], M, y)
tabla(c, [["Etapa", "Entregable", "Días"], ["Tratamiento", "Precio por comunidad, distribución, balance", "2-3"],
          ["Asesoría · semana 15", "Este documento + pruebas 1-5 de validez", "—"],
          ["Bases", "Variables de 1997, ΔHAZ, escolaridad 2014", "4-6"],
          ["Estimación", "Réplica, bosque causal, grupo de 8 años, reglas", "3-4"],
          ["Semana 16", "Presentación de 20 min + README reproducible", "—"]], [120, cw - 160, 40], M + cw + 30, y)

# ---------------------------------------------------------------- 13. Referencias
y = d.nueva("Referencias y alcance de la verificación", "Anexo")
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
cw = (W - 2 * M - 30) / 2
yy = y
for r in refs[:7]:
    yy = txt(c, r, M, yy, cw, "ref") - 5
yy = y
for r in refs[7:]:
    yy = txt(c, r, M + cw + 30, yy, cw, "ref") - 5
c.setFillColor(CREMA); c.rect(M, 52, W - 2 * M, 78, fill=1, stroke=0)
txt(c, f"{B('Verificación.')} Las cifras de la literatura se cotejaron con los PDF de Elmira y Qaim, Frankenberg y Thomas, Frankenberg, Smith y "
       "Thomas, Friedman y Levinsohn, y Friedman y Thomas (páginas impresas). Giles y Satriawan, Thomas et al. y Yamauchi y Larson se citan "
       "sin PDF local. Los tamaños de muestra vienen de la revisión de los datos. Este borrador no contiene estimaciones propias. La "
       "ausencia de CATEs previos para este choque sale de una búsqueda acotada, sin Google Scholar.", M + 14, 122, W - 2 * M - 28, "chico")

d.guardar()
print("PDF:", SALIDA, "páginas:", d.n)
