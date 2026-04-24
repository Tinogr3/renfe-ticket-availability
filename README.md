# 🚄 Renfe Bot Ticket Availability

Un bot de monitorización avanzada para billetes de Renfe (España) que utiliza **Playwright** para evadir bloqueos de seguridad y **Telegram** para enviarte notificaciones en tiempo real cuando se liberan plazas.

Renfe utiliza sistemas anti-bot complejos (Akamai, telemetría activa y validación de sesión en Java). Este bot utiliza el **"Modo Cyborg"**: tú realizas la búsqueda inicial de forma humana para validar la sesión y el bot "intercepta" el tráfico de red para automatizar el escaneo indefinidamente con las credenciales reales.

## ¿Por qué este bot?

El principal fin de la creación de este bot es didáctico ya que nunca había hecho nada parecido y este era un caso sencillo para probar.

El segundo incentivo, importante también, desde que se pusieron los billetes de media distancia gratis o con los abonos multiviaje que cancelas y te devuelven el viaje, es común encontrar trenes bloqueados por reservas masivas que terminan cancelandose a última hora, así con este bot no tengo que estar pendiente. (También se solucionaría este problema si cogiese los billetes con tiempo y no los dejase siempre para cuando faltan 2 días pero eso se me hace más difícil xd)



### Características
- **Evade Akamai:** Al usar un navegador Chromium real, pasa los controles de telemetría.
- **Filtros Inteligentes:**
  - 🕒 Hora mínima de salida.
  - 🏁 Hora máxima de llegada.
  - ⏳ Duración máxima del trayecto.
  - ♿ **Filtro Anti-H:** Ignora las plazas de Hándicap (Silla de ruedas) si así lo deseas.
- **Notificaciones:** Mensajes detallados por Telegram con enlace directo a la web.



##  Instalación

1. **Clonar el repositorio:**

    git clone https://github.com/Tinogr3/renfe-ticket-availability.git
   
    cd renfe-ticket-availability

3. **Crear y activar entorno virtual:**

    python3 -m venv venv
   
    source venv/bin/activate  # En Linux/macOS
   
    .\venv\Scripts\Activate.ps1 # En Windows

5. **Instalar dependencias:**

    pip install -r requirements.txt
   
    playwright install chromium
   


## Configuración Telegram

1. **Crea el bot:**

    Busca a @BotFather en Telegram, escribe /newbot y sigue los pasos. Al final te dará un Token (algo como 712345678:AAH_ABC123...).

2. **Obten tu Chat ID:**

    Busca a @userinfobot en Telegram y envíale cualquier mensaje. Te responderá con tu Id numérico (ej. 12345678).

3. **Inicia el Bot:**

    Entra en el chat de tu nuevo bot y dale a "Iniciar". Si no lo haces, el bot no tendrá permiso para escribirte.

4. **Pega las variables:**

    Pega el token y el chat ID en las variables del .env (elimina ".example")
   


## Uso
Ejecuta el script pasando los filtros deseados:

También puedes usar "python main.py -h" para ver ayuda por terminal

**Ejemplo: Solo trenes que salgan después de las 08:00, lleguen antes de las 22:00 y que no tarden más de 180 minutos (3 horas):**
  
    python main.py --salida 08:00 --llegada 22:00 --duracion 180

Pasos del Modo Cyborg:
Se abrirá una ventana de Chromium. 

**Importante aceptar las cooquies nada más entrar**

Realiza la búsqueda manualmente (Origen, Destino y Fecha).

Haz clic en "Buscar".

En cuanto aparezcan los resultados, la terminal indicará [+] Petición interceptada.

Ya puedes minimizar el navegador (¡no lo cierres!) y el bot se quedará vigilando por ti.

## Uso Automatizado
Modifica el run.sh con los parámetros de tu interés, asegurate de que los nombres sean correctos y ejecuta ./run.sh que llamará al mainAuto.py, o siempre puedes usarlo directamente e insertar parámetros en consola. Más util para ahorrar memoria ya que no tendrá que estar el navegador abierto constantemente pero fallará en el momento que modifiquen la web de renfe por eso dejo la opción manual también.

## Uso en la nube (Github Actions)
Puedes hacer un fork del proyecto, usar el workflow ya creado que ejecuta un cron cada 5 minutos para hacer una única búsqueda, la web de renfe no lo hace pero esto evita bloqueos de ip. Tienes que configurar el token de telegram y tu chat id en los secrets del proyecto, los parámetros de búsqueda se introducen en las variables del actions. ¡¡Cuidado con el número de minutos de uso gratuito de los que disponemos!!



## ⚠️ Descargo de Responsabilidad
Este proyecto ha sido creado con fines educativos y de aprendizaje sobre automatización web. El uso de bots puede violar los términos de servicio de Renfe. Utilízalo de forma responsable y bajo tu propia cuenta y riesgo. El autor no se hace responsable del uso que se le dé a esta herramienta.

Hecho con ❤️ por Tinogr3
