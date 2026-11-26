"""Descarga tipos de cambio de Banxico y los guarda en data/*.json.

Uso:
    BANXICO_TOKEN=tu_token python scripts/actualizar_banxico.py

El token es gratis: https://www.banxico.org.mx/SieAPIRest/service/v1/token
Solo usa la biblioteca estándar de Python (no hay que instalar nada).
"""
import datetime as dt
import json
import os
import sys
import urllib.request

DIAS_HISTORIAL = 400
CARPETA = os.path.join(os.path.dirname(__file__), "..", "data")

# serie de Banxico, archivo de salida, palabra que debe aparecer en el título de la serie
SERIES = [
    ("SF43718", "tipo-cambio.json", "Banco de México, serie SF43718 (FIX)", "dólar"),
    ("SF46410", "euro.json", "Banco de México, tipo de cambio del euro (serie SF46410)", "euro"),
]


def descargar(token: str, serie: str) -> tuple[str, list[dict]]:
    hoy = dt.date.today()
    inicio = hoy - dt.timedelta(days=DIAS_HISTORIAL)
    url = (f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{serie}/datos/"
           f"{inicio.isoformat()}/{hoy.isoformat()}")
    req = urllib.request.Request(url, headers={"Bmx-Token": token, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        cuerpo = json.load(r)
    s = cuerpo["bmx"]["series"][0]
    datos = []
    for d in s.get("datos", []):
        try:
            valor = float(d["dato"].replace(",", ""))
        except (ValueError, KeyError):
            continue  # "N/E" en días sin dato
        dia, mes, anio = d["fecha"].split("/")
        datos.append({"fecha": f"{anio}-{mes}-{dia}", "valor": round(valor, 4)})
    datos.sort(key=lambda x: x["fecha"])
    return s.get("titulo", ""), datos


def guardar(archivo: str, fuente: str, datos: list[dict]) -> None:
    ruta = os.path.join(CARPETA, archivo)
    if os.path.exists(ruta):
        with open(ruta, encoding="utf-8") as f:
            if json.load(f).get("datos") == datos:
                print(f"{archivo}: sin cambios")
                return
    salida = {
        "fuente": fuente,
        "actualizado": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "datos": datos,
    }
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"{archivo}: {len(datos)} días, último {datos[-1]['fecha']} = {datos[-1]['valor']}")


def main() -> int:
    token = os.environ.get("BANXICO_TOKEN", "").strip()
    if not token:
        print("Falta la variable BANXICO_TOKEN", file=sys.stderr)
        return 1
    errores = 0
    for serie, archivo, fuente, palabra in SERIES:
        try:
            titulo, datos = descargar(token, serie)
        except Exception as e:  # una serie que falla no detiene a las demás
            print(f"{serie}: error al descargar ({e})", file=sys.stderr)
            errores += 1
            continue
        print(f"{serie}: {titulo}")
        if palabra.lower() not in titulo.lower():
            print(f"{serie}: el título no menciona '{palabra}'; no se guarda", file=sys.stderr)
            errores += 1
            continue
        if not datos:
            print(f"{serie}: sin datos; no se modifica {archivo}", file=sys.stderr)
            errores += 1
            continue
        guardar(archivo, fuente, datos)
    # Solo falla si la serie principal (dólar) no se pudo actualizar
    return 1 if errores and not os.path.exists(os.path.join(CARPETA, "tipo-cambio.json")) else 0


if __name__ == "__main__":
    sys.exit(main())
