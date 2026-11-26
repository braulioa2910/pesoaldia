"""Descarga el tipo de cambio FIX de Banxico y lo guarda en data/tipo-cambio.json.

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

SERIE = "SF43718"  # Tipo de cambio pesos por dólar E.U.A. FIX
DIAS_HISTORIAL = 400
RUTA = os.path.join(os.path.dirname(__file__), "..", "data", "tipo-cambio.json")


def descargar(token: str) -> list[dict]:
    hoy = dt.date.today()
    inicio = hoy - dt.timedelta(days=DIAS_HISTORIAL)
    url = (f"https://www.banxico.org.mx/SieAPIRest/service/v1/series/{SERIE}/datos/"
           f"{inicio.isoformat()}/{hoy.isoformat()}")
    req = urllib.request.Request(url, headers={"Bmx-Token": token, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as r:
        cuerpo = json.load(r)
    crudos = cuerpo["bmx"]["series"][0].get("datos", [])
    datos = []
    for d in crudos:
        try:
            valor = float(d["dato"].replace(",", ""))
        except (ValueError, KeyError):
            continue  # "N/E" en días sin dato
        dia, mes, anio = d["fecha"].split("/")
        datos.append({"fecha": f"{anio}-{mes}-{dia}", "valor": round(valor, 4)})
    datos.sort(key=lambda x: x["fecha"])
    return datos


def main() -> int:
    token = os.environ.get("BANXICO_TOKEN", "").strip()
    if not token:
        print("Falta la variable BANXICO_TOKEN", file=sys.stderr)
        return 1
    datos = descargar(token)
    if not datos:
        print("Banxico no devolvió datos; no se modifica el archivo", file=sys.stderr)
        return 1

    anterior = None
    if os.path.exists(RUTA):
        with open(RUTA, encoding="utf-8") as f:
            anterior = json.load(f).get("datos")
    if anterior == datos:
        print("Sin cambios")
        return 0

    salida = {
        "fuente": "Banco de México, serie SF43718 (FIX)",
        "url_fuente": "https://www.banxico.org.mx/tipcamb/main.do?page=tip&idioma=sp",
        "actualizado": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "datos": datos,
    }
    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
        f.write("\n")
    print(f"Guardado: {len(datos)} días, último {datos[-1]['fecha']} = {datos[-1]['valor']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
