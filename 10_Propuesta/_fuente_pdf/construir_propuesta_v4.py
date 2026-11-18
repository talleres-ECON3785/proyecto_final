# -*- coding: utf-8 -*-
"""Construye propuesta_borrador.pdf (versión 4) con ReportLab.

Uso: python construir_propuesta_v4.py <carpeta_figuras> <salida.pdf>
Primero: python figuras_v4.py <carpeta_figuras>
"""
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
                                KeepTogether, PageBreak, ListFlowable, ListItem)

FIG = Path(sys.argv[1] if len(sys.argv) > 1 else "fig")
SALIDA = sys.argv[2] if len(sys.argv) > 2 else "propuesta_borrador.pdf"

D = "/usr/share/fonts/truetype/liberation/"
pdfmetrics.registerFont(TTFont("DV", D + "LiberationSerif-Regular.ttf"))
pdfmetrics.registerFont(TTFont("DVB", D + "LiberationSerif-Bold.ttf"))
pdfmetrics.registerFont(TTFont("DVI", D + "LiberationSerif-Italic.ttf"))
pdfmetrics.registerFont(TTFont("DVBI", D + "LiberationSerif-BoldItalic.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVBI")

AZUL = colors.black
GRIS = colors.HexColor("#666666")
AZUL_C = colors.HexColor("#DCE8F5")

st = {
    "titulo": ParagraphStyle("t", fontName="DV", fontSize=15, leading=19, alignment=TA_CENTER, spaceAfter=8),
    "autor": ParagraphStyle("au", fontName="DV", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceAfter=12),
    "abs": ParagraphStyle("ab", fontName="DV", fontSize=9, leading=11.5, alignment=TA_JUSTIFY, leftIndent=1.4*cm, rightIndent=1.4*cm, spaceAfter=4),
    "sub": ParagraphStyle("s", fontName="DV", fontSize=8.5, leading=11, textColor=colors.black, alignment=TA_CENTER, spaceAfter=10),
    "h1": ParagraphStyle("h1", fontName="DV", fontSize=9.5, leading=12, alignment=TA_CENTER, spaceBefore=12, spaceAfter=6, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="DVI", fontSize=10.5, leading=13, spaceBefore=6, spaceAfter=2),
    "p": ParagraphStyle("p", fontName="DV", fontSize=10.5, leading=13.6, alignment=TA_JUSTIFY, firstLineIndent=14, spaceAfter=0),
    "bul": ParagraphStyle("b", fontName="DV", fontSize=10.3, leading=13.2, alignment=TA_JUSTIFY),
    "cap": ParagraphStyle("c", fontName="DV", fontSize=8.5, leading=10.5, alignment=TA_JUSTIFY, spaceAfter=10),
    "tcap": ParagraphStyle("tc", fontName="DV", fontSize=9, leading=11, alignment=TA_CENTER, spaceAfter=4),
    "tab": ParagraphStyle("tb", fontName="DV", fontSize=8.4, leading=10.2),
    "tabh": ParagraphStyle("th", fontName="DVI", fontSize=8.4, leading=10.2),
    "ref": ParagraphStyle("r", fontName="DV", fontSize=8.8, leading=11, leftIndent=12, firstLineIndent=-12, spaceAfter=2, alignment=TA_JUSTIFY),
    "nota": ParagraphStyle("n", fontName="DV", fontSize=8.3, leading=10.3, alignment=TA_JUSTIFY),
}

ROMANOS = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]
_sec = [0]


def SEC(t):
    _sec[0] += 1
    return Paragraph(f"{ROMANOS[_sec[0]-1]}. {t.upper()}", st["h1"])


def P(t, s="p"):
    return Paragraph(t, st[s])


def bullets(items):
    return ListFlowable([ListItem(P(t, "bul"), leftIndent=10, value="•") for t in items],
                        bulletType="bullet", bulletFontSize=7, leftIndent=10, spaceBefore=0, spaceAfter=5)


def figura(nombre, ancho_cm, caption):
    ruta = FIG / nombre
    from PIL import Image as PI
    w, h = PI.open(ruta).size
    ancho = ancho_cm * cm
    import re as _re
    caption = _re.sub(r"^Figura (\d+)\. ", lambda m: f"F<font size=7>IGURA</font> {m.group(1)}. ", caption)
    return KeepTogether([Spacer(1, 4), Image(str(ruta), width=ancho, height=ancho * h / w), Spacer(1, 3), P(caption, "cap")])


_tab = [0]


def tabla(filas, anchos, titulo="", cabecera=True):
    _tab[0] += 1
    datos = [[P(c, "tabh" if (i == 0 and cabecera) else "tab") for c in f] for i, f in enumerate(filas)]
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1 if cabecera else 0)
    n = len(datos)
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEABOVE", (0, 0), (-1, 0), 0.8, colors.black),
                           ("LINEBELOW", (0, 0), (-1, 0), 0.4, colors.black),
                           ("LINEBELOW", (0, n - 1), (-1, n - 1), 0.8, colors.black),
                           ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                           ("TOPPADDING", (0, 0), (-1, -1), 2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
    cab = Paragraph(f"T<font size=7>ABLA</font> {_tab[0]}—{titulo}", st["tcap"])
    return KeepTogether([Spacer(1, 4), cab, t, Spacer(1, 8)])


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFont("DV", 8)
    if doc.page > 1:
        canvas.drawCentredString(letter[0] / 2, letter[1] - 1.25 * cm, "BORRADOR DE PROPUESTA · ECON-3785 · NOVIEMBRE 2026")
    canvas.drawCentredString(letter[0] / 2, 1.2 * cm, str(doc.page))
    canvas.restoreState()


H = []
H += [P("¿A quién golpeó más el arroz caro? Efectos heterogéneos de largo plazo de la crisis de 1997-98 en Indonesia", "titulo"),
      P("Por E<font size=7>QUIPO DEL PROYECTO FINAL</font>, ECON-3785*", "autor"),
      P("<i>Proponemos estimar quién cargó con las consecuencias de largo plazo del alza del precio del arroz durante la crisis "
        "indonesia de 1997-98. Con la Indonesia Family Life Survey replicamos el efecto promedio sobre la talla de los niños, lo "
        "llevamos a la escolaridad completada en 2014 y estimamos efectos condicionales con bosques y árboles causales honestos, "
        "con conglomerados por comunidad. La literatura encontró la heterogeneidad con subgrupos elegidos a mano; proponemos una "
        "prueba global de heterogeneidad, contrastes pre-declarados sobre la posición del hogar en el mercado de arroz, sus activos "
        "y su composición, una prueba de recuperación del subgrupo más citado y una comparación formal de reglas de focalización "
        "para una agencia de asistencia alimentaria.</i>", "abs"),
      P("(JEL C21, I15, I21, O12, O15)", "sub"),
      ]
# 1
H += [SEC("Pregunta y cliente"),
      P("Entre 1997 y 1998 la rupia se desplomó, se retiraron subsidios y el precio del arroz, el alimento básico de Indonesia, "
        "subió con fuerza y de forma desigual entre comunidades. La pregunta es: <b>¿quiénes cargaron, años después, con las "
        "consecuencias de haber vivido donde el arroz subió más, y qué características de 1997 predicen un daño mayor?</b> "
        "El resultado primario es la escolaridad completada en 2014; la estatura (talla-para-edad 1997-2000) es el ancla de "
        "replicación; la estatura adulta y la cognición son secundarias. La salud mental queda como extensión opcional."),
      P("<b>Cliente propuesto:</b> una agencia que deba focalizar ayuda ante choques de precios de alimentos (por ejemplo, el "
        "Programa Mundial de Alimentos). <b>Entregable:</b> una regla simple y defendible de qué hogares proteger primero, con "
        "variables que la agencia puede observar, y la evidencia de cuánto daño evita frente a la regla habitual de focalizar en "
        "los pobres.")]

# 2
H += [SEC("El efecto promedio: replicable, pero en disputa"),
      P("Elmira y Qaim (2026) usan el cambio del precio del arroz 1997-2000 en las 312 comunidades de la Indonesia Family Life "
        "Survey (IFLS). Con efectos fijos individuales, un alza de 100 % reduce la talla-para-edad (HAZ) en 0,135 desviaciones "
        "estándar (0,251 con precio real) y eleva el retraso en talla en 3,5 puntos (p. 1 y 5). En 2014 encuentran 0,65 cm menos "
        "de estatura adulta, que interpretan como asociación (p. 5-6). Frankenberg y Thomas (2017), sin precios y con la zona "
        "urbana como proxy del choque (p. 12), no encuentran daño en estatura. En escolaridad completada en 2014 tampoco lo hay "
        "para las cohortes de 7-12 ni de 13-16 años (+0,002 años, EE 0,17; nota 1), con una excepción: la cohorte de 8 años, "
        "urbana y del cuartil más pobre, pierde 1,95 años (EE 0,63). Con efectos fijos de hogar la pérdida baja a 1,24 (EE 0,69), "
        "significativa solo al 10 % (cuadro 3). Reconciliar ambos con una misma exposición es parte del aporte; un nulo bien "
        "documentado es un resultado válido.")]

# 3
H += [SEC("Lo que se sabe de quién cargó con el choque, y lo que falta"),
      P("La literatura coincide en que el choque fue «devastador para unos hogares y una oportunidad para otros» (Frankenberg, "
        "Smith y Thomas 2003, p. 280); un tercio de los hogares tenía más gasto per cápita en 1998 que en 1997 (p. 295). La figura "
        "1 ordena los hallazgos por dimensión. Tres cosas saltan a la vista: la dimensión urbana es la más consistente; la posición "
        "como comprador o productor de arroz, el oro y la composición del hogar tienen buena teoría pero <b>nunca se han probado "
        "como modificadores del efecto sobre los niños</b>; y la pobreza y la edad dan señales contradictorias según el resultado."),
      P("<b>Patrón metodológico común.</b> Todos hallaron la heterogeneidad con subgrupos elegidos a mano: una interacción binaria "
        "a la vez (Elmira y Qaim, ecuación 2), celdas edad × zona × cuartil frente a una tendencia (Frankenberg y Thomas, figura 7: "
        "17 edades × 4 grupos) o interacciones del choque por zona (Frankenberg, Smith y Thomas, cuadros 8-9). Ninguno hace una "
        "prueba global de heterogeneidad ni corrige por todo lo que miró. De ahí salen cinco vacíos:"),
      tabla([["#", "Vacío", "Cómo lo atacamos"],
             ["V1", "Ninguna prueba global de heterogeneidad para este choque", "Prueba de calibración del bosque causal; si no rechaza, lo reportamos"],
             ["V2", "La posición neta en arroz no se ha probado como modificador del efecto sobre los niños (Elmira y Qaim no la usan, aunque explican lo urbano por la dependencia de las compras, p. 5)",
              "Covariable del bosque, efecto por grupo y comparación comprador–productor dentro de la comunidad"],
             ["V3", "Oro, tierra, hermanos y mujeres mayores suavizaron el consumo (FST p. 313, 316-317; F-T 2017 p. 9-11), pero no se han estudiado como protección de los niños",
              "Modificadores pre-declarados H7-H8"],
             ["V4", "La cohorte urbana pobre de 8 años es una celda hallada a mano entre ~68",
              "Prueba de recuperación con otra exposición (el precio) + bosque placebo"],
             ["V5", "Nadie compara reglas de focalización; Elmira y Qaim sugieren que focalizar en pobres «puede no bastar» (p. 5 y 7)",
              "RATE/TOC: regla del bosque frente a «pobre», «urbano» y «comprador neto»"]],
            [0.8, 8.4, 7.3], "Vacíos en la literatura y cómo los atacamos"),
      Spacer(1, 6),
      figura("f2_mapa_evidencia.png", 15.8,
             "Figura 1. Mapa de la evidencia sobre heterogeneidad, cotejado con los PDF (página o cuadro en cada celda). "
             "Cada estudio usa una exposición y un resultado distintos.")]

# 4
H += [SEC("Datos"),
      P("La IFLS es un panel público (registro gratuito en RAND) que sigue a los mismos individuos desde 1993 en 13 provincias "
        "(cerca del 83 % de la población). Las cinco olas ya se revisaron archivo por archivo. Los tamaños que siguen salen de esa "
        "revisión, no de la documentación."),
      figura("f1_olas.png", 15.5, "Figura 2. Olas de la IFLS y cohortes del proyecto. Parte de la ola de 1997 se levantó en 1998 (627 hogares)."),
      tabla([["Muestra", "1997", "2014", "Uso"],
             ["Cohorte de 0-5 años en 1997 con talla", "3.217", "2.586", "Ancla ΔHAZ (2000: 3.422); estatura adulta"],
             ["Cohorte de 0-5 años con pruebas cognitivas completas (EK)", "—", "2.535", "Secundario"],
             ["Cohortes de 5-21 años: miembros / con escolaridad en 2014", "12.632", "7.925", "<b>Primario</b>"],
             ["Comunidades con precio del arroz (commid97)", "312", "—", "Tratamiento y conglomerado"]],
            [7.2, 1.6, 1.6, 6.1], "Tamaños de muestra (revisión de los datos)"),
      Spacer(1, 4),
      bullets(["<b>Tratamiento:</b> precio del arroz por comunidad en 1997 y 2000. Dos construcciones: una principal (mediana de las "
               "fuentes presentes en ambos años, posyandu y mercado, calidad media, en kg) y otra que replica a Elmira y Qaim (promedio "
               "de todas las fuentes y calidades). El libro PKK de 2000 no tiene precios, y 27 comunidades tienen el de 1997 levantado en 1998.",
               "<b>Covariables de 1997:</b> zona, educación de los padres, gasto per cápita (agregado propio), compra frente a producción "
               "propia de arroz (5.075 hogares compran, 1.511 producen, 193 ambas cosas), oro, tierra, composición del hogar, choques "
               "(pérdida de cosecha por sequía) y precio del arroz en 1997.",
               "<b>Restricción de licencia:</b> los datos no se redistribuyen; la entrega lleva código e instrucciones de descarga."])]

# 5
H += [SEC("Estrategia empírica"),
      P("Comparamos a quienes en 1997 vivían en comunidades del tercil alto del alza del arroz con los del tercil bajo, ajustando "
        "por características previas. Como el precio nominal subió en casi todas partes (media +83 %; Elmira y Qaim, cuadro 1), se "
        "identifica el efecto de <b>más alza frente a menos alza</b>, no el de la crisis. Con dosis continua haría falta el supuesto "
        "más fuerte de «tendencias paralelas fuertes» (Callaway, Goodman-Bacon y Sant'Anna); los terciles son el diseño principal y "
        "la dosis continua, un complemento."),
      P("El supuesto no es automático. La sequía de El Niño y los incendios golpearon la agricultura justo antes de la crisis: la "
        "producción de arroz cayó 4 % en 1997 (Frankenberg, Smith y Thomas 2003, nota 1). El signo del efecto depende de si el "
        "hogar compra o produce arroz, y hubo programas focalizados, como la alimentación complementaria (Giles y Satriawan 2015). "
        "Por eso usamos tres capas de comparación:"),
      figura("f3_tres_capas.png", 15, "Figura 3. Tres capas de comparación y los confusores que elimina cada una."),
      bullets(["<b>Antes de cualquier CATE:</b> tendencias previas 1993-97; la prueba de Yamauchi y Larson (el alza no debe "
               "correlacionarse con la proporción de productores ni con la nutrición inicial); balance y traslape por tercil; desgaste "
               "por tercil hasta 2014.",
               "<b>Placebos:</b> estatura de quienes ya eran adultos en 1997; bosque placebo en la cohorte no expuesta; hermanos con efecto fijo de hogar.",
               "<b>Robustez:</b> precio real y construcción alterna; dosis continua; sin Sumatra ni Kalimantan (humo); sin las entrevistas de 1998."])]

# 6
H += [SEC("Heterogeneidad con bosques y árboles causales honestos"),
      P("El método central es el bosque causal de <i>grf</i> (Laboratorio 10; Wager y Athey 2018; Athey, Tibshirani y Wager 2019) "
        "con conglomerados por comunidad, porque el tratamiento es comunitario y el número efectivo de unidades es de cientos de "
        "comunidades, no de miles de personas. A diferencia de los laboratorios, aquí el tratamiento no es aleatorio: el propensity "
        "se estima, el efecto promedio se calcula sobre la muestra con traslape y los CATE heredan el supuesto de identificación de "
        "la sección 5 (Athey y Wager 2019)."),
      P("<b>Que el bosque herede el diseño.</b> Un bosque compara en corte transversal. Para no perder la identificación de los "
        "diseños de panel y de cohortes, transformamos el resultado: en estatura, Y = HAZ<sub>2000</sub> − HAZ<sub>1997</sub> "
        "(equivale a los efectos fijos individuales de Elmira y Qaim); en escolaridad, Y = años en 2014 − la media de la cohorte no "
        "expuesta (22-30 años en 1997) de la misma comunidad y sexo. Esa media también entra como covariable. El mismo bosque corrido "
        "solo sobre la cohorte no expuesta (bosque placebo) debe dar un efecto nulo y una calibración que no rechace."),
      figura("f4_flujo.png", 16, "Figura 4. Flujo de análisis: cuatro preguntas sobre la heterogeneidad y una regla para el cliente."),
      P("<b>Hipótesis declaradas antes de ver resultados</b> (τ &lt; 0 = daño). Se aprueban por escrito antes de correr el bosque; "
        "los ocho contrastes de grupo (H1-H8) se estiman con los puntajes doblemente robustos del bosque y se corrigen con Holm.", "p"),
      tabla([["H", "Modificador (1997)", "Predicción", "Base"],
             ["H1", "Urbano", "Más daño urbano", "Elmira y Qaim p. 5; Friedman y Levinsohn p. 408; en contra para HAZ: F-T 2017 p. 12"],
             ["H2", "Comprador neto de arroz", "Más daño en compradores; productores ≈ 0 o positivo", "Friedman y Levinsohn p. 414; FST p. 295; F-T 2017 p. 6-7"],
             ["H3", "Gasto per cápita (percentil)", "Ambiguo: daño escolar en pobres urbanos; plano o inverso en HAZ", "F-L p. 408; FST p. 295; E-Q p. 5; F-T 2017 cuadro 3"],
             ["H4", "Madre con primaria o menos", "Más daño", "E-Q p. 5; FST p. 313 (jefe)"],
             ["H5", "Edad en 1997", "Escolaridad: cerca de 8 años; estatura: 3-5", "F-T 2017 cuadro 3; E-Q p. 6"],
             ["H6", "Sexo", "Sin predicción", "E-Q p. 5 frente a F-T 2017 p. 9"],
             ["H7", "Oro y tierra", "Menos daño, sobre todo rural", "FST p. 305, 316-317; F-T 2017 p. 11"],
             ["H8", "Hermanos mayores; mujeres de 50+; niños menores de 5", "Más daño escolar con hermanos mayores; menos con mujeres mayores; más con niños pequeños", "F-T 2017 p. 9-10; FST p. 313; F-L p. 419"],
             ["H9", "Regla de focalización", "La regla del bosque supera a «pobre» y «urbano»", "E-Q p. 5 y 7 (sugerido)"]],
            [0.8, 3.8, 5.7, 6.2], "Hipótesis declaradas antes de ver resultados"),
      Spacer(1, 6),
      bullets(["<b>¿Hay heterogeneidad?</b> <i>test_calibration</i>: si el coeficiente de la predicción diferencial no es positivo y "
               "significativo, reportamos «no hay evidencia de heterogeneidad» y nos apoyamos en el efecto promedio y en H1-H8.",
               "<b>¿Quién?</b> Mejor proyección lineal del CATE sobre H1-H8 (Semenova y Chernozhukov 2021) y efectos por grupo con puntajes "
               "AIPW, con errores por comunidad.",
               "<b>¿Recupera la celda de Frankenberg y Thomas?</b> Efecto promedio de los urbanos del cuartil inferior con 7-9 años en "
               "1997 frente al resto, y τ̂ por edad separado por zona × cuartil. Si aparece con la exposición por precio, el hallazgo "
               "se fortalece; si no aparece y la calibración no rechaza, es evidencia de que pudo ser una comparación múltiple.",
               "<b>¿Cómo focalizar?</b> Un bosque entrenado en la mitad A de las comunidades ordena a la mitad B; otro bosque en B evalúa. "
               "Comparamos el RATE de la regla del bosque con el de «pobre», «urbano» y «comprador neto» (Yadlowsky et al. 2025), como "
               "la curva TOC del Laboratorio 10."]),
      figura("f6_toc.png", 10.5, "Figura 5. Cómo se leerá la comparación de reglas de focalización (curvas hipotéticas)."),
      P("<b>Árbol honesto para el cliente.</b> El árbol del Laboratorio 9 compara medias porque el tratamiento era aleatorio; aquí "
        "se ajusta sobre los puntajes doblemente robustos del bosque, que ya corrigen por la confusión observada. La mitad A de las "
        "comunidades elige los cortes y la mitad B estima el efecto de cada hoja, con al menos 15 comunidades por hoja y a lo sumo "
        "tres niveles. Se reporta la estabilidad del primer corte en 200 particiones."),
      figura("f5_honestidad.png", 14, "Figura 6. Honestidad por comunidad completa: unas comunidades eligen los cortes y otras estiman los efectos."),
      figura("f7_arbol.png", 13.5, "Figura 7. Forma que tendría el árbol si se cumplen H1, H2 y H4. Esquema, no resultados.")]

# 7
H += [SEC("Resultados que estimaremos y alcance"),
      tabla([["Papel", "Resultado", "Por qué"],
             ["<b>Primario</b>", "Años de escolaridad completados en 2014 (cohortes de 5-21 años en 1997)", "Muestra más grande (7.925); subgrupo publicado que poner a prueba; contraste con Frankenberg y Thomas"],
             ["Ancla", "ΔHAZ 1997-2000 (cohorte 0-5)", "Efecto promedio publicado (Elmira y Qaim); valida precios y antropometría"],
             ["Secundarios", "Estatura adulta 2014; cognición 2014 (EK, 12 ítems cognitivos + 5 de matemáticas)", "Exploratorios; sin corrección conjunta con el primario"],
             ["Extensión", "Salud mental de adultos 1993-2000 (3 ítems comunes)", "Solo si sobra tiempo; efectos promedio, sin CATEs"]],
            [2.2, 6.6, 7.7], "Resultados y alcance"),
      Spacer(1, 4),
      P("<b>Alcance mínimo:</b> precio por comunidad, pruebas de validez, replicación de ΔHAZ, bosque y árbol honesto sobre la "
        "escolaridad. <b>Recorte en orden:</b> CES-D 2014, salud mental de adultos, cognición, estatura adulta.")]

# 8
H += [SEC("Riesgos y plan"),
      tabla([["Riesgo", "Mitigación"],
             ["El efecto promedio está en disputa", "Replicar primero; reportar el diseño de cohortes junto al de precios; aceptar un nulo"],
             ["Unas 208 comunidades en la comparación por terciles: poca potencia para diferencias entre CATEs",
              "Calibración antes de interpretar; resultado primario con la muestra más grande; dosis continua con las 312; hipótesis declaradas"],
             ["Choques simultáneos (sequía, humo) y zona urbana", "Tres capas; tendencias previas; Yamauchi-Larson; placebos; sin Sumatra ni Kalimantan"],
             ["Medición del precio: 2000 no es el pico; fuentes que cambian entre olas; levantamientos en 1998", "Fuentes comunes; versión réplica; indicadores de 1998; dosis continua"],
             ["Falta construir el gasto per cápita y la posición neta de 1997", "Agregado propio desde los módulos de consumo; índice de activos como respaldo"],
             ["Comparaciones múltiples", "Un resultado primario; Holm sobre H1-H8; secundarios exploratorios"]],
            [7.5, 9.0], "Riesgos y mitigación"),
      Spacer(1, 6),
      tabla([["Etapa", "Entregable", "Días"],
             ["Tratamiento", "Precio del arroz por comunidad (dos construcciones), distribución y balance", "2-3"],
             ["Asesoría (semana 15)", "Este documento + pruebas 1-5 de validez; envío la noche anterior", "—"],
             ["Bases", "Variables de 1997, ΔHAZ y escolaridad 2014", "4-6"],
             ["Estimación", "Replicación, bosques, prueba de recuperación, RATE, árbol honesto", "3-4"],
             ["Presentación (semana 16)", "20 minutos, conclusión primero; README reproducible sin datos", "—"]],
            [3.6, 11.4, 1.5], "Cronograma")]

# Referencias
refs = [
    "Athey, S. e Imbens, G. (2016). Recursive partitioning for heterogeneous causal effects. <i>PNAS</i>, 113(27), 7353-7360.",
    "Athey, S., Tibshirani, J. y Wager, S. (2019). Generalized random forests. <i>Annals of Statistics</i>, 47(2), 1148-1178.",
    "Athey, S. y Wager, S. (2019). Estimating treatment effects with causal forests: An application. <i>Observational Studies</i>, 5, 36-51.",
    "Callaway, B., Goodman-Bacon, A. y Sant'Anna, P. H. C. Difference-in-differences with a continuous treatment. NBER WP 32117; arXiv:2107.02637 (v8, 2025).",
    "Elmira, E. S. y Qaim, M. (2026). Macroeconomic shocks and long-term nutritional outcomes: Insights from the Asian financial crisis. <i>Global Food Security</i>, 48, 100900.",
    "Frankenberg, E., Smith, J. P. y Thomas, D. (2003). Economic shocks, wealth, and welfare. <i>Journal of Human Resources</i>, 38(2), 280-321.",
    "Frankenberg, E. y Thomas, D. (2017). Human capital and shocks: Evidence on education, health and nutrition. NBER Working Paper 23347.",
    "Friedman, J. y Levinsohn, J. (2002). The distributional impacts of Indonesia's financial crisis on household welfare: A «rapid response» methodology. <i>World Bank Economic Review</i>, 16(3), 397-423.",
    "Friedman, J. y Thomas, D. (2009). Psychological health before, during, and after an economic crisis: Results from Indonesia, 1993-2000. <i>World Bank Economic Review</i>, 23(1), 57-76.",
    "Giles, J. y Satriawan, E. (2015). Protecting child nutritional status in the aftermath of a financial crisis: Evidence from Indonesia. <i>Journal of Development Economics</i>, 114, 97-106.",
    "Jayachandran, S. (2009). Air quality and early-life mortality: Evidence from Indonesia's wildfires. <i>Journal of Human Resources</i>, 44(4), 916-954.",
    "Maccini, S. y Yang, D. (2009). Under the weather: Health, schooling, and economic consequences of early-life rainfall. <i>American Economic Review</i>, 99(3), 1006-1026.",
    "Semenova, V. y Chernozhukov, V. (2021). Debiased machine learning of conditional average treatment effects and other causal functions. <i>Econometrics Journal</i>, 24(2), 264-289.",
    "Thomas, D., Beegle, K., Frankenberg, E., Sikoki, B., Strauss, J. y Teruel, G. (2004). Education in a crisis. <i>Journal of Development Economics</i>, 74(1), 53-85.",
    "Wager, S. y Athey, S. (2018). Estimation and inference of heterogeneous treatment effects using random forests. <i>JASA</i>, 113(523), 1228-1242.",
    "Yadlowsky, S., Fleming, S., Shah, N., Brunskill, E. y Wager, S. (2025). Evaluating treatment prioritization rules via rank-weighted average treatment effects. <i>JASA</i>, 120(549), 38-51.",
    "Yamauchi, F. y Larson, D. F. (2019). Long-term impacts of an unanticipated spike in food prices on child growth in Indonesia. <i>World Development</i>, 113, 330-343.",
]
H += [Paragraph("REFERENCIAS", st["h1"])] + [P(r, "ref") for r in refs]
H += [Spacer(1, 8),
      P("* Borrador para la asesoría de la semana 15, 17 de noviembre de 2026. Las cifras de la literatura se cotejaron con los PDF de Elmira y Qaim (2026), Frankenberg y Thomas (2017), "
        "Frankenberg, Smith y Thomas (2003), Friedman y Levinsohn (2002) y Friedman y Thomas (2009); las páginas del NBER WP son las "
        "impresas en el documento. Giles y Satriawan, Jayachandran, Maccini y Yang, Thomas et al. y Yamauchi y Larson se citan sin "
        "PDF local. Los tamaños de muestra vienen de la revisión de los datos de la IFLS (scripts de las guías de cada ola). Este "
        "borrador no contiene estimaciones propias; las figuras 5 y 7 son esquemas. Que no existan CATEs con bosques causales para "
        "este choque es el resultado de una búsqueda acotada, no de una revisión sistemática.", "nota")]

doc = SimpleDocTemplate(SALIDA, pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                        title="Borrador de propuesta v4: efectos heterogéneos de la crisis de 1998 (IFLS)",
                        author="Equipo proyecto final ECON-3785")
doc.build(H, onFirstPage=pie, onLaterPages=pie)
print("PDF:", SALIDA)
