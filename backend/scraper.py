import urllib.request
import urllib.parse
import json
import uuid
import datetime
import xml.etree.ElementTree as ET
import os
import platform
import subprocess
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

# ==========================================
# CONFIGURACIÓN SUPABASE
# ==========================================
SB_URL = os.getenv('SUPABASE_URL')
SB_KEY = os.getenv('SUPABASE_KEY')

if not SB_URL or not SB_KEY:
    print("[ERROR] No se encontraron las credenciales de Supabase en el archivo .env")
    exit(1)

HEADERS = {
    'apikey': SB_KEY,
    'Authorization': f'Bearer {SB_KEY}',
    'Content-Type': 'application/json',
    'Prefer': 'return=representation'
}

# ==========================================
# MOTOR C++ — Inteligencia Financiera
# ==========================================

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MOTOR_SRC  = os.path.join(SCRIPT_DIR, 'motor.cpp')
MOTOR_BIN  = os.path.join(SCRIPT_DIR, 'motor.exe' if platform.system() == 'Windows' else 'motor')

def compile_motor():
    """Compila motor.cpp si g++ está disponible, de lo contrario usa fallback Python."""
    if not os.path.exists(MOTOR_SRC):
        print("[MOTOR] No se encontró motor.cpp.")
        return False

    needs_compile = (
        not os.path.exists(MOTOR_BIN) or
        os.path.getmtime(MOTOR_SRC) > os.path.getmtime(MOTOR_BIN)
    )

    if needs_compile:
        print("[MOTOR C++] Intentando compilar motor.cpp con g++ ...")
        try:
            result = subprocess.run(
                ['g++', '-O2', '-o', MOTOR_BIN, MOTOR_SRC, '-lm'],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                print("[MOTOR C++] Compilacion exitosa ✓")
                return True
            else:
                print(f"[MOTOR] Error de compilacion C++.")
        except FileNotFoundError:
            print("[MOTOR] G++ no encontrado. Se activara el fallback de Python.")
        except Exception as e:
            print(f"[MOTOR] Error inesperado en compilacion: {e}")
    else:
        if os.path.exists(MOTOR_BIN):
            print("[MOTOR C++] Binario existente listo.")
            return True
    return False

def call_motor(cafe: float, trm: float, banrep: float):
    """Ejecuta el motor C++ y parsea su salida JSON. Retorna dict o None."""
    if not os.path.exists(MOTOR_BIN):
        return None
    try:
        result = subprocess.run(
            [MOTOR_BIN, str(cafe), str(trm), str(banrep)],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            data = json.loads(result.stdout)
            print(f"[MOTOR C++] Score={data['score']}  Clima={data['clima']}  Liquidez={data['liquidez_pct']}%")
            print(f"            Cafe: {data['senal_cafe']}")
            print(f"            TRM:  {data['senal_trm']}")
            print(f"            Proyeccion 7d={data['proyeccion_7d']}  30d={data['proyeccion_30d']}")
            print(f"            Recomendacion: {data['recomendacion']}")
            return data
        else:
            print(f"[MOTOR] Error ejecución: {result.stderr}")
    except Exception as e:
        print(f"[MOTOR] Excepción al ejecutar motor: {e}")
    return None

def calcular_score_python(trm: float, cafe: float, banrep: float):
    """Fallback Python si g++ no está instalado."""
    score = 0
    if cafe < 1200000:   score += 50
    elif cafe < 1500000: score += 30
    elif cafe < 1750000: score += 15
    elif cafe < 2000000: score += 5

    if trm > 5000:   score += 30
    elif trm > 4500: score += 20
    elif trm > 4200: score += 10

    if banrep > 12:  score += 20
    elif banrep > 9: score += 12
    elif banrep > 6: score += 5

    score = min(max(score, 5), 95)
    if score <= 35:   clima = "Bonanza"
    elif score <= 65: clima = "Estabilidad"
    else:             clima = "Tormenta"
    return score, clima


def fetch_trm():
    """Obtiene la TRM actual de Datos Abiertos Colombia."""
    print("Obteniendo TRM...")
    try:
        url = "https://www.datos.gov.co/resource/32sa-8pi3.json?$limit=1&$order=vigenciadesde%20DESC"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
            if data and len(data) > 0:
                trm = float(data[0]['valor'])
                print(f"TRM obtenida: ${trm}")
                return trm
    except Exception as e:
        print(f"Error obteniendo TRM: {e}")
    return 4100.00  # Fallback

def fetch_coffee_price():
    """Obtiene el precio real del café desde la web oficial de la FNC."""
    print("Obteniendo Precio del Café desde la FNC...")
    try:
        url = "https://federaciondecafeteros.org/wp/"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
            # Buscar el patrón "$2.345.000" después de "Precio interno de referencia"
            import re
            match = re.search(r'Precio interno de referencia.*?\$([\d\.]+)', html, re.DOTALL)
            if match:
                precio_str = match.group(1).replace('.', '')
                precio = float(precio_str)
                print(f"Precio Café (FNC): ${precio}")
                return precio
            else:
                print("No se encontró el patrón de precio en la FNC.")
    except Exception as e:
        print(f"Error obteniendo precio FNC: {e}")
    
    # Fallback si falla el scrap (usando rango histórico realista)
    print("Usando precio de respaldo...")
    return 2150000.0

def fetch_news():
    """Lee RSS de La República."""
    print("Obteniendo Noticias de Economía...")
    noticias = []
    try:
        url = "https://www.larepublica.co/rss"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            root = ET.fromstring(response.read())
            for i, item in enumerate(root.findall('./channel/item')):
                if i >= 5: break
                titulo = item.find('title').text if item.find('title') is not None else 'Sin título'
                link   = item.find('link').text  if item.find('link')  is not None else '#'
                noticias.append({
                    "id":     str(uuid.uuid4()),
                    "titulo": titulo,
                    "fuente": "La República",
                    "fecha":  datetime.datetime.now().isoformat(),
                    "enlace": link
                })
                print(f"- {titulo}")
    except Exception as e:
        print(f"Error leyendo noticias RSS: {e}")
        noticias.append({
            "id": str(uuid.uuid4()),
            "titulo": "BanRep mantiene politica monetaria estable",
            "fuente": "BanRep",
            "fecha":  datetime.datetime.now().isoformat(),
            "enlace": "#"
        })
    return noticias

def update_supabase(trm, cafe, noticias, motor_result=None):
    print("Conectando con Supabase...")
    fecha_hoy   = datetime.datetime.now().strftime("%Y-%m-%d")
    TASA_BANREP = 9.75

    # ===== SCORE: Motor C++ primero, Python como respaldo =====
    if motor_result:
        score_riesgo = motor_result['score']
        clima        = motor_result['clima']
        print(f"[C++] Score: {score_riesgo}/100 -> {clima}")
    else:
        score_riesgo, clima = calcular_score_python(trm, cafe, TASA_BANREP)
        print(f"[PY]  Score: {score_riesgo}/100 -> {clima}")

    clima_data = {
        "precio_cafe":  cafe,
        "trm":          trm,
        "tasa_banrep":  TASA_BANREP,
        "score_riesgo": score_riesgo,
        "clima":        clima,
        "fecha":        fecha_hoy
    }

    try:
        req = urllib.request.Request(
            f"{SB_URL}/rest/v1/clima_historico",
            data=json.dumps(clima_data).encode('utf-8'),
            headers=HEADERS, method='POST'
        )
        urllib.request.urlopen(req)
        print("-> Histórico insertado correctamente.")
    except Exception as e:
        print(f"Error insertando clima: {e}")

    print("Insertando Noticias...")
    for n in noticias:
        try:
            req = urllib.request.Request(
                f"{SB_URL}/rest/v1/noticias",
                data=json.dumps(n).encode('utf-8'),
                headers=HEADERS, method='POST'
            )
            urllib.request.urlopen(req)
            print(f"-> Noticia: {n['titulo'][:45]}...")
        except Exception as e:
            msg = str(e)
            if "does not exist" in msg or "404" in msg:
                print("-> Tabla 'noticias' no existe. Omitiendo.")
                break
            print(f"-> Error: {e}")


if __name__ == "__main__":
    print(f"\n{'='*56}")
    print(f"  * BONANZA - Motor de Inteligencia Financiera")
    print(f"  {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Pitalito, Huila")
    print(f"{'='*56}\n")

    # 1. Compilar Motor C++ si es necesario
    motor_ok = compile_motor()

    # 2. Recolectar datos del mercado
    trm_actual  = fetch_trm()
    cafe_actual = fetch_coffee_price()
    novedades   = fetch_news()

    # 3. Ejecutar Motor C++ de Inteligencia Financiera
    motor_result = call_motor(cafe_actual, trm_actual, 9.75) if motor_ok else None

    # 4. Guardar en Supabase con el score de C++
    update_supabase(trm_actual, cafe_actual, novedades, motor_result)

    print(f"\n{'='*56}")
    print(f"  Recoleccion completada. * Bonanza actualizado.")
    print(f"{'='*56}\n")
