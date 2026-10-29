"""
VitalTap - Página de ventas en Streamlit.

Cómo ejecutarla:
    pip install -r requirements.txt
    streamlit run app.py
"""

import base64
import textwrap
from pathlib import Path
from urllib.parse import quote

import streamlit as st
from PIL import Image

# ---------------------------------------------------------------- Config ---
BASE = Path(__file__).parent
ASSETS = BASE / "assets"

WA_PRINCIPAL = "528132404926"  # 81 3240 4926
WA_SECUNDARIO = "528114711236"  # 81 1471 1236
PRECIO_CATALOGO = 89
PRECIO_PERSONALIZADO = 99

st.set_page_config(
    page_title="VitalTap | Tu ficha médica de emergencia",
    page_icon=Image.open(ASSETS / "icono.png"),
    layout="wide",
)

# ---------------------------------------------------------------- Estilos ---
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600&family=Poppins:wght@600;700&display=swap');
/* Siempre en modo claro: evita que el modo noche del dispositivo/navegador cambie los colores */
:root, html, body { color-scheme: light only; }
html, body, .stApp { background-color: #ffffff !important; color: #1c2540; }
html, body, [class*="css"] { font-family: 'Open Sans', sans-serif; }
h1, h2, h3 { font-family: 'Poppins', sans-serif !important; color: #14275f; }
.block-container { max-width: 1120px; padding-top: 5rem; }
.eyebrow { font-weight: 600; font-size: 14px; letter-spacing: .12em; text-transform: uppercase; color: #07708a; margin: 0 0 12px; }
.hero-title { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: clamp(34px, 5vw, 54px); line-height: 1.1; color: #14275f; margin: 0 0 16px; }
.lead { font-size: 18px; color: #3d4a70; }
.muted { color: #3d4a70; }
.card { background: #f3f7fd; border-radius: 20px; padding: 24px; height: 100%; }
.card h3 { font-size: 20px; margin: 0 0 8px; }
.card p { margin: 0; color: #3d4a70; }
.step { display: flex; gap: 14px; align-items: flex-start; margin-bottom: 18px; }
.step .n { flex: 0 0 40px; width: 40px; height: 40px; border-radius: 50%; background: #0bc0e0; color: #0b1d4d; font-family: 'Poppins', sans-serif; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.step h4 { margin: 0 0 2px; font-family: 'Poppins', sans-serif; font-size: 18px; color: #14275f; }
.step p { margin: 0; color: #3d4a70; }
.phone { width: 270px; max-width: 100%; margin: 0 auto; box-sizing: border-box; background: #0d1a3f; border: 6px solid #2b3a6e; border-radius: 36px; padding: 20px 16px 22px; color: #fff; }
.phone .tag { font-size: 12px; font-weight: 600; letter-spacing: .06em; color: #6fe3f5; text-transform: uppercase; margin: 0 0 12px; }
.phone .ttl { font-family: 'Poppins', sans-serif; font-weight: 600; font-size: 17px; margin: 0 0 12px; }
.phone .alert { background: #fde8ea; color: #7a1020; border-radius: 14px; padding: 12px 14px; margin-bottom: 10px; }
.phone .ok { background: #def5ea; color: #0b4a30; border-radius: 14px; padding: 12px 14px; }
.phone small { display: block; font-size: 11px; font-weight: 700; letter-spacing: .06em; text-transform: uppercase; }
.phone .call { background: #0f7a52; color: #fff; text-align: center; border-radius: 10px; padding: 9px 0; font-weight: 700; font-size: 14px; margin-top: 8px; }
.stage { background: #eef3fb; border-radius: 28px; padding: 24px; display: flex; justify-content: center; }
.price { border-radius: 28px; padding: 32px; }
.price.dark { background: #14275f; color: #fff; }
.price.light { background: #fff; border: 2px solid #cfd9ec; color: #14275f; }
.price .lbl { font-weight: 600; font-size: 14px; letter-spacing: .1em; text-transform: uppercase; margin: 0 0 6px; }
.price .amt { font-family: 'Poppins', sans-serif; font-weight: 700; font-size: 52px; line-height: 1.1; margin: 0; }
.price .amt span { font-size: 20px; font-weight: 600; }
.price ul { margin: 18px 0 0; padding-left: 20px; }
.price li { margin-bottom: 6px; }
.band { background: #14275f; color: #fff; border-radius: 28px; padding: 32px; }
.band h2, .band h3 { color: #fff !important; }
.spec { display: flex; justify-content: space-between; gap: 16px; padding: 12px 0; border-bottom: 1px solid #cfd9ec; }
.spec span:first-child { color: #3d4a70; }
.spec span:last-child { font-weight: 600; color: #14275f; text-align: right; }
.footer { text-align: center; color: #3d4a70; font-size: 14px; padding: 24px 0 8px; }
</style>
""",
    unsafe_allow_html=True,
)


def html(contenido: str) -> None:
    """Renderiza HTML sin que Markdown lo tome como bloque de código."""
    st.markdown(textwrap.dedent(contenido).strip(), unsafe_allow_html=True)


# ---------------------------------------------------------------- Datos ---
COLORES = {
    "Celeste": {"fill": "#6ec6ea", "edge": "#4aa6cc", "ink": "#14506e"},
    "Blanco": {"fill": "#f7f9fc", "edge": "#c3cde0", "ink": "#2a6fb0"},
    "Negro": {"fill": "#1d2230", "edge": "#0d1018", "ink": "#e8ecf5"},
    "Rosa": {"fill": "#f4a0bd", "edge": "#d9799c", "ink": "#7a1f45"},
    "Rojo": {"fill": "#ef6b73", "edge": "#cc4a53", "ink": "#5c0f17"},
    "Naranja": {"fill": "#ff9a3d", "edge": "#db7a1e", "ink": "#5a2a00"},
    "Amarillo": {"fill": "#ffd95c", "edge": "#e0b52a", "ink": "#5a4300"},
    "Verde menta": {"fill": "#7edcb9", "edge": "#52b992", "ink": "#0d4a35"},
    "Turquesa": {"fill": "#3cc0b0", "edge": "#239d8e", "ink": "#07463f"},
    "Morado": {"fill": "#a98be6", "edge": "#8567c8", "ink": "#3b2377"},
    "Vino": {"fill": "#7b2d62", "edge": "#5a1c46", "ink": "#f6e6f0"},
}


def circulo(cx, cy, r):
    return f"M{cx - r} {cy} a{r} {r} 0 1 0 {2 * r} 0 a{r} {r} 0 1 0 {-2 * r} 0 Z"


# d: forma, tab: orejita del llavero, hole: (x, y, radio) del orificio,
# content: (x, y, escala) del logo, ew/fw: grosor de borde y relleno.
DISENOS = {
    "Círculo": dict(
        d="M16 108 a84 84 0 1 0 168 0 a84 84 0 1 0 -168 0 Z", tab="",
        hole=(100, 32, 6), content=(100, 114, 1.0), ew=4, fw=0),
    "Estrella": dict(
        d="M100 22 L123.5 79.6 L185.6 84.2 L138 124.4 L152.9 184.8 L100 152 "
          "L47.1 184.8 L62 124.4 L14.4 84.2 L76.5 79.6 Z", tab="",
        hole=(100, 48, 5), content=(100, 116, 0.78), ew=16, fw=12),
    "Corazón": dict(
        d="M100 190 C 30 140 12 100 22 70 C 32 40 78 36 100 70 "
          "C 122 36 168 40 178 70 C 188 100 170 140 100 190 Z",
        tab="M86 62 a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0 Z",
        hole=(100, 62, 5), content=(100, 108, 0.85), ew=4, fw=0),
    "Huella": dict(
        d="M100 100 C 70 100 40 130 40 156 C 40 180 62 188 82 182 "
          "C 92 178 108 178 118 182 C 138 188 160 180 160 156 C 160 130 130 100 100 100 Z "
          "M21 100 a17 17 0 1 0 34 0 a17 17 0 1 0 -34 0 Z "
          "M53 64 a19 19 0 1 0 38 0 a19 19 0 1 0 -38 0 Z "
          "M109 64 a19 19 0 1 0 38 0 a19 19 0 1 0 -38 0 Z "
          "M145 100 a17 17 0 1 0 34 0 a17 17 0 1 0 -34 0 Z",
        tab="M86 50 a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0 Z",
        hole=(100, 48, 5), content=(100, 146, 0.55), ew=4, fw=0),
    "Mariposa": dict(
        d="M10 80 a46 52 0 1 0 92 0 a46 52 0 1 0 -92 0 Z "
          "M98 80 a46 52 0 1 0 92 0 a46 52 0 1 0 -92 0 Z "
          "M30 148 a38 40 0 1 0 76 0 a38 40 0 1 0 -76 0 Z "
          "M94 148 a38 40 0 1 0 76 0 a38 40 0 1 0 -76 0 Z "
          "M92 40 V170 H108 V40 Z",
        tab="M88 36 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 Z",
        hole=(100, 36, 4.5), content=(100, 112, 0.6), ew=4, fw=0),
    "Flor": dict(
        d="M66 58 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0 Z "
          "M115.5 93.9 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0 Z "
          "M96.6 152.1 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0 Z "
          "M35.4 152.1 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0 Z "
          "M16.5 93.9 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0 Z "
          "M50 110 a50 50 0 1 0 100 0 a50 50 0 1 0 -100 0 Z",
        tab="", hole=(100, 36, 5.5), content=(100, 112, 0.8), ew=4, fw=0),
    "Luna": dict(
        d="M130 20 C 70 20 24 66 24 120 C 24 170 66 200 118 200 "
          "C 146 200 168 190 184 172 C 130 176 96 148 96 108 C 96 74 108 44 130 20 Z",
        tab="M114 38 a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0 Z",
        hole=(128, 38, 5), content=(60, 132, 0.5), ew=4, fw=0),
    "Planeta": dict(
        d="M42 100 a58 58 0 1 0 116 0 a58 58 0 1 0 -116 0 Z "
          "M6 124 a94 26 0 1 0 188 0 a94 26 0 1 0 -188 0 Z "
          "M20 124 a80 16 0 1 1 160 0 a80 16 0 1 1 -160 0 Z",
        tab="M88 42 a12 12 0 1 0 24 0 a12 12 0 1 0 -24 0 Z",
        hole=(100, 40, 4.5), content=(100, 92, 0.55), ew=4, fw=0),
    "Nube": dict(
        d="M52 180 C 20 180 10 148 34 132 C 26 104 56 88 78 98 C 86 64 132 60 146 92 "
          "C 174 82 198 112 180 136 C 200 156 186 180 152 180 Z",
        tab="", hole=(112, 84, 5), content=(100, 134, 0.72), ew=4, fw=0),
    "Rayo": dict(
        d="M118 16 L54 110 L94 110 L70 196 L152 84 L110 84 L144 16 Z",
        tab="", hole=(118, 38, 4.5), content=(103, 96, 0.5), ew=4, fw=0),
    "Corona": dict(
        d="M24 172 L24 84 L62 118 L100 58 L138 118 L176 84 L176 172 Z "
          "M14 76 a10 10 0 1 1 20 0 a10 10 0 1 1 -20 0 Z "
          "M90 50 a10 10 0 1 1 20 0 a10 10 0 1 1 -20 0 Z "
          "M166 76 a10 10 0 1 1 20 0 a10 10 0 1 1 -20 0 Z",
        tab="", hole=(100, 50, 4), content=(100, 142, 0.7), ew=14, fw=10),
    "Diamante": dict(
        d="M60 44 L140 44 L184 94 L100 190 L16 94 Z",
        tab="", hole=(100, 62, 5), content=(100, 112, 0.75), ew=4, fw=0),
    "Personalizado": dict(
        d="M46 28 H154 A18 18 0 0 1 172 46 V170 A18 18 0 0 1 154 188 H46 "
          "A18 18 0 0 1 28 170 V46 A18 18 0 0 1 46 28 Z",
        tab="", hole=(100, 48, 6), content=(100, 112, 0.8), ew=4, fw=0),
}


def precio_unitario(diseno: str) -> int:
    return PRECIO_PERSONALIZADO if diseno == "Personalizado" else PRECIO_CATALOGO


def svg_preview(diseno: str, color: str) -> str:
    """Devuelve el llavero como SVG (data URI) con el diseño y color elegidos."""
    f = DISENOS[diseno]
    c = COLORES[color]
    hx, hy, hr = f["hole"]
    cx, cy, s = f["content"]
    tab_edge = tab_fill = ""
    if f["tab"]:
        tab_edge = (f'<path d="{f["tab"]}" fill="{c["edge"]}" stroke="{c["edge"]}" '
                    f'stroke-width="{f["ew"]}" stroke-linejoin="round"/>')
        tab_fill = (f'<path d="{f["tab"]}" fill="{c["fill"]}" stroke="{c["fill"]}" '
                    f'stroke-width="{f["fw"]}" stroke-linejoin="round"/>')
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200" width="320" height="320">
<path d="{f['d']}" fill="{c['edge']}" stroke="{c['edge']}" stroke-width="{f['ew']}" stroke-linejoin="round"/>
{tab_edge}
<path d="{f['d']}" fill="{c['fill']}" stroke="{c['fill']}" stroke-width="{f['fw']}" stroke-linejoin="round"/>
{tab_fill}
<circle cx="{hx}" cy="{hy}" r="{hr}" fill="#eef3fb"/>
<g transform="translate({cx} {cy}) scale({s})">
<text x="0" y="-2" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-weight="700" font-size="20" fill="{c['ink']}">VitalTap</text>
<circle cx="-12" cy="18" r="2.6" fill="{c['ink']}"/>
<path d="M-5 12 q 7 6 0 12 M2 8 q 11 10 0 20" fill="none" stroke="{c['ink']}" stroke-width="3" stroke-linecap="round"/>
</g>
</svg>"""
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode()).decode()


# ---------------------------------------------------------------- Estado ---
if "carrito" not in st.session_state:
    st.session_state.carrito = []
    st.session_state.siguiente_id = 1


def agregar_al_pedido() -> None:
    diseno = st.session_state.sel_diseno
    nota = st.session_state.get("nota_diseno", "").strip() if diseno == "Personalizado" else ""
    st.session_state.carrito.append(
        {
            "id": st.session_state.siguiente_id,
            "diseno": diseno,
            "color": st.session_state.sel_color,
            "cantidad": st.session_state.sel_cantidad,
            "precio": precio_unitario(diseno),
            "nota": nota,
        }
    )
    st.session_state.siguiente_id += 1
    st.session_state.sel_cantidad = 1


def quitar(item_id: int) -> None:
    st.session_state.carrito = [i for i in st.session_state.carrito if i["id"] != item_id]


# ================================================================= PÁGINA ===
# ------------------------------------------------------------------- Hero ---
col_texto, col_logo = st.columns([1.2, 1], gap="large", vertical_alignment="center")
with col_texto:
    html(
        """
<p class="eyebrow">Llavero inteligente con tecnología NFC</p>
<h1 class="hero-title">Tu ficha médica de emergencia, siempre contigo.</h1>
<p class="lead">Alergias, medicamentos y contactos de emergencia al alcance de un toque. Acerca un celular compatible a tu VitalTap y se abre tu ficha. Sin batería, sin apps.</p>
"""
    )
    html(
        """
<a href="#pedido" target="_self" style="display:inline-block;background:#0bc0e0;color:#0b1d4d;text-decoration:none;font-weight:700;padding:14px 26px;border-radius:999px;font-size:17px">Pedir el mío · desde $89 MXN</a>
"""
    )
with col_logo:
    st.image(str(ASSETS / "logo.png"), use_container_width=True)

# ------------------------------------------------------------- Beneficios ---
b1, b2, b3 = st.columns(3, gap="large")
beneficios = [
    ("Sin batería ni apps", "Funciona con ondas electromagnéticas: nunca se descarga y quien lo escanea no necesita instalar nada."),
    ("Acceso instantáneo", "Un toque con un celular compatible con NFC abre tu ficha médica de emergencia en segundos."),
    ("Tú decides qué mostrar", "Eliges qué datos compartir y puedes actualizarlos cuando quieras, sin cambiar de llavero."),
]
for col, (titulo, texto) in zip((b1, b2, b3), beneficios):
    with col:
        html(f'<div class="card"><h3>{titulo}</h3><p>{texto}</p></div>')

st.divider()

# ----------------------------------------------------------- Cómo funciona ---
c_pasos, c_tel = st.columns([1.3, 1], gap="large", vertical_alignment="center")
with c_pasos:
    st.header("Información accesible cuando más importa")
    html(
        """
<div class="step"><div class="n">1</div><div><h4>Registra tu ficha</h4><p>En la plataforma web captura alergias, enfermedades, medicamentos y contactos de emergencia.</p></div></div>
<div class="step"><div class="n">2</div><div><h4>Llévalo como llavero</h4><p>Tu VitalTap se queda en tus llaves, mochila o cierre de la maleta, siempre a la mano.</p></div></div>
<div class="step"><div class="n">3</div><div><h4>Acerca un celular</h4><p>En una emergencia, quien te ayude acerca su teléfono compatible y ve tu ficha de inmediato.</p></div></div>
"""
    )
with c_tel:
    html(
        """
<div class="phone">
<p class="tag">VitalTap NFC activo</p>
<p class="ttl">Ficha pública básica de emergencia</p>
<div class="alert"><small>Alergias importantes</small><b>Aspirina, Penicilina, Látex</b></div>
<div class="ok"><small>Contacto de emergencia</small><b>Nombre de tu contacto</b><div class="call">Llamar ahora</div></div>
</div>
<p style="text-align:center;font-size:14px;color:#3d4a70;margin-top:10px">Ejemplo ilustrativo de una ficha</p>
"""
    )

st.divider()

# -------------------------------------------------------------- Para quién ---
st.header("Pensado para quienes más lo necesitan")
st.markdown("Y para las personas que los cuidan, porque saber que la información está a un toque da tranquilidad.")
publico = [
    ("Adultos mayores", "Medicamentos, padecimientos y a quién llamar, aunque no puedan explicarlo en el momento."),
    ("Niños", "En la mochila o el uniforme: sus alergias y el contacto de mamá o papá siempre disponibles."),
    ("Alergias y enfermedades crónicas", "Lo que un paramédico o un desconocido debe saber de ti, sin que tengas que decirlo."),
    ("Deportistas", "Ligero y portátil para entrenar, correr o competir con tu información a la mano."),
]
for col, (titulo, texto) in zip(st.columns(4, gap="medium"), publico):
    with col:
        html(f'<div class="card"><h3>{titulo}</h3><p>{texto}</p></div>')

st.divider()

# ---------------------------------------------------------------- Diseños ---
st.header("Elige el VitalTap que va contigo")
st.markdown("Doce diseños de catálogo en varios colores, o crea uno totalmente tuyo. Todos con chip NFC y tu ficha médica de emergencia.")
st.image(
    str(ASSETS / "catalogo.jpg"),
    caption="Catálogo VitalTap: círculo, estrella, corazón, huella, mariposa, flor, luna, planeta, nube, rayo, corona y diamante.",
    use_container_width=True,
)
e1, e2 = st.columns(2, gap="large")
with e1:
    html(
        """
<h3>Lo que trae cada llavero</h3>
<div class="spec"><span>Material</span><span>PLA impreso en 3D</span></div>
<div class="spec"><span>Chip</span><span>NFC integrado</span></div>
<div class="spec"><span>Energía</span><span>Pasivo: sin batería ni recarga</span></div>
<div class="spec"><span>Incluye</span><span>Argolla para llaves</span></div>
"""
    )
with e2:
    html(
        f"""
<div class="band"><h3>¿Quieres un diseño personalizado?</h3>
<p style="color:#c9d5f2;margin:0">Cuéntanos la forma, el color o la idea que tienes en mente y la hacemos en impresión 3D para ti. Diseño personalizado: ${PRECIO_PERSONALIZADO} MXN.</p></div>
"""
    )

st.divider()

# ------------------------------------------------------------- Arma tu pedido ---
html('<a id="pedido"></a>')
st.header("Arma tu pedido")
st.markdown("Elige un diseño, cámbiale el color y agrégalo. Cuando termines, envía tu pedido por WhatsApp.")

p_prev, p_ctrl = st.columns([1, 1.2], gap="large")
with p_ctrl:
    diseno = st.selectbox("1. Elige tu diseño", list(DISENOS.keys()), index=1, key="sel_diseno")
    if diseno == "Personalizado":
        st.text_input("Cuéntanos tu idea", placeholder="Forma, color, nombre o texto que quieres", key="nota_diseno")
    color = st.radio("2. Elige el color", list(COLORES.keys()), horizontal=True, key="sel_color")
    st.number_input("3. Cantidad", min_value=1, max_value=99, value=1, step=1, key="sel_cantidad")
    unidad = precio_unitario(diseno)
    cantidad = st.session_state.sel_cantidad
    st.markdown(f"### ${unidad} MXN por llavero")
    st.caption(f"Subtotal: ${unidad * cantidad} MXN")
    st.button("Agregar al pedido", type="primary", use_container_width=True, on_click=agregar_al_pedido)
with p_prev:
    html(f'<div class="stage"><img src="{svg_preview(diseno, color)}" width="320" alt="Vista previa del llavero {diseno} en color {color}"></div>')
    st.caption("Vista previa ilustrativa. El color final puede variar un poco.")

# ------------------------------------------------------------------ Carrito ---
st.subheader("Tu pedido")
carrito = st.session_state.carrito
if not carrito:
    st.info('Aún no has agregado nada. Elige un diseño y toca "Agregar al pedido".')
else:
    for item in carrito:
        i1, i2, i3 = st.columns([5, 2, 1.5], vertical_alignment="center")
        detalle = f"**{item['diseno']}** · {item['color']}"
        if item["nota"]:
            detalle += f" ({item['nota']})"
        i1.markdown(f"{detalle} × {item['cantidad']}")
        i2.markdown(f"**${item['precio'] * item['cantidad']} MXN**")
        i3.button("Quitar", key=f"quitar_{item['id']}", on_click=quitar, args=(item["id"],))

total = sum(i["precio"] * i["cantidad"] for i in carrito)
piezas = sum(i["cantidad"] for i in carrito)
st.markdown(f"## Total: ${total} MXN")

n1, n2 = st.columns(2)
nombre = n1.text_input("Tu nombre", placeholder="Nombre y apellido", key="cliente_nombre").strip()
comentarios = n2.text_input("Comentarios (opcional)", placeholder="Entrega, fecha o lo que necesites", key="cliente_notas").strip()

listo = bool(carrito) and bool(nombre)
lineas = [
    f"- {i['cantidad']} x {i['diseno']}, color {i['color']}"
    + (f" ({i['nota']})" if i["nota"] else "")
    + f": ${i['precio']} c/u = ${i['precio'] * i['cantidad']} MXN"
    for i in carrito
]
mensaje = (
    f"Hola, soy {nombre}. Quiero hacer este pedido de VitalTap:\n\n"
    + "\n".join(lineas)
    + f"\n\nPiezas: {piezas}\nTotal: ${total} MXN"
    + (f"\nComentarios: {comentarios}" if comentarios else "")
    + "\n\nQuedo al pendiente para coordinar el pago y la entrega. Gracias."
)
st.link_button(
    "Enviar pedido por WhatsApp",
    f"https://wa.me/{WA_PRINCIPAL}?text={quote(mensaje)}",
    type="primary",
    disabled=not listo,
)
if not carrito:
    st.warning("Agrega al menos un llavero a tu pedido.")
elif not nombre:
    st.warning("Escribe tu nombre para poder enviar el pedido.")

st.markdown(
    f"¿Buscas otro modelo o un pedido al mayoreo? "
    f"[Cotiza directo por WhatsApp](https://wa.me/{WA_PRINCIPAL}?text={quote('Hola, quiero cotizar otro modelo o mayoreo de VitalTap')})."
)

st.divider()

# ----------------------------------------------------------------- Precios ---
st.header("Precio claro y accesible")
st.markdown("Protege a tu familia o a ti mismo por menos de lo que cuesta una comida.")
pr1, pr2 = st.columns(2, gap="large")
with pr1:
    html(
        f"""
<div class="price dark"><p class="lbl" style="color:#6fe3f5">Diseños de catálogo</p>
<p class="amt">${PRECIO_CATALOGO} <span>MXN</span></p><p style="color:#c9d5f2;margin:4px 0 0">Por llavero</p>
<ul><li>Elige entre los 12 diseños del catálogo</li><li>Llavero con chip NFC y argolla</li><li>Tu ficha médica de emergencia</li><li>Actualiza tus datos cuando quieras</li></ul></div>
"""
    )
with pr2:
    html(
        f"""
<div class="price light"><p class="lbl" style="color:#07708a">Diseño personalizado</p>
<p class="amt">${PRECIO_PERSONALIZADO} <span>MXN</span></p><p style="color:#3d4a70;margin:4px 0 0">Por llavero</p>
<ul><li>Tu propia forma, color o idea</li><li>Hecho en impresión 3D para ti</li><li>Mismo chip NFC y misma ficha médica</li></ul></div>
"""
    )
st.markdown("¿Buscas otro modelo o necesitas varios para una escuela, clínica, equipo o empresa? **Escríbenos y te cotizamos directamente.**")

st.divider()

# -------------------------------------------------------------- Privacidad ---
v1, v2 = st.columns(2, gap="large")
with v1:
    st.subheader("Tu privacidad, primero")
    st.markdown("La ficha es pública y básica a propósito: muestra solo lo que tú decides incluir. Estamos trabajando en mejoras como protección con PIN.")
with v2:
    st.subheader("Uso responsable")
    st.markdown("VitalTap necesita un celular compatible con NFC y no sustituye la atención médica profesional: es una ayuda para que la información importante llegue a tiempo.")

st.divider()

# --------------------------------------------------------------------- FAQ ---
st.header("Preguntas frecuentes")
faq = [
    ("¿Necesito instalar una app?", "No. Basta con acercar un celular compatible con NFC al llavero para abrir la ficha. Tú administras tus datos desde la plataforma web."),
    ("¿Necesita batería o carga?", "No. Funciona de forma pasiva con ondas electromagnéticas, así que siempre está listo."),
    ("¿Puedo pedir un diseño que no está en el catálogo?", f"Sí. Los diseños personalizados cuestan ${PRECIO_PERSONALIZADO} MXN. Para otros modelos o pedidos al mayoreo, escríbenos por WhatsApp con tu idea y te cotizamos directamente."),
    ("¿Puedo cambiar mis datos después?", "Sí. Puedes actualizar alergias, medicamentos y contactos en la plataforma web sin cambiar de llavero."),
    ("¿Quién puede ver mi información?", "Quien acerque un celular compatible a tu llavero verá la ficha pública básica. Por eso tú decides qué datos incluir en ella."),
]
for pregunta, respuesta in faq:
    with st.expander(pregunta):
        st.write(respuesta)

st.divider()

# ---------------------------------------------------------------- Contacto ---
html(
    """
<div class="band" style="text-align:center"><h2>Pide tu VitalTap</h2>
<p style="color:#c9d5f2;margin:0">Escríbenos con el diseño y el color que quieres, y cuántas piezas necesitas. Te respondemos para coordinar tu pedido.</p></div>
"""
)
st.write("")
saludo = quote("Hola, quiero pedir mi VitalTap")
w1, w2 = st.columns(2)
w1.link_button("WhatsApp: 81 3240 4926", f"https://wa.me/{WA_PRINCIPAL}?text={saludo}", type="primary", use_container_width=True)
w2.link_button("WhatsApp: 81 1471 1236", f"https://wa.me/{WA_SECUNDARIO}?text={saludo}", type="primary", use_container_width=True)
s1, s2, s3 = st.columns(3)
s1.link_button("Instagram @vitaltap", "https://instagram.com/vitaltap", use_container_width=True)
s2.link_button("Facebook @vitaltap", "https://facebook.com/vitaltap", use_container_width=True)
s3.link_button("TikTok @vitaltap", "https://tiktok.com/@vitaltap", use_container_width=True)

html(
    """
<p class="footer"><b>VitalTap</b> · Tu ficha médica de emergencia, siempre contigo. · Proyecto de la Facultad de Enfermería, UANL</p>
"""
)
