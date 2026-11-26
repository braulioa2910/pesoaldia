# Peso al Día: cómo ponerlo en internet

Sitio estático (HTML, CSS y JS). No necesita servidor ni base de datos. Se publica gratis con GitHub Pages, y el dólar se actualiza solo con GitHub Actions.

## Qué hay en la carpeta

| Archivo | Para qué sirve |
|---|---|
| `index.html` | Inicio con el dólar del día |
| `dolar-hoy.html` | Tipo de cambio FIX, gráfica, historial y convertidor |
| `calculadora-aguinaldo.html` | Calculadora de aguinaldo 2026 con ISR |
| `acerca.html`, `privacidad.html` | Páginas que AdSense exige (acerca, contacto y privacidad) |
| `data/tipo-cambio.json` | Datos del dólar (los escribe el script, no se editan a mano) |
| `scripts/actualizar_banxico.py` | Baja el FIX de Banxico |
| `.github/workflows/actualizar-dolar.yml` | Corre el script de lunes a viernes |
| `robots.txt`, `sitemap.xml`, `ads.txt` | Para Google y AdSense |

## Paso 1. Token de Banxico (gratis, 2 minutos)
1. Entra a https://www.banxico.org.mx/SieAPIRest/service/v1/token
2. Llena el formulario y copia el token que te dan (64 caracteres).

## Paso 2. Subir a GitHub
1. Crea una cuenta en https://github.com si no tienes.
2. Crea un repositorio público llamado, por ejemplo, `pesoaldia`.
3. Sube todos los archivos de esta carpeta (incluida la carpeta oculta `.github`). Lo más fácil es usar GitHub Desktop o `git push`. Si los arrastras en la página web, asegúrate de que `.github/workflows/actualizar-dolar.yml` también suba.

## Paso 3. Guardar el token como secreto
En el repositorio: **Settings → Secrets and variables → Actions → New repository secret**
- Nombre: `BANXICO_TOKEN`
- Valor: tu token

Después ve a la pestaña **Actions → Actualizar tipo de cambio → Run workflow** para correrlo la primera vez. Va a llenar un año de historial.

## Paso 4. Publicar con GitHub Pages
**Settings → Pages → Source: Deploy from a branch → main / (root)**. En uno o dos minutos tu sitio queda en `https://TU-USUARIO.github.io/pesoaldia/`.

## Paso 5. Dominio propio (recomendado para AdSense)
1. Compra un dominio `.com` o `.com.mx` (aprox. $200–$400 MXN al año en Namecheap, Cloudflare o GoDaddy). Revisa que el nombre esté libre.
2. En **Settings → Pages → Custom domain** escribe tu dominio y sigue las instrucciones de DNS.
3. Activa **Enforce HTTPS**.
4. Cambia `https://www.tudominio.com` por tu dominio en `robots.txt` y `sitemap.xml`.

## Paso 6. Antes de pedir AdSense, rellena esto
- `privacidad.html`: cambia **NOMBRE DEL RESPONSABLE** y **correo@pesoaldia.com.mx**.
- `acerca.html`: cambia **correo@pesoaldia.com.mx** (usa un correo real que revises).
- Da de alta el sitio en **Google Search Console** y envía el `sitemap.xml`.
- Agrega más páginas útiles (ver "Siguientes páginas"). Con 3 páginas AdSense casi siempre rechaza por "contenido de poco valor". Junta de 15 a 25 páginas buenas antes de solicitar.

## Paso 7. Cuando AdSense te apruebe
1. Pega el código `<script async src="https://pagead2.googlesyndication.com/...">` que te dé Google en el `<head>` de cada página (hay un comentario que marca dónde).
2. Pon la línea que te den en `ads.txt`.
3. Dentro de cada `<div class="ad">` pega el bloque de anuncio, o usa "Anuncios automáticos" y borra esos divs.

## Datos que hay que actualizar cada año
En `assets/aguinaldo.js`: `uma` (cambia el 1 de febrero), `salarioMinimo` (cambia el 1 de enero) y `tarifa` (si el SAT publica una nueva en el Anexo 8). Cambia también los textos que dicen 2026.

## Siguientes páginas con buen tráfico en México
Calculadora de finiquito, calculadora de ISR por sueldo, rendimiento de Cetes, calculadora de vacaciones (Vacaciones Dignas), prima vacacional, PTU (mayo), días festivos oficiales, euro hoy.

## Reglas para no perder la cuenta de AdSense
- Nunca des clic en tus propios anuncios ni le pidas a nadie que lo haga.
- No compres visitas en sitios de "tráfico garantizado".
- No copies textos de otros sitios. Cada página tiene que explicar algo con tus palabras.
