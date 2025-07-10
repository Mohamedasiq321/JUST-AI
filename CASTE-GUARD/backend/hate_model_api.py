from fastapi import FastAPI, Request
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F

app = FastAPI()

# Load model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("bert-base-uncased", num_labels=3)
model.load_state_dict(torch.load("hate_model.pt", map_location="cpu"))
model.eval()

tokenizer = AutoTokenizer.from_pretrained("./my_tokenizer")

labels = ["normal", "offensive", "hateful"]

class TextInput(BaseModel):
    text: str

@app.post("/predict")
def predict_text(input: TextInput):
    inputs = tokenizer(input.text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
        probs = F.softmax(outputs.logits, dim=1).squeeze().tolist()
        pred = labels[torch.argmax(outputs.logits, dim=1).item()]
    return {"intent": pred, "scores": dict(zip(labels, probs))}
