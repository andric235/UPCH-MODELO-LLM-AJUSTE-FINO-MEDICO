import os
from bs4 import BeautifulSoup
from tqdm import tqdm
import json
# Rutas
XML_DIR = "grobid_xml"
OUTPUT_DIR = "secciones_extraidas"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def extraer_secciones_de_xml(nombre_xml):
    ruta = os.path.join(XML_DIR, nombre_xml)
    with open(ruta, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "xml")

    # Título del documento (header)
    title_tag = soup.find("title")
    titulo = title_tag.text.strip() if title_tag else "Sin título"

    secciones = []

    for div in soup.find_all("div"):
        encabezado = div.find("head")
        parrafos = div.find_all("p")

        if encabezado and parrafos:
            nombre_seccion = encabezado.text.strip()
            contenido = "\n".join(p.text.strip() for p in parrafos)

            secciones.append({
                "title": titulo,
                "section": nombre_seccion,
                "chunk_text": contenido,
                "source_pdf": nombre_xml.replace(".tei.xml", ".pdf")
            })

    return secciones

def procesar_todos():
    resultados = []
    archivos = [f for f in os.listdir(XML_DIR) if f.endswith(".tei.xml")]

    for archivo in tqdm(archivos, desc="Extrayendo secciones"):
        secciones = extraer_secciones_de_xml(archivo)
        resultados.extend(secciones)

    # Guardar en archivo de salida (opcional)
    ruta_salida = os.path.join(OUTPUT_DIR, "secciones_extraidas.jsonl")
    with open(ruta_salida, "w", encoding="utf-8") as out:
        for item in resultados:
            out.write(json.dumps(item, ensure_ascii=False) + "\n")

    print(f"✅ Se extrajeron {len(resultados)} secciones en total.")
    print(f"📄 Guardado en: {ruta_salida}")

if __name__ == "__main__":
    procesar_todos()