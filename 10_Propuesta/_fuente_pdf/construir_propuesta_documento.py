# -*- coding: utf-8 -*-
"""Construye propuesta_borrador.pdf (versión 4) con ReportLab.

Uso: python construir_propuesta_v4.py <carpeta_figuras> <salida.pdf>
Primero: python figuras_v4.py <carpeta_figuras>
"""
import sys
from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle,
                                KeepTogether, PageBreak, ListFlowable, ListItem)

FIG = Path(sys.argv[1] if len(sys.argv) > 1 else "fig")
SALIDA = sys.argv[2] if len(sys.argv) > 2 else "propuesta_borrador.pdf"

F = Path(__file__).parent / "fuentes"
pdfmetrics.registerFont(TTFont("DV", str(F / "Montserrat-400-normal.ttf")))
pdfmetrics.registerFont(TTFont("DVB", str(F / "Montserrat-700-normal.ttf")))
pdfmetrics.registerFont(TTFont("DVS", str(F / "Montserrat-600-normal.ttf")))
pdfmetrics.registerFont(TTFont("DVI", str(F / "Montserrat-400-italic.ttf")))
pdfmetrics.registerFont(TTFont("DVBI", str(F / "Montserrat-600-italic.ttf")))
pdfmetrics.registerFont(TTFont("FB", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily
registerFontFamily("DV", normal="DV", bold="DVB", italic="DVI", boldItalic="DVBI")
from fontTools.ttLib import TTFont as _FT
_CMAP = set(_FT(str(F / "Montserrat-400-normal.ttf")).getBestCmap())
import re as _re


def fx(t):
    """Glifos que Montserrat no tiene (Δ, τ, ≤, ≈, →) se dibujan con DejaVu Sans."""
    out, dentro = [], False
    for ch in t:
        if ch == "<": dentro = True
        if ch == ">": dentro = False
        if not dentro and ord(ch) > 127 and ord(ch) not in _CMAP:
            out.append(f'<font name="FB">{ch}</font>')
        else:
            out.append(ch)
    return "".join(out)


AZUL = colors.HexColor("#2E6B4F")
OSCURO = colors.HexColor("#16382B")
GRIS = colors.HexColor("#666666")
AZUL_C = colors.HexColor("#EEF3EF")

st = {
    "titulo": ParagraphStyle("t", fontName="DVB", fontSize=22, leading=27, textColor=colors.HexColor("#16382B"), spaceAfter=6),
    "sub": ParagraphStyle("s", fontName="DV", fontSize=9, leading=13, textColor=GRIS, spaceAfter=12),
    "h1": ParagraphStyle("h1", fontName="DVB", fontSize=13, leading=16, textColor=AZUL, spaceBefore=14, spaceAfter=6, keepWithNext=1),
    "h2": ParagraphStyle("h2", fontName="DVB", fontSize=9.3, leading=12, textColor=colors.black, spaceBefore=5, spaceAfter=2),
    "p": ParagraphStyle("p", fontName="DV", fontSize=9, leading=13.2, alignment=TA_LEFT, spaceAfter=6),
    "bul": ParagraphStyle("b", fontName="DV", fontSize=8.8, leading=12.6, alignment=TA_LEFT),
    "cap": ParagraphStyle("c", fontName="DV", fontSize=7.4, leading=9.5, textColor=GRIS, alignment=TA_CENTER, spaceAfter=7),
    "tab": ParagraphStyle("tb", fontName="DV", fontSize=7.3, leading=9.1),
    "tabh": ParagraphStyle("th", fontName="DVB", fontSize=7.4, leading=9.2, textColor=colors.white),
    "ref": ParagraphStyle("r", fontName="DV", fontSize=7.1, leading=9, leftIndent=10, firstLineIndent=-10, spaceAfter=1.5),
    "nota": ParagraphStyle("n", fontName="DVI", fontSize=7.3, leading=9.4, textColor=GRIS, alignment=TA_JUSTIFY),
}


def P(t, s="p"):
    return Paragraph(fx(t), st[s])


def bullets(items):
    return ListFlowable([ListItem(P(t, "bul"), leftIndent=10, value="•") for t in items],
                        bulletType="bullet", bulletFontSize=7, leftIndent=10, spaceBefore=0, spaceAfter=5)


def figura(nombre, ancho_cm, caption):
    ruta = FIG / nombre
    from PIL import Image as PI
    w, h = PI.open(ruta).size
    ancho = ancho_cm * cm
    return KeepTogether([Image(str(ruta), width=ancho, height=ancho * h / w), Spacer(1, 2), P(caption, "cap")])


def tabla(filas, anchos, cabecera=True):
    datos = [[P(c, "tabh" if (i == 0 and cabecera) else "tab") for c in f] for i, f in enumerate(filas)]
    t = Table(datos, colWidths=[a * cm for a in anchos], repeatRows=1 if cabecera else 0)
    estilo = [("VALIGN", (0, 0), (-1, -1), "TOP"),
              ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#C3D3C9")),
              ("LEFTPADDING", (0, 0), (-1, -1), 3.5), ("RIGHTPADDING", (0, 0), (-1, -1), 3.5),
              ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5)]
    if cabecera:
        estilo += [("BACKGROUND", (0, 0), (-1, 0), OSCURO)]
    t.setStyle(TableStyle(estilo))
    return t


def pie(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(OSCURO)
    canvas.rect(0, letter[1] - 0.35 * cm, letter[0], 0.35 * cm, fill=1, stroke=0)
    canvas.setFont("DV", 7)
    canvas.setFillColor(GRIS)
    canvas.drawString(2 * cm, 1.2 * cm, "Proyecto final ECON-3785 · Borrador de propuesta · noviembre de 2026")
    canvas.drawRightString(letter[0] - 2 * cm, 1.2 * cm, str(doc.page))
    canvas.restoreState()


H = []
H += [P("¿A quién golpeó más el arroz caro?", "titulo"),
      P("Efectos heterogéneos de largo plazo de la crisis de 1997-98 en Indonesia, con bosques causales<br/>"
        "Borrador de propuesta · Proyecto final ECON-3785 Ciencia de Datos y Econometría Aplicada · noviembre de 2026", "sub")]

def resumen():
    k = [("+83 %", "alza nominal media del arroz por comunidad, 1997-2000"),
         ("109 / 70 %", "compensación necesaria: pobres urbanos vs. rurales"),
         ("~1/3", "de los hogares gastaba más en 1998 que en 1997"),
         ("−1,95 años", "de escolaridad en la cohorte urbana pobre de 8 años")]
    num = ParagraphStyle("kn", fontName="DVB", fontSize=17, leading=20, textColor=colors.white)
    tx = ParagraphStyle("kt", fontName="DV", fontSize=7.3, leading=9.4, textColor=colors.HexColor("#CFE0D6"))
    celdas = [[[Paragraph(fx(n), num), Spacer(1, 3), Paragraph(t, tx)] for n, t in k]]
    t = Table(celdas, colWidths=[4.125 * cm] * 4)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), OSCURO), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("LINEAFTER", (0, 0), (2, 0), 0.6, colors.HexColor("#2E6B4F")),
                           ("TOPPADDING", (0, 0), (-1, -1), 10), ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
                           ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 7)]))
    caja = Table([[P("<b>En síntesis.</b> El alza del arroz de 1997-98 golpeó de forma muy desigual. La literatura encontró a quién "
                     "dañó con subgrupos elegidos a mano. Proponemos medirlo con una sola exposición y un bosque causal, "
                     "probar si los hallazgos previos resisten, y entregar al cliente una regla de priorización comparada con "
                     "«focalizar en pobres».", "bul")]], colWidths=[16.5 * cm])
    caja.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AZUL_C), ("LINEBEFORE", (0, 0), (0, 0), 3, AZUL),
                              ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
                              ("LEFTPADDING", (0, 0), (-1, -1), 10)]))
    return [t, Spacer(1, 8), caja, Spacer(1, 4)]


H += resumen()

# 1
H += [P('<font color="#9DBFAE">01</font>  Pregunta y cliente', "h1"),
      P("Entre 1997 y 1998 la rupia se desplomó, se retiraron subsidios y el precio del arroz, el alimento básico de Indonesia, "
        "subió con fuerza y de forma desigual entre comunidades. La pregunta es: <b>¿quiénes cargaron, años después, con las "
        "consecuencias de haber vivido donde el arroz subió más, y qué características de 1997 predicen un daño mayor?</b> "
        "El resultado principal es la escolaridad completada en 2014. La estatura de los niños entre 1997 y 2000 sirve para "
        "replicar un estudio previo y validar los datos, y la estatura adulta y las pruebas cognitivas se analizan como resultados secundarios. La salud mental queda como extensión opcional."),
      P("<b>Cliente propuesto:</b> una agencia que deba focalizar ayuda ante choques de precios de alimentos (por ejemplo, el "
        "Programa Mundial de Alimentos). <b>Entregable:</b> una regla simple y defendible de qué hogares proteger primero, con "
        "variables que la agencia puede observar, y la evidencia de cuánto daño evita frente a la regla habitual de focalizar en "
        "los pobres.")]

# 2
H += [P('<font color="#9DBFAE">02</font>  El efecto promedio: replicable, pero en disputa', "h1"),
      P("Elmira y Qaim (2026) usan el cambio del precio del arroz 1997-2000 en las 312 comunidades de la Indonesia Family Life "
        "Survey (IFLS). Con efectos fijos individuales, un alza de 100 % reduce la talla-para-edad (HAZ) en 0,135 desviaciones "
        "estándar (0,251 con precio real) y eleva el retraso en talla en 3,5 puntos (p. 1 y 5). En 2014 encuentran 0,65 cm menos "
        "de estatura adulta, que interpretan como asociación (p. 5-6). Frankenberg y Thomas (2017), sin precios y con la zona "
        "urbana como proxy del choque (p. 12), no encuentran daño en estatura. En escolaridad completada en 2014 tampoco lo hay "
        "para las cohortes de 7-12 ni de 13-16 años (+0,002 años, error estándar de 0,17), con una excepción: la cohorte de 8 años, "
        "urbana y del cuartil más pobre, pierde 1,95 años (EE 0,63). Con efectos fijos de hogar la pérdida baja a 1,24 (EE 0,69), "
        "significativa solo al 10 % (cuadro 3). Aplicar una misma medida de exposición a ambos resultados permite entender de dónde viene la "
        "diferencia entre los dos estudios, y un resultado nulo bien documentado también sería un hallazgo.")]

# 3
H += [P('<font color="#9DBFAE">03</font>  Lo que se sabe de quién cargó con el choque, y lo que falta', "h1"),
      P("La literatura coincide en que el choque fue «devastador para unos hogares y una oportunidad para otros» (Frankenberg, "
        "Smith y Thomas 2003, p. 280). Un tercio de los hogares tenía más gasto per cápita en 1998 que en 1997 (p. 295). La figura "
        "1 ordena los hallazgos por dimensión. Tres cosas saltan a la vista. Vivir en zona urbana es la característica asociada con más daño de forma más consistente. "
        "Comprar o producir arroz, tener oro y la composición del hogar tienen buena justificación económica, pero <b>nunca se ha "
        "medido si cambian el efecto sobre los niños</b>. La pobreza y la edad, por último, dan señales contradictorias según el resultado que se mire."),
      P("<b>Patrón metodológico común.</b> Todos hallaron la heterogeneidad con subgrupos elegidos a mano: una interacción binaria "
        "a la vez (Elmira y Qaim, ecuación 2), celdas edad × zona × cuartil frente a una tendencia (Frankenberg y Thomas, figura 7: "
        "17 edades × 4 grupos) o interacciones del choque por zona (Frankenberg, Smith y Thomas, cuadros 8-9). Ninguno hace una "
        "prueba global de heterogeneidad ni corrige por todo lo que miró. De ahí salen cinco vacíos:"),
      tabla([["#", "Vacío", "Cómo lo atacamos"],
             ["V1", "Ninguna prueba global de heterogeneidad para este choque", "Comprobar si las diferencias que estima el bosque se confirman en datos que no usó"],
             ["V2", "La posición neta en arroz no se ha probado como modificador del efecto sobre los niños (Elmira y Qaim no la usan, aunque explican lo urbano por la dependencia de las compras, p. 5)",
              "Hipótesis H2 y comparación entre compradores y productores de la misma comunidad"],
             ["V3", "Oro, tierra, hermanos y mujeres mayores suavizaron el consumo (FST p. 313, 316-317; F-T 2017 p. 9-11), pero no se han estudiado como protección de los niños",
              "Modificadores pre-declarados H7-H8"],
             ["V4", "La cohorte urbana pobre de 8 años es una celda hallada a mano entre ~68",
              "Ver si el bosque encuentra ese grupo sin indicárselo, usando el precio como exposición"],
             ["V5", "Nadie compara reglas de focalización, aunque Elmira y Qaim sugieren que focalizar en pobres «puede no bastar» (p. 5 y 7)",
              "Comparar cuánto daño evita priorizar según el bosque frente a priorizar por pobreza, zona o compra de arroz"]],
            [0.8, 8.4, 7.3]),
      Spacer(1, 6),
      figura("f2_mapa_evidencia.png", 15.8,
             "Figura 1. Mapa de la evidencia sobre heterogeneidad, cotejado con los PDF (página o cuadro en cada celda). "
             "Cada estudio usa una exposición y un resultado distintos.")]

# 4
H += [P('<font color="#9DBFAE">04</font>  Datos', "h1"),
      P("Usamos la Indonesia Family Life Survey (IFLS), un panel público que sigue a los mismos hogares e individuos desde 1993 en "
        "13 provincias, que reúnen cerca del 83 % de la población. Lo que la hace útil para esta pregunta es que la ola de 1997 se "
        "levantó justo antes del colapso de la rupia y que la encuesta volvió a buscar a las mismas personas en 2000, 2007 y 2014. "
        "Eso permite observar a los niños antes del choque y, otra vez, ya adultos. Revisamos las cinco olas archivo por archivo, y los "
        "tamaños de muestra que siguen salen de esa revisión y no de la documentación de la encuesta."),
      figura("f1_olas.png", 15.5, "Figura 2. Olas de la IFLS y cohortes del proyecto. Parte de la ola de 1997 se levantó en 1998 (627 hogares)."),
      tabla([["Muestra", "1997", "2014", "Uso"],
             ["Cohorte de 0-5 años en 1997 con talla", "3.217", "2.586", "Ancla ΔHAZ (2000: 3.422); estatura adulta"],
             ["Cohorte de 0-5 años con pruebas cognitivas completas", "—", "2.535", "Secundario"],
             ["Cohortes de 5-21 años: miembros / con escolaridad en 2014", "12.632", "7.925", "<b>Primario</b>"],
             ["Comunidades con precio del arroz", "312", "—", "Tratamiento y unidad de agrupación"]],
            [7.2, 1.6, 1.6, 6.1]),
      Spacer(1, 4),
      P("<b>Cómo medimos la exposición al choque.</b> En cada comunidad, la encuesta registró en 1997 y en 2000 el precio del arroz "
        "en mercados, tiendas y puestos de salud comunitarios. La exposición es el cambio porcentual de ese precio entre los dos años. "
        "Las fuentes no son las mismas en ambas olas: en 2000 ya no se preguntó el precio a la líder del grupo de mujeres, que sí se "
        "consultó en 1997. Para que el cambio no refleje un cambio de informante, la medida principal usa solo las fuentes presentes "
        "en los dos años, el arroz de calidad media y los precios en kilos. Construimos además una versión que replica la de Elmira y "
        "Qaim, que promedian todas las fuentes, para poder comparar nuestras estimaciones con las suyas. Un detalle importante es que "
        "27 comunidades respondieron el cuestionario de 1997 en enero o febrero de 1998, cuando el alza ya había comenzado. Las "
        "marcamos y verificamos que los resultados no dependan de ellas."),
      P("<b>Qué características de los hogares tenemos en cuenta y por qué.</b> Todas se miden en 1997, antes de la crisis, porque "
        "cualquier cosa medida después puede haber sido alterada por el propio choque, y controlar por ella ocultaría parte del "
        "efecto que queremos estimar. Cumplen dos funciones distintas. La primera es hacer comparables a las comunidades con alzas "
        "altas y bajas. Si el arroz subió más donde los hogares ya eran más pobres, más urbanos o habían sufrido la sequía de 1997, "
        "una comparación simple atribuiría al precio diferencias que existían antes. Por eso incluimos la zona urbana o rural, el "
        "precio del arroz en 1997 (las comunidades con precios bajos al inicio tienden a subir más, sin que eso diga nada del choque), "
        "la provincia y si el hogar reportó pérdidas de cosecha por sequía. La segunda función es describir a quién afecta más el "
        "choque: la educación de la madre, el gasto del hogar, si compraba o producía su propio arroz (5.075 hogares compraban y 1.511 "
        "producían), si tenía oro o tierra que pudiera vender y la composición del hogar. Estas son las variables sobre las que "
        "buscamos diferencias en el efecto."),
      P("Los datos están bajo licencia de RAND y no se pueden redistribuir. La entrega incluirá el código y las instrucciones para "
        "descargarlos y reconstruir todas las bases.")]

# 5
H += [P('<font color="#9DBFAE">05</font>  Estrategia empírica', "h1"),
      P("<b>La comparación.</b> Dividimos las comunidades en tres grupos según cuánto subió el precio del arroz entre 1997 y 2000 y "
        "comparamos a quienes vivían en 1997 en las comunidades con las alzas más altas con quienes vivían en las de alzas más bajas. "
        "Asignamos a cada persona según dónde vivía en 1997 y no según dónde vive hoy. Muchos hogares se mudaron como respuesta a la "
        "crisis, y asignarlos por su residencia posterior mezclaría el efecto del choque con la decisión de migrar. Como el precio "
        "nominal subió en casi todas partes (en promedio 83 %, según Elmira y Qaim), no existe un grupo que no haya vivido la crisis. "
        "Lo que medimos es cuánto más daño sufrió quien enfrentó un alza grande frente a quien enfrentó una pequeña. Preferimos "
        "comparar grupos extremos a usar el cambio de precio como una variable continua, porque interpretar el efecto de cada punto "
        "adicional de alza exige suponer que las comunidades con distinta alza habrían evolucionado igual en todos los niveles, un "
        "supuesto mucho más exigente (Callaway, Goodman-Bacon y Sant'Anna). La versión continua se presenta como complemento."),
      P("<b>Qué tiene que ser cierto para que la comparación sea válida.</b> Una vez tenidas en cuenta las características de 1997, "
        "las comunidades con alzas altas y bajas deben ser iguales en todo lo demás que afecta la estatura o la escolaridad de los "
        "niños. Hay razones concretas para dudarlo. La sequía de El Niño y los incendios forestales golpearon la agricultura justo antes "
        "de la crisis y redujeron 4 % la producción de arroz en 1997 (Frankenberg, Smith y Thomas 2003). Si esas mismas zonas tuvieron "
        "alzas mayores, parte de lo que atribuyamos al precio sería efecto de la sequía o del humo. Además, el gobierno dirigió "
        "programas de alimentación y becas a las zonas más golpeadas (Giles y Satriawan 2015), lo que podría atenuar el efecto medido."),
      P("<b>Tres comparaciones que se respaldan entre sí.</b> Para no depender de una sola, usamos tres, y cada una descarta una "
        "explicación alternativa distinta (figura 3). La primera compara comunidades, como Elmira y Qaim. La segunda compara, dentro de "
        "una misma comunidad, a los niños que estaban en edad escolar durante la crisis con jóvenes que ya habían terminado la escuela "
        "antes. Todo lo que sea propio de la comunidad (su riqueza, sus escuelas, su clima) afecta a ambos grupos, de modo que la "
        "diferencia entre ellos aísla lo que cambió con la crisis. La tercera compara, dentro de la misma comunidad, a los hogares que "
        "compraban arroz con los que lo producían. Ambos vivieron la misma sequía y los mismos disturbios, pero el alza del precio solo "
        "empobreció a los compradores. Si el daño aparece en ellos y no en los productores, es difícil atribuirlo a otra cosa que al "
        "precio."),
      figura("f3_tres_capas.png", 14.5, "Figura 3. Tres comparaciones y las explicaciones alternativas que descarta cada una."),
      P("<b>Cómo comprobamos que el diseño funciona, antes de mirar los resultados.</b> Primero revisamos si las comunidades que "
        "después tuvieron alzas altas ya venían evolucionando distinto entre 1993 y 1997. Si fuera así, la diferencia posterior no "
        "podría atribuirse a la crisis. Segundo, replicamos una prueba de Yamauchi y Larson (2019): el alza no debería estar "
        "relacionada con la proporción de hogares productores de la comunidad ni con la nutrición de sus niños antes de la crisis. "
        "Tercero, estimamos el mismo efecto sobre grupos en los que no debería existir, como la estatura de quienes ya eran adultos en "
        "1997, que el precio del arroz no puede haber cambiado. Por último, repetimos la estimación excluyendo Sumatra y Kalimantan, "
        "las islas más afectadas por el humo, y las entrevistas hechas en 1998.")]

# 6
H += [P('<font color="#9DBFAE">06</font>  Heterogeneidad con bosques causales', "h1"),
      P("<b>Qué hace un bosque causal y por qué lo usamos.</b> Un bosque causal (Wager y Athey 2018; Laboratorio 10) estima el efecto "
        "del tratamiento para cada persona según sus características. Construye miles de árboles. Cada árbol divide la muestra, una y "
        "otra vez, en grupos de personas parecidas, eligiendo las divisiones donde el efecto del alza difiere más. El efecto para "
        "alguien se obtiene promediando lo que le ocurre a las personas que, en muchos árboles, quedan en su mismo grupo. Es pertinente "
        "aquí por dos razones. La primera es que no obliga a escoger de antemano qué subgrupos mirar: puede encontrar combinaciones "
        "(por ejemplo, hogares urbanos que compran arroz y cuya madre tiene poca educación) que nadie habría especificado. La segunda es "
        "que es <i>honesto</i>: cada árbol usa una parte de los datos para decidir cómo dividir y otra parte, distinta, para estimar el "
        "efecto. Así se evita el problema central de la literatura, que es encontrar diferencias en los mismos datos con que se buscaron. "
        "Como el tratamiento se asigna por comunidad, el bosque toma y separa comunidades completas, y la incertidumbre se calcula con "
        "unas 300 comunidades y no con miles de personas."),
      P("<b>Cómo hacemos que el bosque respete el diseño.</b> El bosque compara personas en un momento dado. Para que conserve las "
        "ventajas de las comparaciones de la sección anterior, no le damos el resultado en niveles sino en diferencias. En estatura, "
        "usamos el cambio de la talla de cada niño entre 1997 y 2000, de modo que lo que es propio de cada niño (su genética, por "
        "ejemplo) se cancela. En escolaridad, usamos los años de estudio de cada joven menos el promedio de los jóvenes de su misma "
        "comunidad que ya habían terminado la escuela antes de la crisis, de modo que se cancela lo que es propio de la comunidad. Como "
        "prueba, corremos el mismo bosque solo con esos jóvenes mayores: como no estaban en la escuela durante la crisis, el bosque no "
        "debería encontrar ningún efecto."),
      figura("f4_flujo.png", 15.5, "Figura 4. Flujo de análisis: cuatro preguntas sobre la heterogeneidad."),
      P("<b>Hipótesis declaradas antes de ver los resultados.</b> Para no terminar contando solo los subgrupos que salgan "
        "significativos, fijamos por escrito qué esperamos encontrar y por qué. Cada hipótesis se apoya en un hallazgo previo y se "
        "pondrá a prueba con el mismo procedimiento. Como probamos ocho, ajustamos el umbral de significancia para que la probabilidad de "
        "obtener por azar al menos un falso positivo no supere el 5 % (corrección de Holm)."),
      tabla([["H", "Característica en 1997", "Qué esperamos", "En qué se basa"],
             ["H1", "Vivir en zona urbana", "Más daño en lo urbano", "Elmira y Qaim p. 5; Friedman y Levinsohn p. 408. En contra, para talla: Frankenberg y Thomas 2017, p. 12"],
             ["H2", "Comprar arroz en vez de producirlo", "Más daño en compradores y poco o ninguno en productores", "Friedman y Levinsohn p. 414; FST p. 295; F-T 2017 p. 6-7"],
             ["H3", "Gasto del hogar", "Sin dirección clara: puede variar entre lo urbano y lo rural", "F-L p. 408; FST p. 295; E-Q p. 5; F-T 2017 cuadro 3"],
             ["H4", "Madre con primaria o menos", "Más daño", "E-Q p. 5; FST p. 313"],
             ["H5", "Edad en 1997", "Escolaridad: cerca de 8 años. Talla: 3-5 años", "F-T 2017 cuadro 3; E-Q p. 6"],
             ["H6", "Sexo", "Sin predicción", "E-Q p. 5 frente a F-T 2017 p. 9"],
             ["H7", "Tener oro o tierra", "Menos daño, sobre todo en lo rural", "FST p. 316-317; F-T 2017 p. 11"],
             ["H8", "Hermanos mayores, mujeres mayores y niños pequeños en el hogar", "Más daño escolar con hermanos mayores o niños pequeños, y menos con mujeres mayores", "F-T 2017 p. 9-10; FST p. 313; F-L p. 419"],
             ["H9", "Regla de focalización", "Priorizar según el bosque evita más daño que priorizar por pobreza o zona", "E-Q p. 5 y 7"]],
            [0.8, 4.0, 5.5, 6.2]),
      Spacer(1, 6),
      P("<b>Cuatro preguntas, en orden.</b> La primera es si hay heterogeneidad real o si las diferencias que muestra el bosque son "
        "ruido. Para responderla comparamos, en datos que el bosque no usó para estimar, si las personas para las que el bosque predice "
        "más daño efectivamente lo sufren. Si no es así, lo reportamos como resultado y nos apoyamos en el efecto promedio. La "
        "segunda es quién sufre más. Para cada hipótesis comparamos el efecto promedio entre los grupos, usando para cada persona una "
        "estimación de su efecto individual que combina la predicción del resultado con la probabilidad de haber estado expuesto. Esta "
        "combinación sigue siendo correcta aunque una de las dos partes esté mal estimada, lo que la hace más confiable en datos que no "
        "provienen de un experimento. La tercera es si el bosque encuentra, sin que se lo indiquemos, el grupo que Frankenberg y Thomas "
        "hallaron a mano: niños urbanos y pobres de 8 años en 1997. Si aparece con una medida de exposición distinta, el hallazgo se "
        "fortalece; si no aparece, es una señal de que pudo ser producto de revisar muchos grupos a la vez."),
      P("La cuarta pregunta es la que importa al cliente: a quién proteger primero. Entrenamos el bosque con la mitad de las "
        "comunidades, lo usamos para ordenar a los niños de la otra mitad de mayor a menor daño esperado, y medimos cuánto más daño "
        "sufrió el 10 %, 20 % o 30 % priorizado que el promedio. Hacemos lo mismo con las reglas que una agencia usaría sin el bosque, "
        "como priorizar a los hogares pobres o a los urbanos, y comparamos cuánto daño evita cada una (Yadlowsky et al. 2025; figura 5). "
        "Al cliente le entregamos esa comparación junto con el perfil de los hogares que el bosque prioriza, descrito con "
        "características que la agencia puede observar."),
      figura("f6_toc.png", 10.5, "Figura 5. Cómo se leerá la comparación de reglas de focalización (curvas hipotéticas).")]

# 7
H += [P('<font color="#9DBFAE">07</font>  Resultados que estimaremos y alcance', "h1"),
      tabla([["Papel", "Resultado", "Por qué"],
             ["<b>Primario</b>", "Años de escolaridad completados en 2014 (cohortes de 5-21 años en 1997)", "Es la muestra más grande (7.925) y permite poner a prueba el grupo hallado por Frankenberg y Thomas"],
             ["Ancla", "Cambio en talla-para-edad 1997-2000 (cohorte de 0-5 años)", "Tiene un efecto publicado (Elmira y Qaim) con el que validar los datos"],
             ["Secundarios", "Estatura adulta y pruebas cognitivas en 2014", "Exploratorios"],
             ["Extensión", "Salud mental de adultos, 1993-2000", "Solo si sobra tiempo y sin análisis de heterogeneidad"]],
            [2.2, 6.6, 7.7]),
      Spacer(1, 4),
      P("Lo mínimo que entregaremos es la medida de exposición por comunidad, las pruebas de validez, la réplica del efecto sobre la "
        "talla y el bosque causal sobre la escolaridad. Si el tiempo no alcanza, recortamos en este orden: salud mental, pruebas "
        "cognitivas y estatura adulta.")]

# 8
H += [P('<font color="#9DBFAE">08</font>  Riesgos y plan', "h1"),
      tabla([["Riesgo", "Cómo lo enfrentamos"],
             ["El efecto promedio está en disputa en la literatura", "Replicamos primero el estudio de referencia y reportamos el resultado aunque sea nulo"],
             ["Con unas 200 comunidades en la comparación, puede faltar potencia para distinguir efectos entre grupos",
              "Comprobamos si hay heterogeneidad antes de interpretarla y usamos la muestra más grande como resultado principal"],
             ["Sequía, humo y diferencias urbano-rurales pueden confundirse con el alza", "Tres comparaciones, pruebas previas y exclusión de las islas con incendios"],
             ["La medida de precio es imperfecta", "Fuentes comunes a ambos años, versión de réplica y control de las entrevistas de 1998"],
             ["Hay que construir el gasto del hogar y su posición en el mercado de arroz", "Agregado propio desde los módulos de consumo, con un índice de activos como respaldo"]],
            [7.5, 9.0]),
      Spacer(1, 6),
      tabla([["Etapa", "Entregable", "Días"],
             ["Exposición", "Precio del arroz por comunidad, distribución y balance", "2-3"],
             ["Asesoría (semana 15)", "Este documento y las primeras pruebas de validez, enviados la noche anterior", "—"],
             ["Bases", "Características de 1997, cambio de talla y escolaridad 2014", "4-6"],
             ["Estimación", "Réplica, bosque causal, prueba del grupo de 8 años y comparación de reglas", "3-4"],
             ["Presentación (semana 16)", "20 minutos y un README que permita reproducir todo sin los datos", "—"]],
            [3.6, 11.4, 1.5])]


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
H += [P("Referencias", "h1")] + [P(r, "ref") for r in refs]
H += [Spacer(1, 8),
      P("Nota: las cifras de la literatura se cotejaron con los PDF de Elmira y Qaim (2026), Frankenberg y Thomas (2017), "
        "Frankenberg, Smith y Thomas (2003), Friedman y Levinsohn (2002) y Friedman y Thomas (2009). Las páginas del NBER WP son las "
        "impresas en el documento. Giles y Satriawan, Jayachandran, Maccini y Yang, Thomas et al. y Yamauchi y Larson se citan sin "
        "PDF local. Los tamaños de muestra vienen de la revisión de los datos de la IFLS (scripts de las guías de cada ola). Este "
        "borrador no contiene estimaciones propias y la figura 5 es un esquema. Que no existan CATEs con bosques causales para "
        "este choque es el resultado de una búsqueda acotada, no de una revisión sistemática.", "nota")]

doc = SimpleDocTemplate(SALIDA, pagesize=letter, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                        title="Borrador de propuesta v4: efectos heterogéneos de la crisis de 1998 (IFLS)",
                        author="Equipo proyecto final ECON-3785")
doc.build(H, onFirstPage=pie, onLaterPages=pie)
print("PDF:", SALIDA)
