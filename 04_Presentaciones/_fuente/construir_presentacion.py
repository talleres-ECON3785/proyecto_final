# =============================================================================
# Construye la presentación final a partir de la base editada a mano
# Proyecto final - ECON-3785 (2026-2)
#
# Toma 04_Presentaciones/_fuente/presentacion_base.pptx, aplica las
# correcciones de formato (sin cambiar cifras ni el número de láminas) y deja:
#   08_Entregables/presentacion_final.pptx
#   08_Entregables/presentacion_final.pdf        (LibreOffice, modo headless)
#   04_Presentaciones/_fuente/_render/laminaNN.png (una imagen por lámina)
# Al final revisa el PDF: textos montados entre sí, sobre imágenes o fuera de
# la página. Si encuentra alguno, lo imprime y termina con error.
#
# Uso (desde la raíz del repositorio):
#   python 04_Presentaciones/_fuente/construir_presentacion.py
# Requiere: python-pptx, pymupdf, pandas y LibreOffice (soffice).
# La base, el .pptx y el .pdf no se versionan (la portada de TIME tiene
# derechos de autor y el repositorio es público).
# =============================================================================

import copy
import shutil
import subprocess
from pathlib import Path

import pandas as pd
import pymupdf
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_CONNECTOR, MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.oxml.ns import qn
from pptx.util import Emu, Pt

RAIZ = Path(__file__).resolve().parents[2]
BASE = RAIZ / "04_Presentaciones/_fuente/presentacion_base.pptx"
SALIDA = RAIZ / "08_Entregables/presentacion_final.pptx"
RENDER = RAIZ / "04_Presentaciones/_fuente/_render"
CSV_ATE = RAIZ / "03_Resultados/Tablas/06_ate/ninos_ate_especificaciones.csv"

M = 914400  # EMU por pulgada; las posiciones se escriben en millones de EMU
def e(x):
    return Emu(int(round(x * 1_000_000)))

VERDE_OSCURO = RGBColor(0x17, 0x3B, 0x2F)
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)
GRIS_TEXTO = RGBColor(0x0B, 0x0B, 0x0B)

prs = Presentation(BASE)
L = list(prs.slides)


# -----------------------------------------------------------------------------
# Utilidades
# -----------------------------------------------------------------------------

def forma(lamina, nombre):
    for sh in lamina.shapes:
        if sh.name == nombre:
            return sh
    raise KeyError(f"No está la forma {nombre!r}")

def borrar(sh):
    sh._element.getparent().remove(sh._element)

def mover(sh, x=None, y=None, w=None, h=None):
    if x is not None: sh.left = e(x)
    if y is not None: sh.top = e(y)
    if w is not None: sh.width = e(w)
    if h is not None: sh.height = e(h)

def alinear(sh, al=PP_ALIGN.LEFT):
    for p in sh.text_frame.paragraphs:
        p.alignment = al

def tamano(sh, pt, solo_parrafo=None):
    for i, p in enumerate(sh.text_frame.paragraphs):
        if solo_parrafo is None or i == solo_parrafo:
            for r in p.runs:
                r.font.size = Pt(pt)

def color_texto(sh, rgb):
    for p in sh.text_frame.paragraphs:
        for r in p.runs:
            r.font.color.rgb = rgb

def sin_autoajuste(cuerpo_xml):
    """bodyPr sin autoajuste, con ajuste de línea; el tamaño lo fija el script."""
    body = cuerpo_xml.find(qn("a:bodyPr"))
    for hijo in list(body):
        if hijo.tag in (qn("a:spAutoFit"), qn("a:normAutofit"), qn("a:noAutofit")):
            body.remove(hijo)
    body.set("wrap", "square")
    return body

def relleno_de(sh):
    """Copia del primer relleno sólido de una forma (para reutilizar su color)."""
    sf = sh._element.spPr.find(qn("a:solidFill"))
    return copy.deepcopy(sf)

def caja(lamina, x, y, w, h, cuerpo_origen, relleno, anclaje="ctr", margen=0.18):
    """Rectángulo sin borde con el texto de otra forma dentro (estilo de la propuesta)."""
    r = lamina.shapes.add_shape(MSO_SHAPE.RECTANGLE, e(x), e(y), e(w), e(h))
    sppr = r._element.spPr
    for viejo in sppr.findall(qn("a:solidFill")):
        sppr.remove(viejo)
    sppr.insert(list(sppr).index(sppr.find(qn("a:prstGeom"))) + 1, copy.deepcopy(relleno))
    r.line.fill.background()
    r.shadow.inherit = False
    viejo = r._element.find(qn("p:txBody"))
    nuevo = copy.deepcopy(cuerpo_origen)
    r._element.replace(viejo, nuevo)
    body = sin_autoajuste(nuevo)
    body.set("anchor", anclaje)
    for lado in ("lIns", "rIns", "tIns", "bIns"):
        body.set(lado, str(int(margen * 1_000_000)))
    # estilo del tema del autoshape: sin él, el texto hereda el blanco del tema
    st = r._element.find(qn("p:style"))
    if st is not None:
        r._element.remove(st)
    return r

def cuadro_pie(lamina):
    """Cuadro verde oscuro del pie (como en las láminas 3 y 10)."""
    for sh in lamina.shapes:
        if sh.shape_type == 1 and abs(sh.left - e(0.548640)) < 20000 and abs(sh.top - e(6.382512)) < 20000:
            return sh
    r = lamina.shapes.add_shape(MSO_SHAPE.RECTANGLE, e(0.548640), e(6.382512),
                                e(0.310896), e(0.310896))
    r.fill.solid()
    r.fill.fore_color.rgb = VERDE_OSCURO
    r.line.fill.background()
    r.shadow.inherit = False
    return r

def titulo(lamina, nombre, pt=26, w=None, x=0.548640, y=0.32):
    sh = forma(lamina, nombre)
    alinear(sh)
    tamano(sh, pt)
    mover(sh, x=x, y=y, w=w)
    return sh

def imagen(lamina, nombre, y, alto):
    """Reubica una figura sin deformarla (conserva su proporción)."""
    sh = forma(lamina, nombre)
    prop = sh.width / sh.height
    mover(sh, y=y, h=alto, w=alto * prop)
    return sh

def desagrupar(lamina, grupo):
    """Saca los hijos de un grupo a la lámina, con sus coordenadas absolutas."""
    g = grupo._element
    xfrm = g.grpSpPr.find(qn("a:xfrm"))
    off, ext = xfrm.find(qn("a:off")), xfrm.find(qn("a:ext"))
    choff, chext = xfrm.find(qn("a:chOff")), xfrm.find(qn("a:chExt"))
    ox, oy, ex, ey = (int(off.get("x")), int(off.get("y")), int(ext.get("cx")), int(ext.get("cy")))
    cx0, cy0, cex, cey = (int(choff.get("x")), int(choff.get("y")), int(chext.get("cx")), int(chext.get("cy")))
    sx, sy = ex / cex, ey / cey
    arbol = g.getparent()
    hijos = [h for h in g if h.tag in (qn("p:sp"), qn("p:pic"), qn("p:grpSp"), qn("p:cxnSp"))]
    pos = arbol.index(g)
    for h in hijos:
        arbol.insert(pos, h)
        pos += 1
        hx = h.find(".//" + qn("a:xfrm"))
        o, x_ = hx.find(qn("a:off")), hx.find(qn("a:ext"))
        o.set("x", str(int(ox + (int(o.get("x")) - cx0) * sx)))
        o.set("y", str(int(oy + (int(o.get("y")) - cy0) * sy)))
        x_.set("cx", str(int(int(x_.get("cx")) * sx)))
        x_.set("cy", str(int(int(x_.get("cy")) * sy)))
    arbol.remove(g)


# -----------------------------------------------------------------------------
# Lámina 1: portada
# -----------------------------------------------------------------------------

s = L[0]
cab = forma(s, "TextBox 3")  # «Proyecto final» / «ECON-3785» en dos párrafos
p0, p1 = cab.text_frame.paragraphs[0], cab.text_frame.paragraphs[1]
r_nuevo = copy.deepcopy(p1.runs[0]._r)
r_nuevo.find(qn("a:t")).text = " · ECON-3785"
p0._p.append(r_nuevo)
p1._p.getparent().remove(p1._p)
mover(cab, x=0.548640, y=0.24, w=6.5)

tit = forma(s, "TextBox 4")
alinear(tit)
mover(tit, x=0.548640, y=0.66, w=7.25)

cli = forma(s, "TextBox 5")
pregunta = cli.text_frame.paragraphs[1]
for r in pregunta.runs:  # el texto viene partido en varios runs
    if "¿a" in r.text:
        r.text = r.text.replace("¿a", "¿A", 1)
        break
assert pregunta.text.startswith("¿A qué niños proteger primero")
alinear(cli)
mover(cli, x=0.548640, y=2.42, w=7.25)

portada = forma(s, "Picture 2")
alto_portada = 2.30
mover(portada, x=0.548640, y=3.95, h=alto_portada, w=alto_portada * portada.width / portada.height)
credito = s.shapes.add_textbox(e(0.548640), e(3.95 + alto_portada + 0.04), e(4.0), e(0.28))
credito.text_frame.word_wrap = True
credito.text_frame.margin_left = credito.text_frame.margin_right = 0
run = credito.text_frame.paragraphs[0].add_run()
# fecha leída en la propia portada («JANUARY 19, 1998»)
run.text = "Portada: TIME, 19 de enero de 1998"
run.font.size = Pt(10)
run.font.name = "Radio Canada"
run.font.color.rgb = RGBColor(0x52, 0x51, 0x4E)

# panel derecho: preguntas más arriba y nombres completos dentro del panel
x_panel = forma(s, "Rectangle 1").left / 1_000_000
for nombre, y in [("TextBox 7", 0.42)]:
    mover(forma(s, nombre), y=y)
for num, txt, y in [("TextBox 8", "TextBox 9", 1.12), ("TextBox 10", "TextBox 11", 2.12),
                    ("TextBox 12", "TextBox 13", 3.12)]:
    mover(forma(s, num), y=y)
    mover(forma(s, txt), y=y + 0.11)
nom = forma(s, "TextBox 6")
mover(nom, x=x_panel + 0.25, y=4.55, w=4.053535 - 0.50)
tamano(nom, 15, 0)
tamano(nom, 13, 1)

# -----------------------------------------------------------------------------
# Lámina 3: barras con bigotes de ±1,96 EE
# -----------------------------------------------------------------------------

s = L[2]
borrar(forma(s, "TextBox 3"))  # «Opción B · Barras: nosotros frente a E-Q»

ate = pd.read_csv(CSV_ATE)
fila = ate.loc[ate["especificacion"] == 4].iloc[0]
b_nos, ee_nos = float(fila["beta"]), float(fila["ee_agrupado"])
# Elmira y Qaim (2026): -0,135, EE robusto 0,041 (CLAUDE.md §5; nota de 06_ate)
b_eq, ee_eq = -0.135, 0.041
assert f"{b_nos:.3f}" == "-0.329", b_nos

x0 = 3.383280            # inicio de las barras (el cero)
ancho_max = 6.75         # el extremo del IC más alejado de cero ocupa esto
escala = ancho_max / max(abs(b_nos) + 1.96 * ee_nos, abs(b_eq) + 1.96 * ee_eq)

def barra_con_bigote(barra, etiqueta, b, ee, y_centro):
    mover(barra, x=x0, w=abs(b) * escala)
    lo, hi = abs(b) - 1.96 * ee, abs(b) + 1.96 * ee
    xa, xb = x0 + lo * escala, x0 + hi * escala
    for xi, yi, xf, yf in [(xa, y_centro, xb, y_centro),
                           (xa, y_centro - 0.16, xa, y_centro + 0.16),
                           (xb, y_centro - 0.16, xb, y_centro + 0.16)]:
        c = s.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, e(xi), e(yi), e(xf), e(yf))
        c.line.color.rgb = GRIS_TEXTO
        c.line.width = Pt(2)
    mover(etiqueta, x=xb + 0.12)

barra_con_bigote(forma(s, "Rectangle 7"), forma(s, "TextBox 8"), b_nos, ee_nos,
                 (1.920240 + 0.822960 / 2))
barra_con_bigote(forma(s, "Rectangle 10"), forma(s, "TextBox 11"), b_eq, ee_eq,
                 (3.520440 + 0.822960 / 2))
for nombre, txt in [("TextBox 6", "EE 0,139, agrupado por comunidad"),
                    ("TextBox 9", "EE 0,041, robusto sin agrupar")]:
    p = forma(s, nombre).text_frame.paragraphs[1]
    p.runs[0].text = txt
    for r in p.runs[1:]:
        r.text = ""
    tamano(forma(s, nombre), 14, 1)
mover(forma(s, "TextBox 12"), y=4.62)
mover(forma(s, "TextBox 13"), y=4.98)
nota = forma(s, "TextBox 12").text_frame.paragraphs[0]
nota.runs[-1].text = nota.runs[-1].text.rstrip() + " Bigotes: ±1,96 EE (IC al 95 %)."

s.notes_slide.notes_text_frame.text = (
    "Presentador 1 · 100 s\n\n"
    "Primera pregunta: ¿dolió? Para cada niño medimos cuánto cambió su talla para la "
    "edad entre 1997 y 2000 y lo comparamos con el alza del precio del arroz en su "
    "comunidad. Los errores se agrupan por comunidad, porque el alza se asigna por "
    "comunidad: el número efectivo de observaciones son 294 comunidades, no 2.421 niños.\n\n"
    "El resultado: donde el precio del arroz se dobló, los niños quedaron 0,33 "
    "desviaciones estándar por debajo de lo esperado para su edad, cerca de 1,7 "
    "centímetros. Es la especificación con controles de 1997, efectos fijos de provincia "
    "y el precio inicial. El error estándar es 0,139 y el intervalo al 95 % va de −0,60 "
    "a −0,06: son los bigotes de la barra verde.\n\n"
    "Elmira y Qaim estiman −0,135 con un error de 0,041. Ojo con la comparación: su error "
    "es robusto sin agrupar por comunidad; el nuestro está agrupado por comunidad, y por "
    "eso es más ancho. La dirección es la misma; nuestro efecto es de 1,6 a 2,5 veces el "
    "suyo según la especificación, y los intervalos se traslapan. Ellos miden el precio "
    "con fuentes distintas en cada año y no comparan dentro de provincia.\n\n"
    "Un matiz que retomamos al final: es un contraste entre comunidades con más y menos "
    "alza, no el efecto de la crisis, y el tamaño exacto es incierto."
)

# -----------------------------------------------------------------------------
# Láminas 2, 4, 6 y 8: título, figura de la izquierda y panel derecho
# -----------------------------------------------------------------------------

for i in (1, 3, 5, 7):
    titulo(L[i], "TextBox 6", pt=24, w=7.70)
    imagen(L[i], "Picture 7", y=1.36, alto=4.92)
    forma(L[i], "Picture 7").left = e(0.457200)

# lámina 2: grupos de onda -> rectángulos con el texto dentro
s = L[1]
grupos = [forma(s, n) for n in ("Grupo 14", "Grupo 15", "Grupo 16")]
relleno = relleno_de(next(h for h in grupos[0].shapes if h.shape_type == 1))
cuerpos = [copy.deepcopy(next(h for h in g.shapes if h.shape_type == 17)._element.txBody)
           for g in grupos]
for g in grupos:
    borrar(g)
for cuerpo, (y, h) in zip(cuerpos, [(0.42, 1.45), (2.02, 1.45), (3.62, 2.55)]):
    c = caja(s, 8.62, y, 3.40, h, cuerpo, relleno)
    for p in c.text_frame.paragraphs:
        for r in p.runs:
            if r.font.size and r.font.size.pt < 30:
                r.font.size = Pt(15)

# láminas 6 y 8: ondas sueltas + cuadros de texto -> rectángulos
def ondas_a_cajas(s, pares, extra=None):
    relleno = relleno_de(forma(s, pares[0][0]))
    cajas = []
    for (onda, texto), (y, h) in zip(pares, [(0.42, 1.80), (2.37, 1.80), (4.32, 1.80)]):
        cuerpo = copy.deepcopy(forma(s, texto)._element.txBody)
        borrar(forma(s, onda))
        borrar(forma(s, texto))
        cajas.append(caja(s, 8.62, y, 3.40, h, cuerpo, relleno))
    return cajas

ondas_a_cajas(L[5], [("Doble onda 11", "TextBox 8"), ("Doble onda 12", "TextBox 9"),
                     ("Doble onda 13", "TextBox 10")])
cajas8 = ondas_a_cajas(L[7], [("Doble onda 12", "TextBox 8"), ("Doble onda 13", "TextBox 9"),
                              ("Doble onda 14", "TextBox 10")])
# «834 niños, 98 comunidades de evaluación» pasa dentro del primer cuadro
suelto = forma(L[7], "TextBox 11")
p_nuevo = copy.deepcopy(suelto.text_frame.paragraphs[0]._p)
cajas8[0].text_frame._txBody.append(p_nuevo)
cajas8[0].text_frame.paragraphs[-1].alignment = PP_ALIGN.CENTER
for r in cajas8[0].text_frame.paragraphs[-1].runs:
    r.font.size = Pt(12)
    r.font.bold = False
    r.font.color.rgb = RGBColor(0x52, 0x51, 0x4E)
borrar(suelto)
for c in cajas8:
    for p in c.text_frame.paragraphs:
        for r in p.runs:
            if r.font.size and r.font.size.pt < 30 and r.font.size.pt > 12:
                r.font.size = Pt(15)

# lámina 4: tabla y textos del panel sin montarse
s = L[3]
tabla = forma(s, "Table 9")
mover(tabla, x=8.60, y=0.92)
tabla.table.columns[0].width = e(1.85)
tabla.table.columns[1].width = e(1.47)
for fila in tabla.table.rows:
    fila.height = e(0.36)
    for celda in fila.cells:
        for p in celda.text_frame.paragraphs:
            for r in p.runs:
                r.font.size = Pt(12)
mover(forma(s, "TextBox 8"), x=8.60, y=0.38)
txt4 = forma(s, "TextBox 10")
mover(txt4, x=8.60, y=3.95, w=3.32)
tamano(txt4, 15)
alinear(txt4)
mover(forma(s, "TextBox 11"), x=8.60, y=5.55, w=3.32)

# -----------------------------------------------------------------------------
# Lámina 5: tabla de las interacciones de E-Q
# -----------------------------------------------------------------------------

s = L[4]
t5 = titulo(s, "TextBox 5", pt=26, w=11.09)
t5.text_frame.paragraphs[0].runs[0].text = (
    "Ninguna de las cinco diferencias que estudian Elmira y Qaim se distingue de cero "
    "con nuestros datos")
for r in t5.text_frame.paragraphs[0].runs[1:]:
    r.text = ""
tab = forma(s, "Table 6")
mover(tab, x=0.548640, y=1.50)
for j, w in enumerate([2.80, 1.95, 0.95, 2.15]):
    tab.table.columns[j].width = e(w)
for fila in tab.table.rows:
    fila.height = e(0.44)
    for celda in fila.cells:
        for p in celda.text_frame.paragraphs:
            for r in p.runs:
                r.font.size = Pt(14)
mover(forma(s, "TextBox 7"), x=0.548640, y=4.65, w=7.85)
for celda in tab.table.rows[0].cells:
    for p in celda.text_frame.paragraphs:
        for r in p.runs:
            r.font.size = Pt(13)
urb = forma(s, "TextBox 8")
mover(urb, x=8.70, y=1.50, w=3.00)
tamano(urb, 24, 1)

# -----------------------------------------------------------------------------
# Lámina 7: figura de GATE lo más grande posible, panel verde más angosto
# -----------------------------------------------------------------------------

s = L[6]
desagrupar(s, forma(s, "Grupo 11"))
ancho_panel = 3.15
mover(forma(s, "Rectangle 1"), w=ancho_panel)
for nombre, y in [("TextBox 8", 0.95), ("TextBox 9", 3.85)]:
    mover(forma(s, nombre), x=0.15, y=y, w=ancho_panel - 0.30)
tamano(forma(s, "TextBox 8"), 30, 1)
t7 = titulo(s, "TextBox 6", pt=26, x=ancho_panel + 0.30, w=12.192 - ancho_panel - 0.60)
gate = forma(s, "Picture 7")
alto = 6.30 - 1.00
mover(gate, y=1.00, h=alto, w=alto * gate.width / gate.height)
gate.left = e(ancho_panel + (12.192 - ancho_panel - gate.width / 1_000_000) / 2)
panel = forma(s, "Rectangle 1")._element
arbol = panel.getparent()
arbol.remove(panel)
arbol.insert(2, panel)  # detrás de todo (después de nvGrpSpPr y grpSpPr)
color_texto(forma(s, "TextBox 3"), BLANCO)
color_texto(forma(s, "TextBox 5"), RGBColor(0x89, 0x87, 0x81))

# -----------------------------------------------------------------------------
# Lámina 9: los tres cuadros a la misma altura
# -----------------------------------------------------------------------------

s = L[8]
titulo(s, "TextBox 5", pt=26, w=11.09)
for rect, txt in [("Rectangle 6", "TextBox 7"), ("Rectangle 8", "TextBox 9"),
                  ("Rectangle 10", "TextBox 11")]:
    mover(forma(s, rect), y=1.70, h=3.60)
    mover(forma(s, txt), y=1.70 + 0.27)

# -----------------------------------------------------------------------------
# Lámina 10: los seis límites en una cuadrícula 2 × 3
# -----------------------------------------------------------------------------

s = L[9]
titulo(s, "TextBox 5", pt=26, w=11.09)
pares = [("Rectangle 6", "TextBox 7"), ("Rectangle 8", "TextBox 9"),
         ("Rectangle 10", "TextBox 11"), ("Rectangle 12", "TextBox 13"),
         ("Rectangle 14", "TextBox 15"), ("Rectangle 16", "TextBox 17")]
columnas = [0.548640, 4.27, 7.99]
filas = [1.75, 3.95]
for k, (barra, texto) in enumerate(pares):
    x, y = columnas[k % 3], filas[k // 3]
    mover(forma(s, barra), x=x, y=y, h=1.85)
    mover(forma(s, texto), x=x + 0.27, y=y, w=3.25, h=1.85)

# -----------------------------------------------------------------------------
# Consistencia: títulos a la izquierda y cuadro verde del pie (salvo portada)
# -----------------------------------------------------------------------------

titulo(L[2], "TextBox 5", pt=26, w=11.09)
for s in L[1:]:
    cuadro_pie(s)

# -----------------------------------------------------------------------------
# Guardar, exportar a PDF y renderizar
# -----------------------------------------------------------------------------

SALIDA.parent.mkdir(exist_ok=True)
prs.save(SALIDA)
assert len(Presentation(SALIDA).slides) == 10

soffice = shutil.which("soffice") or r"C:\Program Files\LibreOffice\program\soffice.exe"
subprocess.run([soffice, "--headless", "--convert-to", "pdf", "--outdir",
                str(SALIDA.parent), str(SALIDA)], check=True, capture_output=True)
pdf = SALIDA.with_suffix(".pdf")

RENDER.mkdir(exist_ok=True)
doc = pymupdf.open(pdf)
for k, pagina in enumerate(doc, 1):
    pagina.get_pixmap(dpi=110).save(RENDER / f"lamina{k:02d}.png")

# -----------------------------------------------------------------------------
# Revisión automática: textos montados, sobre imágenes o fuera de la página
# -----------------------------------------------------------------------------

def area(r):
    return max(0, r.width) * max(0, r.height)

problemas = []
for k, pagina in enumerate(doc, 1):
    borde = pagina.rect
    lineas, imagenes = [], [pymupdf.Rect(i["bbox"]) for i in pagina.get_image_info()]
    for b_i, bloque in enumerate(pagina.get_text("dict")["blocks"]):
        for linea in bloque.get("lines", []):
            texto = "".join(sp["text"] for sp in linea["spans"]).strip()
            if texto:
                lineas.append((b_i, pymupdf.Rect(linea["bbox"]), texto))
    for b_i, r, t in lineas:
        if not borde.contains(r):
            problemas.append((k, "fuera de la página", t))
        for im in imagenes:
            if area(r & im) > 0.25 * area(r):
                problemas.append((k, "texto sobre imagen", t))
    for a in range(len(lineas)):
        for b in range(a + 1, len(lineas)):
            (ba, ra, ta), (bb, rb, tb) = lineas[a], lineas[b]
            if ba != bb and area(ra & rb) > 0.2 * min(area(ra), area(rb)):
                problemas.append((k, "textos montados", f"{ta!r} / {tb!r}"))

for p in problemas:
    print(f"Lámina {p[0]}: {p[1]}: {p[2]}")
print(f"{len(doc)} láminas; {len(problemas)} problemas de texto detectados.")
if problemas:
    raise SystemExit(1)
