# ✹ Pitalito Intel Studio - Bonanza ✹

Sistema de Inteligencia Financiera Regional diseñado para el sector cafetero de Pitalito, Huila. Utiliza un motor híbrido de Python y C++ para analizar el riesgo del mercado en tiempo real.

## 📂 Estructura del Proyecto

El proyecto está organizado de forma profesional para separar la lógica de datos de la interfaz de usuario:

- **`/backend`**: Contiene la lógica del sistema.
  - `scraper.py`: Recolector automático de precios (FNC, TRM, BanRep).
  - `motor.cpp`: Motor de cálculo financiero de alto rendimiento en C++.
  - `alerts_engine.py`: Sistema de monitoreo y alertas críticas.
  - `.env`: Configuración de credenciales de Supabase.
- **`/frontend`**: Aplicación web moderna construida con React + Vite.
- **`/mobile`**: Prototipo de aplicación móvil en Flutter.
- **`index.html`**: Tablero de control (Dashboard) legacy de alta velocidad.

## 🚀 Inicio Rápido

### Instalación
1. Instala las dependencias del backend:
   ```bash
   pip install -r backend/requirements.txt
   ```
2. Instala las dependencias del frontend:
   ```bash
   npm install && npm run setup
   ```
3. Configura tus variables de entorno en `backend/.env` y `frontend/.env`.

### Ejecución
Para iniciar todo el ecosistema simultáneamente:
```bash
npm start
```

## 🛠️ Tecnologías
- **Backend**: Python, C++, Supabase.
- **Frontend**: React, Vite, Vanilla CSS (Quantix Design System).
- **Base de Datos**: Supabase (PostgreSQL) con actualizaciones en tiempo real.

---
© 2026 Pitalito Intel Studio | Huila, Colombia.
