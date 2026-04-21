from playwright.sync_api import sync_playwright
import chompjs
import time
import re
import os
import random
import argparse
import requests
from dotenv import load_dotenv

load_dotenv()

# ==========================================
# CONFIGURACIÓN DE TELEGRAM
# ==========================================

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def enviar_telegram(mensaje):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": mensaje, "parse_mode": "HTML"}
    try:
        requests.post(url, json=payload, timeout=10)
    except Exception as e:
        print(f"[-] Error enviando a Telegram: {e}")

# ==========================================
# LÓGICA DEL BOT
# ==========================================

stolen_request = {"url": None, "headers": None, "post_data": None, "caught": False}

def parse_dwr_response(raw_text):
    try:
        match = re.search(r'handleCallback\(".*?",".*?",(.*?)\);?\s*\}\)\(\);', raw_text, re.DOTALL)
        if match: return chompjs.parse_js_object(match.group(1))
        return None
    except: return None

def intercept_request(request):
    if "trainEnlacesManager.getTrainsList.dwr" in request.url and request.method == "POST":
        if not stolen_request["caught"]:
            stolen_request["url"], stolen_request["headers"], stolen_request["post_data"] = request.url, request.headers, request.post_data
            stolen_request["caught"] = True
            print("\n[+] Sesión interceptada con éxito.")

def main():
    parser = argparse.ArgumentParser(description="Renfe Sniper Elite")
    parser.add_argument("-s", "--salida", type=str, default="00:00", help="Hora MÍNIMA salida")
    parser.add_argument("-l", "--llegada", type=str, default="23:59", help="Hora MÁXIMA llegada")
    parser.add_argument("-d", "--duracion", type=int, default=999, help="Duración MÁXIMA (min)")
    args = parser.parse_args()

    print("\n    =========================================")
    print("    🚄 RENFE BOT TICKET AVAILABILITY")
    print("    =========================================\n")
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        page.on("request", intercept_request)
        page.goto("https://www.renfe.com/es/es")

        print("[*] Esperando búsqueda manual en el navegador...")
        while not stolen_request["caught"]: page.wait_for_timeout(1000)

        while True:
            try:
                response = context.request.post(stolen_request["url"], headers=stolen_request["headers"], data=stolen_request["post_data"])
                if response.status == 200:
                    data = parse_dwr_response(response.text())
                    if data and 'listadoTrenes' in data and len(data['listadoTrenes']) > 0:
                        trenes = data['listadoTrenes'][0].get('listviajeViewEnlaceBean', [])
                        print(f"[+] {time.strftime('%H:%M:%S')} - Escaneando...")

                        for t in trenes:
                            h_salida = t.get('horaSalida', '00:00')
                            h_llegada = t.get('horaLlegada', '23:59')
                            duracion_min = t.get('duracionViajeTotalEnMinutos', 0)
                            tarifas = t.get('tarifasDisponibles')
                            solo_h = str(t.get('soloPlazaH', 'false')).lower() == 'true'

                            # Aplicación de filtros
                            if h_salida >= args.salida and h_llegada <= args.llegada and duracion_min <= args.duracion:
                                if tarifas and tarifas != "null" and not solo_h:
                                    tipo = t.get('tipoTrenUno', 'Tren')
                                    precio = t.get('tarifaMinima', '??')
                                    
                                    msg = (f"<b>¡BILLETE ENCONTRADO!</b> 🚄\n\n"
                                           f"<b>Tipo:</b> {tipo}\n"
                                           f"<b>Salida:</b> {h_salida}\n"
                                           f"<b>Llegada:</b> {h_llegada}\n"
                                           f"<b>Duración:</b> {duracion_min} min\n"
                                           f"<b>Precio:</b> {precio}€\n\n"
                                           f"¡Corre a la web!")
                                    
                                    print(f"  ✅ ¡PLAZA ENCONTRADA!: {h_salida}")
                                    enviar_telegram(msg)
                                    time.sleep(1) 
                else:
                    print(f"[-] Error HTTP: {response.status}")
            except Exception as e:
                print(f"[-] Error: {e}")

            delay = random.randint(180, 300)
            page.wait_for_timeout(delay * 1000)

if __name__ == "__main__":
    main()