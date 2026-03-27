import urllib.request
import json
import time
import datetime
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

SB_URL = os.getenv('SUPABASE_URL')
SB_KEY = os.getenv('SUPABASE_KEY')

if not SB_URL or not SB_KEY:
    print("[ERROR] No se encontraron las credenciales de Supabase en el archivo .env")
    exit(1)

HEADERS = {
    'apikey': SB_KEY,
    'Authorization': f'Bearer {SB_KEY}',
    'Content-Type': 'application/json'
}

def check_risk_and_notify():
    print(f"[{datetime.datetime.now()}] Monitoreando niveles de riesgo...")
    try:
        # Consultar ultimo score
        url = f"{SB_URL}/rest/v1/clima_historico?select=score_riesgo,clima&order=fecha.desc&limit=1"
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read())
            if data:
                score = data[0]['score_riesgo']
                clima = data[0]['clima']
                
                if score > 70:
                    print(f"!!! ALERTA CRITICA !!! Score: {score} ({clima})")
                    print("Simulando envío de WhatsApp a gremios cafeteros...")
                    # Aqui se integraria WhatsApp Business API / Twilio
                else:
                    print(f"Estado nominal. Score: {score}")
    except Exception as e:
        print(f"Error en motor de alertas: {e}")

if __name__ == "__main__":
    while True:
        check_risk_and_notify()
        time.sleep(3600) # Chequear cada hora
