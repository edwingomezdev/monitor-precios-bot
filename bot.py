import requests
from bs4 import BeautifulSoup
import re
import os

# Configuración del objetivo
URL = "https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html"
PRECIO_OBJETIVO = 60.00  # Pusimos 60 para forzar la alerta y probar que llegue a Discord

def verificar_precio():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print("🔍 Conectando con el sitio web...")
    try:
        response = requests.get(URL, headers=headers)
        response.raise_for_status() 
        response.encoding = 'utf-8'
    except requests.exceptions.RequestException as e:
        print(f"❌ Error al conectar con la página: {e}")
        return

    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Extraer el título y precio
        titulo = soup.find('h1').get_text().strip()
        precio_texto = soup.find('p', class_='price_color').get_text().strip()
        
        # Limpiar precio con regex
        precio_limpio_str = "".join(re.findall(r"[\d.]+", precio_texto))
        precio_actual = float(precio_limpio_str)

        print(f"📦 Producto: {titulo}")
        print(f"💰 Precio actual: ${precio_actual}")

        # Lógica de comparación
        if precio_actual <= PRECIO_OBJETIVO:
            mensaje = f"¡ALERTA DE OFERTA! '{titulo}' bajó a ${precio_actual}. Consíguelo aquí: {URL}"
            enviar_alerta(mensaje)
        else:
            print("⏳ El precio sigue por encima del objetivo. No se requiere alerta.")

    except AttributeError:
        print("❌ Error: No se pudieron encontrar los elementos HTML esperados.")



def enviar_alerta(mensaje):
    # Lee la URL de forma segura desde las variables de entorno
    WEBHOOK_URL = os.environ.get("DISCORD_WEBHOOK_URL")
    
    if not WEBHOOK_URL:
        print("❌ Error: No se encontró la variable DISCORD_WEBHOOK_URL.")
        return

    payload = {"content": mensaje}
    
    try:
        response = requests.post(WEBHOOK_URL, json=payload)
        if response.status_code == 204:
            print("✅ Alerta enviada exitosamente a Discord.")
        else:
            print(f"❌ Error al enviar la alerta. Código: {response.status_code}")
    except Exception as e:
        print(f"❌ Error de conexión al enviar alerta: {e}")

if __name__ == "__main__":
    verificar_precio()