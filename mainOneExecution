from playwright.sync_api import sync_playwright
import chompjs
import time
import re
import os
import random
import argparse
import requests
from dotenv import load_dotenv
from datetime import datetime

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

def hacer_clic_en_fecha(page, fecha_str):
    fecha_split = fecha_str.split("/")
    day = fecha_split[0]
    month = fecha_split[1]
    year = fecha_split[2]


    fecha_actual = datetime.now()
    
    meses_diferencia = (int(year) - fecha_actual.year) * 12 + (int(month) - fecha_actual.month)


    # Abrimos el calendario
    page.locator("#first-input").click()
    page.locator("label[for='trip-go']").click()
    for i in range(meses_diferencia):
        page.locator(".lightpick__next-action").click()
        page.wait_for_timeout(100)

    

    page.locator(f"//div[contains(@class, 'lightpick__day') and not(contains(@class, 'is-next-month')) and not(contains(@class, 'is-previous-month')) and text()='{int(day)}']").click()
    
    # Aceptamos
    page.locator(".lightpick__apply-action-sub").click(delay=100)

def buscar_y_capturar_datos(origen, destino, fecha):
    datos_extraidos = None

    # Función interna para espiar las respuestas de red mientras Playwright navega
    def interceptar_respuesta(response):
        nonlocal datos_extraidos
        if "trainEnlacesManager.getTrainsList.dwr" in response.url and response.request.method == "POST":
            try:
                raw_text = response.text()
                datos_extraidos = parse_dwr_response(raw_text)
            except:
                pass

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True) 
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()
        
        # Le decimos a Playwright que escuche todas las respuestas de red
        page.on("response", interceptar_respuesta)

        try:
            # 1. Navegar a la web
            page.goto("https://www.renfe.com/es/es")
            
            # 2. Aceptar cookies
            page.locator("#onetrust-accept-btn-handler").click() 

            # 3. Rellenar el formulario simulando escritura humana (delay)
            page.locator("#origin").type(origen, delay=100)
            page.locator("#awesomplete_list_1_item_0").click()
            page.locator("#destination").type(destino, delay=100)
            page.locator("#awesomplete_list_2_item_0").click()
            hacer_clic_en_fecha(page, fecha)
            
            # 4. Hacer clic en buscar
            page.locator("#ticketSearchBt").click()


            # Esperamos un poco para que la web haga la petición y cargue
            page.wait_for_timeout(10000) 
            
        except Exception as e:
            print(f"[-] Error en la navegación automatizada: {e}")
        finally:
            browser.close() 

    return datos_extraidos

def main():
    parser = argparse.ArgumentParser(description="Renfe Sniper Elite")
    parser.add_argument("-o", "--origen", type=str, help="Estación de origen", required=True)
    parser.add_argument("-d", "--destino", type=str, help="Estación de destino", required=True)
    parser.add_argument("-f", "--fecha", type=str, help="Fecha de viaje", required=True)
    parser.add_argument("-s", "--salida", type=str, default="00:00", help="Hora MÍNIMA salida")
    parser.add_argument("-l", "--llegada", type=str, default="23:59", help="Hora MÁXIMA llegada")
    parser.add_argument("-t", "--duracion", type=int, default=999, help="Duración MÁXIMA (min)")
    args = parser.parse_args()

    print("\n    =========================================")
    print("    🚄 RENFE BOT TICKET AVAILABILITY")
    print("    =========================================\n")

    

    print(f"\n[*] {time.strftime('%H:%M:%S')} - Abriendo navegador e iniciando búsqueda...")
    
    # 1. Ejecutar ciclo completo de navegador
    data = buscar_y_capturar_datos(args.origen, args.destino, args.fecha)

    # 2. Aplicar la lógica de filtrado exacta del código original
    if data and 'listadoTrenes' in data and len(data['listadoTrenes']) > 0:
        trenes = data['listadoTrenes'][0].get('listviajeViewEnlaceBean', [])
        print(f"[+] Datos capturados con éxito. Escaneando {len(trenes)} trenes...")

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
                    
                    print(f"  ✅ ¡PLAZA ENCONTRADA!: Salida a las {h_salida} por {precio}€")
                    enviar_telegram(msg)
                    time.sleep(2) # Pausa breve para no saturar la API de Telegram si hay varios
    else:
        print("[-] No se interceptaron datos válidos en este ciclo (posible error de carga o sin trenes).")


if __name__ == "__main__":
    main()