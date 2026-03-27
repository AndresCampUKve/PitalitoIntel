# Guía de Uso Detallada - Pitalito Intel Studio

Esta guía explica cómo operar y entender cada componente del sistema Bonanza.

## 1. El Motor de Inteligencia (Backend)

El backend es el "cerebro" del sistema. Está compuesto por tres partes:

### Scraper de Datos (`backend/scraper.py`)
- **Qué hace**: Se conecta a la Federación Nacional de Cafeteros, a Datos Abiertos Colombia y al Banco de la República para obtener los precios actuales.
- **Cómo usarlo**: Puedes ejecutarlo manualmente con `python backend/scraper.py`. 
- **Automatización**: Usa el archivo `automatizar_scraper.bat` para que se ejecute solo cada mañana a las 6:00 AM.

### Motor C++ (`backend/motor.cpp`)
- **Qué hace**: Realiza cálculos matemáticos complejos para determinar el "Score de Riesgo". Analiza si el mercado está en "Bonanza", "Estabilidad" o "Tormenta".
- **Nota**: El script de Python lo compila y lo usa automáticamente. No necesitas tocarlo a menos que quieras cambiar las fórmulas financieras.

### Motor de Alertas (`backend/alerts_engine.py`)
- **Qué hace**: Monitorea la base de datos constantemente. Si el riesgo sube de 70 puntos, puede enviar alertas automáticamente.

## 2. El Tablero de Control (Frontend)

Tienes dos opciones para visualizar los datos:

### Dashboard Principal (`frontend/`)
- Es la versión moderna. Para verla, ejecuta `npm run frontend` y abre el enlace que te dé la consola (usualmente `localhost:5173`).

### Dashboard Legacy (`index.html`)
- Es una versión de archivo único, extremadamente rápida y ligera. Puedes abrirla simplemente haciendo doble clic en `index.html`.

## 3. Base de Datos (Supabase)

Toda la información se guarda en la nube de Supabase. Esto permite que los datos que el Scraper recolecta por la mañana se vean instantáneamente en tu celular o en la web.

## 4. Mantenimiento

- **Actualizar claves**: Si cambias de cuenta de Supabase, solo edita los archivos `.env` en las carpetas `backend/` y `frontend/`.
- **Nuevas dependencias**: Si instalas algo nuevo en Python, recuerda actualizar el archivo `backend/requirements.txt`.

---
*Para soporte técnico o consultas sobre el modelo financiero, contacta con el administrador del sistema Pitalito Intel.*
