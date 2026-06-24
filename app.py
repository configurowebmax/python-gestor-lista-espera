"""
=====================================================================
 Gestor de Lista de Espera
 ConfiguroWeb · 2026 · Python real en el navegador (PyScript)
=====================================================================
"""
from pyscript import document, window
from js import localStorage
import json
import math

APP_CLAVE = "python_gestor_lista_espera_datos"
VERSION = "1.0.0"


# =====================================================================
#  Lógica de negocio
# =====================================================================
class Calculadora:
    """Modelo de cálculo de Gestor de Lista de Espera."""

    def __init__(self, en_cola, tiempo_prom):
        self.en_cola = float(en_cola)
        self.tiempo_prom = float(tiempo_prom)

    def calcular(self):
        """Ejecuta el cálculo principal y devuelve un dict de resultados."""

        espera_min = self.en_cola * self.tiempo_prom
        horas = espera_min / 60
        return {"espera_min": espera_min, "espera_horas": horas}


    def diagnostico(self, resultados):
        """Texto explicativo del resultado."""

        if resultados["espera_min"] > 60:
            return "⚠️ Espera larga. Considera llamar refuerzos de personal."
        return "✅ Tiempo de espera razonable."



# =====================================================================
#  Formateadores
# =====================================================================
def fmt_moneda(v):
    if v is None:
        return "—"
    if math.isinf(v):
        return "∞"
    return f"${v:,.0f}"

def fmt_num(v):
    if v is None:
        return "—"
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}"

def fmt_pct(v):
    if v is None:
        return "—"
    return f"{v:.1f}%"


# =====================================================================
#  Persistencia localStorage
# =====================================================================
def cargar_guardado():
    try:
        raw = localStorage.getItem(APP_CLAVE)
        if raw:
            return json.loads(raw)
    except Exception:
        pass
    return None

def guardar_ls(datos):
    try:
        localStorage.setItem(APP_CLAVE, json.dumps(datos))
        return True
    except Exception:
        return False


# =====================================================================
#  UI helpers
# =====================================================================
def input_float(eid):
    el = document.querySelector(f"#{eid}")
    if not el or not el.value:
        return 0.0
    try:
        return float(el.value)
    except (ValueError, TypeError):
        return 0.0

def mostrar(html, clase=""):
    caja = document.querySelector("#resultado")
    caja.innerHTML = html
    caja.classList.remove("hidden", "is-error", "is-success")
    if clase:
        caja.classList.add(clase)


# =====================================================================
#  Handlers
# =====================================================================
def calcular_handler(event=None):
    """Lee inputs, instancia, calcula y muestra."""

    c = Calculadora(input_float("en_cola"), input_float("tiempo_prom"))
    r = c.calcular()
    html = f"""
      <div class="result-value">⏳ ~{fmt_num(r["espera_min"])} min de espera</div>
      <p class="result-detail">Equivale a {r["espera_horas"]:.1f} horas.</p>
      <p class="result-detail">{c.diagnostico(r)}</p>
    """
    mostrar(html, clase="is-success")



def guardar_datos(event=None):
    datos = {
            "en_cola": input_float("en_cola"),
            "tiempo_prom": input_float("tiempo_prom"),
        "version": VERSION,
    }
    ok = guardar_ls(datos)
    if ok:
        mostrar("💾 Datos guardados en este navegador.", clase="is-success")
    else:
        mostrar("❌ No se pudieron guardar los datos.", clase="is-error")


def cargar_al_inicio():
    datos = cargar_guardado()
    if not datos:
        return
    try:
        if "en_cola" in datos:
            document.querySelector("#en_cola").value = datos["en_cola"]
        if "tiempo_prom" in datos:
            document.querySelector("#tiempo_prom").value = datos["tiempo_prom"]
        aviso = document.querySelector("#resultado")
        aviso.innerHTML = "📂 Datos cargados. Pulsa <em>Calcular</em>."
        aviso.classList.remove("hidden")
    except Exception:
        pass


def inicializar():
    cargar_al_inicio()
    window.dispatchEvent(window.Event.new("py:ready"))

inicializar()
