# =============================================================================
# Construye la presentación final DESDE CERO (16:9, 13,333 × 7,5 in)
# Proyecto final - ECON-3785 (2026-2)
#
# 13 láminas principales + separador «Respaldo» + 8 de respaldo. Figuras de
# 03_Resultados/Figuras/15_figuras_presentacion/ (script 15 del pipeline) y
# tablas nativas leídas de los .csv de 03_Resultados/. La única imagen externa
# es la portada de TIME, que se toma de la base local
# (04_Presentaciones/_fuente/presentacion_base.pptx; no se versiona).
#
# Salidas: 08_Entregables/presentacion_final.{pptx,pdf} y un PNG por lámina en
# 04_Presentaciones/_fuente/_render/. El script FALLA si: algún texto mide
# menos de 12 pt; algún texto tiene contraste < 4,5:1 con su fondo; no hay 13
# láminas principales; o el PDF tiene textos montados o fuera de la página.
#
# Uso (desde la raíz): python 04_Presentaciones/_fuente/construir_presentacion.py
# Requiere python-pptx, pandas, pymupdf y LibreOffice. Las fuentes Radio
# Canada se pasan a LibreOffice con un perfil temporal (no se instala nada).
# =============================================================================

import io
import shutil
import subprocess
import tempfile
from pathlib import Path

import pandas as pd
import pymupdf
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Inches, Pt

RAIZ = Path(__file__).resolve().parents[2]
FIG = RAIZ / "03_Resultados/Figuras"
TAB = RAIZ / "03_Resultados/Tablas"
BASE = RAIZ / "04_Presentaciones/_fuente/presentacion_base.pptx"
PORTADA = RAIZ / "04_Presentaciones/_fuente/portada_time.png"  # local, no se versiona
FUENTES = RAIZ / "10_Propuesta/_fuente_pdf/fuentes"
SALIDA = RAIZ / "08_Entregables/presentacion_final.pptx"
RENDER = RAIZ / "04_Presentaciones/_fuente/_render"

FONDO, VERDE, VERDE_OSC = "F8F9F8", "2E6B4F", "16382B"
TINTE, TEXTO, GRIS, BLANCO = "E3EDE7", "222222", "5E5E5E", "FFFFFF"
TITULO_F, CUERPO_F = "Radio Canada Big", "Radio Canada"
W, H = 13.333, 7.5

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(W), Inches(H)
VACIA = prs.slide_layouts[6]
textos = []  # (lámina, texto, color, fondo) para la prueba de contraste


def rgb(h):
    return RGBColor.from_string(h)

def coma(x, d=2):
    return f"{x:.{d}f}".replace(".", ",").replace("-", "−")


# -----------------------------------------------------------------------------
# Piezas
# -----------------------------------------------------------------------------

def lamina(seccion=None, notas=""):
    s = prs.slides.add_slide(VACIA)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = rgb(FONDO)
    s.notes_slide.notes_text_frame.text = notas
    s._seccion = seccion
    return s

def rect(s, x, y, w, h, color, forma=MSO_SHAPE.RECTANGLE):
    r = s.shapes.add_shape(forma, Inches(x), Inches(y), Inches(w), Inches(h))
    r.fill.solid()
    r.fill.fore_color.rgb = rgb(color)
    r.line.fill.background()
    estilo = r._element.find("{http://schemas.openxmlformats.org/presentationml/2006/main}style")
    if estilo is not None:  # sin el estilo del tema: ni sombra ni colores heredados
        r._element.remove(estilo)
    return r

def texto(s, x, y, w, h, parrafos, fondo=FONDO, anclaje=MSO_ANCHOR.TOP, forma=None,
          margen=0.05):
    """parrafos: lista de (texto, pt, negrita, color, fuente, alineación, espacio_antes, viñeta)."""
    caja = forma if forma is not None else s.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h))
    tf = caja.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anclaje
    for lado in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, lado, Inches(margen))
    for i, p in enumerate(parrafos):
        t, pt, neg, col, fuente, al, antes, vineta = (list(p) + [None] * 8)[:8]
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.alignment = al or PP_ALIGN.LEFT
        if antes:
            par.space_before = Pt(antes)
        if vineta:  # viñeta con sangría francesa de 0,25 in
            from lxml import etree
            pPr = par._p.get_or_add_pPr()
            pPr.set("marL", str(Inches(0.25)))
            pPr.set("indent", str(-Inches(0.25)))
            if vineta == "texto":  # viñeta escrita como texto: comparte línea base con la μ grande
                t = [("•\t", None)] + (t if isinstance(t, list) else [(t, None)])
            else:
                etree.SubElement(pPr, "{http://schemas.openxmlformats.org/drawingml/2006/main}buChar", char="•")
        # t puede ser una lista de (texto, estilo) con estilo "i" (cursiva), "b" (negrilla) o None
        for trozo, estilo in (t if isinstance(t, list) else [(t, None)]):
            r = par.add_run()
            r.text = trozo
            r.font.size = Pt(pt * 1.3 if estilo == "grande" else pt)  # "grande": cursiva más grande (la μ sale chica)
            negrita = bool(neg) or estilo == "b"
            r.font.bold = negrita
            r.font.italic = estilo in ("i", "grande")
            r.font.color.rgb = rgb(col or TEXTO)
            # Radio Canada no trae negrita: lo negrito va en Radio Canada Big Bold
            r.font.name = fuente or (TITULO_F if negrita else CUERPO_F)
            textos.append((len(prs.slides), trozo, col or TEXTO, fondo))
    return caja

CAJAS = []  # (lámina, x, y, w, h, color, margen) para auditar el relleno en el PDF

def caja_texto(s, x, y, w, h, color, parrafos, anclaje=MSO_ANCHOR.MIDDLE, margen=0.2):
    """Texto centrado en vertical y con el mismo margen a los cuatro lados; la altura de la
    caja se ajusta al texto (alto del texto + 2 × margen) para que el relleno sea simétrico."""
    CAJAS.append((len(prs.slides), x, y, w, h, color, margen))
    r = rect(s, x, y, w, h, color)
    caja = texto(s, 0, 0, 0, 0, parrafos, fondo=color, anclaje=anclaje, forma=r, margen=margen)
    if anclaje == MSO_ANCHOR.TOP:  # el interlineado ya deja ~0,07 in sobre la tinta
        caja.text_frame.margin_top = Inches(margen - 0.07)
    return caja

def titulo(s, t, y=0.32, h=1.15, w=W - 1.2):
    palabras = [p for p in t.split() if any(c.isalnum() for c in p)]  # «%» no es palabra
    assert len(palabras) <= 15, f"Título de más de 15 palabras: {t}"
    return texto(s, 0.6, y, w, h, [(t, 32, True, TEXTO, TITULO_F)], anclaje=MSO_ANCHOR.MIDDLE)

def figura(s, archivo, x, y, w):
    return s.shapes.add_picture(str(archivo), Inches(x), Inches(y), width=Inches(w))

COMO_LEER = []  # (lámina, texto): no se proyectan; van a 04_Presentaciones/como_leer_laminas.md

def como_leer(s, t, y=6.4):
    COMO_LEER.append((len(prs.slides), t))

OCRE_T = "8F6219"  # ocre oscuro para texto (el ocre de las figuras no llega a contraste 4,5:1)
Y_SUB, Y_FIG, GAP = 1.45, 2.01, 0.2  # subtítulo, figura y separación subtítulo-figura = figura-nota
Y_PIE = 7.05

def subtitulo(s, t):
    """Estimador y estrategia de identificación, en ocre y negrilla, más pequeño que el título."""
    return texto(s, 0.6, Y_SUB, W - 1.2, 0.4, [(t, 20, True, OCRE_T, TITULO_F)], anclaje=MSO_ANCHOR.MIDDLE)

def nota_metodo(s, y_figura_fin, t):
    """Detalles metodológicos bajo la figura, a la misma distancia que el subtítulo de arriba."""
    return texto(s, 0.6, y_figura_fin + GAP - 0.1, W - 1.2, Y_PIE - y_figura_fin, [("Método: " + t, 14, False, GRIS)])

def figura_metodo(s, archivo, sub, metodo, leer, x=None, w=9.0):
    """Subtítulo (estimador y estrategia), figura y nota de método; el «cómo leer» va al .md."""
    subtitulo(s, sub)
    pic = figura(s, archivo, (W - w) / 2 if x is None else x, Y_FIG, w)
    nota_metodo(s, Y_FIG + pic.height / 914400, metodo)
    como_leer(s, leer)
    return pic

def tabla(s, x, y, w, encabezado, filas, anchos, pt=16, alto_fila=0.45):
    n, m = len(filas) + 1, len(encabezado)
    grafo = s.shapes.add_table(n, m, Inches(x), Inches(y), Inches(w), Inches(alto_fila * n))
    t = grafo.table
    for j, a in enumerate(anchos):
        t.columns[j].width = Inches(a)
    for i, fila in enumerate([encabezado] + filas):
        for j, valor in enumerate(fila):
            c = t.cell(i, j)
            c.fill.solid()
            fondo = VERDE_OSC if i == 0 else (BLANCO if i % 2 else TINTE)
            c.fill.fore_color.rgb = rgb(fondo)
            col = BLANCO if i == 0 else TEXTO
            texto(s, 0, 0, 0, 0, [(str(valor), pt, i == 0, col, CUERPO_F,
                                   PP_ALIGN.LEFT if j == 0 else PP_ALIGN.RIGHT)],
                  fondo=fondo, forma=c, margen=0.08)
    return grafo

SECCIONES = ["Contexto", "Método", "Resultados", "Recomendación"]

def pie(s, numero):
    texto(s, 0.6, 7.05, 3.2, 0.32, [("Proyecto Final - ECON-3785", 12, False, GRIS)])
    caja = s.shapes.add_textbox(Inches(4.0), Inches(7.05), Inches(5.6), Inches(0.32))
    tf = caja.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.05)
    par = tf.paragraphs[0]
    par.alignment = PP_ALIGN.CENTER
    r = par.add_run()  # solo la sección actual: dice dónde vamos
    r.text = s._seccion or "Respaldo"
    r.font.size, r.font.name, r.font.bold = Pt(12), TITULO_F, True
    r.font.color.rgb = rgb(VERDE)
    textos.append((numero, r.text, VERDE, FONDO))
    texto(s, W - 1.6, 7.05, 1.0, 0.32, [(str(numero), 12, False, GRIS, None, PP_ALIGN.RIGHT)])


# -----------------------------------------------------------------------------
# Datos (todas las cifras de resultados salen de los .csv)
# -----------------------------------------------------------------------------

ate = pd.read_csv(TAB / "06_ate/ninos_ate_especificaciones.csv")
a4 = ate.loc[ate.especificacion == 4].iloc[0]
edad = pd.read_csv(TAB / "11_gate/ninos_gate.csv").set_index("id").loc["G1"]
assert coma(a4.beta) == "−0,33" and coma(a4.beta_cm, 1) == "−1,7"
assert coma(edad.gate_0) == "−0,31" and coma(edad.gate_1) == "−0,08"

def ecuacion_png(tex, pt=22):
    """Compila una fórmula con pdflatex y la devuelve como PNG recortado (BytesIO) y su tamaño en pulgadas.
    Sin las clases standalone/preview (no vienen en toda instalación): se recorta por la tinta."""
    import numpy as np
    from PIL import Image
    with tempfile.TemporaryDirectory() as d:
        fuente = Path(d) / "eq.tex"
        fuente.write_text(
            "\\documentclass{article}\n\\usepackage[paperwidth=40cm,paperheight=6cm,margin=1cm]{geometry}\n"
            "\\usepackage{amsmath,amssymb}\n\\pagestyle{empty}\n"
            f"\\begin{{document}}\\noindent\\fontsize{{{pt}}}{{{pt + 4}}}\\selectfont\n$\\displaystyle {tex}$\n"
            "\\end{document}\n", encoding="utf-8")
        subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "-output-directory", d,
                        str(fuente)], check=True, capture_output=True)
        pix = pymupdf.open(Path(d) / "eq.pdf")[0].get_pixmap(dpi=300)
        a = np.frombuffer(pix.samples, np.uint8).reshape(pix.height, pix.width, pix.n)[:, :, :3]
        ys, xs = np.where(a.min(axis=2) < 200)
        m = 12
        a = a[max(ys.min() - m, 0):ys.max() + m, max(xs.min() - m, 0):xs.max() + m]
        rgba = np.zeros(a.shape[:2] + (4,), np.uint8)  # fondo transparente, tinta del color del texto
        rgba[..., :3] = (0x22, 0x22, 0x22)
        rgba[..., 3] = 255 - a.min(axis=2)
        img = Image.fromarray(rgba)
        buf = io.BytesIO()
        img.save(buf, "PNG")
        buf.seek(0)
        return buf, (img.width / 300, img.height / 300)


def portada_time():
    """La portada de TIME (derechos de terceros) se toma de la base local."""
    if PORTADA.exists():
        from PIL import Image
        img = Image.open(PORTADA)
        return io.BytesIO(PORTADA.read_bytes()), img.size
    base = Presentation(BASE)
    pic = next(sh for sh in base.slides[0].shapes if sh.shape_type == 13)
    return io.BytesIO(pic.image.blob), pic.image.size


# -----------------------------------------------------------------------------
# 1. Portada
# -----------------------------------------------------------------------------

s = lamina(notas="""Presentador 1 · 45 s

Buenos días. Somos consultores de una agencia que reparte ayuda cuando suben los precios de los alimentos, algo como el Programa Mundial de Alimentos.

Nuestro caso es Indonesia en 1997 y 1998. Con la crisis asiática, el precio del arroz se disparó; esta es la portada de TIME de enero de 1998.

La pregunta del cliente es simple: cuando suben los alimentos, ¿a qué niños hay que proteger primero? Para responderla seguimos la estatura de los niños antes y después del alza.""")
ancho_verde = W * 0.6
rect(s, 0, 0, ancho_verde, H, VERDE_OSC)
# Bloques repartidos con la misma separación desde el borde superior de la portada de TIME (0,32 in,
# fin de su marco rojo) hasta el inferior (7,20 in); las y salen de medir la tinta de cada bloque
Y_PORT = {"titulo": 0.086, "subtitulo": 2.142, "para": 4.215, "autores": 5.411, "credito": 6.96}
texto(s, 0.7, Y_PORT["titulo"], ancho_verde - 1.3, 2.0,
      [("¿A quién golpeó más el arroz caro?", 50, True, BLANCO, TITULO_F)], fondo=VERDE_OSC,
      anclaje=MSO_ANCHOR.TOP)
texto(s, 0.7, Y_PORT["subtitulo"], ancho_verde - 1.3, 1.9,
      [("Análisis de los efectos promedio y heterogéneos de la crisis financiera de Indonesia de 1997-98 "
        "sobre la estatura de los niños", 24, False, BLANCO)], fondo=VERDE_OSC)
texto(s, 0.7, Y_PORT["para"], ancho_verde - 1.3, 0.9,
      [("Para: una agencia que focaliza ayuda ante choques de precios de alimentos",
        20, True, BLANCO)], fondo=VERDE_OSC)
texto(s, 0.7, Y_PORT["autores"], ancho_verde - 1.3, 1.2,
      [("Samuel Escandón, Douglas Plazas, Mateo Olmos, Santiago Muñoz", 20, False, BLANCO),
       ("Ciencia de Datos y Econometría Aplicada, 23-nov-2026", 16, False, BLANCO, None, None, 4)],
      fondo=VERDE_OSC)
texto(s, 0.7, Y_PORT["credito"], ancho_verde - 1.3, 0.35,
      [("Portada: TIME, 19 de enero de 1998", 12, False, BLANCO)], fondo=VERDE_OSC)
blob, (px, py) = portada_time()
ancho_der = W - ancho_verde
ancho_nat = H * px / py  # ancho que tendría a toda la altura sin deformarse
pic = s.shapes.add_picture(blob, Inches(ancho_verde), 0, Inches(ancho_der), Inches(H))
recorte = max(0.0, (ancho_nat - ancho_der) / ancho_nat) / 2
pic.crop_left = pic.crop_right = recorte  # recorta los bordes laterales, no deforma
assert abs((px * (1 - 2 * recorte)) / py - ancho_der / H) < 0.01

# -----------------------------------------------------------------------------
# 2. Situación
# -----------------------------------------------------------------------------

s = lamina("Contexto", """Presentador 1 · 75 s

El arroz es el alimento básico en Indonesia. Con la crisis, su precio subió en todo el país, pero no lo mismo en todas partes.

Este gráfico cuenta comunidades. En el eje horizontal está cuánto subió el precio del arroz en cada comunidad entre 1997 y 2000; la altura de cada barra es cuántas comunidades tuvieron esa alza. Son 297 comunidades de la encuesta.

La línea marca la mitad: en la mitad de las comunidades el precio subió más de 70 %. Pero hay comunidades con alzas de 20 % y otras de más de 150 %. Esa diferencia entre comunidades es la que vamos a aprovechar.""")
titulo(s, "El arroz subió un 70 % entre 1997 y 2000, y en unas comunidades mucho más")
figura(s, FIG / "15_figuras_presentacion/f1_alza.png", (W - 10.0) / 2, Y_FIG, 10.0)
como_leer(s, "Cómo leer: cada barra cuenta comunidades según cuánto subió allí el precio del arroz "
             "(297 comunidades). El arroz es el alimento básico; la crisis lo encareció de forma desigual.")

# -----------------------------------------------------------------------------
# 3. Lo que se sabe
# -----------------------------------------------------------------------------

s = lamina("Contexto", """Presentador 1 · 90 s

Dos estudios usaron estos mismos datos y llegaron a conclusiones distintas.

Elmira y Qaim, en 2026, encuentran que cuando el precio del arroz se duplicaba, la estatura de los niños para su edad bajaba 0,135 desviaciones estándar, y más en las ciudades.

Frankenberg y Thomas, en 2017, comparando zonas urbanas y rurales, no encuentran daño en la estatura.

Ninguno de los dos pregunta lo que necesita la agencia: a quién proteger primero. Por eso nos hacemos tres preguntas. Uno: ¿los niños de comunidades donde el arroz subió más crecieron menos? Dos: ¿a algunos niños les afectó más, según su edad, sexo, pobreza, zona, la educación de su madre o si compraban arroz? Tres: ¿un bosque causal, un método de aprendizaje automático, encuentra a los más afectados mejor que una regla simple?""")
titulo(s, "Dos estudios con estos datos no coinciden, y nadie ha probado a quién proteger primero")
Y_TARJ, H_TARJ = 1.94, 1.75  # centradas entre el título y la franja verde (4,2)
caja_texto(s, 0.6, Y_TARJ, 5.9, H_TARJ, TINTE,
           [("Elmira y Qaim (2026)", 20, True, TEXTO, TITULO_F),
            ("El alza redujo la estatura: −0,135 desviaciones estándar por cada duplicación "
             "del precio, y más en zonas urbanas.", 18, False, TEXTO, None, None, 6)], anclaje=MSO_ANCHOR.TOP, margen=0.25)
caja_texto(s, 6.83, Y_TARJ, 5.9, H_TARJ, TINTE,
           [("Frankenberg y Thomas (2017)", 20, True, TEXTO, TITULO_F),
            ("Comparando zonas urbanas y rurales: sin daño en la estatura de los niños.",
             18, False, TEXTO, None, None, 6)], anclaje=MSO_ANCHOR.TOP, margen=0.25)
caja_texto(s, 0, 4.2, W, 2.75, VERDE,
           [("Nuestras tres preguntas", 22, True, BLANCO, TITULO_F),
            ("1. ¿Los niños de las comunidades donde el arroz subió más crecieron menos?",
             20, False, BLANCO, None, None, 8),
            ("2. ¿Hubo niños a los que el alza afectó más, según su edad, sexo, pobreza, zona, "
             "educación de la madre o compra de arroz?", 20, False, BLANCO, None, None, 6),
            ("3. ¿Un bosque causal (aprendizaje automático) encuentra a los niños más afectados "
             "mejor que una regla simple?", 20, False, BLANCO, None, None, 6)],
           anclaje=MSO_ANCHOR.MIDDLE, margen=0.6)

# -----------------------------------------------------------------------------
# 4. Cómo lo medimos
# -----------------------------------------------------------------------------

s = lamina("Método", """Presentador 1 · 90 s

¿Cómo lo medimos? Usamos la Encuesta de Vida Familiar de Indonesia, la IFLS. Los niños de 0 a 5 años en 1997, antes del alza, fueron medidos de nuevo en 2000. Entre una ola y otra, el arroz subió más en unas comunidades que en otras.

Con la estatura, la edad y el sexo que trae la encuesta calculamos el HAZ, la estatura para la edad, de cada niño, y luego cuánto cambió entre 1997 y 2000. Esa medida compara la estatura del niño con la de niños sanos de su misma edad y sexo, según la referencia de la Organización Mundial de la Salud. Menos uno quiere decir una desviación estándar por debajo; en estos niños, una desviación estándar son unos 5 centímetros.

Son 2.421 niños en 294 comunidades. El método es una regresión del cambio en el HAZ sobre el alza del precio de la comunidad, con errores agrupados por comunidad. Dos aclaraciones: fijamos los grupos y las pruebas antes de ver los resultados; y medimos el efecto de más alza frente a menos alza, no el de la crisis completa, porque todas las comunidades la vivieron.""")
titulo(s, "Seguimos a 2.421 niños de la IFLS y comparamos comunidades con más y menos alza")
pasos = [("1997", "Calculamos el HAZ de cada niño de 0 a 5 años"),
         ("1997-2000", "El arroz sube más en unas comunidades que en otras"),
         ("2000", "Volvemos a calcular el HAZ de los mismos niños")]
for k, (anio, desc) in enumerate(pasos):
    x = 0.6 + k * 4.3
    caja_texto(s, x, 1.8, 3.65, 1.75, VERDE,
               [(anio, 22, True, BLANCO, TITULO_F, PP_ALIGN.CENTER),
                (desc, 18, False, BLANCO, None, PP_ALIGN.CENTER, 4)],
               anclaje=MSO_ANCHOR.MIDDLE, margen=0.15)
    if k < 2:
        flecha = rect(s, x + 3.65 + (0.65 - 0.42) / 2, 1.8 + (1.75 - 0.38) / 2, 0.42, 0.38, GRIS, MSO_SHAPE.RIGHT_ARROW)
        flecha.adjustments[0] = 0.28  # cuerpo delgado, centrada entre los cuadros
texto(s, 0.6, 3.65, W - 1.2, 0.5,
      [("Fuente: IFLS (Indonesia Family Life Survey), 1997 y 2000: 2.421 niños en 294 comunidades.",
        20, True, TEXTO)])
caja_texto(s, 0.6, 4.38, 6.7, 2.5, TINTE,
           [("¿Qué es el HAZ (estatura para la edad)?", 22, True, TEXTO, TITULO_F),
            ("Compara la estatura del niño con la de niños sanos de su misma edad y sexo, "
             "en desviaciones estándar.", 16, False, TEXTO, None, None, 6),
            ("Se calcula siguiendo lineamientos de la OMS.", 16, False, TEXTO, None, None, 6, True),
            ("Ejemplo: −1 es una desviación estándar por debajo; en estos niños, unos 5 cm.",
             16, False, TEXTO, None, None, 4, True)], margen=0.3)
texto(s, 7.7, 4.38, 5.05, 2.5, anclaje=MSO_ANCHOR.MIDDLE, parrafos=
      [("¿Cómo estimamos?", 24, True, TEXTO, TITULO_F),
       ("Regresión del cambio en el HAZ sobre el alza del precio de la comunidad.", 16, False, TEXTO, None, None, 6),
       ("Errores agrupados por comunidad.", 16, False, TEXTO, None, None, 6, True),
       ("Mide el efecto de una mayor alza, no el de la crisis.", 16, False, TEXTO, None, None, 4, True)])
como_leer(s, "Nota del orador (quitada de la lámina): fijamos los grupos y las pruebas antes de ver los "
             "resultados.")

# -----------------------------------------------------------------------------
# 5. Respuesta 1
# -----------------------------------------------------------------------------

lo, hi = a4.beta - 1.96 * a4.ee_agrupado, a4.beta + 1.96 * a4.ee_agrupado
s = lamina("Resultados", f"""Presentador 2 · 150 s

Primera respuesta: sí. Donde el arroz subió más, los niños crecieron menos.

En el eje horizontal está cuánto cambia la estatura para la edad por cada vez que el precio se duplica; más a la izquierda es más daño. El punto verde es nuestra estimación: {coma(a4.beta)} desviaciones estándar, unos {coma(-a4.beta_cm, 1)} centímetros. La línea es el rango plausible: con 95 % de confianza, el efecto está entre {coma(lo)} y {coma(hi)}.

El punto gris es Elmira y Qaim: −0,135. Nuestro efecto es mayor, pero los rangos se traslapan, así que no son incompatibles. Ellos miden el precio con fuentes distintas en cada año y no comparan comunidades dentro de la misma provincia; nosotros sí.

Un detalle técnico: nuestro margen de error tiene en cuenta que los niños de una misma comunidad se parecen entre sí; el de ellos no. Por eso nuestro rango es más ancho.""")
titulo(s, "Replicamos a Elmira y Qaim: donde el arroz subió más, los niños crecieron menos")
subtitulo(s, "MCO con el alza del precio como variable continua")
DEFINICIONES = [  # una viñeta por definición: i, c, p y μ en cursiva, X en negrilla
    [("i", "i"), (" - niño", None)], [("c", "i"), (" - comunidad", None)], [("p", "i"), (" - provincia", None)],
    [("Dosis - cambio proporcional del precio (+1 = +100 %)", None)],
    [("X", "b"), (" - controles de 1997", None)], [("μ", "grande"), (" - efectos fijos de provincia", None)]]
# especificación (sin resultados) centrada arriba; figura y cuadro de definiciones debajo
eq5, (eq5_w, eq5_h) = ecuacion_png(
    r"\Delta\mathrm{HAZ}_{ic}=\beta\,\mathrm{Dosis}_c+\gamma\,\ln P_{c,1997}"
    r"+\mathbf{X}_{ic}'\,\boldsymbol{\delta}+\mu_{p(c)}+\varepsilon_{ic}", pt=22)
y_eq = Y_SUB + 0.4 + GAP - 0.04  # misma separación (GAP) bajo el subtítulo y sobre la figura
s.shapes.add_picture(eq5, Inches((W - eq5_w) / 2), Inches(y_eq), width=Inches(eq5_w))
y_fig5 = y_eq + eq5_h + GAP - 0.04
pic5 = figura(s, FIG / "15_figuras_presentacion/f2_efecto_principal.png", 0.6, y_fig5, 7.3)
alto5 = pic5.height / 914400
X_P = 0.6 + 7.3 + 0.3
H_DEF = 2.82  # alto ajustado al texto (alto de la tinta + 2 × margen); arriba, alineado con el tope de la figura
caja5 = caja_texto(s, X_P, y_fig5, W - 0.6 - X_P, H_DEF, TINTE,
                   [(d, 16, False, TEXTO, None, None, 5, "texto") for d in DEFINICIONES],
                   anclaje=MSO_ANCHOR.TOP, margen=0.3)
como_leer(s, "Cómo leer: cada punto es el efecto promedio; la línea, su rango plausible al 95 %. "
             "Más a la izquierda = más daño. 2.421 niños en 294 comunidades.")

# -----------------------------------------------------------------------------
# 6. Qué tan sólido
# -----------------------------------------------------------------------------

s = lamina("Resultados", """Presentador 2 · 150 s

¿Qué tan sólido es este resultado? Repetimos la estimación cambiando una cosa a la vez: sin las comunidades medidas en 1998, con los pesos de la encuesta, sin recortar las alzas extremas, solo con precios por kilo y sin los niños con cambios de estatura extremos, que parecen errores de medición.

Todas las estimaciones quedan a la izquierda del cero: la dirección se sostiene. Pero el tamaño va de −0,20 a −0,50: el número exacto es incierto.

Abajo, en naranja, está el placebo: miramos cómo crecieron niños entre 1993 y 1997, antes del alza. Si las comunidades con más alza no tenían nada especial antes, debería dar cero. No se distingue de cero, pero tampoco lo podemos descartar: podría haber una tendencia previa. Lo decimos tal cual.""")
titulo(s, "El signo del efecto resiste cinco pruebas de robustez, pero su tamaño cambia")
figura_metodo(s, FIG / "15_figuras_presentacion/f3_robustez.png",
              "MCO con el alza del precio como variable continua, cinco variantes y un placebo",
              "la misma especificación de la lámina anterior, repetida cambiando un supuesto por fila. "
              "Placebo: el mismo modelo sobre el cambio en el HAZ de 1993 a 1997, antes del alza.",
              "Cómo leer: todas las estimaciones quedan a la izquierda de cero; "
              "el placebo debería estar en cero.")

# -----------------------------------------------------------------------------
# 7. El bosque reproduce el ATE
# -----------------------------------------------------------------------------

bos = pd.read_csv(TAB / "10_bosque/ninos_bosque_ate.csv")
b_bos = bos.loc[bos.estimador == "Bosque causal (AIPW)"].iloc[0]
b_mco = bos.loc[bos.estimador.str.startswith("MCO")].iloc[0]
assert coma(b_bos.estimacion) == "−0,18" and coma(b_mco.estimacion) == "−0,19"
s = lamina("Resultados", f"""Presentador 3 · 60 s

Antes de buscar diferencias entre niños, una comprobación: ¿el bosque causal da el mismo efecto promedio que las regresiones? Para el bosque comparamos el tercio de comunidades con más alza contra el tercio con menos.

Cada barra cuenta niños según el efecto que el bosque predice para ellos. La línea punteada es el promedio del bosque, {coma(b_bos.estimacion, 3)} desviaciones estándar. La regresión con el mismo contraste da {coma(b_mco.estimacion, 3)}: prácticamente el mismo número.

Una advertencia: la dispersión de la distribución mezcla diferencias reales y ruido de estimación. La prueba de calibración, que veremos más adelante, no logra separarlas.""")
titulo(s, "Un bosque causal logra replicar el ATE de las especificaciones lineales")
figura_metodo(s, FIG / "15_figuras_presentacion/f7_cate_distribucion.png",
              "Terciles del alza dentro de cada provincia: tercio alto frente a tercio bajo",
              "grf con 4.000 árboles, agrupado por comunidad; "
              f"promedio con puntajes AIPW: {coma(b_bos.estimacion, 3)} "
              f"(EE {coma(b_bos.ee, 3)}). "
              f"MCO, especificación (4), mismo contraste: {coma(b_mco.estimacion, 3)} (EE {coma(b_mco.ee, 3)}).",
              "Cómo leer: cada barra cuenta niños según el efecto que el bosque predice para ellos; la "
              "línea punteada es el promedio. La dispersión mezcla diferencias reales y ruido de "
              "estimación: la prueba de calibración no los distingue.")

# -----------------------------------------------------------------------------
# 8. Respuesta 2
# -----------------------------------------------------------------------------

s = lamina("Resultados", """Presentador 3 · 100 s

Segunda pregunta: ¿a quién le dolió más? Antes de ver los datos fijamos seis comparaciones: edad, zona, educación de la madre, sexo, si la familia compra o produce su arroz, y pobreza.

Cada panel compara dos grupos. El punto es el daño estimado en cada grupo, comparando el tercio de comunidades con más alza contra el tercio con menos; la línea es su rango plausible. En los doce grupos el punto queda a la izquierda del cero: todos se vieron afectados.

Pero los grupos de cada panel se parecen mucho: las diferencias son pequeñas frente a su margen de error. Tras corregir por hacer muchas comparaciones a la vez, ninguna diferencia es clara. Tampoco confirmamos que el daño fuera mayor en las ciudades, como dicen Elmira y Qaim; ni lo descartamos.""")
titulo(s, "Un bosque causal no reproduce la heterogeneidad de las interacciones identificadas por Elmira y Qaim")
figura_metodo(s, FIG / "15_figuras_presentacion/f4_grupos.png",
              "Terciles del alza dentro de cada provincia, efecto por grupo (GATE)",
              "GATE con puntajes doblemente robustos (AIPW); contrastes corregidos con Holm. "
              "La réplica con MCO e interacciones está en el respaldo.",
              "Cómo leer: punto = daño en cada grupo; línea = rango plausible. Todos los grupos "
              "quedan a la izquierda de cero; tampoco confirmamos un daño mayor en zonas urbanas.")

# -----------------------------------------------------------------------------
# 8. La única pista
# -----------------------------------------------------------------------------

s = lamina("Resultados", f"""Presentador 3 · 100 s

La única pista está en la edad. Los niños que tenían 0 a 2 años en 1997 muestran más daño, {coma(edad.gate_0)}, que los de 3 a 5 años, {coma(edad.gate_1)}. Pero ojo: esto es exploratorio.

¿Por qué no lo afirmamos? Por la precisión. En el gráfico, la barra verde es el daño promedio del alza: 0,18 desviaciones estándar, comparando el tercio de comunidades con más alza contra el de menos. La barra naranja es la menor diferencia entre dos grupos que nuestros datos alcanzarían a detectar: entre 0,36 y 0,44, el doble del daño promedio. Es un cálculo aproximado.

Con unos cientos de comunidades, solo veríamos diferencias muy grandes. Así que "no encontramos diferencias" no quiere decir "el daño fue igual para todos".""")
titulo(s, "Los menores de 3 años quizá sufrieron más, pero los datos no alcanzan para afirmarlo")
subtitulo(s, "Bosque causal con terciles del alza: efecto por edad (GATE)")
pic8 = figura(s, FIG / "15_figuras_presentacion/f5_potencia.png", 0.6, Y_FIG, 7.0)
caja_texto(s, 9.15, Y_FIG + 0.05, 3.6, 0.5, VERDE_OSC,
           [("Exploratorio", 20, True, BLANCO, TITULO_F, PP_ALIGN.CENTER)],
           anclaje=MSO_ANCHOR.MIDDLE, margen=0.05)
texto(s, 9.15, Y_FIG + 0.75, 3.6, 3.3,
      [("0-2 años", 22, True, TEXTO),
       (coma(edad.gate_0), 44, True, TEXTO, TITULO_F),
       ("3-5 años", 22, True, TEXTO, None, None, 12),
       (coma(edad.gate_1), 44, True, TEXTO, TITULO_F),
       ("desviaciones estándar (más alza frente a menos alza)", 18, False, TEXTO, None, None, 6)])
nota_metodo(s, Y_FIG + pic8.height / 914400,
            "0-2 frente a 3-5 años; diferencia mínima detectable ≈ 2,8 × el margen de error del "
            "contraste (aproximación normal).")
como_leer(s, "Cómo leer: la barra naranja es la menor diferencia entre dos grupos que estos datos "
             "detectarían (aproximada). La parte oscura llega al contraste más fácil de detectar (0,36) y "
             "la clara, al más difícil (0,44): es un rango entre los seis contrastes, no un intervalo de "
             "confianza. Es el doble del daño promedio.")

# -----------------------------------------------------------------------------
# 9. Respuesta 3
# -----------------------------------------------------------------------------

s = lamina("Resultados", """Presentador 3 · 100 s

Tercera pregunta: ¿un bosque causal, un método de aprendizaje automático, encuentra a los más afectados mejor que una regla simple? El bosque busca por su cuenta a quién afectó más.

La prueba simula a la agencia: si atiende primero a los niños que señala cada regla, ¿esos niños sufrieron más que el promedio? Entrenamos el bosque en la mitad de las comunidades y lo evaluamos en la otra mitad.

Más a la derecha es mejor. La línea vertical es no hacerlo mejor que escoger al azar. El bosque, y también las reglas de pobreza, zona urbana y compra de arroz, tienen rangos que cruzan esa línea: ninguna se distingue de escoger al azar, y ninguna supera a las otras. La prueba de calibración del bosque tampoco encuentra diferencias reales entre niños.""")
titulo(s, "Un bosque causal no encuentra a los más afectados mejor que una regla simple")
figura_metodo(s, FIG / "15_figuras_presentacion/f6_focalizacion.png",
              "Evaluación con RATE (AUTOC) en una mitad de las comunidades",
              "el bosque se entrena en la otra mitad; el RATE mide cuánto más daño sufren los priorizados "
              "que el promedio; cada regla simple se evalúa igual.",
              "Cómo leer: si la agencia atiende primero a quien señala cada regla, ¿esos niños sufrieron "
              "más que el promedio? La calibración del bosque tampoco encuentra diferencias entre niños.")

# -----------------------------------------------------------------------------
# 10. Recomendación
# -----------------------------------------------------------------------------

s = lamina("Recomendación", """Presentador 4 · 110 s

¿Qué le recomendamos a la agencia? Focalizar por comunidad, no por hogar.

Hacer: vigilar el alza del precio del arroz comunidad por comunidad, que es lo que sí se asocia con menos crecimiento, y cubrir a todos los niños pequeños de las comunidades donde más sube.

No hacer: usar un bosque causal para escoger a quién ayudar dentro de la comunidad, ni dejar fuera a los niños no pobres o rurales: con esta evidencia, no sabemos que hayan sufrido menos.

Por confirmar: los menores de 3 años. Es la única pista, pero no alcanza para convertirla en regla; habría que comprobarla con más datos.""")
titulo(s, "Recomendación: Focalizar por comunidad")
columnas = [("Hacer", VERDE, BLANCO,
             ["Vigilar el alza del arroz por comunidad.",
              "Cubrir a todos los niños pequeños donde más sube."]),
            ("No hacer", VERDE_OSC, BLANCO,
             ["Escoger con un bosque causal dentro de la comunidad.",
              "Excluir a los no pobres o a los rurales."]),
            ("Por confirmar", TINTE, TEXTO,
             ["Los menores de 3 años: una pista, no una regla."])]
Y_COL, H_COL, OFF2 = (H - 4.1) / 2, 4.1, 2.25  # OFF2: el segundo bloque arranca a la misma altura en las dos primeras
for k, (enc, fondo, col, items) in enumerate(columnas):
    x = 0.6 + k * 4.1
    rect(s, x, Y_COL, 3.85, H_COL, fondo)
    bloque1 = texto(s, x, Y_COL, 3.85, OFF2, [(enc, 26, True, col, TITULO_F),
                                              (items[0], 22, False, col, None, None, 12)],
                    fondo=fondo, anclaje=MSO_ANCHOR.TOP, margen=0.3)
    bloque1.text_frame.margin_top = Inches(0.23)  # el interlineado ya deja ~0,07 in sobre la tinta
    if len(items) > 1:
        bloque2 = texto(s, x, Y_COL + OFF2, 3.85, H_COL - OFF2, [(items[1], 22, False, col)],
                        fondo=fondo, anclaje=MSO_ANCHOR.TOP, margen=0.3)
        bloque2.text_frame.margin_top = Inches(0)

# -----------------------------------------------------------------------------
# 11. Aporte y límites
# -----------------------------------------------------------------------------

s = lamina("Recomendación", """Presentador 4 · 110 s

¿Qué añadimos? Primero, replicamos el resultado de Elmira y Qaim con errores que tienen en cuenta que los niños de una misma comunidad se parecen. Segundo, fijamos los grupos antes de mirar y corregimos por hacer muchas comparaciones a la vez. Tercero, hasta donde revisamos, es la primera prueba de si un bosque causal focaliza mejor que reglas simples ante este choque.

¿Qué no podemos afirmar? Puede haber una tendencia previa, porque el placebo no es concluyente. Puede haber otros choques al mismo tiempo, como la sequía de El Niño o el humo de los incendios. En las comunidades donde más subió el arroz se midió a menos niños en 1997. El tamaño del efecto cambia con los valores extremos. Y tenemos poca precisión para comparar grupos.""")
titulo(s, "Qué añadimos y limitaciones del estudio")
caja_texto(s, 0.6, (H - 4.3) / 2, 5.9, 4.3, TINTE,
           [("Qué añadimos", 26, True, TEXTO, TITULO_F),
            ("Réplica con errores agrupados por comunidad.", 20, False, TEXTO, None, None, 12),
            ("Grupos fijados de antemano y corregidos por hacer muchas comparaciones a la vez (Holm).",
             20, False, TEXTO, None, None, 10),
            ("Primera prueba, hasta donde revisamos, de si un bosque causal focaliza mejor que "
             "reglas simples ante este choque.", 20, False, TEXTO, None, None, 10)], anclaje=MSO_ANCHOR.TOP, margen=0.3)
caja_texto(s, 6.83, (H - 4.3) / 2, 5.9, 4.3, VERDE_OSC,
           [("Limitaciones", 26, True, BLANCO, TITULO_F),
            ("Puede haber una tendencia previa.", 20, False, BLANCO, None, None, 12),
            ("Otros choques al mismo tiempo (sequía, humo).", 20, False, BLANCO, None, None, 8),
            ("Menos niños medidos donde más subió el arroz.", 20, False, BLANCO, None, None, 8),
            ("El tamaño cambia con los valores extremos.", 20, False, BLANCO, None, None, 8),
            ("Poca precisión para comparar grupos.", 20, False, BLANCO, None, None, 8)], anclaje=MSO_ANCHOR.TOP, margen=0.3)

# -----------------------------------------------------------------------------
# 12. Cierre
# -----------------------------------------------------------------------------

s = lamina("Recomendación", """Presentador 4 · 80 s

Para cerrar, tres preguntas y tres respuestas.

¿Los niños de las comunidades donde el arroz subió más crecieron menos? Sí: cerca de 1,7 centímetros menos por cada vez que el precio se duplicó, aunque el tamaño exacto es incierto.

¿Hubo niños a los que les afectó más? No hay evidencia estadística que permita confirmar la existencia de efectos heterogéneos del alza en el precio del arroz. La edad es la única pista, pero no alcanza para afirmarla.

¿Un bosque causal encuentra mejor a los más afectados? No: una regla simple funciona igual de bien.

Gracias. Quedamos atentos a sus preguntas.""")
titulo(s, "Tres preguntas, tres respuestas")
qa = [("¿Los niños de las comunidades donde el arroz subió más crecieron menos?",
       "Sí, crecieron menos (≈ 1,7 cm por cada duplicación del precio), con incertidumbre sobre el tamaño exacto."),
      ("¿Hubo niños a los que el alza afectó más?",
       "No hay evidencia estadística que permita confirmar la existencia de efectos heterogéneos del alza en el precio del arroz."),
      ("¿Un bosque causal encuentra a los más afectados mejor que una regla simple?",
       "No: una regla simple funciona igual de bien.")]
for k, (q, a) in enumerate(qa):
    y = 1.55 + k * 1.4
    caja_texto(s, 0.6, y, 0.75, 1.25, VERDE,
               [(str(k + 1), 32, True, BLANCO, TITULO_F, PP_ALIGN.CENTER)],
               anclaje=MSO_ANCHOR.MIDDLE, margen=0.02)
    texto(s, 1.55, y, W - 2.15, 1.25,
          [(q, 20, False, TEXTO), (a, 20, True, TEXTO, None, None, 4)], anclaje=MSO_ANCHOR.MIDDLE)
caja_texto(s, 0, 6.0, W, 0.85, VERDE_OSC,
           [("Gracias. ¿Preguntas?", 28, True, BLANCO, TITULO_F, PP_ALIGN.CENTER)],
           anclaje=MSO_ANCHOR.MIDDLE)

N_PRINCIPALES = len(prs.slides)

# -----------------------------------------------------------------------------
# Referencias (APA 7), después del cierre y antes del respaldo; no cuenta en los 20 min
# Cada una se verificó: E-Q y F-T contra los PDF de 07_Recursos/Articulos/; el resto, contra la
# página del editor o de RePEc (23-nov-2026)
# -----------------------------------------------------------------------------

REFS = [  # (partes (texto, cursiva))
    [("Athey, S., Tibshirani, J., & Wager, S. (2019). Generalized random forests. ", 0),
     ("The Annals of Statistics, 47", 1), ("(2), 1148–1178. https://doi.org/10.1214/18-AOS1709", 0)],
    [("Chernozhukov, V., Demirer, M., Duflo, E., & Fernández-Val, I. (2025). Fisher-Schultz lecture: Generic "
      "machine learning inference on heterogeneous treatment effects in randomized experiments, with an "
      "application to immunization in India. ", 0),
     ("Econometrica, 93", 1), ("(4), 1121–1164. https://doi.org/10.3982/ECTA19303", 0)],
    [("Elmira, E. S., & Qaim, M. (2026). Macroeconomic shocks and long-term nutritional outcomes: Insights "
      "from the Asian financial crisis. ", 0), ("Global Food Security, 48", 1),
     (", Article 100900. https://doi.org/10.1016/j.gfs.2025.100900", 0)],
    [("Frankenberg, E., & Thomas, D. (2017). ", 0),
     ("Human capital and shocks: Evidence on education, health and nutrition", 1),
     (" (NBER Working Paper No. 23347). National Bureau of Economic Research. "
      "http://www.nber.org/papers/w23347", 0)],
    [("RAND Corporation. (2026). ", 0), ("IFLS data and documentation", 1),
     (" [Sitio web]. https://www.rand.org/health/surveys/FLS/IFLS/download.html", 0)],
    [("Wager, S., & Athey, S. (2018). Estimation and inference of heterogeneous treatment effects using "
      "random forests. ", 0), ("Journal of the American Statistical Association, 113", 1),
     ("(523), 1228–1242. https://doi.org/10.1080/01621459.2017.1319839", 0)],
    [("WHO Multicentre Growth Reference Study Group. (2006). ", 0),
     ("WHO child growth standards: Length/height-for-age, weight-for-age, weight-for-length, "
      "weight-for-height and body mass index-for-age: Methods and development", 1),
     (". World Health Organization. https://www.who.int/publications/i/item/924154693X", 0)],
    [("Yadlowsky, S., Fleming, S., Shah, N., Brunskill, E., & Wager, S. (2025). Evaluating treatment "
      "prioritization rules via rank-weighted average treatment effects. ", 0),
     ("Journal of the American Statistical Association, 120", 1),
     ("(549), 38–51. https://doi.org/10.1080/01621459.2024.2393466", 0)],
]
autores = [r[0][0].split(",")[0] for r in REFS]
assert autores == sorted(autores, key=str.lower), autores  # orden alfabético (APA)
s = lamina("Referencias", "Referencias en formato APA 7. No cuenta en los 20 minutos.")
titulo(s, "Referencias")
caja = s.shapes.add_textbox(Inches(0.6), Inches(1.65), Inches(W - 1.2), Inches(5.2))
tf = caja.text_frame
tf.word_wrap = True
for lado in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
    setattr(tf, lado, Inches(0.05))
for i, partes in enumerate(REFS):
    par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    par.space_after = Pt(5)
    pPr = par._p.get_or_add_pPr()  # sangría francesa de APA: 0,5 in
    pPr.set("marL", str(Inches(0.5)))
    pPr.set("indent", str(-Inches(0.5)))
    for txt, cursiva in partes:
        r = par.add_run()
        r.text = txt
        r.font.size, r.font.name, r.font.italic = Pt(13), CUERPO_F, bool(cursiva)
        r.font.color.rgb = rgb(TEXTO)
        textos.append((len(prs.slides), txt, TEXTO, FONDO))

(RAIZ / "04_Presentaciones/como_leer_laminas.md").write_text(
    "# Cómo leer cada figura\n\nTextos que se quitaron de las láminas: «Cómo leer» de cada figura y aclaraciones para el orador. Los genera "
    "`04_Presentaciones/_fuente/construir_presentacion.py`; no se editan a mano.\n\n"
    + "\n".join(f"## Lámina {k}\n\n{x}\n" for k, x in COMO_LEER), encoding="utf-8")

# -----------------------------------------------------------------------------
# Respaldo
# -----------------------------------------------------------------------------

s = lamina(notas="Respaldo: no cuenta en los 20 minutos.")
rect(s, 0, 0, W, H, VERDE_OSC)
texto(s, 0.8, 2.9, W - 1.6, 1.5, [("Respaldo", 54, True, BLANCO, TITULO_F)], fondo=VERDE_OSC,
      anclaje=MSO_ANCHOR.MIDDLE)

def respaldo_figura(t, archivo, notas):
    s = lamina(notas=notas)
    titulo(s, t)
    pic = s.shapes.add_picture(str(archivo), 0, Inches(1.8), height=Inches(5.15))
    pic.left = int((prs.slide_width - pic.width) / 2)
    return s

respaldo_figura("Respaldo: el bosque causal compara niños con probabilidades parecidas de estar en cada grupo",
                FIG / "10_bosque/ninos_bosque_traslape.png",
                "Traslape del bosque (10_bosque): probabilidad estimada entre 0,10 y 0,93; ningún niño fuera de 0,05-0,95.")
respaldo_figura("Respaldo: el daño aparece en los tres cuartiles de mayor alza",
                FIG / "07_cuartiles/ninos_cuartiles_coeficientes.png",
                "Forma por cuartiles (07_cuartiles): Q2 −0,189, Q3 −0,116, Q4 −0,295 frente al cuartil 1.")

s = lamina(notas="Especificaciones del efecto promedio (06_ate).")
titulo(s, "Respaldo: el efecto promedio en cuatro especificaciones")
filas = [["Efecto por duplicación del precio"] + [coma(v, 3) for v in ate.beta],
         ["Margen de error, agrupado por comunidad"] + [coma(v, 3) for v in ate.ee_agrupado],
         ["Margen de error, robusto sin agrupar"] + [coma(v, 3) for v in ate.ee_robusto],
         ["Equivalente en cm (aproximado)"] + [coma(v, 2) for v in ate.beta_cm],
         ["Controles de 1997", "No", "Sí", "Sí", "Sí"],
         ["Efectos fijos de provincia", "No", "No", "Sí", "Sí"],
         ["Precio del arroz de 1997", "No", "No", "No", "Sí"],
         ["Niños / comunidades"] + [f"{n:,}".replace(",", ".") + f" / {c}"
                                    for n, c in zip(ate.ninos, ate.comunidades)]]
beta_t = coma(a4.beta, 3).replace(",", "{,}").replace("−", "-")
ee_t = coma(a4.ee_agrupado, 3).replace(",", "{,}")
eq, (eq_w, eq_h) = ecuacion_png(
    r"\widehat{\Delta\mathrm{HAZ}}_{ic} \;=\; \underset{(" + ee_t + r")}{" + beta_t + r"}\,\mathrm{Dosis}_c"
    r"\;+\; \hat\gamma\,\ln P_{c,1997} \;+\; \mathbf{X}_{ic}'\,\hat{\boldsymbol{\delta}}"
    r"\;+\; \hat\mu_{p(c)}")
s.shapes.add_picture(eq, Inches((W - eq_w) / 2), Inches(1.75), width=Inches(eq_w))
texto(s, 0.6, 1.75 + eq_h + 0.1, W - 1.2, 0.8,
      [("Especificación (4): i = niño, c = comunidad en 1997, p = provincia. Dosis = cambio proporcional del "
        "precio del arroz 1997-2000 (el coeficiente es el efecto por +100 %); X = controles de 1997; "
        "efectos fijos de provincia. Entre paréntesis, el error estándar agrupado por comunidad.",
        14, False, GRIS, None, PP_ALIGN.CENTER)])
tabla(s, 0.6, 3.45, W - 1.2, ["", "(1)", "(2)", "(3)", "(4)"], filas,
      [5.13, 1.75, 1.75, 1.75, 1.75], pt=14, alto_fila=0.36)

inter = pd.read_csv(TAB / "09_interacciones_eq/ninos_interacciones_eq.csv")
inter = inter[(inter.ee == "agrupado") & (inter.especificacion == 4)]
s = lamina(notas="Interacciones de Elmira y Qaim (09_interacciones_eq), especificación 4, Holm F2.")
titulo(s, "Respaldo: ninguna de las cinco diferencias de Elmira y Qaim se distingue de cero")
filas = [[f"{r.grupo_1} frente a {r.grupo_0.lower()}",
          f"{coma(r.b2, 3)} ({coma(r.ee_b2, 3)})", coma(r.p_b2_holm, 3),
          f"{coma(r.eq_b2, 3)} ({coma(r.eq_ee, 3)})"] for r in inter.itertuples()]
tabla(s, 0.6, 1.85, W - 1.2,
      ["Diferencia", "Nuestra (margen de error)", "p corregido por múltiples comparaciones",
       "Elmira y Qaim (margen de error)"], filas, [4.5, 2.6, 2.4, 2.63], pt=16)
texto(s, 0.6, 5.5, W - 1.2, 0.8,
      [("Cambio en la estatura para la edad por cada duplicación del precio. Nuestros márgenes "
        "de error están agrupados por comunidad; los de Elmira y Qaim, no (cuadro A4 de su suplemento).",
        14, False, GRIS)])

cal = pd.read_csv(TAB / "12_calibracion/ninos_calibracion.csv")
s = lamina(notas="test_calibration del bosque (12_calibracion); p de una cola; EE agrupado por comunidad.")
titulo(s, "Respaldo: la prueba de calibración no encuentra diferencias reales entre niños")
filas = [["Predicción media (≈ 1 si el promedio está bien)", coma(cal.coeficiente[0], 3),
          coma(cal.ee[0], 3), coma(cal.p_unilateral[0], 3)],
         ["Predicción diferencial (> 0 si capta diferencias reales)", coma(cal.coeficiente[1], 3),
          coma(cal.ee[1], 3), coma(cal.p_unilateral[1], 3)]]
tabla(s, 0.6, 2.0, W - 1.2, ["", "Coeficiente", "Margen de error", "p (una cola)"], filas,
      [6.53, 1.9, 1.9, 1.8], pt=18)

per = pd.read_csv(TAB / "13_perfil/ninos_perfil_cuartil_tau.csv")
s = lamina(notas="Perfil por cuartil del efecto predicho (13_perfil). Descriptivo, sin validar.")
titulo(s, "Respaldo: el bosque causal priorizaría sobre todo a los más pequeños")
pct = lambda v: f"{100 * v:.1f} %".replace(".", ",")
filas = [["Efecto predicho medio"] + [coma(v, 3) for v in per.tau_medio],
         ["Edad en 1997 (meses)"] + [coma(v, 1) for v in per.edad_meses],
         ["Urbano"] + [pct(v) for v in per.urbano],
         ["Pobre"] + [pct(v) for v in per.pobre],
         ["Compra arroz"] + [pct(v) for v in per.comprador_neto],
         ["Madre con más que primaria"] + [pct(v) for v in per.madre_mas_primaria]]
tabla(s, 0.6, 1.85, W - 1.2, ["", "Cuartil 1 (más daño predicho)", "Cuartil 2", "Cuartil 3",
                             "Cuartil 4 (menos)"], filas, [3.93, 2.4, 1.9, 1.9, 2.0], pt=16)

sc = pd.read_csv(TAB / "11_gate/ninos_edad_sin_cola_exploratorio.csv")
s = lamina(notas="Exploratorio, fuera de Holm (11_gate).")
titulo(s, "Respaldo: la pista de la edad crece sin los cambios de estatura extremos")
filas = [[r.muestra, coma(r.g1_gate_0_2, 3), coma(r.g1_gate_3_5, 3),
          f"{coma(r.g1_delta, 3)} ({coma(r.g1_ee_delta, 3)})", coma(r.g1_p, 3)]
         for r in sc.itertuples()]
tabla(s, 0.6, 2.0, W - 1.2, ["Muestra", "0-2 años", "3-5 años", "Diferencia (margen de error)",
                             "p sin corregir"], filas, [3.73, 1.8, 1.8, 3.0, 1.8], pt=18)
texto(s, 0.6, 3.9, W - 1.2, 0.8,
      [("Exploratorio: no estaba en el plan y no se corrige por múltiples comparaciones.",
        16, False, GRIS)])

respaldo_figura("Respaldo: curvas de priorización del bosque causal y de las reglas simples",
                FIG / "14_rate/ninos_rate_toc.png",
                "Curvas TOC (14_rate), escala de daño; 834 niños, 98 comunidades de evaluación.")

# pie en todas menos la portada y el separador
for k, s in enumerate(prs.slides, 1):
    if k not in (1, N_PRINCIPALES + 2):
        pie(s, k)

# -----------------------------------------------------------------------------
# Verificaciones en el .pptx: 13 principales, ≥ 12 pt, contraste ≥ 4,5
# -----------------------------------------------------------------------------

assert N_PRINCIPALES == 13, N_PRINCIPALES

def luminancia(h):
    c = [int(h[i:i + 2], 16) / 255 for i in (0, 2, 4)]
    c = [v / 12.92 if v <= 0.03928 else ((v + 0.055) / 1.055) ** 2.4 for v in c]
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]

def contraste(a, b):
    la, lb = sorted([luminancia(a), luminancia(b)], reverse=True)
    return (la + 0.05) / (lb + 0.05)

fallas = []
for k, s in enumerate(prs.slides, 1):
    for sh in s.shapes:
        marcos = [sh.text_frame] if sh.has_text_frame else []
        if sh.has_table:
            marcos += [c.text_frame for f in sh.table.rows for c in f.cells]
        for tf in marcos:
            for p in tf.paragraphs:
                for r in p.runs:
                    if r.text.strip() and (r.font.size is None or r.font.size.pt < 12):
                        fallas.append(f"Lámina {k}: texto < 12 pt: {r.text[:40]!r}")
for k, t, col, fondo in textos:
    if contraste(col, fondo) < 4.5:
        fallas.append(f"Lámina {k}: contraste {contraste(col, fondo):.2f} < 4,5: {t[:40]!r}")
if fallas:
    raise SystemExit("\n".join(fallas))

import json
SALIDA.parent.mkdir(exist_ok=True)
(RENDER.parent / "_cajas.json").write_text(json.dumps(CAJAS))
prs.save(SALIDA)

# -----------------------------------------------------------------------------
# PDF con las fuentes Radio Canada (perfil temporal de LibreOffice) y PNG
# -----------------------------------------------------------------------------

soffice = shutil.which("soffice") or r"C:\Program Files\LibreOffice\program\soffice.exe"
ttf = [str(f) for f in FUENTES.glob("RC*.ttf")]
gdi = None
try:
    import ctypes  # Windows: carga las fuentes solo durante esta sesión, sin instalarlas
    gdi = ctypes.windll.gdi32
    for f in ttf:
        gdi.AddFontResourceW(f)
except (ImportError, AttributeError):
    pass  # en otro sistema, instalar las fuentes o aceptar la sustitución
try:
    with tempfile.TemporaryDirectory() as perfil:  # perfil limpio: relee la lista de fuentes
        carpeta_fuentes = Path(perfil) / "user" / "fonts"  # fuentes propias del perfil (macOS/Linux)
        carpeta_fuentes.mkdir(parents=True)
        for f in ttf:
            shutil.copy(f, carpeta_fuentes)
        subprocess.run([soffice, f"-env:UserInstallation={Path(perfil).as_uri()}", "--headless",
                        "--convert-to", "pdf", "--outdir", str(SALIDA.parent), str(SALIDA)],
                       check=True, capture_output=True)
finally:
    if gdi is not None:
        for f in ttf:
            gdi.RemoveFontResourceW(f)
doc = pymupdf.open(SALIDA.with_suffix(".pdf"))
print("Fuentes en el PDF:", sorted({f[3] for p in doc for f in p.get_fonts()}))
shutil.rmtree(RENDER, ignore_errors=True)
RENDER.mkdir()
for k, p in enumerate(doc, 1):
    p.get_pixmap(dpi=100).save(RENDER / f"lamina{k:02d}.png")

# textos montados o fuera de la página (en el PDF)
def area(r):
    return max(0, r.width) * max(0, r.height)

for k, p in enumerate(doc, 1):
    lineas = []
    for b_i, b in enumerate(p.get_text("dict")["blocks"]):
        for ln in b.get("lines", []):
            t = "".join(sp["text"] for sp in ln["spans"]).strip()
            if t:
                lineas.append((b_i, pymupdf.Rect(ln["bbox"]), t))
    for b_i, r, t in lineas:
        if not p.rect.contains(r):
            fallas.append(f"Lámina {k}: fuera de la página: {t!r}")
    for a in range(len(lineas)):
        for b in range(a + 1, len(lineas)):
            (ba, ra, ta), (bb, rb, tb) = lineas[a], lineas[b]
            if ba != bb and area(ra & rb) > 0.2 * min(area(ra), area(rb)):
                fallas.append(f"Lámina {k}: textos montados: {ta!r} / {tb!r}")
if fallas:
    raise SystemExit("\n".join(fallas))
print(f"{len(doc)} láminas ({N_PRINCIPALES} principales); tamaños, contraste y solapes: OK.")
