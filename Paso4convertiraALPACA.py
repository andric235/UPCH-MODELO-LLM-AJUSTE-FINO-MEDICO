import json
import os
from tqdm import tqdm

ENTRADA = "secciones_extraidas/chunks_por_tokens.jsonl"
SALIDA = "secciones_extraidas/dataset_alpaca.json"

def construir_instruction(nombre_seccion):
    return f"Resume o explica la sección '{nombre_seccion}' del protocolo CAP para diagnóstico."

def construir_output(chunk):
    # Por ahora dejamos el output igual al chunk_text (auto-supervisado)
    return chunk.strip()

registros_convertidos = []

with open(ENTRADA, "r", encoding="utf-8") as f:
    for linea in tqdm(f, desc="Generando formato Alpaca"):
        entrada = json.loads(linea)
        registro = {
            "instruction": construir_instruction(entrada["section"]),
            "input": entrada["chunk_text"],
            "output": construir_output(entrada["chunk_text"])
        }
        registros_convertidos.append(registro)

# Guardar en JSON (lista completa, no JSONL)
with open(SALIDA, "w", encoding="utf-8") as out:
    json.dump(registros_convertidos, out, indent=2, ensure_ascii=False)

print(f"✅ Dataset guardado en: {SALIDA}")
print(f"📊 Total de ejemplos: {len(registros_convertidos)}")