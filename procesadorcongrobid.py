import os
import requests
from tqdm import tqdm

# Directorios
PDF_DIR = "/Users/andricguerrero/ENTORNOS/nuevos entornos/ACUMULADATOS/PDF"
OUTPUT_DIR = "grobid_xml"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Función para procesar un PDF individual
def enviar_a_grobid(nombre_pdf):
    ruta_pdf = os.path.join(PDF_DIR, nombre_pdf)
    ruta_salida = os.path.join(OUTPUT_DIR, nombre_pdf.replace(".pdf", ".tei.xml"))

    with open(ruta_pdf, 'rb') as archivo:
        response = requests.post(
            "http://localhost:8070/api/processFulltextDocument",
            files={"input": archivo},
            data={"consolidateHeader": "1", "consolidateCitations": "0"}
        )

    if response.status_code == 200:
        with open(ruta_salida, "w", encoding="utf-8") as f:
            f.write(response.text)
        print(f"✅ Procesado: {nombre_pdf}")
    else:
        print(f"❌ Error con {nombre_pdf}: {response.status_code}")

# Procesar todos los PDFs
def procesar_todos():
    archivos = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    for archivo in tqdm(archivos, desc="Procesando PDFs"):
        enviar_a_grobid(archivo)

if __name__ == "__main__":
    procesar_todos()