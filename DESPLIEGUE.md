# Guía de Despliegue y Actualizaciones - Bonanza ✹

Esta guía te ayudará a poner tu aplicación "en vivo" para que puedas acceder desde cualquier lugar y mantenerla actualizada.

## 1. Cómo subir actualizaciones ⬆️

Hacer cambios es muy fácil. Cada vez que quieras subir algo nuevo a GitHub, usa estos 3 comandos en tu terminal (dentro de la carpeta del proyecto):

```powershell
# 1. Avisa que hay cambios
git add .

# 2. Crea una nota sobre lo que cambiaste
git commit -m "Explica brevemente tu cambio aqui"

# 3. Súbelos a internet
git push origin main
```

## 2. Cómo poner la página en Internet (Frontend) 🌐

Para que tu Dashboard se vea en un enlace público (como `mi-pitalito-intel.vercel.app`), te recomiendo usar **Vercel** o **Netlify**:

1. Crea una cuenta en [Vercel](https://vercel.com/) usando tu GitHub.
2. Pulsa en **"Add New Project"** y selecciona tu repositorio `PitalitoIntel`.
3. **Paso CRÍTICO (Variables de Entorno)**: 
   - Durante la configuración, verás una sección llamada "Environment Variables".
   - Allí debes copiar los valores de tu archivo `frontend/.env` (ej: `VITE_SUPABASE_URL` y `VITE_SUPABASE_KEY`).
4. Dale a **"Deploy"**. En un minuto tendrás un enlace público que puedes compartir.

## 3. Automatización del Scraper (Backend) 🤖

Para que el recolector de datos funcione solo sin necesidad de tener tu computadora encendida, podemos usar **GitHub Actions**.

He preparado un archivo (que crearé a continuación) para que GitHub ejecute tu script cada mañana automáticamente. Solo necesitarás configurar los "Secrets" en GitHub:
1. En tu repo de GitHub ve a **Settings** > **Secrets and variables** > **Actions**.
2. Pulsa en **New repository secret** y añade:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`

---
*Con esto, tu sistema será un "robot" autónomo que vive en la red.*
