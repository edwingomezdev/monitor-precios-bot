import os
import re
import logging
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

# Cargar variables de entorno si estamos en local (busca un archivo .env)
load_dotenv()

# Configuración profesional de Logs (muestra fecha, hora y nivel del mensaje)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()]
)

# Configuración del objetivo
URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
PRECIO_OBJETIVO = 60.00  # Cambiar al precio real cuando lo dejes operando

def verificar_precio():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    logging.info("Iniciando escaneo de producto...")
    try:
        response = requests.get(URL, headers=headers, timeout=10)
        response.raise_for_status() 
        response.encoding = 'utf-8'
    except requests.exceptions.RequestException as e:
        logging.error(f"Error crítico de red al conectar con la página: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Extracción de datos
        titulo = soup.find('h1').get_text().strip()
        precio_texto = soup.find('p', class_='price_color').get_text().strip()
        
        # Limpieza robusta con expresiones regulares
        precio_limpio_str = "".join(re.findall(r"[\d.]+", precio_texto))
        precio_actual = float(precio_limpio_str)

        logging.info(f"Producto detectado: '{titulo}' | Precio actual: ${precio_actual}")

        # Lógica de negocio
        if precio_actual <= PRECIO_OBJETIVO:
            mensaje = f"¡ALERTA DE OFERTA! '{titulo}' bajó a ${precio_actual}. Consíguelo aquí: {URL}"
            enviar_alerta(mensaje)
        else:
            logging.info("El precio se mantiene por encima del objetivo. Sin acciones requeridas.")

    except AttributeError:
        logging.error("No se pudieron encontrar los selectores HTML esperados (posible cambio en la estructura web).")

def enviar_alerta(mensaje):
    # Obtiene la URL desde las variables de entorno (GitHub Secrets o archivo .env local)
    webhook_url = os.getenv("DISCORD_WEBHOOK_URL")
    
    if not webhook_url:
        logging.error("No se encontró la variable DISCORD_WEBHOOK_URL en el entorno.")
        return

    payload = {"content": mensaje}
    
    try:
        response = requests.post(webhook_url, json=payload)
        if response.status_code == 204:
            logging.info("Alerta de oferta enviada exitosamente a Discord.")
        else:
            logging.error(f"Fallo al enviar alerta a Discord. Código de estado: {response.status_code}")
    except Exception as e:
        logging.error(f"Excepción al intentar notificar a Discord: {e}")

if __name__ == "__main__":
    verificar_precio()