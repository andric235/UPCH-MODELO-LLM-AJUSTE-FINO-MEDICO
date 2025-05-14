import json
import os
import tiktoken
from tqdm import tqdm

# Configuración
INPUT_FILE = "secciones_extraidas/secciones_extraidas.jsonl"
OUTPUT_FILE = "secciones_extraidas/chunks_por_tokens.jsonl"
MAX_TOKENS = 512

# Tokenizador de OpenAI (modelo cl100k_base es usado por GPT-4, GPT-3.5, etc.)
tokenizer = tiktoken.get_encoding("cl100k_base")

def dividir_en_chunks(texto, max_tokens):
    tokens = tokenizer.encode(texto)
    chunks = []
    for i in range(0, len(tokens), max_tokens):
        sub_tokens = tokens[i:i + max_tokens]
        chunk_text = tokenizer.decode(sub_tokens)
        chunks.append(chunk_text)
    return chunks

with open(INPUT_FILE, "r", encoding="utf-8") as f_in, open(OUTPUT_FILE, "w", encoding="utf-8") as f_out:
    for linea in tqdm(f_in, desc="Dividiendo en chunks"):
        entrada = json.loads(linea)
        fragmentos = dividir_en_chunks(entrada["chunk_text"], MAX_TOKENS)
        for i, frag in enumerate(fragmentos):
            nuevo = {
                "title": entrada["title"],
                "section": entrada["section"],
                "chunk_text": frag,
                "chunk_id": f"{entrada['section']}_{i+1}",
                "source_pdf": entrada["source_pdf"]
            }
            f_out.write(json.dumps(nuevo) + "\n")

print(f"✅ Chunks generados y guardados en: {OUTPUT_FILE}")