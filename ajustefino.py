from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments
from peft import LoraConfig, get_peft_model
from trl import SFTTrainer
from torch import device as torch_device, cuda, backends

# 🔍 Detectar el dispositivo
if cuda.is_available():
    device = torch_device("cuda")
elif backends.mps.is_available():
    device = torch_device("mps")
else:
    device = torch_device("cpu")

print(f"📦 Usando dispositivo: {device}")

# 📘 Configuración
MODEL_ID = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
DATA_PATH = "secciones_extraidas/dataset_alpaca.json"

# 🔹 Cargar dataset
dataset = load_dataset("json", data_files=DATA_PATH)["train"]

# 🔹 Formateo de entrada tipo Alpaca
def format_prompt(example):
    return f"{example['instruction'].strip()}\n{example['input'].strip()}\n###\n{example['output'].strip()}"

# 🔹 Tokenizador
tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)
tokenizer.pad_token = tokenizer.eos_token

# 🔹 Aplicar formato
def formatting_func(example):
    return {"text": format_prompt(example)}

dataset = dataset.map(formatting_func)

# 🔹 Cargar modelo base y configurar LoRA
model = AutoModelForCausalLM.from_pretrained(MODEL_ID, torch_dtype="float32").to(device)

peft_config = LoraConfig(
    r=8,
    lora_alpha=16,
    lora_dropout=0.1,
    bias="none",
    task_type="CAUSAL_LM"
)
model = get_peft_model(model, peft_config)

# 🔹 Configurar entrenamiento
training_args = TrainingArguments(
    output_dir="./modelo_finetuneado",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    num_train_epochs=2,
    learning_rate=2e-4,
    logging_steps=10,
    save_strategy="epoch",
    bf16=False,
    fp16=False,
    report_to="none",
)

# 🔹 Entrenar
trainer = SFTTrainer(
    model=model,
    train_dataset=dataset,
    args=training_args,
    formatting_func=lambda e: format_prompt(e),
)

trainer.train()

# ✅ Guardar correctamente el modelo PEFT (LoRA) y tokenizer
trainer.model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print("✅ Entrenamiento y guardado completados.")