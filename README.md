# 🤖 Web Scraper & Price Monitor Bot

> Un bot automatizado desarrollado en Python para el monitoreo de precios en tiempo real con notificaciones automatizadas en la nube mediante CI/CD.

## 🚀 Características Principales
* **Extracción Robusta:** Utiliza `BeautifulSoup` y expresiones regulares (`re`) para el parsing y limpieza de datos independiente de símbolos monetarios.
* **Arquitectura Serverless / Cloud Cron:** Automatizado mediante **GitHub Actions** para ejecutarse de forma autónoma cada 6 horas sin costos de servidores.
* **Sistema de Alertas en Tiempo Real:** Integración directa con Webhooks de Discord para notificaciones instantáneas de caídas de precios.
* **Manejo de Logs Profesionales:** Trazabilidad completa de eventos y errores basada en el módulo `logging` de Python.

## 🛠️ Stack Tecnológico
* **Lenguaje:** Python 3.10+
* **Librerías:** Requests, BeautifulSoup4, Python-Dotenv
* **Infraestructura & CI/CD:** GitHub Actions (Cron Jobs)
* **Notificaciones:** Discord Webhooks

## ⚙️ Configuración y Ejecución Local

1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/monitor-precios-bot.git](https://github.com/tu-usuario/monitor-precios-bot.git)
   cd monitor-precios-bot