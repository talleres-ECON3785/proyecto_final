# =============================================================================
# Construye la presentación final DESDE CERO (16:9, 13,333 × 7,5 in)
# Proyecto final - ECON-3785 (2026-2)
#
# 12 láminas principales + separador «Respaldo» + 8 de respaldo. Figuras de
# 03_Resultados/Figuras/15_figuras_presentacion/ (script 15 del pipeline) y
# tablas nativas leídas de los .csv de 03_Resultados/. La única imagen externa
# es la portada de TIME, que se toma de la base local
# (04_Presentaciones/_fuente/presentacion_base.pptx; no se versiona).
#
# Salidas: 08_Entregables/presentacion_final.{pptx,pdf} y un PNG por lámina en
# 04_Presentaciones/_fuente/_render/. El script FALLA si: algún texto mide
# menos de 12 pt; algún texto tiene contraste < 4,5:1 con su fondo; no hay 12
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
    """parrafos: lista de (texto, pt, negrita, color, fuente, alineación, espacio_antes)."""
    caja = forma if forma is not None else s.shapes.add_textbox(
        Inches(x), Inches(y), Inches(w), Inches(h))
    tf = caja.text_frame
    tf.word_wrap = True
    tf.auto_size = None
    tf.vertical_anchor = anclaje
    for lado in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, lado, Inches(margen))
    for i, p in enumerate(parrafos):
        t, pt, neg, col, fuente, al, antes = (list(p) + [None] * 7)[:7]
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.alignment = al or PP_ALIGN.LEFT
        if antes:
            par.space_before = Pt(antes)
        r = par.add_run()
        r.text = t
        r.font.size = Pt(pt)
        r.font.bold = bool(neg)
        r.font.color.rgb = rgb(col or TEXTO)
        # Radio Canada no trae negrita: lo negrito va en Radio Canada Big Bold
        r.font.name = fuente or (TITULO_F if neg else CUERPO_F)
        textos.append((len(prs.slides), t, col or TEXTO, fondo))
    return caja

def caja_texto(s, x, y, w, h, color, parrafos, anclaje=MSO_ANCHOR.TOP, margen=0.2):
    r = rect(s, x, y, w, h, color)
    return texto(s, 0, 0, 0, 0, parrafos, fondo=color, anclaje=anclaje, forma=r, margen=margen)

def titulo(s, t, y=0.32, h=1.15, w=W - 1.2):
    palabras = [p for p in t.split() if any(c.isalnum() for c in p)]  # «%» no es palabra
    assert len(palabras) <= 15, f"Título de más de 15 palabras: {t}"
    return texto(s, 0.6, y, w, h, [(t, 32, True, TEXTO, TITULO_F)], anclaje=MSO_ANCHOR.MIDDLE)

def figura(s, archivo, x, y, w):
    return s.shapes.add_picture(str(archivo), Inches(x), Inches(y), width=Inches(w))

def como_leer(s, t, y=6.4):
    return texto(s, 0.6, y, W - 1.2, 0.6, [(t, 14, False, GRIS)])

def tabla(s, x, y, w, encabezado, filas, anchos, pt=16):
    n, m = len(filas) + 1, len(encabezado)
    grafo = s.shapes.add_table(n, m, Inches(x), Inches(y), Inches(w), Inches(0.45 * n))
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
    texto(s, 0.6, 7.05, 3.2, 0.32, [("Proyecto final · ECON-3785", 12, False, GRIS)])
    caja = s.shapes.add_textbox(Inches(4.0), Inches(7.05), Inches(5.6), Inches(0.32))
    tf = caja.text_frame
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = Inches(0.05)
    par = tf.paragraphs[0]
    par.alignment = PP_ALIGN.CENTER
    for k, sec in enumerate(SECCIONES):
        actual = sec == s._seccion
        r = par.add_run()
        r.text = sec + ("   ·   " if k < 3 else "")
        r.font.size, r.font.name, r.font.bold = Pt(12), TITULO_F if actual else CUERPO_F, actual
        r.font.color.rgb = rgb(VERDE if actual else GRIS)
        textos.append((numero, sec, VERDE if actual else GRIS, FONDO))
    texto(s, W - 1.6, 7.05, 1.0, 0.32, [(str(numero), 12, False, GRIS, None, PP_ALIGN.RIGHT)])


# -----------------------------------------------------------------------------
# Datos (todas las cifras de resultados salen de los .csv)
# -----------------------------------------------------------------------------

ate = pd.read_csv(TAB / "06_ate/ninos_ate_especificaciones.csv")
a4 = ate.loc[ate.especificacion == 4].iloc[0]
edad = pd.read_csv(TAB / "11_gate/ninos_gate.csv").set_index("id").loc["G1"]
assert coma(a4.beta) == "−0,33" and coma(a4.beta_cm, 1) == "−1,7"
assert coma(edad.gate_0) == "−0,31" and coma(edad.gate_1) == "−0,08"

def portada_time():
    """La portada de TIME (derechos de terceros) se toma de la base local."""
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
texto(s, 0.7, 0.45, ancho_verde - 1.3, 2.8,
      [("¿A quién golpeó más el arroz caro?", 50, True, BLANCO, TITULO_F)], fondo=VERDE_OSC,
      anclaje=MSO_ANCHOR.BOTTOM)
texto(s, 0.7, 3.35, ancho_verde - 1.3, 1.3,
      [("La crisis de 1997-98 en Indonesia, la estatura de los niños y cómo focalizar la ayuda",
        24, False, BLANCO)], fondo=VERDE_OSC)
texto(s, 0.7, 4.65, ancho_verde - 1.3, 0.9,
      [("Para: una agencia que focaliza ayuda ante choques de precios de alimentos",
        20, True, BLANCO)], fondo=VERDE_OSC)
texto(s, 0.7, 5.55, ancho_verde - 1.3, 1.25,
      [("Samuel Escandón · Douglas Plazas · Mateo Olmos · Santiago Muñoz", 20, False, BLANCO),
       ("Ciencia de Datos y Econometría Aplicada · 23-nov-2026", 16, False, BLANCO, None, None, 4)],
      fondo=VERDE_OSC)
texto(s, 0.7, 7.02, ancho_verde - 1.3, 0.35,
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
figura(s, FIG / "15_figuras_presentacion/f1_alza.png", 1.42, 1.45, 10.5)
como_leer(s, "Cómo leer: cada barra cuenta comunidades según cuánto subió allí el precio del arroz "
             "(297 comunidades). El arroz es el alimento básico; la crisis lo encareció de forma desigual.")

# -----------------------------------------------------------------------------
# 3. Lo que se sabe
# -----------------------------------------------------------------------------

s = lamina("Contexto", """Presentador 1 · 90 s

Dos estudios usaron estos mismos datos y llegaron a conclusiones distintas.

Elmira y Qaim, en 2026, encuentran que cuando el precio del arroz se duplicaba, la estatura de los niños para su edad bajaba 0,135 desviaciones estándar, y más en las ciudades.

Frankenberg y Thomas, en 2017, comparando zonas urbanas y rurales, no encuentran daño en la estatura.

Ninguno de los dos pregunta lo que necesita la agencia: a quién proteger primero. Por eso nos hacemos tres preguntas. Uno: ¿los niños de comunidades donde el arroz subió más crecieron menos? Dos: ¿a algunos niños les afectó más, según su edad, sexo, pobreza, zona, la educación de su madre o si compraban arroz? Tres: ¿un algoritmo de aprendizaje automático encuentra a los más afectados mejor que una regla simple?""")
titulo(s, "Dos estudios con estos datos no coinciden, y nadie ha probado a quién proteger primero")
caja_texto(s, 0.6, 1.55, 5.9, 2.25, TINTE,
           [("Elmira y Qaim (2026)", 22, True, TEXTO, TITULO_F),
            ("El alza redujo la estatura: −0,135 desviaciones estándar por cada duplicación "
             "del precio, y más en zonas urbanas.", 20, False, TEXTO, None, None, 6)])
caja_texto(s, 6.83, 1.55, 5.9, 2.25, TINTE,
           [("Frankenberg y Thomas (2017)", 22, True, TEXTO, TITULO_F),
            ("Comparando zonas urbanas y rurales: sin daño en la estatura de los niños.",
             20, False, TEXTO, None, None, 6)])
caja_texto(s, 0, 3.98, W, 2.85, VERDE,
           [("Nuestras tres preguntas", 22, True, BLANCO, TITULO_F),
            ("1. ¿Los niños de las comunidades donde el arroz subió más crecieron menos?",
             20, False, BLANCO, None, None, 8),
            ("2. ¿Hubo niños a los que el alza afectó más, según su edad, sexo, pobreza, zona, "
             "educación de la madre o compra de arroz?", 20, False, BLANCO, None, None, 6),
            ("3. ¿Un algoritmo de aprendizaje automático encuentra a los niños más afectados "
             "mejor que una regla simple?", 20, False, BLANCO, None, None, 6)],
           anclaje=MSO_ANCHOR.MIDDLE, margen=0.6)

# -----------------------------------------------------------------------------
# 4. Cómo lo medimos
# -----------------------------------------------------------------------------

s = lamina("Método", """Presentador 1 · 90 s

¿Cómo lo medimos? Usamos la Encuesta de Vida Familiar de Indonesia. Medimos a los niños de 0 a 5 años en 1997, antes del alza, y los volvimos a medir en 2000. Entre una medición y otra, el arroz subió más en unas comunidades que en otras.

Para cada niño calculamos cuánto cambió su estatura para la edad. Esa medida compara la estatura del niño con la de niños sanos de su misma edad y sexo, según la referencia de la Organización Mundial de la Salud. Menos uno quiere decir una desviación estándar por debajo; en estos niños, una desviación estándar son unos 5 centímetros.

Son 2.421 niños en 294 comunidades. Dos aclaraciones: fijamos los grupos y las pruebas antes de ver los resultados; y medimos el efecto de más alza frente a menos alza, no el de la crisis completa, porque todas las comunidades la vivieron.""")
titulo(s, "Seguimos a 2.421 niños y comparamos comunidades con más y menos alza")
pasos = [("1997", "Medimos la estatura de cada niño de 0 a 5 años"),
         ("1997-2000", "El arroz sube más en unas comunidades que en otras"),
         ("2000", "Volvemos a medir a los mismos niños")]
for k, (anio, desc) in enumerate(pasos):
    x = 0.6 + k * 4.3
    caja_texto(s, x, 1.55, 3.65, 1.65, VERDE,
               [(anio, 24, True, BLANCO, TITULO_F, PP_ALIGN.CENTER),
                (desc, 20, False, BLANCO, None, PP_ALIGN.CENTER, 4)],
               anclaje=MSO_ANCHOR.MIDDLE, margen=0.15)
    if k < 2:
        rect(s, x + 3.72, 2.15, 0.5, 0.44, GRIS, MSO_SHAPE.RIGHT_ARROW)
texto(s, 0.6, 3.35, W - 1.2, 0.55,
      [("Cambio en la estatura de cada niño: 2.421 niños en 294 comunidades.",
        22, True, TEXTO)])
caja_texto(s, 0.6, 4.0, 6.9, 2.75, TINTE,
           [("¿Qué es la estatura para la edad?", 22, True, TEXTO, TITULO_F),
            ("Compara la estatura del niño con la de niños sanos de su misma edad y sexo "
             "(referencia de la OMS), en desviaciones estándar.", 20, False, TEXTO, None, None, 6),
            ("Ejemplo: −1 es una desviación estándar por debajo; en estos niños, unos 5 cm.",
             20, False, TEXTO, None, None, 6)])
texto(s, 7.85, 4.0, 4.9, 2.75,
      [("Fijamos los grupos y las pruebas antes de ver los resultados.", 20, True, TEXTO),
       ("Medimos el efecto de más alza frente a menos alza, no el de la crisis completa.",
        20, False, TEXTO, None, None, 14)])

# -----------------------------------------------------------------------------
# 5. Respuesta 1
# -----------------------------------------------------------------------------

lo, hi = a4.beta - 1.96 * a4.ee_agrupado, a4.beta + 1.96 * a4.ee_agrupado
s = lamina("Resultados", f"""Presentador 2 · 150 s

Primera respuesta: sí. Donde el arroz subió más, los niños crecieron menos.

En el eje horizontal está cuánto cambia la estatura para la edad por cada vez que el precio se duplica; más a la izquierda es más daño. El punto verde es nuestra estimación: {coma(a4.beta)} desviaciones estándar, unos {coma(-a4.beta_cm, 1)} centímetros. La línea es el rango plausible: con 95 % de confianza, el efecto está entre {coma(lo)} y {coma(hi)}.

El punto gris es Elmira y Qaim: −0,135. Nuestro efecto es mayor, pero los rangos se traslapan, así que no son incompatibles. Ellos miden el precio con fuentes distintas en cada año y no comparan comunidades dentro de la misma provincia; nosotros sí.

Un detalle técnico: nuestro margen de error tiene en cuenta que los niños de una misma comunidad se parecen entre sí; el de ellos no. Por eso nuestro rango es más ancho.""")
titulo(s, "Sí: donde el arroz subió más, los niños crecieron menos")
figura(s, FIG / "15_figuras_presentacion/f2_efecto_principal.png", 1.42, 1.45, 10.5)
como_leer(s, "Cómo leer: cada punto es el efecto promedio; la línea, su rango plausible al 95 %. "
             "Más a la izquierda = más daño. 2.421 niños en 294 comunidades.")

# -----------------------------------------------------------------------------
# 6. Qué tan sólido
# -----------------------------------------------------------------------------

s = lamina("Resultados", """Presentador 2 · 150 s

¿Qué tan sólido es este resultado? Repetimos la estimación cambiando una cosa a la vez: sin las comunidades medidas en 1998, con los pesos de la encuesta, sin recortar las alzas extremas, solo con precios por kilo y sin los niños con cambios de estatura extremos, que parecen errores de medición.

Todas las estimaciones quedan a la izquierda del cero: la dirección se sostiene. Pero el tamaño va de −0,20 a −0,50: el número exacto es incierto.

Abajo, en naranja, está el placebo: miramos cómo crecieron niños entre 1993 y 1997, antes del alza. Si las comunidades con más alza no tenían nada especial antes, debería dar cero. No se distingue de cero, pero tampoco lo podemos descartar: podría haber una tendencia previa. Lo decimos tal cual.""")
titulo(s, "La dirección se sostiene en todas las pruebas; el tamaño exacto no")
figura(s, FIG / "15_figuras_presentacion/f3_robustez.png", 1.42, 1.45, 10.5)
como_leer(s, "Cómo leer: cada fila repite el cálculo cambiando una cosa. Todas quedan a la izquierda "
             "de cero; el placebo (antes del alza) debería estar en cero.")

# -----------------------------------------------------------------------------
# 7. Respuesta 2
# -----------------------------------------------------------------------------

s = lamina("Resultados", """Presentador 3 · 100 s

Segunda pregunta: ¿a quién le dolió más? Antes de ver los datos fijamos seis comparaciones: edad, zona, educación de la madre, sexo, si la familia compra o produce su arroz, y pobreza.

Cada panel compara dos grupos. El punto es el daño estimado en cada grupo, comparando el tercio de comunidades con más alza contra el tercio con menos; la línea es su rango plausible. En los doce grupos el punto queda a la izquierda del cero: todos se vieron afectados.

Pero los grupos de cada panel se parecen mucho: las diferencias son pequeñas frente a su margen de error. Tras corregir por hacer muchas comparaciones a la vez, ninguna diferencia es clara. Tampoco confirmamos que el daño fuera mayor en las ciudades, como dicen Elmira y Qaim; ni lo descartamos.""")
titulo(s, "Todos los grupos se vieron afectados; no encontramos uno al que le doliera claramente más")
figura(s, FIG / "15_figuras_presentacion/f4_grupos.png", 1.42, 1.45, 10.5)
como_leer(s, "Cómo leer: punto = daño en cada grupo; línea = rango plausible. Tampoco confirmamos que el "
             "daño fuera mayor en zonas urbanas, como reportan Elmira y Qaim, ni lo descartamos.")

# -----------------------------------------------------------------------------
# 8. La única pista
# -----------------------------------------------------------------------------

s = lamina("Resultados", f"""Presentador 3 · 100 s

La única pista está en la edad. Los niños que tenían 0 a 2 años en 1997 muestran más daño, {coma(edad.gate_0)}, que los de 3 a 5 años, {coma(edad.gate_1)}. Pero ojo: esto es exploratorio.

¿Por qué no lo afirmamos? Por la precisión. En el gráfico, la barra verde es el daño promedio del alza: 0,18 desviaciones estándar, comparando el tercio de comunidades con más alza contra el de menos. La barra naranja es la menor diferencia entre dos grupos que nuestros datos alcanzarían a detectar: entre 0,36 y 0,44, el doble del daño promedio. Es un cálculo aproximado.

Con unos cientos de comunidades, solo veríamos diferencias muy grandes. Así que "no encontramos diferencias" no quiere decir "el daño fue igual para todos".""")
titulo(s, "Los menores de 3 años quizá sufrieron más, pero los datos no alcanzan para afirmarlo")
figura(s, FIG / "15_figuras_presentacion/f5_potencia.png", 0.6, 1.55, 8.2)
caja_texto(s, 9.15, 1.6, 3.6, 0.5, VERDE_OSC,
           [("Exploratorio", 20, True, BLANCO, TITULO_F, PP_ALIGN.CENTER)],
           anclaje=MSO_ANCHOR.MIDDLE, margen=0.05)
texto(s, 9.15, 2.3, 3.6, 3.9,
      [("0-2 años", 22, True, TEXTO),
       (coma(edad.gate_0), 54, True, TEXTO, TITULO_F),
       ("3-5 años", 22, True, TEXTO, None, None, 12),
       (coma(edad.gate_1), 54, True, TEXTO, TITULO_F),
       ("desviaciones estándar (más alza frente a menos alza)", 20, False, TEXTO, None, None, 8)])
como_leer(s, "Cómo leer: la barra naranja es la menor diferencia entre dos grupos que estos datos "
             "detectarían (aproximada); es el doble del daño promedio.")

# -----------------------------------------------------------------------------
# 9. Respuesta 3
# -----------------------------------------------------------------------------

s = lamina("Resultados", """Presentador 3 · 100 s

Tercera pregunta: ¿un algoritmo de aprendizaje automático encuentra a los más afectados mejor que una regla simple? Usamos un bosque causal, que busca por su cuenta a quién afectó más.

La prueba simula a la agencia: si atiende primero a los niños que señala cada regla, ¿esos niños sufrieron más que el promedio? Entrenamos el algoritmo en la mitad de las comunidades y lo evaluamos en la otra mitad.

Más a la derecha es mejor. La línea vertical es no hacerlo mejor que escoger al azar. El algoritmo, y también las reglas de pobreza, zona urbana y compra de arroz, tienen rangos que cruzan esa línea: ninguna se distingue de escoger al azar, y ninguna supera a las otras. La prueba de calibración del algoritmo tampoco encuentra diferencias reales entre niños.""")
titulo(s, "Un algoritmo no encuentra a los más afectados mejor que una regla simple")
figura(s, FIG / "15_figuras_presentacion/f6_focalizacion.png", 1.42, 1.45, 10.5)
como_leer(s, "Cómo leer: si la agencia atiende primero a quien señala cada regla, ¿esos niños sufrieron "
             "más que el promedio? La calibración del algoritmo tampoco encuentra diferencias entre niños.")

# -----------------------------------------------------------------------------
# 10. Recomendación
# -----------------------------------------------------------------------------

s = lamina("Recomendación", """Presentador 4 · 110 s

¿Qué le recomendamos a la agencia? Focalizar por comunidad, no por hogar.

Hacer: vigilar el alza del precio del arroz comunidad por comunidad, que es lo que sí se asocia con menos crecimiento, y cubrir a todos los niños pequeños de las comunidades donde más sube.

No hacer: usar un algoritmo para escoger a quién ayudar dentro de la comunidad, ni dejar fuera a los niños no pobres o rurales: con esta evidencia, no sabemos que hayan sufrido menos.

Por confirmar: los menores de 3 años. Es la única pista, pero no alcanza para convertirla en regla; habría que comprobarla con más datos.""")
titulo(s, "Focalice por comunidad, no por hogar")
columnas = [("Hacer", VERDE, BLANCO,
             ["Vigilar el alza del arroz por comunidad.",
              "Cubrir a todos los niños pequeños donde más sube."]),
            ("No hacer", VERDE_OSC, BLANCO,
             ["Escoger con un algoritmo dentro de la comunidad.",
              "Excluir a los no pobres o a los rurales."]),
            ("Por confirmar", TINTE, TEXTO,
             ["Los menores de 3 años: una pista, no una regla."])]
for k, (enc, fondo, col, items) in enumerate(columnas):
    caja_texto(s, 0.6 + k * 4.1, 1.7, 3.85, 4.2, fondo,
               [(enc, 28, True, col, TITULO_F)] +
               [(it, 22, False, col, None, None, 14) for it in items], margen=0.3)

# -----------------------------------------------------------------------------
# 11. Aporte y límites
# -----------------------------------------------------------------------------

s = lamina("Recomendación", """Presentador 4 · 110 s

¿Qué añadimos? Primero, replicamos el resultado de Elmira y Qaim con errores que tienen en cuenta que los niños de una misma comunidad se parecen. Segundo, fijamos los grupos antes de mirar y corregimos por hacer muchas comparaciones a la vez. Tercero, hasta donde revisamos, es la primera prueba de si un algoritmo focaliza mejor que reglas simples ante este choque.

¿Qué no podemos afirmar? Puede haber una tendencia previa, porque el placebo no es concluyente. Puede haber otros choques al mismo tiempo, como la sequía de El Niño o el humo de los incendios. En las comunidades donde más subió el arroz se midió a menos niños en 1997. El tamaño del efecto cambia con los valores extremos. Y tenemos poca precisión para comparar grupos.""")
titulo(s, "Qué añadimos y qué no podemos afirmar")
caja_texto(s, 0.6, 1.6, 5.9, 5.1, TINTE,
           [("Qué añadimos", 26, True, TEXTO, TITULO_F),
            ("Réplica con errores agrupados por comunidad.", 20, False, TEXTO, None, None, 12),
            ("Grupos fijados de antemano y corregidos por hacer muchas comparaciones a la vez.",
             20, False, TEXTO, None, None, 10),
            ("Primera prueba, hasta donde revisamos, de si un algoritmo focaliza mejor que "
             "reglas simples ante este choque.", 20, False, TEXTO, None, None, 10)], margen=0.3)
caja_texto(s, 6.83, 1.6, 5.9, 5.1, VERDE_OSC,
           [("Qué no podemos afirmar", 26, True, BLANCO, TITULO_F),
            ("Puede haber una tendencia previa.", 20, False, BLANCO, None, None, 12),
            ("Otros choques al mismo tiempo (sequía, humo).", 20, False, BLANCO, None, None, 8),
            ("Menos niños medidos donde más subió el arroz.", 20, False, BLANCO, None, None, 8),
            ("El tamaño cambia con los valores extremos.", 20, False, BLANCO, None, None, 8),
            ("Poca precisión para comparar grupos.", 20, False, BLANCO, None, None, 8)], margen=0.3)

# -----------------------------------------------------------------------------
# 12. Cierre
# -----------------------------------------------------------------------------

s = lamina("Recomendación", """Presentador 4 · 80 s

Para cerrar, tres preguntas y tres respuestas.

¿Los niños de las comunidades donde el arroz subió más crecieron menos? Sí: cerca de 1,7 centímetros menos por cada vez que el precio se duplicó, aunque el tamaño exacto es incierto.

¿Hubo niños a los que les afectó más? Todos se vieron afectados; la edad es la única pista, y no alcanza para afirmarla.

¿Un algoritmo encuentra mejor a los más afectados? No: una regla simple funciona igual de bien.

Gracias. Quedamos atentos a sus preguntas.""")
titulo(s, "Tres preguntas, tres respuestas")
qa = [("¿Los niños de las comunidades donde el arroz subió más crecieron menos?",
       "Sí, crecieron menos (≈ 1,7 cm por cada duplicación del precio), con incertidumbre sobre el tamaño exacto."),
      ("¿Hubo niños a los que el alza afectó más?",
       "Todos se vieron afectados; la edad es la única pista."),
      ("¿Un algoritmo encuentra a los más afectados mejor que una regla simple?",
       "No: una regla simple funciona igual de bien.")]
for k, (q, a) in enumerate(qa):
    y = 1.55 + k * 1.45
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
# Respaldo
# -----------------------------------------------------------------------------

s = lamina(notas="Respaldo: no cuenta en los 20 minutos.")
rect(s, 0, 0, W, H, VERDE_OSC)
texto(s, 0.8, 2.9, W - 1.6, 1.5, [("Respaldo", 54, True, BLANCO, TITULO_F)], fondo=VERDE_OSC,
      anclaje=MSO_ANCHOR.MIDDLE)

def respaldo_figura(t, archivo, notas):
    s = lamina(notas=notas)
    titulo(s, t)
    pic = s.shapes.add_picture(str(archivo), 0, Inches(1.5), height=Inches(5.45))
    pic.left = int((prs.slide_width - pic.width) / 2)
    return s

respaldo_figura("Respaldo: el algoritmo compara niños con probabilidades parecidas de estar en cada grupo",
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
tabla(s, 0.6, 1.6, W - 1.2, ["", "(1)", "(2)", "(3)", "(4)"], filas,
      [5.13, 1.75, 1.75, 1.75, 1.75], pt=16)

inter = pd.read_csv(TAB / "09_interacciones_eq/ninos_interacciones_eq.csv")
inter = inter[(inter.ee == "agrupado") & (inter.especificacion == 4)]
s = lamina(notas="Interacciones de Elmira y Qaim (09_interacciones_eq), especificación 4, Holm F2.")
titulo(s, "Respaldo: ninguna de las cinco diferencias de Elmira y Qaim se distingue de cero")
filas = [[f"{r.grupo_1} frente a {r.grupo_0.lower()}",
          f"{coma(r.b2, 3)} ({coma(r.ee_b2, 3)})", coma(r.p_b2_holm, 3),
          f"{coma(r.eq_b2, 3)} ({coma(r.eq_ee, 3)})"] for r in inter.itertuples()]
tabla(s, 0.6, 1.6, W - 1.2,
      ["Diferencia", "Nuestra (margen de error)", "p corregido por múltiples comparaciones",
       "Elmira y Qaim (margen de error)"], filas, [4.5, 2.6, 2.4, 2.63], pt=16)
texto(s, 0.6, 5.3, W - 1.2, 0.8,
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
tabla(s, 0.6, 1.8, W - 1.2, ["", "Coeficiente", "Margen de error", "p (una cola)"], filas,
      [6.53, 1.9, 1.9, 1.8], pt=18)

per = pd.read_csv(TAB / "13_perfil/ninos_perfil_cuartil_tau.csv")
s = lamina(notas="Perfil por cuartil del efecto predicho (13_perfil). Descriptivo, sin validar.")
titulo(s, "Respaldo: el algoritmo priorizaría sobre todo a los más pequeños")
pct = lambda v: f"{100 * v:.1f} %".replace(".", ",")
filas = [["Efecto predicho medio"] + [coma(v, 3) for v in per.tau_medio],
         ["Edad en 1997 (meses)"] + [coma(v, 1) for v in per.edad_meses],
         ["Urbano"] + [pct(v) for v in per.urbano],
         ["Pobre"] + [pct(v) for v in per.pobre],
         ["Compra arroz"] + [pct(v) for v in per.comprador_neto],
         ["Madre con más que primaria"] + [pct(v) for v in per.madre_mas_primaria]]
tabla(s, 0.6, 1.6, W - 1.2, ["", "Cuartil 1 (más daño predicho)", "Cuartil 2", "Cuartil 3",
                             "Cuartil 4 (menos)"], filas, [3.93, 2.4, 1.9, 1.9, 2.0], pt=16)

sc = pd.read_csv(TAB / "11_gate/ninos_edad_sin_cola_exploratorio.csv")
s = lamina(notas="Exploratorio, fuera de Holm (11_gate).")
titulo(s, "Respaldo: la pista de la edad crece sin los cambios de estatura extremos")
filas = [[r.muestra, coma(r.g1_gate_0_2, 3), coma(r.g1_gate_3_5, 3),
          f"{coma(r.g1_delta, 3)} ({coma(r.g1_ee_delta, 3)})", coma(r.g1_p, 3)]
         for r in sc.itertuples()]
tabla(s, 0.6, 1.8, W - 1.2, ["Muestra", "0-2 años", "3-5 años", "Diferencia (margen de error)",
                             "p sin corregir"], filas, [3.73, 1.8, 1.8, 3.0, 1.8], pt=18)
texto(s, 0.6, 3.7, W - 1.2, 0.8,
      [("Exploratorio: no estaba en el plan y no se corrige por múltiples comparaciones.",
        16, False, GRIS)])

respaldo_figura("Respaldo: curvas de priorización del algoritmo y de las reglas simples",
                FIG / "14_rate/ninos_rate_toc.png",
                "Curvas TOC (14_rate), escala de daño; 834 niños, 98 comunidades de evaluación.")

# pie en todas menos la portada y el separador
for k, s in enumerate(prs.slides, 1):
    if k not in (1, N_PRINCIPALES + 1):
        pie(s, k)

# -----------------------------------------------------------------------------
# Verificaciones en el .pptx: 12 principales, ≥ 12 pt, contraste ≥ 4,5
# -----------------------------------------------------------------------------

assert N_PRINCIPALES == 12, N_PRINCIPALES

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

SALIDA.parent.mkdir(exist_ok=True)
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
